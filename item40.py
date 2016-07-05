import datetime

def validateDate(dob):

    try:
        s = dob.split('/')
        d = datetime.date(int(s[2]),int(s[0]),int(s[1]))

#check if date entered is greater than today
        if  d > datetime.date.today():
            print('You can\'t be born in the future! Enter birthdate as DD/MM/YYYY')
            return True
        else:
            return False
    except:
        print('I don\'t understand what you mean... enter your birthdate as DD/MM/YYYY')
        return True

def calcAge(d):
    currYr = int(str(datetime.date.today())[:4])
    bornYr = int(d[6:])
    return currYr-bornYr

def calcDaysAlive(dob):
    s = dob.split('/')
    dFrom = datetime.date(int(s[2]),int(s[0]),int(s[1]))
    dTo = datetime.date.today()
    delta = dTo - dFrom
    return delta.days        

def summary(n,dob):
    a = calcAge(dob)
    days = calcDaysAlive(dob)
    minutes = days * 1440
    seconds = days * 86400
    #days = a * 365    #minutes = a * 525948    #seconds = a * 31556926
    if a < 13:
        print('\n{}, you\'re just a baby!'.format(n))
    elif a >=13 and a < 20:
        print('\nEnjoy those teen years {}!'.format(n))
    elif a >=20 and a < 30:
        print('\n{}, you\'re in the prime of your life!'.format(n))
    elif a >=30 and a < 40:
        print('\nDon\'t worry {}, it\'s not all downhill after 30!'.format(n))
    elif a >=40 and a < 50:
        print('\nYou\'ve done a lot! Enjoy your 40s {}!'.format(n))
    elif a >=50 and a < 60:
        print('\nYour 50s are some of the best years of {}\'s life!'.format(n))
    elif a >=60 and a < 70:
        print('\nIt\'s a golden time {}!'.format(n))
    elif a >=70 and a < 80:
        print('\nYou\'re more experienced than most {}! Enjoy life!'.format(n))
    elif a >=80 and a < 90:
        print('\nWe could all learn a lesson from you {}!'.format(n))
    elif a >=90 and a < 100:
        print('\nKeep it up {}! You\'re almost to triple digits!'.format(n))
    elif a >=100 :
        print('\nAmazing! What\'s your secret {}!'.format(n))

    print('From your birthday on {}, you\'ve been alive for {} days, \nwhich is {} minutes... \nor {} seconds!\n'.format(dob, days, minutes, seconds))

def main():
    print("Let's see how long you have lived in days, minutes, and seconds.")
    name = ''
    while name == '':
        name = raw_input("Enter your name: ")
        if name == '':
            print('Name can\'t be blank!')
        else:
            break
    print("and your...")
    badDate = True
    while badDate:
        dob = str(raw_input("birthdate (mm/dd/yyyy): "))
        badDate = validateDate(dob)

    summary(name,dob)

main()
