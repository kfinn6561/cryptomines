from requests import Session
import json

CRYPTO_API_KEY='c1fc3d61-034c-4347-8fce-1293556618bf'

bnb_price=600#this will get updated by init
etl_price=100
initialised=False



def get_latest_prices():
    print('downloading latest crypto prices')
    global bnb_price,etl_price,initialised
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
    'symbol':'BNB,ETERNAL',
    'convert':'USD'
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': CRYPTO_API_KEY,
    }

    session = Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    data=data['data']
    for coin in data.values():
        if coin['symbol']=='BNB':
            bnb_price=coin['quote']['USD']['price']
        elif coin['symbol']=='ETERNAL':
            etl_price=coin['quote']['USD']['price']
        else:
            print('unexpected coin '+coin['symbol'])
    print(f'BNB: {bnb_price: 0.2f}\tETL: {etl_price: 0.2f}')
    initialised=True

def etl_to_usd(etl):
    if not initialised:
        get_latest_prices()
    return etl*etl_price

def usd_to_etl(usd):
    if not initialised:
        get_latest_prices()
    return usd/etl_price

def bnb_to_usd(bnb):
    if not initialised:
        get_latest_prices()
    return bnb*bnb_price

def usd_to_bnb(usd):
    if not initialised:
        get_latest_prices()
    return usd/bnb_price

def bnb_to_etl(bnb):
    if not initialised:
        get_latest_prices()
    return bnb*bnb_price/etl_price

def etl_to_bnb(etl):
    if not initialised:
        get_latest_prices()
    return etl*etl_price/bnb_price