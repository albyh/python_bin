#import nester

#print_lol can be added to a module called "nester"
import sys

def print_lol(coll,indent=True,indent_amt=0,dest=sys.stdout):
    for el in coll:
        if isinstance(el,list):
            #indent += 1
            print_lol(el, indent, indent_amt+1, dest)
        else:
            if indent:
                for i in range(indent_amt):
                    print("")
                    print("\t", end='', file=dest)
            print(el, file=dest)
            
'''========BEGIN MAIN========'''

man1 = []
man2 = []

try:
    with open('sketch.txt') as data:
        for l in data:
            try:
                (role, line) = l.split(':',1)
                line = line.strip()
                if role == 'Man':
                    man1.append(line)
                elif role == 'Other Man':
                    man2.append(line)

                print(role, end='')
                print(' said: ' , end='')
                print(line, end='')
            except ValueError:
                    pass
except IOError as err:
    print('File is missing...quitting :(')

try:
    with open("man1.txt", "w") as man1_file:
        print_lol(man1, dest=man1_file)
    with open("man2.txt", "w") as man2_file:    
        print_lol(man2, dest=man2_file)

except IOError as err:
    print("error printing to file...quitting :(")


#print(man1)
#print(man2)
