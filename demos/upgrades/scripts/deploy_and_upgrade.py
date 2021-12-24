from scripts.helpful_scripts import get_account, encode_function_data, upgrade
from brownie import Box, network, ProxyAdmin, Contract, TransparentUpgradeableProxy, BoxV2

def main():
    account = get_account()
    print(f'Deploying to {network.show_active()}')
    box = Box.deploy({'from':account},publish_source=True)
    print(box.retrieve())

    proxy_admin = ProxyAdmin.deploy({'from':account}, publish_source=True)

    initializer = box.store, 1
    box_encoded_initializer_function = encode_function_data()  # this time, we don't use initializer

    
    proxy = TransparentUpgradeableProxy.deploy(  # all functions are called on proxy, not box
        box.address,
        proxy_admin.address, # 'upgrade' function is called from this address
        box_encoded_initializer_function,
        {'from':account, 'gas_limit':1000000}, publish_source=True
        )
    # proxy: this contract address can be changed, but Box can't. That's why we use proxy
    print(f'Proxy developed to {proxy}, you can now upgrade to v2!')
    proxy_box = Contract.from_abi('Box', proxy.address, Box.abi)
    # Below sentence imploy how upgrading of decentralized contract
    #I have different contract address from Box in Proxy, but proxy delegated box functions, so we can use box functions without box contract address  
    proxy_box.store(1, {'from':account})

    # upgrades
    box_v2 = BoxV2.deploy({'from':account}, publish_source=True)
    upgrade_transaction = upgrade(account, proxy, box_v2.address, proxy_admin_contract=proxy_admin)
    upgrade_transaction.wait(1)
    print('Proxy has been upgraded!')
    proxy_box = Contract.from_abi("BoxV2", proxy.address, box_v2.abi)
    proxy_box.increment({'from':account})
    print(proxy_box.retrieve())