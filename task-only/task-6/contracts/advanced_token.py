from algopy import ARC4Contract, arc4, Global, BoxMap, itxn

class AdvancedToken(ARC4Contract):
    unlock_time: arc4.UInt64
    oracle_address: arc4.Address
    oracle_price: arc4.UInt64
    whitelist: BoxMap[arc4.Address, arc4.Bool]
    blacklist: BoxMap[arc4.Address, arc4.Bool]

    def __init__(self, unlock_time: arc4.UInt64, oracle_address: arc4.Address) -> None:
        self.unlock_time = unlock_time
        self.oracle_address = oracle_address
        self.oracle_price = arc4.UInt64(0)

    @arc4.abimethod
    def add_to_whitelist(self, addr: arc4.Address) -> None:
        self.whitelist[addr] = arc4.Bool(True)

    @arc4.abimethod
    def remove_from_whitelist(self, addr: arc4.Address) -> None:
        del self.whitelist[addr]

    @arc4.abimethod
    def add_to_blacklist(self, addr: arc4.Address) -> None:
        self.blacklist[addr] = arc4.Bool(True)

    @arc4.abimethod
    def remove_from_blacklist(self, addr: arc4.Address) -> None:
        del self.blacklist[addr]

    @arc4.abimethod
    def update_price(self, new_price: arc4.UInt64, *, sender: arc4.Address) -> None:
        if sender == self.oracle_address:
            self.oracle_price = new_price

    @arc4.abimethod
    def conditional_transfer(self, receiver: arc4.Address, amount: arc4.UInt64, *, sender: arc4.Address) -> None:
        # Time lock
        unlock_check = Global.latest_timestamp() >= self.unlock_time
        if not unlock_check:
            return

        # Whitelist check (default False)
        whitelisted = self.whitelist.get(sender, default=arc4.Bool(False))
        if not whitelisted:
            return

        # Blacklist check (default False)
        blacklisted = self.blacklist.get(receiver, default=arc4.Bool(False))
        if blacklisted:
            return

        # Oracle price condition
        if self.oracle_price <= arc4.UInt64(50):
            return

        # Perform transfer
        itxn.Payment(
            receiver=arc4.Account(receiver),  # Must convert Address to Account
            amount=int(amount),               # Cast UInt64 to int
            fee=0
        ).submit()