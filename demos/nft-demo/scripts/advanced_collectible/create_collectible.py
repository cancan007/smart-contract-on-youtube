from brownie import AdvancedCollectible, accounts
from scripts.helpful_scripts import get_account, get_contract, fund_with_link
from web3 import Web3

def main():
    account = get_account()
    advanced_collectible = AdvancedCollectible[-1]
    fund_with_link(advanced_collectible.address, amount=Web3.toWei(0.1, 'ether'))
    creation_transaction = advanced_collectible.createCollectible({'from':account})
    creation_transaction.wait(1)
    print('Collectible created!')