from brownie import Solomon, accounts, Wei
from scripts.helpful_scripts import get_account
import uuid, time
import pytest


@pytest.fixture(scope="module")
def solomon_contract():
    account = get_account()
    solomon = Solomon.deploy({"from": account})
    uniqe_id = int(bin(uuid.uuid4().int)[2:] + bin(uuid.uuid4().int)[2:], 2)
    return {"solomon": solomon, "id": uniqe_id, "owner": account}


def test_deal_creation(solomon_contract):

    solomon = solomon_contract["solomon"]
    account = get_account()
    uniqe_id = solomon_contract["id"]
    implementor = accounts[1].address
    implementorResponsibility = Wei("0.02 ether")
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
    result = solomon.currentDeals(uniqe_id).dict()
    assert result["id"] == hex(uniqe_id)
    assert result["customer"] == account
    assert result["implementor"] == implementor
    assert result["value"] == Wei("1 ether")
    assert result["implementorResponsibility"] == Wei("0.02 ether")
    assert result["expirationDate"] == expiration
    assert result["implementorPayed"] == False


def test_pay_responsibility(solomon_contract):
    uniqe_id = solomon_contract["id"]
    solomon = solomon_contract["solomon"]
    solomon.payResponsibility(
        uniqe_id, {"from": accounts[1], "value": Wei("0.02 ether")}
    )
    result = solomon.currentDeals(uniqe_id).dict()
    assert result["implementorPayed"] == True


def test_approove(solomon_contract):
    owner = solomon_contract["owner"]
    uniqe_id = solomon_contract["id"]
    solomon = solomon_contract["solomon"]
    implementor_balance_before = accounts[1].balance()
    solomon.approveContract(uniqe_id, {"from": owner})
    implementor_balance_after = accounts[1].balance()
    money_earned = implementor_balance_after - implementor_balance_before
    assert Wei("1.02 ether") == money_earned
