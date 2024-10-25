import mysql.connector as sql


def setup():
    global MyDB
    global MyCursor
    for i in range(3):
        
        pwd = input('Enter password: ')
        try:
            MyDB = sql.connect(host='localhost', user='root', password=pwd, database='stocks')
            break
        except:
            print('Invalid Password!')
            print(f'Attempt {i+1} of 3\n')
            
    else:
        print('\nExiting...')
        exit()

    MyCursor = MyDB.cursor()
    
    return (MyDB, MyCursor)