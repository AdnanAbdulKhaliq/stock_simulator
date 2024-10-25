from ScrapeYahoo import FetchData
from MySQL import setup
from pandas import DataFrame
from datetime import date


DB, Cursor = setup()

def update():
    Tickers = []
    Cursor.execute('SELECT Ticker FROM Companies WHERE SOLD is NULL;')
    Tickers.extend(Cursor.fetchall())
    Cursor.execute('SELECT Ticker FROM Indexes WHERE SOLD is NULL;')
    Tickers.extend(Cursor.fetchall())
    Cursor.execute('SELECT Ticker FROM Mining WHERE SOLD is NULL;')
    Tickers.extend(Cursor.fetchall())
    
    for i in Tickers:
        for j in i:
            if j== []:
                print('empty')
                return 0
                
            Data = FetchData(j)
            if Data['Type'] == 'Company':
                Cursor.execute(f"UPDATE Companies SET CurrentPrice = {Data['Price']}, DivRate = {Data['DivRate']}, DivDate = '{Data['DivDate']}', Beta = {Data['Beta']}, DeltaTTM = {Data['DeltaTTM']} WHERE Ticker = '{j}';")
                DB.commit()
                print(j, 'updated')
            elif Data['Type'] == 'Index':
                cmd = "UPDATE Indexes SET CurrentPrice = %s WHERE Ticker = %s;"
                val = (Data['Price'], j)
                Cursor.execute(cmd, val)
                DB.commit()
                print(j, 'updated')

            else:
                cmd = "UPDATE Mining SET CurrentPrice = %s WHERE Ticker = %s;"
                val = (Data['Price'], j)
                Cursor.execute(cmd, val)
                DB.commit()
                print(j, 'updated')

        


# Data: ['Type', 'Ticker', 'Name', 'Currency', 'Price', 'DivRate', 'DivDate', 'Beta', 'DeltaTTM']
#Companies: (Ticker, Name, BuyDate, Currency, BuyPrice, BuyQty, CurrentPrice, DivRate, DivDate, Beta, DeltaTTM, Sold)

# update()

while True:
    choice = input('1. Buy Stock\n2. Sell Stock\n3. View Stock Data\n4. View Financial Statement\n5. Update\n6. Exit\n\nEnter choice: ')

    if choice == '1':
        STOCK = input('Enter Stock Ticker: ')
        Date = date.today()
        Data = FetchData(STOCK)
        # try:
        #     Data = FetchData(STOCK)
        # except:
        #     print('Invalid Stock Ticker!')
        #     continue
            
        Qty = float(input(f'Enter value of stocks to buy at the price of {Data["Currency"]} {Data["Price"]} per stock: '))/Data['Price']
        
        if Data['Type'] == 'Company':
            cmd = 'INSERT INTO Companies (Ticker, Name, BuyDate, Currency, BuyPrice, BuyQty, DivRate, DivDate, Beta, DeltaTTM) Values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
            values = (Data['Ticker'], Data['Name'], Date, Data['Currency'], Data['Price'], Qty, Data['DivRate'], Data['DivDate'] , Data['Beta'], Data['DeltaTTM'])
            print(values)
            Cursor.execute(cmd, values)
            DB.commit()
        
        elif Data['Type'] in ('Index', 'Mining'):
            nm = 'Indexes' if Data['Type'] == 'Index' else 'Mining'
            cmd = f'INSERT INTO {nm} (Ticker, Name, BuyDate, Currency, BuyPrice, BuyQty) values(%s, %s, %s, %s, %s, %s);'
            values = (Data['Ticker'], Data['Name'], Date, Data['Currency'], Data['Price'], Qty)
            Cursor.execute(cmd, values)
            DB.commit()
            
        else:
            print('Error, Nothing added')
            
    if choice == '2':
        choice2 = input('\t1. Sell a  Company Stock\n\t2. Sell an Index Stock\n\t3. Sell a Mining Stock\n\n\tEnter choice: ')
        STOCK = input('\tEnter Stock Ticker: ')
        if choice2 == '1':
            cmd = 'UPDATE Companies SET Sold = %s WHERE Ticker = %s'
            val = (1, STOCK)
            Cursor.execute(cmd, val)
            DB.commit()
            print('Sold stock\n\n')
        if choice2 == '2':
            cmd = 'UPDATE Indexes SET Sold = %s WHERE Ticker = %s'
            val = (1, STOCK)
            Cursor.execute(cmd, val)
            DB.commit()
            print('Sold stock\n\n')
        if choice2 == '3':
            cmd = 'UPDATE Mining SET Sold = %s WHERE Ticker = %s'
            val = (1, STOCK)
            Cursor.execute(cmd, val)
            DB.commit()
            print('Sold stock\n\n')


            
    elif choice == '3':
        choice2 = input('\t1. View Company Stocks\n\t2. View Index Stocks\n\t3. View Mining Stocks\n\n\tEnter choice: ')

        if choice2 == '1':
            Cursor.execute('DESC Companies;')
            Headers = Cursor.fetchall()
            Headers = [i[0] for i in Headers]
            Cursor.execute('SELECT * FROM Companies;')
            data = Cursor.fetchall()
            df = DataFrame(data)
            df.columns = Headers
            print(df, end='\n\n')
            
        elif choice2 == '2':
            Cursor.execute('DESC Indexes;')
            Headers = Cursor.fetchall()
            Headers = [i[0] for i in Headers]
            Cursor.execute('SELECT * FROM Indexes;')
            data = Cursor.fetchall()
            df = DataFrame(data)
            df.columns = Headers
            print(df, end='\n\n')
            
        elif choice2 == '3':
            Cursor.execute('DESC Mining;')
            Headers = Cursor.fetchall()
            Headers = [i[0] for i in Headers]
            Cursor.execute('SELECT * FROM Mining;')
            data = Cursor.fetchall()
            df = DataFrame(data)
            df.columns = Headers
            print(df, end='\n\n')
    
    elif choice == '4':
        Invested = 0
        Current = 0
        for i in ('Companies', 'Indexes', 'Mining'):
            Cursor.execute(f'SELECT SUM(BuyPrice*BuyQty) FROM {i};')
            try:
                Invested += float(Cursor.fetchall()[0][0])
                print(Invested, i)
            except:
                pass
        
            Cursor.execute(f'SELECT SUM(CurrentPrice*BuyQty) FROM {i};')
            try:
                Current += float(Cursor.fetchall()[0][0])
            except:
                pass
        temp_ret = round((Current-Invested)/Invested, 3)
        Invested = round(Invested, 2)
        Current = round(Current, 2)
        Returns = str(temp_ret*100) + '%'

        print('Invested: ', Invested)
        print('Current: ', Current)
        print('Returns: ', Returns)


    elif choice == '5':
        update()
        print('updated!\n')
        
    elif choice == '6':
        break

    else:
        print('Invalid input!\n\n')