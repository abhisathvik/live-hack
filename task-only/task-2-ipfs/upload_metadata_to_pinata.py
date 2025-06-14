import requests
import json
import config

def upload_to_pinata():
    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
    headers = {
        "pinata_api_key": config.PINATA_API_KEY,
        "pinata_secret_api_key": config.PINATA_SECRET_API_KEY
    }

    metadata = {
        "name": "MedicalNFT Controlled Asset",
        "description": "An ARC-53 compliant Algorand asset",
        "image": "https://example.com/logo.png",
        "properties": {
            "project": "MedicalNFT",
            "type": "Healthcare Asset",
            "author": "Abhi Sathvik"
        }
    }

    response = requests.post(url, headers=headers, json={"pinataContent": metadata})

    # Print full response for debugging
    print("Status Code:", response.status_code)
    print("Response:", response.text)

    response.raise_for_status()

    ipfs_hash = response.json()["IpfsHash"]
    return f"ipfs://{ipfs_hash}"

if __name__ == "__main__":
    uri = upload_to_pinata()
    print("✅ Metadata URI:", uri)
