---
name: memecoin-early-entry-system
title: Systematic Early Memecoin Entry & Risk Management
description: Data‑driven framework for entering early‑stage memecoins while avoiding rugs, based on lessons from RH‑chain trades (ROGE, CashCat patterns). User demands realistic analysis, no‑hype, systematic filters.
tags:
  - memecoin
  - early-entry
  - risk-management
  - robinhood-chain
  - token-screening
---

# Systematic Early Memecoin Entry

User previously suffered from **ROGE‑style rugs**—entered early (day 2.9) but token dumped after massive pump. This skill encodes the **filters and timing** that catch promising tokens while avoiding obvious traps.

## When to Use

Apply when:
- User asks “cari token early” or “micin robinhood”
- Scanning new launches on Noxa, DexScreener, or GeckoTerminal
- Evaluating a token the user is considering entering

## Core Filters (Must‑Pass)

### 1. **Liquidity Threshold**
- **Minimum liquidity**: **$100 K** (USD).
- Why: Below $100 K, a single whale can easily pump‑and‑dump; liquidity pulls are instant rugs.
- Check: `liquidity.usd` from DexScreener / GeckoTerminal API.

### 2. **Volume/Liquidity Ratio**
- **Max ratio**: **5×** (e.g., $500 K volume on $100 K liquidity).
- Why: Ratios above 5× often indicate whale accumulation before a dump.
- Calculate: `volume_24h / liquidity_usd`.

### 3. **Developer & Community Signals**
- **Active Telegram/X** with dev responses within 24 h.
- **Website or litepaper** that describes a narrative (not just “memecoin”).
- **No anonymous‑only team** (if completely anon, treat as higher risk).

### 4. **Token Age (Sweet Spot)**
- **Day 3–7** after creation.
- Why: Day 1–2 are dev‑dump territory; day 8+ may have missed the early run.
- Check: `createdAt` from DexScreener or block explorer.

### 5. **Buy/Sell Pressure**
- **Net buys** over 24 h should be positive (more buys than sells).
- Look for **steady accumulation**, not one‑spike pump.

## Robinhood‑Chain Specifics

- **Bonding‑curve graduation**: Tokens start on Noxa bonding curve, graduate to Uniswap V3 at ~4.2 ETH pool size. **Wait for graduation** before entering—pre‑graduation data is invisible to standard APIs.
- **RPC**: `https://rpc.mainnet.chain.robinhood.com` (needs `Content-Type: application/json` header).
- **Explorer**: `https://robinscan.io` (primary) and `https://robinhoodchain.blockscout.com` (alternate, CF-gated).

## Entry Checklist (Run Before Buying)

```yaml
- [ ] Liquidity > $100 K
- [ ] Volume / Liquidity < 5×
- [ ] Token age 3–7 days
- [ ] Active Telegram/X (dev replies)
- [ ] Website / narrative exists
- [ ] Net buys positive (24 h)
- [ ] No large holder (>10% supply) recently dumping
- [ ] Graduated to Uniswap V3 (for RH‑chain)
```

## Position Sizing & Management

- **Max per token**: 5 % of total crypto risk capital.
- **Take‑profit tiers**:
  - 2× → sell 30 %
  - 3× → sell another 30 %
  - 5× → sell remaining 40 %
- **Mental stop‑loss**: –50 % from entry price.

## Monitoring & Alerts

Set up a watcher that tracks:
- Liquidity changes (alert if drops below $50 K)
- Large holder movements (>5 % supply transfer)
- Dev social‑media silence > 48 h

## Common Pitfalls & Lessons

### ROGE Post‑Mortem
- **What happened**: Entered day 2.9, liquidity $30 K, volume $350 K (11.7× ratio), whale pumped then dumped.
- **What the filters would have caught**: liquidity too low ($30 K < $100 K), volume ratio 11.7× > 5×.
- **Lesson**: Enforce liquidity and volume filters strictly.

### CashCat Success Pattern
- **Graduated to Uniswap V3** around day 10.
- **Liquidity grew organically** from $8 K to $8 M.
- **Dev team active** on Telegram throughout.
- **Lesson**: Wait for graduation, verify dev engagement.

## RH-Chain Scanning via GeckoTerminal (proven, no key)

