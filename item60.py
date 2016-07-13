#from __future__ import unicode_literals
import Tkinter as tk, Tkconstants, tkFileDialog, tkMessageBox
import shutil
import os
import glob
import datetime, time
import sqlite3 as q
import json

class Hq:
    def __init__(self, win, db):
        self.win = win  
        self.db = db
        self.win.title("Send Files to HQ (v3)")
        self.paths     = {'src': '', 'dest': '' } #actual path
        self.locLabels = {'src': '', 'dest': '' } #Tkinter pointer
        self.text = [
            "Send Files to HQ", 
            "This application will move files modified or edited in the past 24 hours",
            "from the Source folder to the Destination folder selected using the buttons below.",
            "Select Source and Destination folders then click 'Move Staged Files'",
        ]
        # defining options for opening a directory
        self.dir_opt = self.options = {}
        self.options['initialdir'] = 'C:/'
        self.options['mustexist'] = False
        self.options['parent'] = win
        self.options['title'] = ''
        self.results = {'moved'  : [], 'skipped': [], 'lastXfer': ''}
        self.initMenu()
        self.initWin()
        self.getDbPaths()

    def initMenu(self):
        # create a toplevel menu 
        menubar = tk.Menu(self.win) 
        # create a pulldown menu, and add it to the menu bar 
        filemenu    = tk.Menu(menubar, tearoff=False)
        optionmenu  = tk.Menu(menubar, tearoff=False) 
        exitmenu    = tk.Menu(menubar, tearoff=False)
        filemenu.add_command(label='Select Source Folder', command= lambda: self.setFolder('src')) 
        filemenu.add_command(label='Select Destination Folder', command= lambda: self.setFolder('dest')) 
        filemenu.add_separator() 
        filemenu.add_command(label='Exit', command=self.win.destroy) 
        optionmenu.add_command(label='Manually enter last copy date/time', command=self.newCopyDate) 
        exitmenu.add_command(label='About', command=self.aboutBox) 
        menubar.add_cascade(menu=filemenu, label='File') 
        menubar.add_cascade(menu=optionmenu, label='Options') 
        menubar.add_cascade(menu=exitmenu, label='Help') 
        self.win.config(menu=menubar) 

    def initWin(self):
        tk.Label(self.win, text = self.text[0], font = ('Arial', 18, 'bold'), pady=20).pack()
        tk.Frame(self.win, height = 1).pack()
        tk.Label(self.win, text = self.text[1]).pack()
        tk.Label(self.win, text = self.text[2], padx = 20).pack()
        tk.Label(self.win, text = self.text[3]).pack()
        tk.Frame(self.win, height = 20).pack()
        #create button container frame
        self.con1 = tk.Frame(self.win, height=100, width = 200, padx=10, pady=10, bd=2, relief='groove' )
        self.con1.pack()
        # options for src/dest buttons
        self.button_opt = { 'fill': Tkconstants.BOTH, 'padx': 80, 'pady': 10}
        # define buttons
        self.bSource = tk.Button(self.con1, width=30, text='Source Folder', command= lambda: self.setFolder('src')).pack(**self.button_opt) 
        self.locLabels['src'] = tk.Label(self.con1, text = os.path.normpath(self.paths['src']))
        self.locLabels['src'].pack()
        tk.Frame(self.win, height = 20).pack()
        #create button container frame    
        self.con2 = tk.Frame(self.win, height=100, width = 200,  padx=10, pady=10,  bd=2, relief='groove' )
        self.con2.pack()
        self.bDest = tk.Button(self.con2, width=30, text='Destination Folder', command= lambda: self.setFolder('dest')).pack(**self.button_opt)
        self.locLabels['dest'] = tk.Label(self.con2, text = os.path.normpath(self.paths['dest'])) 
        self.locLabels['dest'].pack()
        tk.Frame(self.win, height = 30).pack()
        self.bCopy   = tk.Button(self.win, state='disabled', text='Move Staged Files', pady = 10, command=self.moveFiles)
        self.bCopy.pack() #**self.button_opt)
        tk.Frame(self.win, height = 10).pack()
        self.xferLabel = tk.Label(self.win, text = 'Last Transfer: {}'.format(self.results['lastXfer'])).pack()
        tk.Frame(self.win, height = 50).pack()
    
    def newCopyDate(self):
        tkMessageBox.showinfo( "Options", "Enter a new date/time to be used " )       

    def aboutBox(self):
        tkMessageBox.showinfo( "About", "Send files to HQ.\n\n(c) 2016 HQ" )       

    def okToCopy(self):
        if self.paths["src"] != '' and self.paths["dest"] != '' and self.paths["src"] != self.paths["dest"]:
            return True
        else:
            if self.paths["src"] == self.paths["dest"]:
                tkMessageBox.showerror( "Error", "Source and destination can't be the same folder./nChange one of the folders." )
            return False

    def setFolder(self,loc):
        #called when the user clicks button to set the source or destination folder
        self.dir_opt['title'] = 'Select the SOURCE directory' if (loc=='src') else 'Select the DESTINATION directory'
        path = tkFileDialog.askdirectory(**self.dir_opt)
        d = Db()
        self.paths[loc] = path
        #self.locLabels[loc].config(text = os.path.normpath(path))
        self.updateLabels(loc)
        d.saveDir(self, loc)

        if self.okToCopy():
            self.bCopy['state'] = 'normal'
        else:
            self.bCopy['state'] = 'disabled'

    def getDbPaths(self):
        for loc in self.locLabels:
            rows = self.db.query('SELECT {}_dir FROM hq_data WHERE hq_id = 100'.format(loc))
            assert len(rows) is 1, "Didn't receive exactly one item back."
            
            try:
                self.paths[loc] = rows[0][0] if os.path.isdir( rows[0][0] ) else os.path.normpath('C:/')
                self.updateLabels(loc)
            except:
                print('Error retrieving saved folder. Setting to root.')
                self.paths[loc] = os.path.normpath('C:/')

    def updateLabels(self,loc):
        #Updates the label passed as 'loc' with the currently selected path 
        self.locLabels[loc].config(text = (self.paths[loc]))    
        self.locLabels[loc].config(text = os.path.normpath(self.paths[loc]) )

    def showResults(self):
        #display the results of the file copy
        tkMessageBox.showinfo( "Summary", "{} files moved and {} files skipped.\nSee console for details.".format( len(self.results["moved"]), len(self.results["skipped"]) ) )

    def moveFiles(self):
        #inner function instead of private function
        def edited(f,cutoff):
	        #was the file edited in the prior 24 hours
            return True if ((cutoff - os.path.getmtime(f))/3600 <= 24) else False

        #copy ALL .txt files MODIFIED/CREATED in the past 24 hours from Folder "src" to Folder "dest"
        file_filter = "*.txt"
        cutoff = time.time()

        try:
            for file_ in glob.glob(self.paths["src"]+"/"+file_filter):

                if edited(file_,cutoff):
                    editTime = datetime.datetime.fromtimestamp( int(os.path.getmtime(file_)) ).strftime("%H:%M:%S")
                    shutil.move( file_, self.paths["dest"] )
                    print( '{} modified at {}.\n-->Moving to batch folder "{}"'.format(file_, editTime, self.paths["dest"]) )
                    self.results['moved'].append( file_ )
                else:
                    print( "{} not new/modified...skipping".format(file_) )
                    self.results['skipped'].append( file_ )

        except IOError as err:
            print("I/O Error ({}) moving {}.".format(err,file_))
            pass

        except Exception as err:
            print("{} moving {}".format(err,file_))
            pass

        self.showResults()

