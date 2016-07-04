def calcs(n,a):
    days = a * 365
    minutes = a * 525948
    seconds = a * 31556926
    if a < 13:
        print('{}, you\'re just a baby!'.format(n))
    elif a >=13 and a < 20:
        print('Enjoy those teen years {}!'.format(n))
    elif a >=20 and a < 30:
        print('{}, you\'re in the prime of your life!'.format(n))
    elif a >=30 and a < 40:
        print('Don\'t worry {}, it\'s not all downhill after 30!'.format(n))
    elif a >=40 and a < 50:
        print('Enjoy these years {}!'.format(n))
    elif a >=50 and a < 60:
        print('Some of the best years of {}\'s life!'.format(n))
    elif a >=60 and a < 70:
        print('It\'s a golden time {}!'.format(n))
    elif a >=70 and a < 80:
        print('You\'re more experienced than most {}! Enjoy life!'.format(n))
    elif a >=80 and a < 90:
        print('We could all learn a lesson from you {}!'.format(n))
    elif a >=90 and a < 100:
        print('Keep it up {}! You\'re almost to triple digits!'.format(n))
    elif a >=100 and a < 120:
        print('Amazing! What\'s your secret {}!'.format(n))

    print('You\'ve been alive for {} days, or {} minutes, or {} seconds!'.format(days, minutes, seconds))

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
    age = 0
    while age < 1 or age > 120:
        age = raw_input("age: ")
        if age == '':
            print('Can\'t calculate if you don\'t give me a number...\nEnter your age: ')
        else:
            try:
                age = int(age)
                if age > 0 and age < 120:
                    break
                else:
                    print('Yeah, right!\nEnter your REAL age:')
            except:
                print('I don\'t understand what you mean. Enter your age:')
    calcs(name,age)

main()
