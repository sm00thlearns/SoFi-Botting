import json
from web3 import Web3, middleware
import requests
import time
from colorama import Fore, Style, init
import os

init()

# Discord Webhook URL
discord_webhook_url = ''

# Ethereum RPC URL
web3 = Web3(Web3.HTTPProvider('https://api.avax.network/ext/bc/C/rpc')) # Bu URL'yi Ethereum RPC URL ile değiştirin

# Kontrat adresi
private_key = ''
application_address = ''
contract_address = ''  # Kontratınızın adresi ile değiştirin
contract_abi = []

transactions = []
last_transaction_hash = None  

cchain_middleware = middleware.geth_poa_middleware
web3.middleware_onion.inject(cchain_middleware, layer=0)

contract = web3.eth.contract(address=contract_address, abi=contract_abi)
account = web3.eth.account.from_key(private_key)

start_block = web3.eth.block_number - 5  # Son 100 bloğu izleyin
event_filter = contract.events.Trade.create_filter(fromBlock=start_block)


processed_addresses = set()
bought_addresses = set()

os.system('cls')

while True:

    for address in bought_addresses:
        key_balance = contract.functions.keysBalance(application_address, address).call()
        sell_price_for_bought =  contract.functions.getSellPrice(address, 1).call()
        sell_price_avax_for_bought = web3.from_wei(sell_price_for_bought, 'ether')
        if key_balance != 0:
            if sell_price_avax_for_bought > 0.2 :
                # Gas ve gas fiyatını ayarlayın (isteğe bağlı olarak)
                gas = 200000  # Alım işlemi için tahmini gas limit
                gas_price = web3.to_wei('25', 'gwei')  # Gas fiyatı
                # Alım işlemi için gereken fonksiyonu çağırın
                transaction = contract.functions.sellKeys(address, 1).build_transaction({
                    'chainId': 43114,  # Avalanche C-Chain ağının chain ID'si
                    'gas': gas,
                    'gasPrice': gas_price,
                    'nonce': web3.eth.get_transaction_count(account.address),
                    'value': sell_price_for_bought
                })
                signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)
                tx_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
                print(Fore.GREEN + "Satış işlemi başlatıldı. "+ address +" için \nİşlem Hash: " + tx_hash.hex() +" Fiyat: "+ sell_price_avax_for_bought + Style.RESET_ALL)
                bought_addresses.remove(address)
            else:
                print(Fore.RED + "Alınanlar fiyat altında. " + Style.RESET_ALL)
        else:
            print(f'Bir şekilde {address} satın alınamamış.')
            bought_addresses.remove(address)

    try :
        event_logs = event_filter.get_all_entries()
        
        for log in event_logs:
            trader_address = log.args.trader
            subject_address = log.args.subject
            eth_amount = log.args.ethAmount
            
            if eth_amount == 0 and trader_address == subject_address and trader_address not in processed_addresses:
                # Alım ve satış fiyatlarını almak için kontrat fonksiyonlarını kullanın
                amount = log.args.keyAmount
                buy_price = contract.functions.getBuyPrice(subject_address, amount).call()
                sell_price = contract.functions.getSellPrice(subject_address, amount).call()
                buy_price_avax = web3.from_wei(buy_price, 'ether')
                sell_price_avax = web3.from_wei(sell_price, 'ether')
                buy_price_avax1 = str(buy_price_avax)
                sell_price_avax1 = str(sell_price_avax)
    
                if trader_address not in processed_addresses:
                    if buy_price_avax < 0.005:
                        # Gas ve gas fiyatını ayarlayın (isteğe bağlı olarak)
                        gas = 200000  # Alım işlemi için tahmini gas limit
                        gas_price = web3.to_wei('25', 'gwei')  # Gas fiyatı
                        # Alım işlemi için gereken fonksiyonu çağırın
                        transaction = contract.functions.buyKeys(application_address, trader_address, 1).build_transaction({
                            'chainId': 43114,  # Avalanche C-Chain ağının chain ID'si
                            'gas': gas,
                            'gasPrice': gas_price,
                            'nonce': web3.eth.get_transaction_count(account.address),
                            'value': buy_price
                        })
                        signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)
                        tx_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
                        print(Fore.GREEN + trader_address +" için alım işlemi başlatıldı. \nİşlem Hash: " + tx_hash.hex() + "Fiyat : " + buy_price_avax1 + Style.RESET_ALL)
                        bought_addresses.add(trader_address)
                    else:
                         print(Fore.RED + trader_address +" için alım yapılamadı, alış fiyatı belirlenenden fazla. Fiyat : " + buy_price_avax1 + Style.RESET_ALL)
    
                # İşlenen adresi kümeye ekleyin
                processed_addresses.add(trader_address)

    except ValueError:
        print(event_logs)
        print("\n xd")
    except:
        print("xd")

    # İşlem aralarında bir süre bekleme
    time.sleep(0.3)