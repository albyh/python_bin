import shutil
import os
import glob

#copy ALL .txt files from FolderA to FolderB

file_filter = "*.txt"
fromTo      = {"src"   : "FolderA",
               "dest"  : "FolderB"}

try:
    for file_ in glob.glob(fromTo["src"]+"/"+file_filter):
        print( 'Copying {} to {}'.format(file_, fromTo["dest"]) )
        shutil.move( file_, fromTo["dest"] )

except IOError:
    print("I/O Error copying file")
except:
    print("Error copying file")