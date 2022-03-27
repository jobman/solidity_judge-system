from brownie import Solomon, accounts, Wei
from scripts.helpful_scripts import get_account
import uuid, time
import pytest


def test_terminate_system():
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
    judge_balance_before = accounts[4].balance()

    solomon.judgeContract(uniqe_id, True, judge_list, {"from": account})
    judge_balance_after = accounts[4].balance()

    judge_earn = judge_balance_after - judge_balance_before

    owner_balance_before = account.balance()
    solomon.terminateSystem([account], {"from": account})
    owner_balance_after = account.balance()
    owner_earn = owner_balance_after - owner_balance_before
    assert owner_earn == (fee // 2) + ((fee // 2) - 3 * judge_earn)


def test_system_failure_withdraw():
    account = get_account()
    solomon = Solomon.deploy({"from": account})
    uniqe_id = int(bin(uuid.uuid4().int)[2:] + bin(uuid.uuid4().int)[2:], 2)
    implementor = accounts[1].address
    implementorResponsibility = Wei("0.02 ether")
    expiration = int(time.time() + 5)
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
    time.sleep(6)
    owner_balance_before = account.balance()
    solomon.systemFailureWithdrawFunds(uniqe_id, {"from": account})
    owner_balance_after = account.balance()
    owner_earn = owner_balance_after - owner_balance_before
    assert owner_earn == Wei("1 ether")
