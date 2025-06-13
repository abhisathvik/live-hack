import os
from dotenv import load_dotenv

load_dotenv()

CREATOR_MNEMONIC = os.getenv("CREATOR_MNEMONIC")
RECEIVER_MNEMONIC = os.getenv("RECEIVER_MNEMONIC")

ALGOD_ADDRESS = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""  # No token for AlgoNode
