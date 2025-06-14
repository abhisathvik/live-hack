from algosdk.v2client import algod
from algosdk import account,mnemonic, transaction
import config
from upload_metadata_to_pinata import upload_to_pinata

def create_asset(metadata_ipfs_uri):
    algod_client = algod.AlgodClient(config.ALGOD_TOKEN, config.ALGOD_ADDRESS)

    creator_private_key = mnemonic.to_private_key(config.CREATOR_MNEMONIC)
    creator_address = account.address_from_private_key(creator_private_key)

    freeze_private_key = mnemonic.to_private_key(config.FREEZE_MNEMONIC)
    freeze_address = account.address_from_private_key(freeze_private_key)
    reserve_private_key = mnemonic.to_private_key(config.RESERVE_MNEMONIC)
    reserve_address = account.address_from_private_key(reserve_private_key)
    clawback_private_key = mnemonic.to_private_key(config.CLAWBACK_MNEMONIC)
    clawback_address = account.address_from_private_key(clawback_private_key)

    params = algod_client.suggested_params()

    txn = transaction.AssetConfigTxn(
        sender=creator_address,
        sp=params,
        total=1000000,
        decimals=0,
        default_frozen=False,
        unit_name="MEDNFT",
        asset_name="MedicalNFT Token",
        manager=creator_address,
        reserve=reserve_address,
        freeze=freeze_address,
        clawback=clawback_address,
        url=metadata_ipfs_uri,
        strict_empty_address_check=False
    )

    signed_txn = txn.sign(creator_private_key)
    txid = algod_client.send_transaction(signed_txn)

    print(f"Transaction sent with txID: {txid}")
    transaction_response = transaction.wait_for_confirmation(algod_client, txid, 4)
    print("Transaction confirmed")

    asset_id = transaction_response["asset-index"]
    print(f"✅ ASA Created with Asset ID: {asset_id}")
    return asset_id

if __name__ == "__main__":
    ipfs_uri = upload_to_pinata()
    create_asset(ipfs_uri)
