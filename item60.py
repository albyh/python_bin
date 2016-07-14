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
        self.__setHistoryLabels()
        self.__getDbPaths()

    def __initMenu(self):
        # create a toplevel menu 
        menubar = tk.Menu(self.win) 
        # create a pulldown menu, and add it to the menu bar 
        filemenu    = tk.Menu(menubar, tearoff=False)
        reportmenu  = tk.Menu(menubar, tearoff=False) 
        exitmenu    = tk.Menu(menubar, tearoff=False)
        filemenu.add_command(label='Select Source Folder'       , command= lambda: self.setFolder('src')) 
        filemenu.add_command(label='Select Destination Folder'  , command= lambda: self.setFolder('dest')) 
        filemenu.add_separator() 
        filemenu.add_command(label='Exit'                                  , command=self.win.destroy) 
        reportmenu.add_command(label='Results of last 10 Transfers'        , command=self.showXfers) 
        reportmenu.add_command(label='List files included in last transfer', command=self.showHistory) 
        exitmenu.add_command(label='About'                                 , command=self.aboutBox) 
        menubar.add_cascade(menu=filemenu, label='File') 
        menubar.add_cascade(menu=reportmenu, label='Reports') 
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
    
    def showHistory(self):
        tkMessageBox.showinfo( "Report", "Files in the last transfer" )       

    def showXfers(self):
        tkMessageBox.showinfo( "Report", "Last 10 Transfers" )       

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

    def __setHistoryLabels(self):
        #update the last transfer data and stats
        rows = self.db.q('SELECT move_date, copied, failed, skipped FROM {0} WHERE move_date = (SELECT MAX(move_date) FROM {0}) AND hq_id = 100'.format(self.db.dbConfig['hqTables'][1])) 
        assert len(rows) is 1, "Didn't receive exactly one item back."
        xferDate, copied, failed, skipped = rows[0]

        self.xferLabel.config(text = 'Last Transfer Completed: {}'.format( xferDate.strftime( "%b %d, %Y at  %H:%M:%S")) )
        self.xferMove.config(text = 'Files Moved Last Transfer: {}'.format( copied ))
        self.xferSkip.config(text = 'Files Skipped Last Transfer: {}'.format( skipped ))

    def setFolder(self,loc):
        #called when the user clicks button to set the source or destination folder
        self.dir_opt['title'] = 'Select the SOURCE directory' if (loc=='src') else 'Select the DESTINATION directory'
        path = tkFileDialog.askdirectory(**self.dir_opt)
        if path:
            #if a valid path is returned | else don't change anything
            self.paths[loc] = path
            self.__setPathLabel(loc)
            sqlStmt = r"UPDATE {} SET {}_dir = '{}' WHERE hq_id = 100".format(self.db.dbConfig['hqTables'][0], loc, self.paths[loc])
            self.db.x(sqlStmt)

        self.bCopy['state'] = 'normal' if self.__okToCopy() else 'disabled'


    def __getDbPaths(self):
        for loc in self.locLabels:
            rows = self.db.q('SELECT {}_dir FROM hq_data WHERE hq_id = 100'.format(loc))
            assert len(rows) is 1, "Didn't receive exactly one item back."
            
            try:
                self.paths[loc] = rows[0][0] if os.path.isdir( rows[0][0] ) else os.path.normpath('C:/')
                self.__setPathLabel(loc)
            except:
                print('Error retrieving saved folder. Setting to root.')
                self.paths[loc] = os.path.normpath('C:/')
        
        if not self.db.newTables:
            self.bCopy['state'] = 'normal' if self.__okToCopy() else 'disabled'
            self.db.newTables = False


    def __setPathLabel(self,loc):
        #Updates the label passed as 'loc' with the currently selected path 
        self.locLabels[loc].config(text = (self.paths[loc]))    
        self.locLabels[loc].config(text = os.path.normpath(self.paths[loc]) )

    def __showResults(self,m,c):
        #display the results of the file copy
        tkMessageBox.showinfo( "Summary", "{} files moved and {} files skipped.\nSee console for details.".format(m, c) )

    def __edited(self, f):
	    #was the file edited since the last_move date stored to db
        #return True if ((cutoff - os.path.getmtime(f))/3600 <= 24) else False
        #return true if file's current datetime is > than the cutoff
        
        #x = datetime.datetime.fromtimestamp( os.path.getmtime(f) )
        #z = self.results['lastXfer']

        #print( datetime.datetime.fromtimestamp( os.path.getmtime(f) ) ) 
        #print( self.results['lastXfer'] ) 
        #print( datetime.datetime.strptime(self.results['lastXfer'], '%Y-%m-%d %H:%M:%S.0000') )
        
        return True if ( datetime.datetime.fromtimestamp( os.path.getmtime(f) ) > self.results['lastXfer'] ) else False

    def moveFiles(self):
        #copy ALL .txt files MODIFIED/CREATED since last move from Folder "src" to Folder "dest"
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
            pass

        self.__saveXfer(cutoff, moved, skipped)

    def __saveXfer(self, cutoff, moved, skipped):
        sqlStmt = r"UPDATE {} SET last_move = '{}' WHERE hq_id = 100".format(self.db.dbConfig['hqTables'][0], cutoff)
        self.db.x(sqlStmt)
        sqlStmt = r"INSERT INTO hq_history VALUES (?,?,?,?,?)"
        values = (100, cutoff, len(moved), 0, len(skipped))
        self.db.x(sqlStmt, values)
        
        self.__showResults(len(moved), len(skipped))
        self.__setHistoryLabels()
        self.results["moved"] = moved
        self.results["skipped"] = skipped

    

