


def stratData(strategy, token, vUSDC, vVSP, vsp, vault):
    decimals = token.decimals()
    print('\n----STRATEGY----')
    stratBal = token.balanceOf(strategy)
    vesperSharesU = vUSDC.balanceOf(strategy)
    vesperSharesV = vVSP.balanceOf(strategy)
    vspBal = vsp.balanceOf(strategy)
    print("yvUSDC bal:", vault.balanceOf(strategy)/(10 ** decimals))
    print("usdc bal:", stratBal/(10 ** decimals))
    print("vsp bal:", vspBal/1e18)
    print("vesper shares USDC:", vesperSharesU / 1e18)
    print("vesper shares vVSP:", vesperSharesV / 1e18)
    print('Estimated total assets:', strategy.estimatedTotalAssets()/  (10 ** decimals))  

def vaultData(vault, token):
    print('\n----VAULT----')
    decimals = token.decimals()
    vaultBal = token.balanceOf(vault)
    balance = vault.totalAssets()/  (10 ** decimals)
    print("loose usdc bal:", vaultBal/(10 ** decimals))
    debt = vault.totalDebt()/  (10 ** decimals)
    print(f"Total Debt: {debt:.5f}")
    print(f"Total Assets: {balance:.5f}")