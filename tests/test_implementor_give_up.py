from brownie import Solomon, accounts, Wei
from scripts.helpful_scripts import get_account
import uuid, time
import pytest


def test_implementor_give_up_contract_responsibility_YES_payed_NO():
    account = get_account()
    solomon = Solomon.deploy({"from": account})
    uniqe_id = int(bin(uuid.uuid4().int)[2:] + bin(uuid.uuid4().int)[2:], 2)
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

    customer_balance_before = account.balance()
    implementor_balance_before = accounts[1].balance()
    solomon.giveUpContract(uniqe_id, {"from": accounts[1]})
    customer_balance_after = account.balance()
    implementor_balance_after = accounts[1].balance()
    implementor_money_earned = implementor_balance_after - implementor_balance_before
    assert 0 == implementor_money_earned
    customer_money_returned = customer_balance_after - customer_balance_before
    assert customer_money_returned == Wei("1 ether")


def test_implementor_give_up_contract_responsibility_YES_payed_YES():
    account = get_account()
    solomon = Solomon.deploy({"from": account})
    uniqe_id = int(bin(uuid.uuid4().int)[2:] + bin(uuid.uuid4().int)[2:], 2)
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

    tx = solomon.payResponsibility(
        uniqe_id, {"from": accounts[1], "value": Wei("0.02 ether")}
    )
    tx.wait(1)
    result = solomon.currentDeals(uniqe_id).dict()
    assert result["implementorPayed"] == True

    customer_balance_before = account.balance()
    implementor_balance_before = accounts[1].balance()
    solomon.giveUpContract(uniqe_id, {"from": accounts[1]})
    customer_balance_after = account.balance()
    implementor_balance_after = accounts[1].balance()
    implementor_money_earned = implementor_balance_after - implementor_balance_before
    assert 0 == implementor_money_earned
    customer_money_returned = customer_balance_after - customer_balance_before
    assert customer_money_returned == Wei("1.02 ether")


def test_implementor_give_up_contract_responsibility_NO_payed_NO():
    account = get_account()
    solomon = Solomon.deploy({"from": account})
    uniqe_id = int(bin(uuid.uuid4().int)[2:] + bin(uuid.uuid4().int)[2:], 2)
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

    customer_balance_before = account.balance()
    implementor_balance_before = accounts[1].balance()
    solomon.giveUpContract(uniqe_id, {"from": accounts[1]})
    customer_balance_after = account.balance()
    implementor_balance_after = accounts[1].balance()
    implementor_money_earned = implementor_balance_after - implementor_balance_before
    assert 0 == implementor_money_earned
    customer_money_returned = customer_balance_after - customer_balance_before
    assert customer_money_returned == Wei("1 ether")
