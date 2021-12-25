from web3 import Web3
import pytest

# you can this value on all test scripts
@pytest.fixture
def amount_staked():
    return Web3.toWei(1, 'ether')