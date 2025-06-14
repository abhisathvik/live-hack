from algosdk.kmd import KMDClient
from algosdk.v2client import algod
from algopy import ARC4ContractClient
from contracts.token_manager import TokenManager

ALGOD_ADDRESS = "http://localhost:4001"
ALGOD_TOKEN = "a" * 64  # Default for sandbox/localnet

KMD_ADDRESS = "http://localhost:4002"
KMD_TOKEN = "a" * 64  # Default KMD token in sandbox

WALLET_NAME = "unencrypted-default-wallet"
WALLET_PASSWORD = ""  # default password

# Set up algod + kmd clients
algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)
kmd_client = KMDClient(KMD_TOKEN, KMD_ADDRESS)

# Get wallet + account
wallets = kmd_client.list_wallets()
wallet = next(w for w in wallets if w['name'] == WALLET_NAME)
wallet_id = wallet['id']
wallet_handle = kmd_client.init_wallet_handle(wallet_id, WALLET_PASSWORD)
addresses = kmd_client.list_keys(wallet_handle)
sender = addresses[0]

# Deploy contract
client = ARC4ContractClient(TokenManager, algod_client)
app_client = client.create(sender, deploy_args={"admin": sender, "token_id": 123456, "mint_limit": 1000})

print("App ID:", app_client.app_id)

# Whitelist + Mint
app_client.call("add_to_whitelist", user=sender)
app_client.call("mint", to=sender, amount=100)