class Db:
    def __init__(self):
        self.dbConfig = {}
        self.newTables = False
        self.dbConfig['configFile'] = 'hq.json'
        #name and path are default values that will be used if hq.json is not found or is corrupt
        self.dbConfig['dbName']     = 'hq.db'
        self.dbConfig['dbPath']     = ''
        self.dbConfig['hqTables']   = ['hq_data', 'hq_history']
        #TO SET a field to TYPE=TIMESTAMP you also must INCLUDE detect_types=q.PARSE_DECLTYPES in the database connection command
        self.dbConfig['hqFields']   = [
            'hq_id INTEGER PRIMARY KEY, src_dir TEXT NOT NULL, dest_dir TEXT NOT NULL, last_move TIMESTAMP',
            'hq_id INTEGER, move_date TIMESTAMP, moved INTEGER, failed INTEGER, skipped INTEGER, FOREIGN KEY(hq_id) REFERENCES {}(hq_id)'.format(self.dbConfig['hqTables'][0]),
            ]
        self.hqdb = self.dbConfig['dbPath']+self.dbConfig['dbName']

        self.prepDb()

    def q(self, sqlStmt):
        # q=query
        cursor = self.con.cursor()
        cursor.execute(sqlStmt)
        result = cursor.fetchall()
        cursor.close()
        return result

    def x(self, sqlStmt, values=()):
        # x=execute
        cursor = self.con.cursor()
        cursor.execute(sqlStmt, values) if values else cursor.execute(sqlStmt)
        self.con.commit()
        cursor.close()

    def prepDb(self):
        try:
            with open(self.dbConfig['configFile']) as file:
                hq_json = json.load(file)
                self.dbConfig['dbName'] = hq_json['dbName']
                self.dbConfig['dbPath'] = hq_json['dbPath']

        except IOError as e:
            tkMessageBox.showerror( "File Error", "Error opening F:\Skydrive\dev\projects\python\test_bin\source{0} to open file.\n Creating {0} and using defaults.".format(self.dbConfig['configFile']) )
            #Does not exist OR no read permissions
            print "Error opening {} to open file".format(self.dbConfig['configFile']) 
            
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
                #this will return 0 if empty table and 1 if !empty but there has to be a better way?
                #=========================
                recs = self.c.execute('SELECT COUNT(*) FROM {} LIMIT 1'.format(self.dbConfig['hqTables'][0]))
                x = recs.fetchone()
                if x[0] == 0:
                    print( 'no records...populating table')
                    self.populateTables()
                    #assume tables are new
                    self.newTables = True

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

def centerRoot(root):
    w = 600 # width for the Tk root
    h = 600 # height for the Tk root
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    # set the dimensions of the screen 
    # and where it is placed
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

def main():
    root = tk.Tk()
    centerRoot(root)
    db = Db()
    win = Hq(root, db)

    root.mainloop()

if __name__ == "__main__": main()    