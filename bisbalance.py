#!/usr/bin/python3
from datetime import datetime
from bismuthclient.bismuthclient import BismuthClient
client = BismuthClient(wallet_file='wallet.der')
default_wallet_address = []

def to_localtime(stamp_time):
    #print(stamp_time)
    t = datetime.utcfromtimestamp(stamp_time)
    return(t.strftime('%Y-%m-%d %H:%M'))

def tx_history(addr):
    transactions = client.command("addlistlim", [addr, 5])
    for tx in transactions:
        #print(tx)
        time = to_localtime(tx[1])
        print("block:{}, utc:{}, from:{}, to:{}, amount:{}".format(tx[0],time,tx[2],tx[3],tx[4]))

def main():
    wallet_address = input("Wallet Address: ")
    if not wallet_address:
        wallet_address = default_wallet_address
        if client.address:
            wallet_address = wallet_address + [ client.address ]
    else:
        wallet_address = [ x.strip() for x in str(wallet_address).split(',') ]
        if len(wallet_address) < 2 :
            for addr in  wallet_address:
                wallet_address = [ x.strip() for x in str(addr).split(' ') ]
        if client.address:
            wallet_address = wallet_address + [ client.address ]
    for address in wallet_address:
        print(f"Looking up address {address} ...")
        balance = client.command("balanceget", [address])
        balance = balance[0]
        if balance == '0E-8':
            balance = 0.000
        print(f"Your current balance is {balance}")
        tx_history(address)

if __name__ == '__main__':
    main()


