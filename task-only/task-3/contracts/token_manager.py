from algopy import ARC4Contract, arc4, Global, itxn, BoxMap, UInt64, Address, Account


class TokenManager(ARC4Contract):
    token_id: UInt64
    admin: Address
    whitelist: BoxMap[Address, arc4.Bool]

    def __init__(self) -> None:
        self.admin = Global.current_application_address  # Use this for Address, not Account
        self.whitelist = BoxMap[Address, arc4.Bool]("whitelist")

    @arc4.abimethod
    def set_token_id(self, token_id: UInt64) -> None:
        self.token_id = token_id

    @arc4.abimethod
    def add_to_whitelist(self, addr: Address) -> None:
        self.whitelist[addr] = arc4.Bool(True)

    @arc4.abimethod
    def mint(self, to: Address, amount: UInt64) -> None:
        assert self.whitelist[to] == arc4.Bool(True)

        itxn.AssetTransfer(
            xfer_asset=self.token_id,
            asset_amount=amount,
            receiver=to
        ).submit()

    @arc4.abimethod
    def burn(self, from_addr: Account, amount: UInt64) -> None:
        itxn.AssetTransfer(
            xfer_asset=self.token_id,
            asset_amount=amount,
            asset_sender=from_addr
        ).submit()

    @arc4.abimethod
    def transfer(self, from_addr: Account, to: Address, amount: UInt64) -> None:
        assert self.whitelist[to] == arc4.Bool(True)

        itxn.AssetTransfer(
            xfer_asset=self.token_id,
            asset_amount=amount,
            asset_sender=from_addr,
            receiver=to
        ).submit()
