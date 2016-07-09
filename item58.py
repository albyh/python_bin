import shutil
import os
import glob
import datetime
import time
#copy ALL .txt files MODIFIED/CREATED in the past 24 hours from Folder "source" to Folder "dest"

def edited(f):
	#was the file edited in the prior 24 hours
	return True if ((cutoff - os.path.getmtime(f))/3600 <= 24) else False

file_filter = "*.txt"
fromTo      = {"src"   : "source",
               "dest"  : "dest"}
cutoff = time.time()

try:
	for file_ in glob.glob(fromTo["src"]+"/"+file_filter):

		if edited(file_):
			editTime = datetime.datetime.fromtimestamp( int(os.path.getmtime(file_)) ).strftime("%H:%M:%S")
			shutil.move( file_, fromTo["dest"] )
			print( '{} modified at {}. Moving to batch folder "{}"'.format(file_, editTime, fromTo["dest"]) )
		else:
			print( "{} not new/modified...skipping".format(file_) )

except IOError:
    print("I/O Error copying file...quitting.")

except:
    print("Error copying file...quitting.")
