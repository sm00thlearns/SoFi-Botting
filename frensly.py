from web3 import Web3
import requests
import time
import json
from hexbytes import HexBytes  # Gerekli kütüphane


# 'Base Mainnet' RPC endpoint'ine bağlanın
w3 = Web3(Web3.HTTPProvider('https://mainnet.base.org'))

# Sözleşme ABI'sini ekleyin
frensly_abi = [
    {"inputs":[{"internalType":"address","name":"_feeDestination","type":"address"},{"internalType":"address","name":"_owner","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},
    {"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"holder","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Claim","type":"event"},
    {"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"destination","type":"address"}],"name":"FeeDestinationChanged","type":"event"},
    {"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"oldHolder","type":"address"},{"indexed":True,"internalType":"address","name":"holder","type":"address"},{"indexed":True,"internalType":"address","name":"subject","type":"address"},{"indexed":False,"internalType":"uint256","name":"shares","type":"uint256"}],"name":"NewEligibleHolder","type":"event"},
    {"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":True,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},
    {"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"subject","type":"address"}],"name":"SubjectAdded","type":"event"},
    {"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"trader","type":"address"},{"indexed":True,"internalType":"address","name":"subject","type":"address"},{"indexed":True,"internalType":"bool","name":"isBuy","type":"bool"},{"indexed":False,"internalType":"uint256","name":"shareAmount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"ethAmount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"protocolEthAmount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"subjectEthAmount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"holderEthAmount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"supply","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"price","type":"uint256"}],"name":"Trade","type":"event"},
    {"inputs":[],"name":"DECIMALS","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"HOLDER_FEE_PERCENT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"MAX_SHAREHOLDERS_PER_SUBJECT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"PROTOCOL_FEE_PERCENT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"SUBJECT_FEE_PERCENT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"availableToClaim","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"address","name":"sharesSubject","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"buyShares","outputs":[],"stateMutability":"payable","type":"function"},
    {"inputs":[],"name":"claim","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[{"internalType":"address","name":"sharesSubject","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"getBuyPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"address","name":"sharesSubject","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"getBuyPriceAfterFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"uint256","name":"supply","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"getPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},
    {"inputs":[{"internalType":"address","name":"sharesSubject","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"getSellPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"address","name":"sharesSubject","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"getSellPriceAfterFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"initShares","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"isSharesSubject","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"protocolFeeDestination","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[{"internalType":"address","name":"sharesSubject","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"sellShares","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[{"internalType":"address","name":"_feeDestination","type":"address"}],"name":"setFeeDestination","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"sharesBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"sharesSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"subjectToEligibleHolderShares","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"subjectToEligibleHolders","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"address","name":"","type":"address","internalType":"address","name":"","type":"address"}],"name":"subjectToHolderToIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"subjectToValidHolderCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}
]

ft_abi = [
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "previousOwner",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "newOwner",
                "type": "address"
            }
        ],
        "name": "OwnershipTransferred",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "trader",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "subject",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "bool",
                "name": "isBuy",
                "type": "bool"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "shareAmount",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "ethAmount",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "protocolEthAmount",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "subjectEthAmount",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "supply",
                "type": "uint256"
            }
        ],
        "name": "Trade",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "sharesSubject",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "buyShares",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "sharesSubject",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "getBuyPrice",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "sharesSubject",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "getBuyPriceAfterFee",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "supply",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "getPrice",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "pure",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "sharesSubject",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "getSellPrice",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "sharesSubject",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "getSellPriceAfterFee",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "protocolFeeDestination",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "protocolFeePercent",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "renounceOwnership",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "sharesSubject",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "sellShares",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_feeDestination",
                "type": "address"
            }
        ],
        "name": "setFeeDestination",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_feePercent",
                "type": "uint256"
            }
        ],
        "name": "setProtocolFeePercent",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_feePercent",
                "type": "uint256"
            }
        ],
        "name": "setSubjectFeePercent",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "name": "sharesBalance",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "name": "sharesSupply",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "subjectFeePercent",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "newOwner",
                "type": "address"
            }
        ],
        "name": "transferOwnership",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]


# JSON formatına dönüştürün
frensly_abi_json = json.loads(json.dumps(frensly_abi))
ft_abi_json = json.loads(json.dumps(ft_abi))

frensly_address = '0x66fA4044757Fb7812EF5b8149649d45d607624E0'  # Frensly'nin sözleşme adresi
ft_address = '0xCF205808Ed36593aa40a44F10c7f7C2F67d4A4d4'  # FT'nin sözleşme adresi

frensly = w3.eth.contract(address=frensly_address, abi=frensly_abi_json)
ft = w3.eth.contract(address=ft_address, abi=ft_abi_json)

# Discord Webhook URL'sini tanımlayın
webhook_url = 'https://discord.com/api/webhooks/1168846973655339008/HClQiRKX5xkXalo3CIGuztJZp3zHQou3VDUYX5i_G1jEAIA05ajb5UMD0QbmskbGDC1m'

# Önceki işlem hashini takip etmek için bir değişken tanımlayın
last_transaction_hash = ''
transactions = []

# Daha önce gönderilmiş adresleri takip etmek için bir küme (set) tanımlayın
processed_addresses = set()

# 'Init Shares' işlemlerini almak ve Discord Webhook ile işlemi başlatan adresi iletmek için döngü
while True:
    # Son işlem bloğunu alın
    current_block = w3.eth.block_number
    for block_number in range(current_block, current_block - 10, -1):
        block = w3.eth.get_block(block_number)
        transactions += block['transactions']
        for tx_hash in block['transactions']:
            if tx_hash != last_transaction_hash:
                tx_receipt = w3.eth.get_transaction_receipt(tx_hash)
                if tx_receipt is not None and tx_receipt['to'] == frensly_address:
                    # 'Init Shares' işlemi bulundu
                    input_data = w3.eth.get_transaction(tx_hash).input
                    hex_converted_input_data = input_data.hex()
                    if hex_converted_input_data.startswith('0x737b83de'):
                        from_address = tx_receipt['from']

                        # Adres daha önce işlem göndermediyse ve işlemi Discord Webhook ile göndermediyse işlemi işaretle
                        if from_address not in processed_addresses:
                            # 'Init Shares' işlemi bulundu, Discord Webhook ile işlemi başlatan adresi gönderin
                            message = f'Yeni Init Shares işlemi başlatan adres: {from_address}'
                            requests.post(webhook_url, json={'content': message})

                            # Adresi daha önce işlem gönderdi olarak işaretle
                            processed_addresses.add(from_address)

                    # En son işlem hash'ini güncelleyin
                    last_transaction_hash = tx_hash

    # FT ve Frensly'deki alım ve satım fiyatlarını kontrol edin
    ft_buy_price = ft.functions.getBuyPrice(ft_address, 1).call()
    ft_sell_price = ft.functions.getSellPrice(ft_address, 1).call()
    frensly_buy_price = frensly.functions.getBuyPrice(frensly_address, 1).call()
    frensly_sell_price = frensly.functions.getSellPrice(frensly_address, 1).call()

    # Alım ve satım fiyatlarını Discord Webhook ile paylaşın
    price_message = f'FT Alım Fiyatı: {ft_buy_price}, FT Satım Fiyatı: {ft_sell_price}\nFrensly Alım Fiyatı: {frensly_buy_price}, Frensly Satım Fiyatı: {frensly_sell_price}'
    requests.post(webhook_url, json={'content': price_message})

    # Sürekli döngüyü yavaşlatmak için bir bekleme ekleyin
    time.sleep(0.1)
