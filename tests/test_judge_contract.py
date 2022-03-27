from brownie import Solomon, accounts, Wei
from scripts.helpful_scripts import get_account
import uuid, time
import pytest


def test_implementor_fail_YES_payed_YES():
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

    judge_list = [accounts[2], accounts[3], accounts[4]]
    customer_balance_before = account.balance()
    implementor_balance_before = accounts[1].balance()
    judge_balance_before = accounts[4].balance()

    solomon.judgeContract(uniqe_id, True, judge_list, {"from": account})

    implementor_balance_after = accounts[1].balance()
    judge_balance_after = accounts[4].balance()
    customer_balance_after = account.balance()

    customer_earn = customer_balance_after - customer_balance_before
    judge_earn = judge_balance_after - judge_balance_before
    implementor_earn = implementor_balance_after - implementor_balance_before
    assert judge_earn == (fee // 2) // 200
    assert implementor_earn == 0
    assert customer_earn == Wei("1.02 ether")


def test_implementor_fail_YES_payed_NO():
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

    judge_list = [accounts[2], accounts[3], accounts[4]]
    customer_balance_before = account.balance()
    implementor_balance_before = accounts[1].balance()
    judge_balance_before = accounts[4].balance()

    solomon.judgeContract(uniqe_id, True, judge_list, {"from": account})

    implementor_balance_after = accounts[1].balance()
    judge_balance_after = accounts[4].balance()
    customer_balance_after = account.balance()

    customer_earn = customer_balance_after - customer_balance_before
    judge_earn = judge_balance_after - judge_balance_before
    implementor_earn = implementor_balance_after - implementor_balance_before
    assert judge_earn == (fee // 2) // 200
    assert implementor_earn == 0
    assert customer_earn == Wei("1.00 ether")


def test_implementor_fail_NO_payed_YES():
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

    judge_list = [accounts[2], accounts[3], accounts[4]]
    customer_balance_before = account.balance()
    implementor_balance_before = accounts[1].balance()
    judge_balance_before = accounts[4].balance()

    solomon.judgeContract(uniqe_id, False, judge_list, {"from": account})

    implementor_balance_after = accounts[1].balance()
    judge_balance_after = accounts[4].balance()
    customer_balance_after = account.balance()

    customer_earn = customer_balance_after - customer_balance_before
    judge_earn = judge_balance_after - judge_balance_before
    implementor_earn = implementor_balance_after - implementor_balance_before
    assert judge_earn == (fee // 2) // 200
    assert implementor_earn == Wei("1.02 ether")
    assert customer_earn == 0


def test_implementor_fail_NO_payed_NO():
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

    judge_list = [accounts[2], accounts[3], accounts[4]]
    customer_balance_before = account.balance()
    implementor_balance_before = accounts[1].balance()
    judge_balance_before = accounts[4].balance()

    solomon.judgeContract(uniqe_id, False, judge_list, {"from": account})

    implementor_balance_after = accounts[1].balance()
    judge_balance_after = accounts[4].balance()
    customer_balance_after = account.balance()

    customer_earn = customer_balance_after - customer_balance_before
    judge_earn = judge_balance_after - judge_balance_before
    implementor_earn = implementor_balance_after - implementor_balance_before
    assert judge_earn == (fee // 2) // 200
    assert implementor_earn == Wei("1.00 ether")
    assert customer_earn == 0
