def my_func(name):
    return city

def my_print( ):
    pass


def my_main():
    #tuple
    defaults = ( 'M', 21, 'Portland', 'OR')

    minAge = 18
    state = 'OR'
    minScore = 80.5

    go = True

    while go:

        students = [
        ['Jimmy Jones', 145 , 'NE', 'THOMPSON'   ,'St'  , 'Portland' , 'OR','503-246-3588', 20, 'M', True ,100.00],
        ['Timmy Smith', 5422, 'NW', 'miller'     ,'RD'  , 'Portland' , 'OR','503-875-2113', 24, 'M', False,88.75 ],
        ['Nancy White', 43  , 'SE', 'McLaughlin' ,'Ave' , 'Milwaukie', 'OR','503-577-8899', 28, 'F', True ,92.20 ],
        ['Tina Turner', 2365, 'sw', 'Barbur'     ,'Blvd', 'Portland' , 'OR','503-545-5455', 17, 'F', True ,66.95 ],
        ['Grace Jones', 5224, 'E' , 'Harbor'     ,'Ave' , 'Reading'  , 'PA','315-455-4566', 22, 'F', True ,97.58 ],
        ]
        #    0             1   2         3           4        5          6          7        8   9     10    11    
        print( "*Defaults*\nMinumum Age: {}\nLocal Area: {}\nMin. Test Score: {}\n***************************".format(minAge, state, minScore) )

        go = False
    revisedStudents = []
    
    #revisedStudents = [my_fixAddress(i) for i in students]

    def my_fixAddress(student):
        pass


    for i in students:
        address = "{} {} {} {}. {}, {}".format(i[1], i[2].upper(), i[3].title(), i[4].title(), i[5].title(), i[6].upper())
        revisedStudents.append([i[0], i[8], i[9], address, i[10], i[11]]) 
    print( revisedStudents )


my_main()
