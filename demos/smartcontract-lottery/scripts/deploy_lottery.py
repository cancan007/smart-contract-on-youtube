from scripts.helpful_scripts import get_account, get_contract, fund_with_link
from brownie import Lottery, config, network
import time


def deploy_lottery():
    #account = get_account(id="freecodecamp-account")  #id: you can see with 'brownie accounts list'
    account = get_account()
    lottery = Lottery.deploy(
        get_contract('eth_usd_price_feed').address,
        get_contract('vrf_coordinator').address,
        get_contract('link_token').address,
        config['networks'][network.show_active()]['fee'],
        config['networks'][network.show_active()]['keyhash'],
        {'from': account},
        #publish_source=config['networks'][network.show_active()].get('verify', False)  # if there is not verify key, default is False
        # if I release publich_source, I have an error
    )
    print('Deployed lottery!')
    return lottery

def start_lottery():
    #account = get_account(id="freecodecamp-account")
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({'from':account})
    starting_tx.wait(1)  # you have to wait for late transaction every time 
    print('The lottery is started!')

def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100000000
    tx = lottery.enter({"from":account, "value":value})  #this function is payable, so we have to value key
    tx.wait(1)
    print("You entered the lottery!")

def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # fund the contract
    # then end the lottery
    tx = fund_with_link(lottery.address) # because we have to pay the link_token to get the service
    tx.wait(1)
    ending_transaction = lottery.endLottery({"from":account})
    ending_transaction.wait(1)
    time.sleep(60)
    print(f"{lottery.recentWinner()} is the new winner!")

def main():
    
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()

#result: miss the recentWinner, I guess something wrong in Lottery.sol
    