from solcx import compile_standard
import solcx
import json
from web3 import Web3
import os
from dotenv import load_dotenv #.envファイルを扱うためのもの

#.envファイルに、秘密にしたい変数などを書き、.gitignoreでgithubにpushされないようにする

load_dotenv() #.envファイルの中身の内容を行う(こっちはmacやlinuxの形式で書いても大丈夫)

solcx.install_solc('0.6.0')

#with: to open this file and close
with open("./SimpleStorage.sol", "r", encoding="utf-8") as file:  #'r': read
    simple_storage_file = file.read()
    #print(simple_storage_file)


# Compile our solidity
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol":{"content":simple_storage_file}},
        "settings":{
            "outputSelection": {
                "*":{
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        },
    },
    solc_version = "0.6.0"
)

with open("compiled_code.json", "w") as file:  # 'w': write
    json.dump(compiled_sol, file)  # compiled_solをcompiled_code.jsonにエンコードする

#get bytecode  下の意味はcompiled_code.jsonを見ればわかる
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

#get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

#for connecting to rinkeby
w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/9c853dedc4a94644a58269225149ccd0"))   # https://infura.io/dashboard/ethereum/9c853dedc4a94644a58269225149ccd0/settings
chain_id = 4  #https://chainlist.org/
my_address = "0xcfc443e8602D14Ba48541e0B3BBb3D4D4B8aC747"  #MetaMaskのRinkebyから取得
#private_key = "0x1f28fc833c79a3c3e24463f47379989212be70c99147618b3ab6f85011741114"  # 必ず先頭に'0x'をつける(16進法で探すため)
#private_key = os.getenv("PRIVATE_KEY_FOR_BLOCKCHAIN_LESSON") #windowsの環境変数に登録したものを取得(設定した後、VSCを再起動しないとnoneのまま)
private_key = os.getenv("PRIVATE_KEY_BLOCKCHAIN_LESSON2")
print(private_key)
print(os.getenv("SOME_OTHER_VAR"))

# Create the contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
print(nonce)

#1. Build a transaction
#2. Sign a transaction
#3. Send a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {"gasPrice": w3.eth.gas_price,"chainId":chain_id, "from":my_address, "nonce":nonce} #"gasPrice"がないとerror
)

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# Send this signed transaction
print("Deploying contract...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction) 
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)  #transactionがきちんと承認されるまで、codeを止める
print("Deployed!")

# Working with the contract, you always need
# Contract Address
# Contract ABI
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Call -> Simulate making the call and getting a return value(in remix, this is like blue button)
# Transact -> Actually make a state change(like yellow button)
print(simple_storage.functions.retrieve().call())
print("Updating contract...")
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {"gasPrice": w3.eth.gas_price, "chainId":chain_id, "from":my_address, "nonce":nonce+1}  #なぜnonce+1なのか
)
signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key = private_key)
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("Updated!")

print(simple_storage.functions.retrieve().call())