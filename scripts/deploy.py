from brownie import Solomon, network, config
from scripts.helpful_scripts import get_account


def deploy_fund_me():
    account = get_account()
    print("Аккаунт:", account)
    solomon = Solomon.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )

    print(f"Контракт развернут по адрессу: {solomon.address}")


def main():
    deploy_fund_me()
