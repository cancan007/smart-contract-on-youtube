from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, get_contract
from scripts.advanced_collectible.deploy_and_create import deploy_and_create
from brownie import network, accounts
import pytest


def test_can_create_advanced_collectible():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Act
    advanced_collectible, creation_transaction = deploy_and_create()
    requestId = creation_transaction.events['requestedCollectible']['requestId']
    random_number = 777
    get_contract('vrf_coordinator').callBackWithRandomness(requestId, random_number, advanced_collectible.address, {'from':get_account()})
    # Assert
    assert advanced_collectible.tokenCounter() > 0
    assert advanced_collectible.tokenIdToBreed(0) == random_number % 3

    