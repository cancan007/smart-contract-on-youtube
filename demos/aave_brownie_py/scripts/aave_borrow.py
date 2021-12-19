from scripts.helpful_scripts import get_account
from brownie import network, config, interface
from scripts.get_weth import get_weth
from web3 import Web3

# 0.1
amount = Web3.toWei(0.1, 'ether')  # 100000000000000000

def main():
    account = get_account()
    erc20_address = config['networks'][network.show_active()]['weth_token']
    if network.show_active() in ['mainnet-fork']:
        get_weth()
    lending_pool = get_lending_pool()
    # Approve sending out ERC20 tokens
    approve_erc20(amount, lending_pool, erc20_address, account)
    print('Depositing...')
    tx = lending_pool.deposit(erc20_address, amount, account.address, 0, {'from':account})  # don't care about this 0, it's already done service, just put 0
    tx.wait(1)
    print('Deposited!')
    # ... how much?
    borrowable_eth, total_debt = get_borrowable_data(lending_pool, account)
    # 0.1 ETH deposited
    # 0.0825 ETH you can borrow
    print("Let's borrow!")
    # DAI in terms of ETH
    dai_eth_price = get_asset_price(config['networks'][network.show_active()]['dai_eth_price_feed'])

def get_lending_pool():  # https://docs.aave.com/developers/the-core-protocol/lendingpool
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config['networks'][network.show_active()]['lending_pool_addresses_provider']
    )
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    # ABI
    # Address - Check!
    lending_pool = interface.ILendingPool(lending_pool_address)  #lending_pool:  entire contract what we want
    return lending_pool

def approve_erc20(amount, spender, erc20_address, account):
    print('Approving ERC20 token...')
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {'from':account})
    tx.wait(1)
    print('Approved!')
    return tx

def get_borrowable_data(lending_pool, account):
    (
        total_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        current_liquidation_threshold,
        ltv,
        health_factor
    ) = lending_pool.getUserAccountData(account.address)
    available_borrow_eth = Web3.fromWei(available_borrow_eth, 'ether')
    total_collateral_eth = Web3.fromWei(total_collateral_eth, 'ether')
    total_debt_eth = Web3.fromWei(total_debt_eth, 'ether')
    print(f'You have {total_collateral_eth} worth of ETH deposited.')
    print(f'You have {total_debt_eth} worth of ETH borrowed.')
    print(f'You can borrow {available_borrow_eth} worth of ETH.')
    return (float(available_borrow_eth), float(total_debt_eth))

def get_asset_price(price_feed_address):
    # ABI
    # Address
    dai_eth_price_feed = interface.AggregatorV3Interface()