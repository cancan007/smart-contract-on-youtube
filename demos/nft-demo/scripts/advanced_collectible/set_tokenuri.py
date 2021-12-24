from brownie import network, AdvancedCollectible
from scripts.helpful_scripts import get_breed, get_account, OPENSEA_URL


dog_metadata_dic = {
    'PUG': 'https://ipfs.io/ipfs/Qmcim1XMFpctcx4cdPYUYxkUmYD6VW7XwaKFbbYvEborRR?filename=1-PUG.json',
    'SHIBA_INU': 'https://ipfs.io/ipfs/QmT9pue4sBjFKUYsx4Uexi96QqiAFCnVro8Dwb6E81Ekev?filename=0-SHIBA_INU.json',
    'ST_BERNARD': "https://ipfs.io/ipfs/QmbBnUjyHHN7Ytq9xDsYF9sucZdDJLRkWz7vnZfrjMXMxs?filename=2-ST_BERNARD.json", # paste from patrick github
}


def main():
    print(f'Working on {network.show_active()}')
    advanced_collectible = AdvancedCollectible[-1]
    number_of_collectibles = advanced_collectible.tokenCounter()
    print(f'You have {number_of_collectibles} tokenIds')
    for token_id in range(number_of_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        if not advanced_collectible.tokenURI(token_id).startswith('https://'):  # if the uri doesn't start with 'https://'
            print(f'Setting tokenURI of {token_id}')
            set_tokenURI(token_id, advanced_collectible, dog_metadata_dic[breed])


def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, tokenURI, {'from':account})
    tx.wait(1)
    print(f'Awesome! You can view your NFT at {OPENSEA_URL.format(nft_contract.address, token_id)}')
    print('Please wait up 20 minutes, and hit the refresh metadata button')