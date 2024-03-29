from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from scripts.simple_collectible.deploy_and_create import deploy_and_create
from brownie import network, accounts
import pytest


def test_can_create_simple_collectible():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Act
    simple_collectible = deploy_and_create()
    # Assert
    assert simple_collectible.ownerOf(0) == get_account()