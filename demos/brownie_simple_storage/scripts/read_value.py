from brownie import SimpleStorage, accounts, config


def read_contract():
    #simple_storage = SimpleStorage[0]   # get first contract
    simple_storage = SimpleStorage[-1]  # get the most recent contract
    # go take the index thats one less than the length
    # ABI
    # Address
    print(simple_storage.retrieve())


def main():
    read_contract()