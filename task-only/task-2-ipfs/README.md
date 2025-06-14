# Algorand ASA with Pinata IPFS Integration

## Prerequisites

- Python 3.8+
- Algorand TestNet account with funded wallet
- Pinata account (API Key + Secret Key)

## Setup

1️⃣ Install dependencies:

# bash
pip install -r requirements.txt

2️⃣ Create .env file:

ALGOD_TOKEN=
ALGOD_ADDRESS=https://testnet-api.algonode.cloud
CREATOR_MNEMONIC=your-algorand-mnemonic
PINATA_API_KEY=your-pinata-api-key
PINATA_SECRET_API_KEY=your-pinata-secret-api-key

# Run the full pipeline
python create_asa_with_metadata.py
