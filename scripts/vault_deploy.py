from brownie import Strategy, accounts, config, network, project, web3
from brownie import Contract



def main():
    token = '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'
    governance = '0x6AFB7c9a6E8F34a3E0eC6b734942a5589A84F44C'
    guardian = '0x6AFB7c9a6E8F34a3E0eC6b734942a5589A84F44C'
    treasury = '0x93A62dA5a14C80f265DAbC077fCEE437B1a0Efde'
    name = 'USDC yVault'
    symbol = 'yvUSDC'

    deployer = accounts.load('deployer')
    # registry = Contract('0x50c1a2eA0a861A967D9d0FFE2AE4012c2E053804')
    # #Contract.from_abi('0x50c1a2eA0a861A967D9d0FFE2AE4012c2E053804', proxyname, impl.abi)
    # registry.newExperimentalVault(token, governance, guardian, treasury, name, symbol,{"from": deployer})
    vault = Contract('0x477faf103dadc5fe5baa40951cf7512dcbc18126')
    #vault.setDepositLimit(50_000 * 1e6,{"from":deployer})

    # Strategy
    #strategy = deployer.deploy(Strategy, vault)
    #strategy.setKeeper(keeper)
    #strategy.setStrategist(deployer,{"from": deployer})
    # Verify source
    strategy = Strategy.at("0x282e8Af431d082D4A27251588315954b9BEc341b")
    #Strategy.publish_source(strategy)
    # strategy_address = "0x282e8Af431d082D4A27251588315954b9BEc341b"
    # debt_ratio = 9800
    # minDebtPerHarvest = 0
    # maxDebtPerHarvest = 2 ** 256 - 1
    # performance_fee = 1000


    ms = accounts.at("0x16388463d60ffe0661cf7f1f31a7d658ac790ff7", force=True)
    ydev = accounts.at("0x846e211e8ba920B353FB717631C015cf04061Cc9", force=True)
    vault = Contract("0x477faf103dadc5fe5baa40951cf7512dcbc18126")
    assert vault.managementFee() == 0
    vault.setRewards(ms, {"from":deployer})
    vault.setGuardian(ydev, {"from":deployer})
    vault.setDepositLimit(50_000 * 1e6, {"from":deployer})
    vault.setGovernance(ms, {"from":deployer})

    #vault.setDepositLimit(50_000 * 1e18,{"from":deployer})

    # vault.addStrategy(
    #     strategy_address, 
    #     debt_ratio, 
    #     minDebtPerHarvest,
    #     maxDebtPerHarvest,
    #     performance_fee,
    #     {"from":deployer}
    # )

    # multisig = '0x846e211e8ba920b353fb717631c015cf04061cc9'
    # vault.setGovernance(multisig,{"from":deployer})
    # strategy.setRewards(deployer,{"from":deployer})
    # vault.setManagementFee(0,{"from":deployer})

    # TODO 
    #Tag vault
            #registry.tagVault(vaultAddr, "https://meta.yearn.network/vaults/0x477faf103dadc5fe5baa40951cf7512dcbc18126/vault.json")
    #Setup sharer
    #Setup keeper