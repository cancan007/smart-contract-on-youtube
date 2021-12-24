from brownie import network, config, accounts
import eth_utils

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ['hardhat', 'development', 'ganache']

def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id:
        return accounts.load(id)
    return accounts.add(config['wallets']['from_key'])

# encode_function_data:
"""Encodes the function call so we can work with an initializer.
    Args:
        initializer ([brownie.network.contract.ContractTx], optional):
        The initializer function we want to call. Example: `box.store`.
        Defaults to None.
        args (Any, optional):
        The arguments to pass to the initializer function
    Returns:
        [bytes]: Return the encoded bytes.
"""
# this func is for upgrading with constructor
# initializer=box.store, (1,2,3,4,5)
def encode_function_data(initializer=None, *args):  # *args: get values in tupple

    if len(args) == 0 or not initializer:
        return eth_utils.to_bytes(hexstr='0x')  # to inform the arguments are empty
    return initializer.encode_input(*args)

def upgrade(account, proxy, new_implementation_address, proxy_admin_contract=None, initializer=None, *args):
    transaction = None
    if proxy_admin_contract:
        if initializer:
            encoded_function_call = encode_function_data(initializer, *args)
            transaction = proxy_admin_contract.upgradeAndCall(  # when you have constructor, you have to do this
                proxy.address,
                new_implementation_address,
                encode_function_call,
                {'from':account}
            )
        else:
            transaction = proxy_admin_contract.upgrade(  # when you don't have constructor, you do this
                proxy.address,
                new_implementation_address,
                {'from':account}
            )
    else:
        if initializer:
            encoded_function_call = encode_function_data(initializer, *args)
            transaction  = proxy.upgradeToAndCall(
                new_implementation_address,
                encode_function_call,
                {'from':account}
            )
        else:
            transaction = proxy.upgradeTo(
                new_implementation_address,
                {'from':account}
            )
    return transaction
