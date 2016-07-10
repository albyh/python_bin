#import Tkinter as tk
#win = tk.Tk()

import Tkinter as tk, Tkconstants, tkFileDialog

class tkMainWin(tk.Frame):

    def __init__(self, root):
        
        tk.Frame.__init__(self, root)

        # options for buttons
        button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}

        # define buttons
        tk.Button(self, text='Source Folder', command=self.askdirectory).pack(**button_opt)
        tk.Button(self, text='Destination Folder', command=self.getDest ).pack(**button_opt)


        # defining options for opening a directory
        self.dir_opt = options = {}
        options['initialdir'] = 'C:\\'
        options['mustexist'] = False
        options['parent'] = root
        options['title'] = 'Select the {} directory'.format( 'source' )

        instruction_text = ["This application will move files modified or edited in the past 24 hours",
                            "from the Source folder to the Destination folder selected using the buttons below.",
                            "Select Source and Destination folders",
                            ]

        instructions1 = tk.Label(root, text = instruction_text[0]).pack()
        instructions2 = tk.Label(root, text = instruction_text[1]).pack()
        instructions3 = tk.Label(root, text = instruction_text[2]).pack()
        sourcePath = tk.Label(root, text = options['initialdir']).pack()
        destPath = tk.Label(root, text = options['initialdir']).pack()

    def askdirectory(self):
        #Returns a selected directoryname.
        return tkFileDialog.askdirectory(**self.dir_opt)

    def getSource(self):
        print("getSource")
        sourceDir = tkFileDialog.askdirectory(**self.dir_opt)
        print(sourceDir)

    def getDest(self):
        print("getDest")
        destDir = tkFileDialog.askdirectory(**self.dir_opt)
        print(destDir)
        self.destPath.config(text = destDir)

if __name__=='__main__':
    root = tk.Tk()
    tkMainWin(root).pack()
    root.mainloop()
    