from brownie import network, accounts, config, MockV3Aggregator, Contract, VRFCoordinatorMock, LinkToken, interface

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-url"]


# if you handle rnadomness, you have to interact with chain_token
def get_account(index=None, id=None):
    # accounts[0]
    # accounts.add('env')
    # accounts.load('id')
    # Priorities: index > id > networks
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if(
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    
    #else:
    return accounts.add(config["wallets"]["from_key"])




contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken
}

def get_contract(contract_name):
    """This function will grab the contract address from the brownie config
    if defined, otherwise, it will deploy a mock version of that contract, and
    return that mock contract.

        Args:
            contract_name (string)

        Returns:
            brownie.network.contract.ProjectContract: The most recently deployed
            version of this contract.
            MockV3Aggregator[-1]
    """
    contract_type = contract_to_mock[contract_name]

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:  # we don't need mock in test net or fork
        if len(contract_type) <= 0:  # it's counting  how many  deployed in MockV3Aggregator, and if it's never deployed, it works
            # MockV3Aggregator.length
            deploy_mocks()
        contract = contract_type[-1]  #MockV3Aggregator[-1]
    else:  # if it is on test-net or forks, it works
        contract_address = config["networks"][network.show_active()][contract_name]
        # address
        # ABI                       #MockV3Aggregator._name
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi) # MockV3Aggregator.abi
    return contract



DECIMALS = 8  # standard
INITIAL_VALUE = 200000000000  # 2000

# mock: a method to simulate or test something 
def deploy_mocks(decimals = DECIMALS, initial_value = INITIAL_VALUE):
    account = get_account()
    MockV3Aggregator.deploy(decimals, initial_value, {"from":account})
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {'from':account})
    print("Deployed!")

# this is used to use randomness function from other server, we have to pay for the function
def fund_with_link(contract_address, account=None, link_token=None, amount=100000000000000000): #0.1LINK
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract('link_token')
    tx = link_token.transfer(contract_address, amount, {"from":account})

    # this is another way, using interface(maybe, you can customize link_token's functions in the interface)
    """
    link_token_contract = interface.LinkTokenInterface(link_token.address)
    tx = link_token_contract.transfer(contract_address, amount, {"from":account})
    """
    tx.wait(1)
    print("Fund contract!")
    return tx