# MODAL BACOT live trading

Goal ID: goal_ef5a18871d91
Goal slug: modal-bacot-live-trading

## Description
Autonomous Solana memecoin trading (pindah dari BSC 14 Nov 2026; live terblokir 0 SOL, paper Solana yang jalan) on the main wallet only, with full gates, money-flow confirmation, a feed score of 60, and entries of about $1.90, with no trade forced before a candidate passes. Discovery and safety infrastructure now include a GeckoTerminal fast layer, holder and Ankr buy-log money-flow confirmation, a 5-minute feed, a backtest recorder, an 11-endpoint RPC pool with circuit breaker, Ankr as holder-count fallback, candidate-triggered X search, and an LP recheck that sells all if secured LP falls below half an entry baseline of at least 50%. Blockscout is not used for BSC holder counts because its API does not serve BSC.
