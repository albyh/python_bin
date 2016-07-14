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
        self.results = {'moved'  : [], 'skipped': [], 'lastXfer': None }
        self.__initMenu()
        self.__initWin()
        self.__getDbPaths()
        self.__updateXferLabel()

    def __initMenu(self):
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

    def __initWin(self):
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
        self.bCopy   = tk.Button(self.win, state='normal' if self.__okToCopy() else 'disabled', text='Move Staged Files', pady = 10, command=self.moveFiles)
        #self.bCopy   = tk.Button(self.win, state='disabled', text='Move Staged Files', pady = 10, command=self.moveFiles)
        self.bCopy.pack() #**self.button_opt)
        tk.Frame(self.win, height = 10).pack()
        self.xferLabel = tk.Label(self.win, text = 'Last Transfer Completed: {}'.format(self.results['lastXfer']))
        self.xferLabel.pack()
        self.xferMove = tk.Label(self.win, text = 'Files Moved Last Transfer: {}'.format(len(self.results['moved'])))
        self.xferMove.pack()
        self.xferSkip = tk.Label(self.win, text = 'Files Skipped Last Transfer: {}'.format(len(self.results['skipped'])))
        self.xferSkip.pack()
        tk.Frame(self.win, height = 50).pack()
    
    def newCopyDate(self):
        tkMessageBox.showinfo( "Options", "Enter a new date/time to be used " )       

    def aboutBox(self):
        tkMessageBox.showinfo( "About", "Send files to HQ.\n\n(c)  2016 HQ" )       

    def __okToCopy(self):
        if self.paths["src"] != '' and self.paths["dest"] != '' and self.paths["src"] != self.paths["dest"]:
            return True
        else:
            if self.paths["src"] == self.paths["dest"]:
                #self.paths["src"] will be '' if new tables
                if self.paths["src"] != '':
                    tkMessageBox.showerror( "Error", "Source and destination can't be the same folder.\nChange source or destination folder." )
            return False

    def __updateXferLabel(self):
        rows = self.db.q('SELECT last_move as "[timestamp]" FROM {} WHERE hq_id = 100'.format(self.db.dbConfig['hqTables'][0]))
        assert rows, "Didn't receive a response to last transfer date"
        if rows[0][0] == None:
            print('None rows == None')
            #this should already be None
            self.results['lastXfer'] = None
        else:
            print('prior xfer noted')
            self.results['lastXfer'] = rows[0][0]
######################
        #self.xferLabel.config(text = 'Last Transfer: {}'.format(self.results['lastXfer'].strftime('%h:%m')))

    def setFolder(self,loc):
        #called when the user clicks button to set the source or destination folder
        self.dir_opt['title'] = 'Select the SOURCE directory' if (loc=='src') else 'Select the DESTINATION directory'
        path = tkFileDialog.askdirectory(**self.dir_opt)
        if path:
            #if a valid path is returned | else don't change anything
            self.paths[loc] = path
            self.__updateLabels(loc)
            sqlStmt = r"UPDATE {} SET {}_dir = '{}' WHERE hq_id = 100".format(self.db.dbConfig['hqTables'][0], loc, self.paths[loc])
            self.db.x(sqlStmt)

        #if self.__okToCopy():
        #    self.bCopy['state'] = 'normal'
        #else:
        #    self.bCopy['state'] = 'disabled'

        self.bCopy['state'] = 'normal' if self.__okToCopy() else 'disabled'


    def __getDbPaths(self):
        for loc in self.locLabels:
            rows = self.db.q('SELECT {}_dir FROM hq_data WHERE hq_id = 100'.format(loc))
            assert len(rows) is 1, "Didn't receive exactly one item back."
            
            try:
                self.paths[loc] = rows[0][0] if os.path.isdir( rows[0][0] ) else os.path.normpath('C:/')
                self.__updateLabels(loc)
            except:
                print('Error retrieving saved folder. Setting to root.')
                self.paths[loc] = os.path.normpath('C:/')
        
