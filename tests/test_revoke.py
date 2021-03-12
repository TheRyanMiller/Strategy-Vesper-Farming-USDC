def test_revoke_strategy_from_vault(token, vault, strategy, amount, gov, user, strategist):
    # Deposit to the vault and harvest
    token.approve(vault.address, amount, {"from": user})
    vault.deposit(amount, {"from": user})
    strategy.harvest({"from": strategist})
    assert strategy.estimatedTotalAssets()+1 == amount

    # In order to pass this tests, you will need to implement prepareReturn.
    # TODO: uncomment the following lines.
    # vault.revokeStrategy(strategy.address, {"from": gov})
    # strategy.harvest()
    # assert token.balanceOf(vault.address) == amount


def test_revoke_strategy_from_strategy(token, vault, strategy, amount, gov, user, strategist):
    # Deposit to the vault and harvest
    token.approve(vault.address, amount, {"from": user})
    vault.deposit(amount, {"from": user})
    strategy.harvest({"from": strategist})
    assert strategy.estimatedTotalAssets()+1 == amount

    strategy.setEmergencyExit()
    strategy.harvest({"from": strategist})
    assert strategy.estimatedTotalAssets() == amount
