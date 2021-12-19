from brownie import accounts, config, SimpleStorage, network
import os

def deploy_simple_storage():
    #account = accounts[0]  #Only for Local ganache chain
    #account = accounts.load("freecodecamp-account")
    #account = accounts.add(os.getenv("PRIVATE_KEY"))
    #account = accounts.add(config["wallets"]["from_key"])  #get from brwnie-config.yaml which is connected with environmental variables
    #print(account)
    account = get_account()
    simple_storage = SimpleStorage.deploy({"from":account})
    stored_value = simple_storage.retrieve()  #call
    print(stored_value)
    transaction = simple_storage.store(15,{"from":account})  # transact   You need {"from": ---} if it is state changeable
    transaction.wait(1)
    updated_stored_value = simple_storage.retrieve()
    print(updated_stored_value)


def get_account():
    if(network.show_active() == "development"):
        return accounts[0]
    else:
        return accounts.add(config['wallets']['from_key'])
def main():
    deploy_simple_storage()