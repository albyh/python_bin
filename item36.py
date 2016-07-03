def my_func(name):
    return city

def my_print( ):
    pass

def my_fixAddress(i):
    address = "{} {} {} {}. {}, {}".format(i[1], i[2].upper(), i[3].title(), i[4].title(), i[5].title(), i[6].upper())
    return [i[0], i[8], i[9], address, i[10], i[11]]

def make_groups(s, defaults):
    x = 0
    even_group = []
    odd_group = []
    nopass_group = []
    while x < len(s):
        #5. Use each of these operators +, ­ , * , / , +=, ­= , %
        #6. Use of logical operators and, or , not
        if x % 2 == 0 and s[x][5] > (defaults[2]*.95):
            even_group.append(s[x])
        elif s[x][5] > defaults[2]:
            odd_group.append(s[x])
        else:
            nopass_group.append(s[x])
        #5. Use each of these operators +, ­ , * , / , +=, ­= , %
        x += 1    

    print("\n******* EVEN GROUP *******")
    print(even_group)
    print("\n******** ODD GROUP *******")
    print(odd_group)
    print("\n******* NO PASS GROUP ******")
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
   
    print( "\nORIGINAL STUDENT ADDRESSES")
    for i in students:
        #4. Use the print function and .format() notation to print out the variable you assigned
        print( "Name: {} | Address: {} {} {} {} {} {}".format(i[0], i[1], i[2], i[3], i[4], i[5], i[6]))

    #List Comprehension
    revisedStudents = [my_fixAddress(i) for i in students]
    
    print( "\nREVISED STUDENT ADDRESSES")
    for i in revisedStudents:
        #4. Use the print function and .format() notation to print out the variable you assigned
        print( "Name: {} | Address: {} ".format( i[0],i[3] ))

    #sort on age
    print( sorted(revisedStudents, key=lambda x: x[1], reverse=True) )

    print( revisedStudents )

    groups_touple = make_groups(revisedStudents, defaults)

    #11. Create a tuple and iterate through it using a for loop to print each item out on a new line
    for t in groups_touple: 
        for l in t:
            print("\n")
            for count,v in enumerate(l, start=0):
                if count > 0:
                    print "--"+str(count)+"--", ;
                    print(v)
                else:
                    print(v)



    

    return
    


my_main()
