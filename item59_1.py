import Tkinter as tk, Tkconstants, tkFileDialog
import shutil
import os
import glob
import datetime
import time

def setup():

    win = tk.Tk()        
    win.title("Send Files to HQ")
    srcPath  = ""
    destPath = ""
    paths    = {"src"   : "",
                "dest"  : ""}

    text = [
        "Send Files to HQ", 
        "This application will move files modified or edited in the past 24 hours",
        "from the Source folder to the Destination folder selected using the buttons below.",
        "Select Source and Destination folders then click 'Move Staged Files'",
    ]
    # defining options for opening a directory
    dir_opt = options = {}
    options['initialdir'] = 'C:/'
    options['mustexist'] = False
    options['parent'] = win
    options['title'] = ''

    tk.Label(win, text = text[0], font = ('Arial', 18, 'bold'), pady=20).pack()
    tk.Frame(win, height = 10).pack()
    tk.Label(win, text = text[1]).pack()
    tk.Label(win, text = text[2], padx = 20).pack()
    tk.Label(win, text = text[3]).pack()

    tk.Frame(win, height = 15).pack()

    con1 = tk.Frame(win, height=100, width = 200, padx=10, pady=10, bd=2, relief='groove' )
    con1.pack()

    # options for buttons
    button_opt = { 'fill': Tkconstants.BOTH, 'padx': 80, 'pady': 10}

    # define buttons
    bSource = tk.Button(con1, width=30, text='Source Folder', command= lambda: setFolder(dir_opt,labelSrc,paths,True,bCopy)).pack(**button_opt)
    labelSrc = tk.Label(con1, text = options['initialdir'])
    labelSrc.pack()

    tk.Frame(win, height = 20).pack()
    
    con2 = tk.Frame(win, height=100, width = 200,  padx=10, pady=10,  bd=2, relief='groove' )
    con2.pack()

    bDest   = tk.Button(con2, width=30, text='Destination Folder', command= lambda: setFolder(dir_opt,labelDest,paths,False,bCopy)).pack(**button_opt)
    labelDest   = tk.Label(con2, text = options['initialdir']) 
    labelDest.pack()

    tk.Frame(win, height = 30).pack()

    bCopy   = tk.Button(win, state='disabled', text='Move Staged Files', pady = 10, command= lambda: moveFiles(paths))
    bCopy.pack() #**button_opt)

    tk.Frame(win, height = 50).pack()

    return win

def okToCopy(paths):
    if paths["src"] != '' and paths["dest"] != '':
        return True
    else:
        return False


def setFolder(x,y,paths,source,bCopy):
    x['title'] = 'Select the SOURCE directory' if source else 'Select the DESTINATION directory'

    print("setFolder")
    path = tkFileDialog.askdirectory(**x)
    print(path)
    if source:
        paths["src"] = path
    else: 
        paths["dest"] = path

    y.config(text = path)

    if okToCopy:
        bCopy['state'] = 'normal'

def edited(f,cutoff):
	#was the file edited in the prior 24 hours
	return True if ((cutoff - os.path.getmtime(f))/3600 <= 24) else False

def moveFiles(paths):
    #copy ALL .txt files MODIFIED/CREATED in the past 24 hours from Folder "src" to Folder "dest"
    file_filter = "*.txt"
    cutoff = time.time()
    results = { 'moved'  : [],
                'skipped': []
              }

    try:
        for file_ in glob.glob(paths["src"]+"/"+file_filter):

            if edited(file_,cutoff):
                editTime = datetime.datetime.fromtimestamp( int(os.path.getmtime(file_)) ).strftime("%H:%M:%S")
                shutil.move( file_, paths["dest"] )
                print( '{} modified at {}. Moving to batch folder "{}"'.format(file_, editTime, paths["dest"]) )
                results['moved'].append( file_ )
            else:
                print( "{} not new/modified...skipping".format(file_) )
                results['skipped'].append( file_ )

    except IOError as err:
        print("I/O Error ({}) moving {}.".format(err,file_))
        pass

    except Exception as err:
        print("{} moving {}".format(err,file_))
        pass

    return results

win = setup()

win.mainloop()
    