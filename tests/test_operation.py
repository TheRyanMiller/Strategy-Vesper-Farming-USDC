import brownie
from brownie import Contract


def test_operation(accounts, token, vault, strategy, strategist, amount, user, vUSDC, chain, gov, vVSP, vsp):
    
    # Deposit to the vault
    token.approve(vault.address, amount, {"from": user})
    vault.deposit(amount, {"from": user})
    assert token.balanceOf(vault.address) == amount

    # harvest
    strategy.harvest({"from": strategist})
    assert strategy.estimatedTotalAssets()+1 == amount # Won't match because we must account for withdraw fees

    # tend()
    # strategy.tend({"from": strategist})
    
    # Allow rewards to be earned
    seconds_in_day = 86400
    chain.sleep(seconds_in_day*5) # 1 day
    chain.mine(1)
    strategy.harvest({"from": strategist})
    print("\nEst No Dump APR: ", "{:.2%}".format(
            ((vault.totalAssets() - amount) * 73) / (amount)
        )
    )

    seconds_in_day = 86400 # 1 day
    chain.sleep(seconds_in_day*5)
    chain.mine(1)
    strategy.harvest({"from": strategist})
    
    chain.sleep(seconds_in_day*5)
    chain.mine(1)
    strategy.toggleHarvestVvsp({"from":strategist}) # Dump VSP tokens this time
    strategy.harvest({"from": strategist})
    print("\nEst Dump APR: ", "{:.2%}".format(
            ((vault.totalAssets() - amount) * 24.33) / (amount)
        )
    )
    # withdrawal
    chain.sleep(3600) #six hours
    vault.withdraw(vault.balanceOf(user),user,61,{"from": user}) # Need more loss protect to handle 0.6% withdraw fee
    assert token.balanceOf(user) != 0


def test_emergency_exit(accounts, token, vault, strategy, strategist, amount, user, vVSP):
    # Deposit to the vault
    token.approve(vault.address, amount, {"from": user})
    vault.deposit(amount, {"from": user})
    strategy.harvest({"from": strategist})
    assert strategy.estimatedTotalAssets() + 1 >= amount

    # set emergency and exit
    strategy.setEmergencyExit()
    strategy.harvest({"from": strategist})
    assert strategy.estimatedTotalAssets() < amount


def test_profitable_harvest(accounts, token, vault, strategy, strategist, amount, user, chain, vVSP):
    # Deposit to the vault
    token.approve(vault.address, amount, {"from": user})
    vault.deposit(amount, {"from": user})
    # harvest
    strategy.harvest({"from": strategist})
    assert strategy.estimatedTotalAssets()+1 >= amount
    chain.sleep(3600 * 24)
    chain.mine(1)
    # You should test that the harvest method is capable of making a profit.
    # TODO: uncomment the following lines.
    strategy.harvest({"from": strategist})
    chain.sleep(3600 * 24)
    chain.mine(1)
    assert strategy.estimatedTotalAssets() > amount


def test_change_debt(gov, token, vault, strategy, strategist, amount, user, vUSDC, vVSP):
    # Deposit to the vault and harvest
    token.approve(vault.address, amount, {"from": user})
    vault.deposit(amount, {"from": user})
    vault.updateStrategyDebtRatio(strategy.address, 5_000, {"from": gov})
    strategy.harvest({"from": strategist})

    assert strategy.estimatedTotalAssets()+1 == amount / 2

    vault.updateStrategyDebtRatio(strategy.address, 10_000, {"from": gov})
    strategy.harvest({"from": strategist})
    assert strategy.estimatedTotalAssets() == amount

    # In order to pass this tests, you will need to implement prepareReturn.
    # TODO: uncomment the following lines.
    # vault.updateStrategyDebtRatio(strategy.address, 5_000, {"from": gov})
    # assert token.balanceOf(strategy.address) == amount / 2


def test_sweep(gov, vault, strategy, token, amount, weth, weth_amout, vsp, user):
    # Strategy want token doesn't work
    token.transfer(strategy, amount, {"from": user})
    vsp.transfer(strategy, 1e20, {"from": user})
    assert token.address == strategy.want()
    assert token.balanceOf(strategy) > 0
    with brownie.reverts("!want"):
        strategy.sweep(token, {"from": gov})

    # Vault share token doesn't work
    with brownie.reverts("!shares"):
        strategy.sweep(vault.address, {"from": gov})

    # TODO: If you add protected tokens to the strategy.
    # Protected token doesn't work
    # with brownie.reverts("!protected"):
    #     strategy.sweep(strategy.protectedToken(), {"from": gov})

    with brownie.reverts("!want"):
         strategy.sweep(token.address, {"from": gov})
    
    with brownie.reverts("!authorized"):
         strategy.sweep(token.address, {"from": user})

    weth.transfer(strategy, weth.balanceOf(gov), {"from": gov})
    assert weth.address != strategy.want()
    strategy.sweep(weth, {"from": gov})
    assert weth.balanceOf(gov) > 0


def test_triggers(gov, vault, strategy, token, amount, weth, weth_amout, user, strategist):
    # Deposit to the vault and harvest
    token.approve(vault.address, amount, {"from": user})
    depositAmount = amount
    vault.deposit(depositAmount, {"from": user})
    vault.updateStrategyDebtRatio(strategy.address, 5_000, {"from": gov})
    strategy.harvest({"from": strategist})
    strategy.harvestTrigger(0)
    strategy.tendTrigger(0)
