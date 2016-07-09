import datetime

def openOrClosed(x):
    
    if (pdxTime.hour + x[1]) >= hrFrom and (pdxTime.hour + x[1]) < hrTo:
        print( '{} is currently: {}'.format( x[0], 'OPEN' ))
    else:
        print( '{} is currently: {}'.format( x[0], 'CLOSED' ))

#USE CURRENT PDX TIME 
pdxTime = datetime.datetime.today()

#OR TEST ANY PDX TIME
#pdxTime = datetime.time( 14, 01, 00 )

cities  = [('NYC Store', 3), ('London Store', 8)]
hrFrom  = 9
hrTo    = 21

for el in cities:   
    openOrClosed(el)


