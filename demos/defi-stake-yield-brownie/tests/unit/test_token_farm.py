from brownie import network, config, accounts, exceptions
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_contract, INITIAL_VALUE_PRICE_FEED
import pytest
from scripts.deploy import deploy_token_farm_and_dapp_token


def test_set_price_feed_contract():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip('Only for local testing!')
    account = get_account()
    non_owner = get_account(index=1)
    price_feed_address = get_contract('eth_usd_price_feed')
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()
    # Act
    token_farm.setPriceFeedContract(dapp_token.address, price_feed_address, {'from':account})
    # Assert
    assert token_farm.tokenPriceFeedMapping(dapp_token.address) == price_feed_address
    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.setPriceFeedContract(
            dapp_token.address, price_feed_address, {'from':non_owner}
        )
def test_stake_tokens(amount_staked):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip('Only for local testing!')
    account = get_account()
    #p2 = get_account(index=2)
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()
    # Act
    owner_balance_before = dapp_token.balanceOf(account.address)
    print(f"owner_balance_before:{owner_balance_before}")
    dapp_token.approve(token_farm.address, amount_staked, {'from':account})
    #dapp_token.transfer(p2.address, amount_staked ,{'from':account})
    token_farm.stakeTokens(amount_staked, dapp_token.address, {'from':account})
    #token_farm.stakeTokens(amount_staked, dapp_token.address, {'from':p2})
    owner_balance_after = dapp_token.balanceOf(account.address)
    print(f"owner_balance_after:{owner_balance_after}")
    # Assert
    assert (
        token_farm.stakingBalance(dapp_token.address, account.address) == amount_staked
    )
    assert token_farm.uniqueTokensStaked(account.address) == 1
    assert token_farm.stakers(0) == account.address
    #assert token_farm.stakers(1) == p2.address
    return token_farm, dapp_token

def test_issue_tokens(amount_staked):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip('Only for local testing!')
    account = get_account()
    token_farm, dapp_token = test_stake_tokens(amount_staked)
    starting_balance = dapp_token.balanceOf(account.address)
    # Act
    token_farm.issueTokens({'from':account})
    # Assert
    # we are staking 10 dapp tokens == in price to 1 ETH
    # soo... we should get 2,000 dapp tokens in reward
    # since the price of eth is $2,000
    assert (
        dapp_token.balanceOf(account.address) == starting_balance + INITIAL_VALUE_PRICE_FEED
    )