DexScreener often lacks RH-chain coverage. Use GeckoTerminal — network id is **`robinhood`**
(discovered by paging `/api/v2/networks`; it's NOT on page 1). No API key needed.

```bash
# Trending / new / top-volume pools (swap the last path segment)
curl -sL "https://api.geckoterminal.com/api/v2/networks/robinhood/trending_pools?page=1" -H "Accept: application/json"
curl -sL "https://api.geckoterminal.com/api/v2/networks/robinhood/new_pools?page=1"      -H "Accept: application/json"
curl -sL "https://api.geckoterminal.com/api/v2/networks/robinhood/pools?page=1&sort=h24_volume_usd_desc" -H "Accept: application/json"
```
Per-pool `attributes` carry everything the filters need: `reserve_in_usd` (liq),
`volume_usd.h24`, `pool_created_at` (age), `fdv_usd`, `market_cap_usd`,
`price_change_percentage.h24`. Compute `ratio = vol_h24 / liq`.

Launchpads seen on RH chain: NOXA Fun (`fun.noxa.eth.limo`), StonkBrokers
(`stonkbrokers.cash`), Sentry. New launchpad tokens land in `new_pools` — almost all day-0.

### The low-mcap trap (recurring — state it honestly, don't fight it)
When the user asks for "token micin / low mcap", expect this EVERY scan:
**every low-FDV (<$5M) token FAILS the ratio filter (ratio 8–50x), while everything that
PASSES the filter has already grown to $50M+ FDV (not "micin" anymore).** Low mcap and safe
entry are mutually exclusive on a hot chain — the cheap ones are cheap because they're day-0
dev-dump/rug bait (the ROGE pattern). Do NOT send a CA that fails the filter just because the
user wants low mcap. Report the conflict plainly and offer the watcher instead.

### Sending a contract address (CA) — gate
Only send a CA when it passes ALL core filters. For "send CA if dev good": on-chain metrics
(liq, ratio, age, holders) are auto-checkable, but "dev good" (active X/TG, credible team) is
NOT fully automatable — flag candidates that pass metrics + have live socials, but the final
"good dev" entry call stays with the user. Never present a filter-failing token as a pick.

When the user explicitly requests a copyable CA, render each validated address as inline code and include a chart link. Re-fetch the exact token immediately before sending, confirm it is a 42-character EVM address, and label marginal candidates **watchlist**, not picks. Presentation pressure never weakens the gate.

### RH sub-$30K scan protocol

For microcaps below $30K, page through GeckoTerminal `new_pools`, deduplicate by **base-token address**, and retain the most liquid pool. Require at minimum positive buy pressure, non-trivial liquidity, a manageable volume/liquidity ratio, and a live route check. Most records are minutes old; age under one day is an elevated-risk observation, not a normal recommendation.

Before calling a dev “active”:
1. Resolve the exact base-token address from `relationships.base_token.data.id`; strip only the literal `robinhood_` prefix.
2. Query `/tokens/{address}/info` for X/TG/site/description.
3. Verify the X identity belongs to the project/dev—not an unrelated famous account, news article, or borrowed status URL. Unrelated institutional accounts are spoof signals.
4. Search Dexscreener by both token name and address to detect clones/name collisions. Never reconstruct or truncate a CA from display output.
5. Re-fetch live pair data immediately before the final answer because MC and liquidity move materially within minutes.
6. Verify the bot can discover and execute both buy and sell on that venue. Fresh RH microcaps are frequently Uniswap V4; if V4 is off, label them untradeable by the bot and do not recommend entry.

A project with website + X + Telegram (MEDUSA-style social completeness) is a useful benchmark, but social completeness never overrides sell pressure, thin liquidity, clone risk, holder uncertainty, or inaccessible exit routing.

### "Dev claimed" verification (info endpoint) — recurring user ask
User frequently asks for tokens where "dev udah claim". Check `/tokens/{addr}/info`
(base token addr = `relationships.base_token.data.id`, strip `robinhood_` prefix). A token is
**dev-claimed** when `twitter_handle` / `telegram_handle` / `websites` / `description` are
populated. Read the signals:
- `gt_score == 67.9` exactly with empty socials = **default/unclaimed** boilerplate, anonymous dev.
- `gt_score == 0` / all null = no metadata at all.
- Socials pointing to `RobinhoodApp` / `RobinhoodCrypto` (the exchange's own handles) = **NOT the
  token dev** — it's a tokenized stock (e.g. NVDA "NVIDIA Robinhood Token") or decoy, not a community micin.
Live-check claimed socials: `curl -o /dev/null -w "%{http_code}"` the site/X, and pull TG member
count from `t.me/{handle}` via `grep -oiE '[0-9,]+ (members|subscribers)'`.

**CRITICAL: dev-claim ≠ safe.** HOOPLA (Aug 2026) was dev-claimed (web+X+TG live, gt_score 79) yet
`price_change_percentage.h24 = +170,000%`, ratio 47x, TG only 23 members, 14k buys/3k sells in 24h =
distribution phase. Entering = becoming exit liquidity. Dev-claim is necessary, NOT sufficient — every
liq/ratio/age/community filter still applies on top.

### Watcher pattern (preferred over blind picks)
User prefers a cron watcher that scans launchpad/chain every few hours and pings a CA ONLY
when a token passes all filters (liq>$100k, ratio<5x, age 3-7d, FDV under user's cap,
net-positive vol, live socials). Before creating, get: (1) FDV cap defining "low mcap",
(2) scan frequency + delivery target. Build with `cronjob`.

For a mixed-chain Telegram signal feed and an explicitly aggressive RH microcap profile, use the two-layer collection/revalidation design in `references/telegram-rh-signal-filter.md`. Keep this distinct from the full conservative entry checklist: a sub-$30K result is a **filtered watchlist**, not automatically a safe entry.

## Automation Scripts

See `references/rh-chain-scanner.md` for a Python scanner that applies these filters to the RH‑chain token list.
See `references/telegram-rh-signal-filter.md` for exact-CA parsing, deduplication, live revalidation, social spoof rejection, and alert formatting for Telegram RH/RBH feeds.

## Related Skills

- `token-mc-analysis` – for market‑cap potential estimation.
- `testnet-quest-bots` – for non‑memecoin airdrop farming.

---
**Maintained from session** 2026‑07‑11 (ROGE rug frustration → systematic entry demand).