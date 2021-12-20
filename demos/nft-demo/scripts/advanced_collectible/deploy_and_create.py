from scripts.helpful_scripts import get_account, OPENSEA_URL
from brownie import AdvancedCollectible

# https://github.com/PatrickAlphaC/nft-mix/blob/main/scripts/simple_collectible/create_collectible.py
sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"



def deploy_and_create():
    account = get_account()
    # We want to be able to use the deployed contracts if we are on a testnet
    # Otherwise, we want to deploy some mocks and use those
    # Rinkeby(Opensea works only on rinkeby)
    advanced_collectible = AdvancedCollectible.deploy({'from':account})

    

def main():
    deploy_and_create()