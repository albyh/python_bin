import Tkinter as tk, Tkconstants, tkFileDialog, tkMessageBox
import shutil
import os
import glob
import datetime
import time

class Hq:
    #def setup():
    # the first code which is executed, when a new instance of a class is created. 
    def __init__(self, win  ):
    
        #win = tk.Tk()        
        win.title("Send Files to HQ (v2)")
        self.srcPath  = ""
        self.destPath = ""
        self.paths    = {"src"   : "",
                         "dest"  : ""}
        self.text = [
            "Send Files to HQ", 
            "This application will move files modified or edited in the past 24 hours",
            "from the Source folder to the Destination folder selected using the buttons below.",
            "Select Source and Destination folders then click 'Move Staged Files'",
        ]
        # defining options for opening a directory
        self.dir_opt = options = {}
        options['initialdir'] = 'C:/'
        options['mustexist'] = False
        options['parent'] = win
        options['title'] = ''

        self.results = { 'moved'  : [], 'skipped': []}

        tk.Label(win, text = self.text[0], font = ('Arial', 18, 'bold'), pady=20).pack()
        tk.Frame(win, height = 10).pack()
        tk.Label(win, text = self.text[1]).pack()
        tk.Label(win, text = self.text[2], padx = 20).pack()
        tk.Label(win, text = self.text[3]).pack()

        tk.Frame(win, height = 15).pack()

        self.con1 = tk.Frame(win, height=100, width = 200, padx=10, pady=10, bd=2, relief='groove' )
        self.con1.pack()

        # options for src/dest buttons
        self.button_opt = { 'fill': Tkconstants.BOTH, 'padx': 80, 'pady': 10}

        # define buttons
        self.bSource = tk.Button(self.con1, width=30, text='Source Folder', command= lambda: self.setFolder(True)).pack(**self.button_opt) 
        self.labelSrc = tk.Label(self.con1, text = options['initialdir'])
        self.labelSrc.pack()

        tk.Frame(win, height = 20).pack()
    
        self.con2 = tk.Frame(win, height=100, width = 200,  padx=10, pady=10,  bd=2, relief='groove' )
        self.con2.pack()

        self.bDest   = tk.Button(self.con2, width=30, text='Destination Folder', command= lambda: self.setFolder(False)).pack(**self.button_opt)
        self.labelDest   = tk.Label(self.con2, text = options['initialdir']) 
        self.labelDest.pack()

        tk.Frame(win, height = 30).pack()

        self.bCopy   = tk.Button(win, state='disabled', text='Move Staged Files', pady = 10, command= lambda: self.moveFiles())
        self.bCopy.pack() #**self.button_opt)

        tk.Frame(win, height = 50).pack()

        #return win

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

def main():
    root = tk.Tk()
    win = Hq(root)
    root.mainloop()

if __name__ == "__main__": main()
    