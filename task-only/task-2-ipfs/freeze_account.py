from algosdk.v2client import algod
from algosdk import account,mnemonic, transaction
import config

def freeze_account(asset_id, target_account, freeze_state):
    algod_client = algod.AlgodClient(config.ALGOD_TOKEN, config.ALGOD_ADDRESS)

    freeze_private_key = mnemonic.to_private_key(config.FREEZE_MNEMONIC)
    freeze_address = account.address_from_private_key(freeze_private_key)

    params = algod_client.suggested_params()

    txn = transaction.AssetFreezeTxn(
        sender=freeze_address,
        sp=params,
        index=asset_id,
        target=target_account,
        new_freeze_state=freeze_state
    )

    signed_txn = txn.sign(freeze_private_key)
    txid = algod_client.send_transaction(signed_txn)

    print(f"Freeze transaction sent with txID: {txid}")
    transaction.wait_for_confirmation(algod_client, txid, 4)
    print("✅ Freeze state updated")

if __name__ == "__main__":
    asset_id = int(input("Enter ASA ID: "))
    target_account = input("Enter target address to freeze: ")
    freeze_state = input("Freeze? (yes/no): ").lower() == 'yes'
    freeze_account(asset_id, target_account, freeze_state)
