import brownie
from brownie import Contract
from helpers import stratData,vaultData


def test_profitable_harvest(accounts, token, vault, strategy, strategist, amount, user, chain, vVSP):
    # Deposit to the vault
    token.approve(vault.address, amount, {"from": user})
    vault.deposit(amount, {"from": user})
    # harvest
    strategy.harvest({"from": strategist})
    assert strategy.estimatedTotalAssets()+1 >= vault.debtRatio()
    chain.sleep(3600 * 24)
    chain.mine(1)
    # You should test that the harvest method is capable of making a profit.
    # TODO: uncomment the following lines.
    strategy.harvest({"from": strategist})
    chain.sleep(3600 * 24)
    chain.mine(1)
    amt = vault.debtRatio() * amount / 10000
    assert strategy.estimatedTotalAssets() > amt