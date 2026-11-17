# Local adaptation — installed 2026-11-05 (user order, survey decision)

Source: Penguin-Life/meme-terminal, `skills/dexscreener/SKILL.md`
(DexScreener public API, no key).

ADOPTED — installed ONCE with chain tags (not twice):
- Chains: `bsc`, `solana`, `robinhood`, `ethereum`, `base` (+ others the API
  covers). This single install serves both the BSC survey leg and the
  Robinhood+Solana survey leg; do not install a second DexScreener skill.
- Uses: token/pair search, pairs by token, pair detail, new pairs, boosts,
  profiles. Rate limit: API general ~300 req/min; this skill advises
  reasonable use (~30 req/min) — stay conservative.

CAUTIONS (from the survey):
- DexScreener trending/boosts are NOT quality: boosts are purchasable.
  Trending is discovery only, never a buy signal on its own.
- GeckoTerminal GT Score is a second opinion, not a gate replacement.
