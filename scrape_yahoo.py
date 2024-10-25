from bs4 import BeautifulSoup
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0'}
url = 'https://finance.yahoo.com/quote/{}/key-statistics?p={}'

def FetchData(stock):

    response = requests.get(url.format(stock, stock), headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    name = soup.title.text
    name = name[:name.index(')')+1]

    price, change, percentage = soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('fin-streamer')[:3]
    temp = soup.find('div', {'class': 'C($tertiaryColor) Fz(12px)'}).find('span').text
    currency = temp[-3:]
    price = float(price.text.replace(',', ''))
    change = change.text
    percentage = percentage.text[1:-1]

    if '^' in stock:
        stock_type = 'Index'
        beta = 'NULL'
        del52 = 'NULL'
        div_rate = 0
        div_date = 'NULL'

    elif 'COMEX' in temp:
        stock_type = 'Mining'
        beta = 'NULL'
        del52 = 'NULL'
        div_rate = 0
        div_date = 'NULL'

    else:
        stock_type = 'Company'
        l1 = soup.find('div', {'class': 'Fl(end) W(50%) smartphone_W(100%)'}).find_all('td', {'class': 'Fw(500) Ta(end) Pstart(10px) Miw(60px)'})
        beta = float(l1[0].text)
        del52 = float(l1[1].text[:-1])*0.01
        
        l2 = soup.find('div', {'class': 'Pstart(20px) smartphone_Pstart(0px)'}).find_all('div', {'class': 'Pos(r) Mt(10px)'})[2].find_all('td', {'class': 'Fw(500) Ta(end) Pstart(10px) Miw(60px)'})

        for i in range(len(l2)):
            if l2[i] == 'N/A':
                l2[i] = None

        div_rate = l2[0].text
        div_rate = 0 if div_rate == 'N/A' else div_rate
        div_date = l2[6].text
        div_date = 'NULL' if div_date == 'N/A' else div_date

    # print(stock_type)
    # print(currency, price)
    # print('beta', beta)
    # print('del52', del52)
    # print('div_rate', div_rate)
    # print('div_date', div_date)

    Data = {'Type': stock_type, 'Ticker': stock, 'Name': name, 'Currency': currency, 'Price': price, 'DivRate': div_rate, 'DivDate': div_date, 'Beta': beta, 'DeltaTTM': del52}

    return Data