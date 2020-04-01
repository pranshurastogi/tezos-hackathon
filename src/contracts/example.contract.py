"""Example Tezos smart contract"""

import smartpy as sp


class Example(sp.Contract):
    def __init__(self, owner):
        self.init(
            participants=sp.bigMap(tkey=sp.TAddress, tvalue=sp.TMutez),
            owner=owner,
        )

    @sp.entryPoint
    def addParticipant(self, params):
        sp.verify(sp.sender == self.data.owner, False, 'ERROR_ONLY_OWNER_CAN_ADD_PARTICIPANT')
        self.data.participants[params.address] = sp.amount

    @sp.entryPoint
    def participate(self, params):
        sp.verify(self.data.participants.contains(sp.sender), False, 'ERROR_PARTICIPANT_MUST_EXIST_BEFORE_PARTICIPATING')
        self.data.participants[sp.sender] += sp.amount


@addTest(name="example")
def test_example_contract():
    ownerAddress = sp.address('tz1ABC')
    user1Address = sp.address('tz1DEF')
    user2Address = sp.address('tz1GHI')
    user3Address = sp.address('tz1JKL')

    # given ... an Example contract instance with owner set
    contract = Example(owner=ownerAddress)
    scenario = sp.testScenario()
    scenario += contract

    # when
    # ... we add a participant as the owner
    # then
    # ... should succeed
    scenario += contract.addParticipant(address=user1Address).run(sender=ownerAddress, amount=sp.mutez(0))
    scenario += contract.addParticipant(address=user2Address).run(sender=ownerAddress, amount=sp.mutez(20))
    # ... adding the user to participants map
    scenario.verify(contract.data.participants.contains(user1Address))
    scenario.verify(contract.data.participants.contains(user2Address))
    # ... with the provided mutez as their initial value
    scenario.verify(contract.data.participants[user1Address] == sp.mutez(0))
    scenario.verify(contract.data.participants[user2Address] == sp.mutez(20))

    # when
    # ... we add a participant as not the owner
    # then
    # ... should fail
    scenario += contract.addParticipant(address=user3Address).run(sender=user3Address, amount=sp.mutez(50), valid=False)
    # ... not adding user to participants map
    scenario.verify(~contract.data.participants.contains(user3Address))

    # when
    # ... we participate as an existing user
    # then
    # ... should succeed
    scenario += contract.participate().run(sender=user1Address, amount=sp.mutez(5))
    scenario += contract.participate().run(sender=user2Address, amount=sp.mutez(7))
    # ... incrementing the user's mutez by provided amount
    scenario.verify(contract.data.participants[user1Address] == sp.mutez(5))
    scenario.verify(contract.data.participants[user2Address] == sp.mutez(27))

    # when
    # ... we attempt to participate as an non-existing user
    # then
    # ... should fail
    scenario += contract.participate().run(sender=user3Address, amount=sp.mutez(50), valid=False)
