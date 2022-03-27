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


def test_minimal_deal_change(solomon_contract):
    solomon = solomon_contract["solomon"]
    assert solomon.minimalDeal() == Wei("0.01 ether")
    account = solomon_contract["owner"]
    tx = solomon.changeMinimalDeal(Wei("0.02 ether"), {"from": account})
    tx.wait(1)
    assert solomon.minimalDeal() == Wei("0.02 ether")


def test_judge_reward_part_change(solomon_contract):
    solomon = solomon_contract["solomon"]
    assert solomon.judgeRewardPart() == 200
    account = solomon_contract["owner"]
    tx = solomon.changeJudgeRewardPart(100, {"from": account})
    tx.wait(1)
    assert solomon.judgeRewardPart() == 100
