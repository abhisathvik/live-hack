from algosdk.v2client import algod
from algosdk import account, mnemonic, transaction
import config
import time

# Utility function to wait for confirmation
def wait_for_confirmation(client, txid):
    while True:
        try:
            tx_info = client.pending_transaction_info(txid)
            if tx_info.get("confirmed-round", 0) > 0:
                print(f"Transaction {txid} confirmed in round {tx_info['confirmed-round']}.")
                return tx_info
            else:
                time.sleep(1)
        except Exception:
            time.sleep(1)

# Setup client
algod_client = algod.AlgodClient(config.ALGOD_TOKEN, config.ALGOD_ADDRESS)

# Recover accounts
creator_private_key = mnemonic.to_private_key(config.CREATOR_MNEMONIC)
creator_address = account.address_from_private_key(creator_private_key)

receiver_private_key = mnemonic.to_private_key(config.RECEIVER_MNEMONIC)
receiver_address = account.address_from_private_key(receiver_private_key)

# Create ASA
params = algod_client.suggested_params()

total_supply = 1_000_000
decimals = 2
unit_name = "LIVEHACK"
asset_name = "Live-Hack"
url = ""
default_frozen = False  

txn = transaction.AssetConfigTxn(
    sender=creator_address,
    sp=params,
    total=total_supply,
    default_frozen=default_frozen,
    unit_name=unit_name,
    asset_name=asset_name,
    manager=creator_address,
    reserve=creator_address,
    freeze=creator_address,
    clawback=creator_address,
    url=url,
    decimals=decimals
)

signed_txn = txn.sign(creator_private_key)
txid = algod_client.send_transaction(signed_txn)
confirmed_txn = wait_for_confirmation(algod_client, txid)
asset_id = confirmed_txn["asset-index"]
print(f"Created ASA with Asset ID: {asset_id}")

# Opt-in receiver
params = algod_client.suggested_params()
opt_in_txn = transaction.AssetTransferTxn(
    sender=receiver_address,
    sp=params,
    receiver=receiver_address,
    amt=0,
    index=asset_id
)
signed_opt_in = opt_in_txn.sign(receiver_private_key)
opt_in_txid = algod_client.send_transaction(signed_opt_in)
wait_for_confirmation(algod_client, opt_in_txid)
print("Receiver opted-in successfully.")

# Transfer ASA to receiver
transfer_amount = 500  # 5.00 tokens if decimals=2
params = algod_client.suggested_params()
transfer_txn = transaction.AssetTransferTxn(
    sender=creator_address,
    sp=params,
    receiver=receiver_address,
    amt=transfer_amount,
    index=asset_id
)
signed_transfer_txn = transfer_txn.sign(creator_private_key)
transfer_txid = algod_client.send_transaction(signed_transfer_txn)
wait_for_confirmation(algod_client, transfer_txid)
print("Transfer completed successfully.")