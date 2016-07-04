#12. Defining a function that returns a string variable
def my_func(student):
    my_string = student[5]
    return my_string

def my_fixAddress(i):
    address = "{} {} {} {}. {}, {}".format(i[1], i[2].upper(), i[3].title(), i[4].title(), i[5].title(), i[6].upper())
    return [i[0], i[8], i[9], address, i[10], i[11]]

def make_groups(s, defaults):
    x = 0
    even_group = []
    odd_group = []
    nopass_group = []
    #8. Use of a while loop
    while x < len(s):
        #5. Use each of these operators +, ­ , * , / , +=, ­= , %
        #6. Use of logical operators and, or , not
        #7. Use of conditional statements: if, elif, else
        if x % 2 == 0 and s[x][5] > (defaults[2]*.95):
            even_group.append(s[x])
        elif s[x][5] > defaults[2]*.95:
            odd_group.append(s[x])
        else:
            nopass_group.append(s[x])
        #5. Use each of these operators +, ­ , * , / , +=, ­= , %
        x += 1    

    print("\n********* EVEN GROUP *********")
    print(even_group)
    print("\n********** ODD GROUP *********")
    print(odd_group)
    print("\n******** NO PASS GROUP *******")
    print(nopass_group)
    return (odd_group, even_group, nopass_group)

def my_main():

    #1. Assign an integer to a variable
    minAge = 18
    #2. Assign a string to a variable
    state = 'OR'
    #3. Assign a float to a variable
    minScore = 80.5
    #tuple
    defaults = ( minAge, state, minScore )
    #5. Use each of these operators +, ­ , * , / , +=, ­= , %
    students = [
        ['Jimmy Jones', 145 , 'NE', 'THOMPSON'   ,'St'  , 'Portland' , 'OR','503-246-3588', 20, 'M', True ,100.00],
        ['Timmy Smith', 5422, 'NW', 'miller'     ,'RD'  , 'Portland' , 'OR','503-875-2113', 24, 'M', True ,88.75 ],
        ['Nancy White', 43  , 'SE', 'McLaughlin' ,'Ave' , 'Milwaukie', 'OR','503-577-8899', 28, 'F', True ,92.20 ],
        ['Tina Turner', 2365, 'sw', 'Barbur'     ,'Blvd', 'Portland' , 'OR','503-545-5455', 17, 'F', True ,66.95 ],
        ['Grace Jones', 5224, 'e' , 'HarBOR'     ,'ave' , 'reading'  , 'PA','315-455-4566', 22, 'F', False,97.58 ],
        ]
        
    print( "****DEFAULTS****\nMinumum Age: {}\nLocal Area: {}\nMin. Test Score: {}\n*********************".format(minAge, state, minScore) )
    
    print( "\nCity for students[3]: "+my_func( students[3]))
    print( "\n****ORIGINAL STUDENT ADDRESSES****")
    #10. Creating a list and iterate through that list using a for loop to print each item out on a new line
    for i in students:
        #4. Use the print function and .format() notation to print out the variable you assigned
        print( "Name: {} | Address: {} {} {} {} {} {}".format(i[0], i[1], i[2], i[3], i[4], i[5], i[6]))

    #List Comprehension
    revisedStudents = [my_fixAddress(i) for i in students]
    
    print( "\n****REVISED STUDENT ADDRESSES****")
    #9. Use of a for loop
    for i in revisedStudents:
        #4. Use the print function and .format() notation to print out the variable you assigned
        print( "Name: {} | Address: {} ".format( i[0],i[3] ))

    #sort on age
    print("\n****STUDENTS SORTED BY AGE****")
    print( sorted(revisedStudents, key=lambda x: x[1], reverse=True) )

    print("\n****STUDENTS OVER MIN AGE****")
    for i in revisedStudents:
        if i[1] >= 18 or i[5] >= minScore:
            print( "Name: {} | Age: {} | Score: {}".format( i[0],i[1],i[5]))

    print("\n****STUDENTS NOT FROM OREGON****")
    for i in revisedStudents:
        if not i[4] :
            print( "Name: {} | Address: {} ".format( i[0],i[3]))

    groups_touple = make_groups(revisedStudents, defaults)

    print("\n************************************")
    #11. Create a tuple and iterate through it using a for loop to print each item out on a new line
    #9. Use of a for loop x3
    for t in groups_touple: 
        for l in t:
            print("")
            for count,v in enumerate(l, start=0):
                if count > 0:
                    print "--"+str(count)+"--", ;
                    print(v)
                else:
                    print(v)
    return

my_main()
