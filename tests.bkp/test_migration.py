# TODO: Add tests that show proper migration of the strategy to a newer one
#       Use another copy of the strategy to simulate the migration
#       Show that nothing is lost!

import pytest

def test_migration(
    chain,
    token,
    vault,
    external_vault,
    strategy,
    amount,
    Strategy,
    strategist,
    gov,
    user,
    RELATIVE_APPROX,
):
    # Deposit to the vault and harvest
    token.approve(vault.address, amount, {"from": user})
    vault.deposit(amount, {"from": user})
    chain.sleep(2)
    strategy.harvest()
    # print("#deposit to the vault and harvest")
    # print("strategy.estimatedTotalAssets(): , RELLATIVE_APPROX: ", "amount: ", (strategy.estimatedTotalAssets(), RELATIVE_APPROX, amount))
    assert pytest.approx(strategy.estimatedTotalAssets(), rel=RELATIVE_APPROX) == amount

    # migrate to a new strategy
    new_strategy = strategist.deploy(Strategy, vault, external_vault)
    print("address of an old strategy: ", (strategy.address))
    print("address of a new strategy: ", (new_strategy.address))
    print("address of vault: ", (vault.address))
    # was before
    vault.migrateStrategy(strategy, new_strategy, {"from": gov})
    # is now ( retest with vault later )
    # strategy.migrate(new_strategy.address, {"from": gov})
    print("after migration: strategy.estimatedTotalAssets(): , RELLATIVE_APPROX: ", "amount: ", (strategy.estimatedTotalAssets(), RELATIVE_APPROX, amount))
    print("after migration: new_strategy.estimatedTotalAssets(): , RELLATIVE_APPROX: ", "amount: ", (new_strategy.estimatedTotalAssets(), RELATIVE_APPROX, amount))
    assert (
        pytest.approx(new_strategy.estimatedTotalAssets(), rel=RELATIVE_APPROX)
        == amount
    )