---
name: cli-trader-memecoin
description: "CLI Trader memecoin framework, adapted: event-driven exits, layered take-profit, slippage and volume/liquidity rules. Read-only method — no execution, no MCP trade tools."
source: "https://clitrader.com/trading-skills/memecoin-trading/"
adapted: "2026-11-05, user order 'Pasang keduanya + adopsi metodenya'"
---

# CLI Trader Memecoin — adapted method

This is an ADAPTATION, not a verbatim copy, of the CLI Trader memecoin
skill (clitrader.com). Only the parts below are adopted. Installing this
file authorises NO trade and NO execution.

## Adopted: entry screening (read-only)

- Rug checklist before any entry: mint authority revoked, freeze authority
  revoked, LP locked/burned (lock < 7 days = meaningless, 30+ days =
  meaningful), honeypot check (sell transactions visible, sell tax < 5%),
  ownership renounced, deployer history clean, top-10 holders < 30%
  (30-50% caution, > 50% fail; single wallet > 20% extreme fail),
  bundled launch (5+ wallets in first block = insider launch),
  social verification, token age > 24h with sustained volume.
- Liquidity: micro-cap minimum > $10K, small-cap > $50K preferred.
  Single LP provider with > 80% of liquidity = rug risk.
- Volume/liquidity ratio: healthy 1-5x; > 10x overheated; < 0.1x dead.
  (Agrees with the hermes < 5x cap adopted alongside this skill.)
- Slippage / price impact: trade size / pool liquidity = approximate impact.
  Rule: impact > 5% = position too large for the liquidity.
  (This mirrors the live round-trip depth guard already in place: refuse
  above 5% impact.)
- Never market-buy the first spike; wait for the first pullback. Avoid the
  first 30 minutes of launch (highest manipulation).

## Adopted: layered exits + event-driven exits

Layered take-profit (sell into strength, keep a moonbag):
- 2x -> sell 50% (initial recovered)
- 3x -> sell 25% more
- 5x -> sell 15% more
- 10x -> sell 5% more (keep 5% moonbag)
- Any rug flag at any level -> sell everything immediately.

Event exits (immediate, no hesitation):
- Deployer wallet moves tokens -> sell immediately.
- Volume drops > 80% from peak -> sell within 1 hour.
- Social momentum dies / accounts deleted or silent -> exit.
- Liquidity decreases > 20% -> exit now.
- Price drops > 50% from entry with no recovery in 2 hours -> exit.
- New critical red flag appears -> sell immediately, do not wait for a bounce.

Other adopted rules:
- Mental stop at -50% from entry (sell remaining).
- Time stop: flat 1-2 days after entry -> close (CLI Trader says 24h of no
  movement; the adopted window is 1-2 days, per the survey's Altrady
  time-stop addition).
- Trailing stop 20-25% from peak on the remainder (survey addition).
- Size from stop, not from conviction (survey addition, Altrady).
- Never average down on a memecoin. Never use leverage. Never hold a
  memecoin "for the long term". Never FOMO back in after exiting.
- Post-entry monitoring cadence: every 15-30 minutes while a position is
  open (as a monitoring rule; live monitoring frequency stays as the
  armed live jobs define it — this skill does not create new jobs).

## NOT adopted (explicit exclusions)

- The 0.5%-per-position ceiling (and 2-5% total memecoin allocation):
  NOT adopted. Current MODAL BACOT sizing stays risk 5% / cap 20% until
  the user decides otherwise. This ceiling remains an OPEN decision.
- MCP/CLI execution tools named upstream (Jupiter Talk swaps, Monorail
  wallet execution, etc.): NOT installed, NOT used. No execution path
  comes from this skill.
- "Verify you can sell before you buy (attempt a small test sell)":
  NOT adopted as an automatic step — a test sell is itself a real trade
  and needs its own authorisation.
- The mandatory risk-disclosure script ("Proceed? user must acknowledge"):
  NOT copied as a blocking script; risk is already disclosed per trade
  under the user's existing guard/reporting rules.