#####################################
        self.bCopy['state'] = 'normal' if self.__okToCopy() else 'disabled'


    def __updateLabels(self,loc):
        #Updates the label passed as 'loc' with the currently selected path 
        self.locLabels[loc].config(text = (self.paths[loc]))    
        self.locLabels[loc].config(text = os.path.normpath(self.paths[loc]) )

    def __showResults(self):
        #display the results of the file copy
        tkMessageBox.showinfo( "Summary", "{} files moved and {} files skipped.\nSee console for details.".format( len(self.results["moved"]), len(self.results["skipped"]) ) )

    def __edited(self, f):
	    #was the file edited since the last_move date stored to db
        #return True if ((cutoff - os.path.getmtime(f))/3600 <= 24) else False
        #return true if file's current datetime is > than the cutoff
        
        x = datetime.datetime.fromtimestamp( os.path.getmtime(f) )
        z = self.results['lastXfer']

        print( datetime.datetime.fromtimestamp( os.path.getmtime(f) ) ) 
        print( self.results['lastXfer'] ) 
        #print( datetime.datetime.strptime(self.results['lastXfer'], '%Y-%m-%d %H:%M:%S.0000') )
        
        return True if ( datetime.datetime.fromtimestamp( os.path.getmtime(f) ) > self.results['lastXfer'] ) else False

    def moveFiles(self):
        #copy ALL .txt files MODIFIED/CREATED in the past 24 hours from Folder "src" to Folder "dest"
        file_filter = "*.txt"
        #cutoff = time.time()
        cutoff = datetime.datetime.now()
        #if no prior transfer, set datetime to now
        if self.results['lastXfer'] == None:
            self.results['lastXfer'] = cutoff
    
        #holding the list allows for extendability in recording files transfered
        moved = []
        skipped = []
        
        try:
            for file_ in glob.glob(self.paths["src"]+"/"+file_filter):

                if self.__edited(file_):
                    editTime = datetime.datetime.fromtimestamp( int(os.path.getmtime(file_)) ).strftime("%b %d-%y %H:%M:%S")
                    #editTime = datetime.datetime.fromtimestamp(os.path.getmtime(file_))
                    #print("edit time") ; print(editTime)

                    shutil.move( file_, self.paths["dest"] )
                    print( '{} modified at {}.\n-->Moving to batch folder "{}"'.format(file_, editTime, self.paths["dest"]) )
                    moved.append( file_ )
                else:
                    print( "{} not new/modified...skipping".format(file_) )
                    skipped.append( file_ )

        except IOError as err:
            print("I/O Error ({}) moving {}.".format(err,file_))
            pass

        except Exception as err:
            print("{} moving {}".format(err,file_))
            raise



        #PASS IN THE VALUES TUPLE 
        self.__saveXfer(cutoff, moved, skipped)
        

    def __saveXfer(self, cutoff, moved, skipped):
        sqlStmt = r"UPDATE {} SET last_move = '{}' WHERE hq_id = 100".format(self.db.dbConfig['hqTables'][0], cutoff)
        self.db.x(sqlStmt)

        print('update value list for hq_history')
        #sqlStmt = r"'INSERT INTO {} VALUES (?,?,?,?,?)'".format(self.db.dbConfig['hqTables'][1]), (100, cutoff, len(self.results['moved']), 0, len(self.results['skipped']))
        
        #sqlStmt = r"'INSERT INTO {} VALUES (?,?,?,?,?)'".format(self.db.dbConfig['hqTables'][1])
        #sqlStmt += r",(100, {}, {}, 0, {} )".format( cutoff,len(self.results['moved']),len(self.results['skipped']))

        print( "FIX INSERT INTO TABLE 2")                
        sqlStmt = r"INSERT INTO hq_history VALUES (100, 0, 0, 0, 0)"
        self.db.x(sqlStmt)
        
        self.__showResults()
        self.results["moved"] = moved
        self.results["skipped"] = skipped

class Db:
    def __init__(self):
        self.dbConfig = {}
        self.dbConfig['configFile'] = 'hq.json'
        #name and path are default values that will be used if hq.json is not found or is corrupt
        self.dbConfig['dbName']     = 'hq.db'
        self.dbConfig['dbPath']     = ''
        self.dbConfig['hqTables']   = ['hq_data', 'hq_history']
        #YOU CAN SET A FIELD TO TYPE=TIMESTAMP AS IT'S A PYTHON CONVERSION
        self.dbConfig['hqFields']   = [
            'hq_id INTEGER PRIMARY KEY, src_dir TEXT NOT NULL, dest_dir TEXT NOT NULL, last_move TIMESTAMP',
            'hq_id INTEGER, move_date TIMESTAMP, copied INTEGER, failed INTEGER, skipped INTEGER, FOREIGN KEY(hq_id) REFERENCES {}(hq_id)'.format(self.dbConfig['hqTables'][0]),
            ]
        #prefer not to hardcode "hq_data" table above but it's throwing an exception
        #'hq_id INTEGER, move_date DATE, copied INTEGER, failed INTEGER, skipped INTEGER, FOREIGN KEY(hq_id) REFERENCES {}(hq_id)'.format(self.dbConfig['hqTables'][0]),

        self.hqdb = self.dbConfig['dbPath']+self.dbConfig['dbName']

        self.prepDb()

    def q(self, sqlStmt):
        # q=query
        cursor = self.con.cursor()
        cursor.execute(sqlStmt)
        result = cursor.fetchall()
        cursor.close()
        return result

    def x(self, sqlStmt):
        # x=execute
        cursor = self.con.cursor()
        cursor.execute(sqlStmt)
        self.con.commit()
        cursor.close()
        #return result

    def prepDb(self):
        try:
            with open(self.dbConfig['configFile']) as file:
                hq_json = json.load(file)
                self.dbConfig['dbName'] = hq_json['dbName']
                self.dbConfig['dbPath'] = hq_json['dbPath']
                print('Config file found.')
        except IOError as e:
            tkMessageBox.showerror( "File Error", "Error opening F:\Skydrive\dev\projects\python\test_bin\source{0} to open file.\n Creating {0} and using defaults.".format(self.dbConfig['configFile']) )
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
            with q.connect(self.hqdb, detect_types=q.PARSE_DECLTYPES) as self.con:
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
        hqDataVals = [100, "C:/", "C:/", None]
        print( self.c.rowcount)
        self.c.execute('INSERT INTO {} VALUES (?,?,?,?)'.format(self.dbConfig['hqTables'][0]), (hqDataVals[0],hqDataVals[1],hqDataVals[2],hqDataVals[3],) )
        print('added {}'.format(hqDataVals))
        print( self.c.rowcount)
        self.con.commit()

def main():
    root = tk.Tk()
    db = Db()
    win = Hq(root, db)

    root.mainloop()

if __name__ == "__main__": main()    