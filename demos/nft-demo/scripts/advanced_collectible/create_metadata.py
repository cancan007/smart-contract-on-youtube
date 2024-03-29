from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import json
import requests
import os


breed_to_image_uri = {
    "PUG": "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png",
}

def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f'You have created {number_of_advanced_collectibles} collectibles!')
    for token_id in range(number_of_advanced_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        metadata_file_name = (
            f'./metadata/{network.show_active()}/{token_id}-{breed}.json'
        )
        collecible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f'{metadata_file_name} already exists! Delete it to overwrite!')
        else:
            print(f'Creating Metadata file: {metadata_file_name}')
            collecible_metadata['name'] = breed
            collecible_metadata['description'] = f'An adorable {breed} pup!'
            image_path = './img/' + breed.lower().replace('_', '-') + '.png'

            image_uri = None
            if os.getenv('UPLOAD_IPFS') == 'true':
                image_uri = upload_to_ipfs(image_path)
            image_uri = image_uri if image_uri else breed_to_image_uri[breed]
            collecible_metadata['image_uri'] = image_uri
            with open(metadata_file_name, 'w') as file: # create json file
                json.dump(collecible_metadata, file)  # dump: dict to json
            if os.getenv('UPLOAD_IPFS') == 'true':
                upload_to_ipfs(metadata_file_name)

def upload_to_ipfs(filepath):
    with Path(filepath).open('rb') as fp:  # rb: read in binary
        image_binary = fp.read()
        ipfs_url =  'http://127.0.0.1:5001'
        endpoint = "/api/v0/add"  # https://docs.ipfs.io/reference/http/api/#api-v0-add
        response = requests.post(ipfs_url + endpoint, files={'file':image_binary})  # get response
        #print(response.headers)
        ipfs_hash = response.json()["Hash"]
        # ./img/0-PUG.png -> 0-PUG.png
        filename = filepath.split('/')[-1:][0]
        # https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json
        image_uri = f'https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}'
        print(image_uri)
        return image_uri

