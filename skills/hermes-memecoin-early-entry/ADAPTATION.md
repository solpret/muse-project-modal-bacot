# Local adaptation — installed 2026-11-05 (user order, survey decision)

Source: rickyananda/hermes-skills, `crypto-ops/memecoin-early-entry-system/SKILL.md`
(plus its `references/` folder as shipped).

EXCLUDED in this local copy:
- The upstream "Related Skills" reference to `evm-dex-sniper` was REMOVED
  (line deleted at install). No sniper, no autonomous execution is adopted
  from this skill. This skill is a read-only entry framework only.
- No execution, no trade, no wallet signing is authorised by installing it.
  Execution still needs the user's existing guards + armed scope.

ADOPTED (as documented method, not yet wired into live code):
- Core filters: liquidity > $100K, volume/liquidity ratio < 5x,
  token age day 3-7 sweet spot (vs our <=48h bias — a lens, not a replacement),
  net buys positive over 24h, no large holder recently dumping.
- Robinhood-chain: wait for graduation (Noxa curve -> Uniswap V3 at ~4.2 ETH)
  before treating a token as open-market tradeable; pre-graduation tokens are
  not open-market entries.
- Low-FDV honesty rule: do not send a CA that fails the filters just because
  the user wants low mcap; report the conflict plainly.
- GeckoTerminal Robinhood network id `robinhood` (keyless) for RH scanning.
- Watcher pattern preferred over blind picks; a filtered watchlist is not
  automatically a safe entry.
