# Local adaptation — installed 2026-11-05 (user order, survey decision)

Source: Dawgomatic/Xagent, `skills/skills/psychotechv4/rugcheck`
(SKILL.md + scripts/rugcheck.sh, curl-only, no key).

EXCLUDED:
- JWT bulk endpoints (`POST /v1/bulk/tokens/summary`, `/v1/bulk/tokens/report`)
  are NOT used — they need Solana wallet auth and are out of scope.
- No execution, no signing. Read-only Solana audit only.

ADOPTED RULE:
- Read the `risks[]` list, NEVER the score number alone (upstream notes the
  score direction has been reported inconsistently).
- Brand-new tokens may have no RugCheck report yet — fall back to the on-chain
  authority/holder check, never treat "no report" as safe.
- This is the Solana equivalent of the Binance audit + GoPlus + Clarus stack
  for BSC; it does not replace a sellability check.