class Db:
    def __init__(self):
        self.dbConfig = {}
        self.dbConfig['configFile'] = 'hq.json'
        #name and path are default values that will be used if hq.json is not found or is corrupt
        self.dbConfig['dbName']     = 'hq.db'
        self.dbConfig['dbPath']     = ''
        self.dbConfig['hqTables']   = ['hq_data', 'hq_history']
        self.dbConfig['hqFields']   = [
            'hq_id INTEGER, src_dir TEXT, dest_dir TEXT, last_copy DATE',
            'copy_date DATE, copied INTEGER, failed INTEGER, skipped INTEGER',
            ]
        self.hqdb = self.dbConfig['dbPath']+self.dbConfig['dbName']
        #self.src = ''
        #self.dest = ''
        self.prepDb()

    def query(self, sqlStmt):
        cursor = self.con.cursor()
        cursor.execute(sqlStmt)
        result = cursor.fetchall()
        cursor.close()
        return result
        

    #def updateLabels(self,win):
    #    with q.connect(self.hqdb) as self.con:
    #        self.con.text_factory = str
    #        for loc in win.locLabels:
    #            self.c  = self.con.cursor()
    #            self.c.execute('SELECT {}_dir FROM hq_data WHERE hq_id = 100'.format(loc))
    #            row = self.c.fetchone()
    #            try:
    #                win.paths[loc] = row[0]
    #            except:
    #                pass
    
    #    win.updateLabels('src')
    #    win.updateLabels('dest')

    #def updateLabels(self,win):
    #    for loc in win.locLabels:
    #        self.c.execute('SELECT {}_dir FROM hq_data WHERE hq_id = 100'.format(loc))
    #        row = self.c.fetchone()
    #        try:
    #            win.paths[loc] = row[0]
    #        except:
    #            pass
    
    #    win.updateLabels('src')
    #    win.updateLabels('dest')

    def saveDir(self, win, loc):
        with q.connect(self.hqdb) as self.con:
            self.con.text_factory = str
            self.c  = self.con.cursor()
            self.c.execute(r"UPDATE {} SET {}_dir = '{}' WHERE hq_id = 100".format(self.dbConfig['hqTables'][0], loc, win.paths[loc]))

    def prepDb(self):
        try:
            with open(self.dbConfig['configFile']) as file:
                hq_json = json.load(file)
                self.dbConfig['dbName'] = hq_json['dbName']
                self.dbConfig['dbPath'] = hq_json['dbPath']
                print('Config file found.')
        except IOError as e:
            tkMessageBox.showerror( "File Error", "Error opening {0} to open file.\n Creating {0} and using defaults.".format(self.dbConfig['configFile']) )
            print "Error opening {} to open file".format(self.dbConfig['configFile']) #Does not exist OR no read permissions
            
            with open(self.dbConfig['configFile'], 'w') as newDbFile:
                json.dump(self.dbConfig, newDbFile)
        self.verifyDb() 

    def verifyDb(self):
        try:
            #create database directory or fail gracefully if exists
            os.makedirs(self.dbConfig['dbPath'])

        except OSError as exception:
            #if exception.errno != errno.EEXIST:
            #    raise
            #self.hqdb = self.dbConfig['dbPath']+self.dbConfig['dbName']
            with q.connect(self.hqdb) as self.con:
                self.con.text_factory = str
                self.c  = self.con.cursor()
                self.verifyTables()
                #=========================
                #this will return 0 if empty table and 1 if ! empty but there has to be a better way?
                #=========================
                recs = self.c.execute('SELECT COUNT(*) FROM {} LIMIT 1'.format(self.dbConfig['hqTables'][0]))
                x = recs.fetchone()
                if x[0] == 0:
                    print( 'no records...populating table')
                    self.populateTables()
            

    def verifyTables(self):
        for i in range(len(self.dbConfig['hqTables'])):
            self.c.execute('CREATE TABLE IF NOT EXISTS {}({})'.format(self.dbConfig['hqTables'][i],self.dbConfig['hqFields'][i]) )

    def populateTables(self):
        hqDataVals = [100, "c:/", "c:/", None]
        print( self.c.rowcount)
        self.c.execute('INSERT INTO {} VALUES (?,?,?,?)'.format(self.dbConfig['hqTables'][0]), (hqDataVals[0],hqDataVals[1],hqDataVals[2],hqDataVals[3],))
        print('added {}'.format(hqDataVals))
        print( self.c.rowcount)
        self.con.commit()

def main():
    root = tk.Tk()

    db = Db()
    win = Hq(root, db)

    #db.updateLabels(win)
    

    root.mainloop()

if __name__ == "__main__": main()    