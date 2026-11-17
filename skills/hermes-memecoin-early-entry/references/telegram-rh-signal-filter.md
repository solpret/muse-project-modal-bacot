# Filtered Telegram Signal Watcher for RH Microcaps

Use this pattern when a public Telegram feed mixes SOL/BSC/RH calls and the user wants only actionable Robinhood Chain candidates—not a raw CA firehose.

## Collection

- Poll the public channel preview (`https://t.me/s/<channel>`) on a short interval.
- Parse message IDs from `data-post`, persist the highest ID, and deduplicate strictly by message ID.
- Establish the first observed message as a silent baseline so startup does not replay old calls.
- Accept only posts explicitly marked `RH` or `RBH` and only exact 42-character EVM addresses.

## Two-Layer Filter

### Feed fields

Require:

- MC at or below the user's cap;
- minimum liquidity;
- minimum holder count;
- at least three smart-wallet buys;
- no severe feed flags such as suspected control, serial deployer/death-rate, or retained mint/freeze authority.

### Live revalidation

Before delivery, refetch by exact CA:

1. DexScreener: deepest Robinhood pair, current MC/FDV, liquidity, volume/liquidity, buy/sell pressure, venue, chart URL.
2. GeckoTerminal token info: project X/TG/site, description, dev holding/honeypot fields when available.
3. Reject stale candidates whose live MC/liquidity no longer satisfies the gate.
4. Reject unrelated institutional handles, borrowed post URLs, and other social-metadata spoofing.
5. Search by name and CA when necessary to detect clones; never reconstruct an address from truncated display output.
6. If alerts are intended for bot execution, require a discovered buy and sell route on an enabled adapter. A V4 or launchpad token is not executable merely because chart data exists.

## Output and mode changes

Deliver only passing candidates, with:

- token and ticker;
- CA in inline-code tap-to-copy format;
- live MC, liquidity, and volume/liquidity;
- age, holders, smart-wallet count, and source risk flags;
- project X, source message, and chart;
- label `filtered watchlist` until human/dev activity and sell-path verification are complete.

If the user initially asks for every RH/RBH CA and later says “saring,” treat that as an immediate watcher-mode replacement—not an additional commentary preference. Move the gates into the deterministic collection script itself, update the job description/name, retain the existing message-ID baseline, and test both a passing fixture and rejects for wrong chain, over-cap MC, and severe flags. Do not replay messages seen under the previous mode.

An X handle present in token metadata proves only that a social was supplied. Say **project-owned X** after identity checks; say **active dev** only after confirming recent project/dev posts or replies. A famous unrelated account, article URL, or isolated status link fails the social gate.

Silence is correct when no candidate passes. Do not weaken the gate just to ensure frequent alerts.

## Configurable Microcap Profile

For an intentionally aggressive sub-$30K watcher, a practical *prefilter* is:

- MC ≤ $30K;
- liquidity ≥ $10K;
- holders ≥ 50;
- smart-wallet buys ≥ 3;
- 24h volume/liquidity ≤ 5×;
- project-owned X required;
- severe feed flags absent.

This is a discovery profile, not the full conservative entry checklist. It must be described as a filtered watchlist rather than a safe entry recommendation.