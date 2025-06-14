from algosdk.v2client import algod
from algosdk import account,mnemonic, transaction
import config

def clawback(asset_id, sender_account, receiver_account, amount):
    algod_client = algod.AlgodClient(config.ALGOD_TOKEN, config.ALGOD_ADDRESS)

    clawback_private_key = mnemonic.to_private_key(config.CLAWBACK_MNEMONIC)
    clawback_address = account.address_from_private_key(clawback_private_key)

    params = algod_client.suggested_params()

    txn = transaction.AssetTransferTxn(
        sender=clawback_address,
        sp=params,
        receiver=receiver_account,
        amt=amount,
        index=asset_id,
        revocation_target=sender_account
    )

    signed_txn = txn.sign(clawback_private_key)
    txid = algod_client.send_transaction(signed_txn)

    print(f"Clawback transaction sent with txID: {txid}")
    transaction.wait_for_confirmation(algod_client, txid, 4)
    print("✅ Clawback transfer done")

if __name__ == "__main__":
    asset_id = int(input("Enter ASA ID: "))
    sender_account = input("Enter account to revoke tokens from: ")
    receiver_account = input("Enter receiver account: ")
    amount = int(input("Enter amount: "))
    clawback(asset_id, sender_account, receiver_account, amount)
