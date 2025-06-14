# Algorand ASA Management System 🛡️

A complete Python-based solution for managing Algorand Standard Assets (ASA), including:
- ASA creation
- Account Opt-In
- Asset Freeze & Unfreeze
- Clawback (Revoke)
- Role management
- IPFS Integration (Pinata / NFT.Storage for asset metadata storage)

---

## 📦 Project Structure

bash
.
 ├── create-asa.py          # ASA creation script 
 
 ├── clawback_transfer.py   # Clawback (revocation) script
 
 ├── freeze_account.py      # Freeze / Unfreeze asset script
 
 ├── upload_metadata_to_ipfs.py         # Upload asset metadata to IPFS (via Pinata)
 
 ├── config.py              # Algorand client configuration (Algod URL + Token)
 
 └── README.md              # This documentation file

# 🔧 Setup Instructions
 
 1️⃣ Install Dependencies
 
 pip install py-algorand-sdk requests

 2️⃣ Create config.py
 
 ALGOD_ADDRESS = "https://testnet-api.algonode.cloud"
 
 ALGOD_TOKEN = ""  # No token needed for AlgoNode public endpoints

# Optional: IPFS (Pinata or NFT.Storage) credentials

 PINATA_API_KEY = "your-pinata-api-key"
 
 PINATA_API_SECRET = "your-pinata-api-secret"
 
 NFT_STORAGE_API_KEY = "your-nft-storage-api-key"

#🚀 Usage Guide
 
 ✅ 1. ASA Creation 
 
 python3 create-asa.py
 
 ✅ 2. Upload Asset Metadata to IPFS
 
 python3 upload_metadata_to_ipfs.py
 
 ✅ 3. Freeze / Unfreeze Account
 
 python3 freeze_account.py
 
 ✅ 4. Clawback / Revoke Assets
 
 python3 clawback_transfer.py

#🔐 Role Management
 
 Manager: Full control over ASA parameters
 
 Freeze Address: Can freeze/unfreeze accounts
 
 Clawback Address: Can revoke assets from accounts
 
 Reserve Address: Can hold reserve balance
