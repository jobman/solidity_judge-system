from brownie import Solomon, accounts, Wei
from scripts.helpful_scripts import get_account
import uuid, time


def main():
    account = get_account()
    solomon = Solomon.deploy({"from": account})
    uniqe_id = int(bin(uuid.uuid4().int)[2:] + bin(uuid.uuid4().int)[2:], 2)
    # customer = accounts[0].address
    implementor = accounts[1].address
    implementorResponsibility = 0
    expiration = int(time.time() + 3600)
    value = Wei("1 ether")
    fee = Wei("0.01 ether")
    tx = solomon.makeContract(
        uniqe_id,
        implementor,
        implementorResponsibility,
        expiration,
        value,
        fee,
        {"from": account, "value": value + fee},
    )
    tx.wait(1)
    result = solomon.currentDeals(uniqe_id)
    print(type(result))
    print(result)
    print(result.dict())
    print(type(result.dict()["id"]))
    if result.dict()["id"] == hex(uniqe_id):
        print("UUID OK")
    else:
        print("UUINT NOT OK")
