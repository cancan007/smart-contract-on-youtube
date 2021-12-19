from scripts.helpful_scripts import get_account
from brownie import interface, network, config

def get_weth():
    """
    Mints WETH by depositing ETH.
    """
    # ABI
    # Address
    account = get_account()
    weth = interface.IWeth(config['networks'][network.show_active()]['weth_token'])  #maybe, you can get actual functions with weth_token
    tx = weth.deposit({'from':account, 'value':0.1*10**18})  # deposit 0.1 eth and receive 0.1 weth
    tx.wait(1)
    print('Recieved 0.1 WETH')
    #return tx

def main():
    get_weth()