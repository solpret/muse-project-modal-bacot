# Solana Smart-Money Buy Watcher

Use this pattern when the user supplies a labeled Solana wallet watchlist and wants Telegram alerts for new micin buys.

## Detection pipeline

1. Validate addresses are unique Base58-shaped public keys.
2. Create a silent baseline with `getSignaturesForAddress`; never alert historical transactions on first run.
3. Poll each wallet's newest confirmed signatures through multiple public RPC fallbacks.
4. Fetch each fresh transaction with `getTransaction` (`jsonParsed`, `maxSupportedTransactionVersion: 0`).
5. Compare the watched owner's `preTokenBalances` and `postTokenBalances`.
6. Treat an event as a buy only when token balance increased and native SOL balance decreased beyond a configurable threshold (default 1 SOL).
7. Enrich the mint through DexScreener with symbol, liquidity, FDV, chart URL, Solscan transaction, and CA.
8. Persist the last signature per wallet atomically. A quiet run prints nothing.

## Alert quality

- Script-only cron is preferred: no LLM tokens on empty polling runs.
- Deliver only non-empty stdout; RPC degradation should alert only when a majority of wallets fail.
- Include wallet label, approximate SOL spent, token received, liquidity, FDV, CA, transaction, and chart.
- A whale buy is a signal, not an endorsement. Keep the existing liquidity/age/ratio/rug filters before suggesting entry.
- Avoid false positives from transfers, airdrops, LP operations, or token-account closure. The SOL-spend + token-gain gate is a baseline; enhanced transaction parsers (Helius/Shyft) improve classification when a key is available.

## Scaling and reliability

- Public RPC polling is acceptable for tens of wallets at 5-minute cadence, with throttling and endpoint fallback.
- For larger/faster watchlists, use Helius enhanced transactions/webhooks and deduplicate by signature.
- Maintain watchlist labels separately from state so targets can change without resetting historical cursors.
- Keep thresholds configurable (`MIN_SOL_SPEND`, token gain, liquidity/FDV caps).
