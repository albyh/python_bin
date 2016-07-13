import Tkinter as tk, Tkconstants, tkFileDialog, tkMessageBox
import shutil
import os
import glob
import datetime
import time
import sqlite3 as q
import json

class Hq:
    #def setup():
    # the first code which is executed, when a new instance of a class is created. 
    def __init__(self, win):
        win.title("Send Files to HQ (v3)")
        self.paths    = {"src"   : "",
                         "dest"  : ""}
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
        self.results = { 'moved'  : [], 'skipped': []}

        self.initMenu(win)
        self.initWin(win)

    def initMenu(self,win):
        # create a toplevel menu 
        menubar = tk.Menu(win) 
        # create a pulldown menu, and add it to the menu bar 
        filemenu = tk.Menu(menubar, tearoff=False) 
        exitmenu = tk.Menu(menubar, tearoff=False)
        filemenu.add_command(label='Select Source Folder', command= lambda: self.setFolder(True)) 
        filemenu.add_command(label='Select Destination Folder', command= lambda: self.setFolder(False)) 
        filemenu.add_separator() 
        filemenu.add_command(label='Exit', command=win.destroy) 
        exitmenu.add_command(label='About', command=self.aboutBox) 
        menubar.add_cascade(menu=filemenu, label='File') 
        menubar.add_cascade(menu=exitmenu, label='Help') 
        win.config(menu=menubar) 

    def initWin(self, win):
        tk.Label(win, text = self.text[0], font = ('Arial', 18, 'bold'), pady=20).pack()
        tk.Frame(win, height = 10).pack()
        tk.Label(win, text = self.text[1]).pack()
        tk.Label(win, text = self.text[2], padx = 20).pack()
        tk.Label(win, text = self.text[3]).pack()
        tk.Frame(win, height = 15).pack()
        #create button container frame
        self.con1 = tk.Frame(win, height=100, width = 200, padx=10, pady=10, bd=2, relief='groove' )
        self.con1.pack()
        # options for src/dest buttons
        self.button_opt = { 'fill': Tkconstants.BOTH, 'padx': 80, 'pady': 10}
        # define buttons
        self.bSource = tk.Button(self.con1, width=30, text='Source Folder', command= lambda: self.setFolder(True)).pack(**self.button_opt) 
        self.labelSrc = tk.Label(self.con1, text = self.options['initialdir'])
        self.labelSrc.pack()
        tk.Frame(win, height = 20).pack()
        #create button container frame    
        self.con2 = tk.Frame(win, height=100, width = 200,  padx=10, pady=10,  bd=2, relief='groove' )
        self.con2.pack()
        self.bDest   = tk.Button(self.con2, width=30, text='Destination Folder', command= lambda: self.setFolder(False)).pack(**self.button_opt)
        self.labelDest   = tk.Label(self.con2, text = self.options['initialdir']) 
        self.labelDest.pack()
        tk.Frame(win, height = 30).pack()
        self.bCopy   = tk.Button(win, state='disabled', text='Move Staged Files', pady = 10, command=self.moveFiles)
        self.bCopy.pack() #**self.button_opt)
        tk.Frame(win, height = 50).pack()
    
    def aboutBox(self):
        tkMessageBox.showinfo( "About", "Send files to HQ.\n\n(c) 2016 HQ" )       

    def okToCopy(self):
        if self.paths["src"] != '' and self.paths["dest"] != '' and self.paths["src"] != self.paths["dest"]:
            return True
        else:
            if self.paths["src"] == self.paths["dest"]:
                tkMessageBox.showerror( "Error", "Source and destination can't be the same folder." )
            return False

    def setFolder(self,source):
        self.dir_opt['title'] = 'Select the SOURCE directory' if source else 'Select the DESTINATION directory'
        path = tkFileDialog.askdirectory(**self.dir_opt)
        if source:
            self.paths["src"] = path
            self.labelSrc.config(text = path)
        else: 
            self.paths["dest"] = path
            self.labelDest.config(text = path)

        if self.okToCopy():
            self.bCopy['state'] = 'normal'
        else:
            self.bCopy['state'] = 'disabled'

    def showResults(self):
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

        print( 'self.dbConfig = {}'.format(self.dbConfig) )
        self.prepDb()
       
    def prepDb(self):
        print('Reading Config. File. Setting up connection to database')
        try:
            with open(self.dbConfig['configFile']) as file:
                hq_json = json.load(file)
                print('setDb *** '); print(hq_json)
                self.dbConfig['dbName'] = hq_json['dbName']
                self.dbConfig['dbPath'] = hq_json['dbPath']

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
            hqdb = self.dbConfig['dbPath']+self.dbConfig['dbName']
            with q.connect(hqdb) as self.con:
                self.c  = self.con.cursor()
                print('db open *success*')
                self.verifyTables()
                #this will return 0 if empty table and 1 if ! empty but there has to be a better way?
                recs = self.c.execute('SELECT COUNT(*) FROM {} LIMIT 1'.format(self.dbConfig['hqTables'][0]))
                x = recs.fetchone()
                if x[0] == 0:
                    print( 'no records...populating table')
                    self.populateTables()

    def verifyTables(self):
        for i in range(len(self.dbConfig['hqTables'])):
            self.c.execute('CREATE TABLE IF NOT EXISTS {}({})'.format(self.dbConfig['hqTables'][i],self.dbConfig['hqFields'][i]) )

    def populateTables(self):
        hqDataVals = [100, "", "", None]
        print( self.c.rowcount)
        self.c.execute('INSERT INTO {} VALUES (?,?,?,?)'.format(self.dbConfig['hqTables'][0]), (hqDataVals[0],hqDataVals[1],hqDataVals[2],hqDataVals[3],))
        print('added {}'.format(hqDataVals))
        print( self.c.rowcount)
        self.con.commit()

def main():
    root = tk.Tk()
    win = Hq(root)
    db = Db()
    root.mainloop()

if __name__ == "__main__": main()    