# MIGRASI M3 MODAL BACOT → SOLANA — progress log

Perintah user 14 Nov ~21:11 WIB. Unblock M3 BSC DIBATALKAN. Paper dulu; live Solana tetap terblokir (wallet 0 SOL).

## 21:11 — Mulai. Konteks dibaca
- CHALLENGE.md §5.3 (parameter live BSC), GOAL.md modal-bacot, paper-bsc-rules.md, INFRA_PROGRESS.md, paper_run_solana.py (M1).
- M1 Solana terbukti jalan: GeckoTerminal, DexScreener (curl fallback), RugCheck (audit/holder/LP), Jupiter v1 quote, PumpPortal WS ingest, wallet-signals.json (9 sinyal, tier-ab Solana sudah ada), funnel candidates.json, prices.db.
- Mati dari VM: Solscan public API (404), GoPlus Solana (2022), Jupiter v6, RPC getTokenLargestAccounts (429), GMGN (Cloudflare), X search (402).

## Riset (selesai, terverifikasi live dari VM 14 Nov ~21:20 WIB)
- DexScreener boosts/top + latest + metas/trending + profiles/latest + search: JALAN (tanpa key). Metas = tag narasi; boosts = sinyal berbayar (caveat dicatat).
- GeckoTerminal trending/new pools: JALAN. RugCheck report+summary: JALAN (score 1, LP 99,98% pada mint M1).
- Jupiter v1 quote: JALAN (M1). tokens.jup.ag: MATI (HTTP 000). GoPlus Solana: MATI (2022). Solscan API: MATI (404). GMGN: MATI (Cloudflare). X: MATI (402).
- PumpPortal trade stream: butuh key + wallet ≥0,02 SOL — TIDAK gratis. Helius/Birdeye: free tier ada tapi butuh API key signup dashboard (tidak bisa dari VM); engine dukung HELIUS_API_KEY opsional.
- Wallet-signals.json: 9 sinyal terverifikasi (deployer/whale/smart; factory diblokir).
- Riset web: Birdeye/Cielo/Nansen/Arkham butuh akun; RugCheck score aditif bisa menyesatkan (BONK 96 vs memecoin 2 menit 1) — skor hanya satu input.

## Dokumen (selesai)
- Spec: ~/workspace/trading-challenge/m3-modal-bacot-solana-spec.md
- CHALLENGE.md §5.1/§5.3/§5.3.4/§3/§8 → versi Solana; log trial baru trials-m3-modal-bacot-solana.md
- scoreboard.json M3: status open, ronde 1 open fresh 0/10, ledger m3-ledger.json; updater: sync_m3 + gerbang audit_rugcheck
- INSIDEN SYNC (diperbaiki): sync pertama sempat mengimpor 20 trial historis M2 (backtest 3-14 Nov, termasuk varian fee = simulasi ulang trade sama) → M2 dipulihkan ke waiting 0/10, sync_m2 diberi filter exit_ts ≥ 14 Nov 20:34 WIB, 10 file backtest ditandai excluded + dicatat di CHALLENGE.md §3. Verifikasi: sync ulang → [m2] 0 trial baru; status M2 waiting 0W/0L, M3 open 0W/0L.

## Mesin (SELESAI + teruji live)
- m3_engine.py (850 baris, py_compile OK) — discovery/gates/skor/money-flow/entry/exit/ledger terpisah
- Dry-run live 14 Nov 21:17 WIB (72 dtk): 20 kandidat dievaluasi, 0 entry (11 RugCheck danger, 8 no pair data, 1 money-flow fail — skor 76,2 tapi sighting pertama). TIDAK ada trade yang difabrikasi.
- Run nyata 14 Nov 21:19 WIB: ledger m3-ledger.json dibuat (kas $1.000, 0 posisi, 0 trade), 8 baseline sighting tercatat di m3-state.json.
- Verifikasi updater: sync → [m3] 0 trial baru; add dengan gerbang BSC lama (audit_binance) DITOLAK exit 1 — format trial BSC tidak bisa lagi masuk.
- Cron BELUM dipasang — keputusan parent (pola M1: 15 menit).
