# MANIFEST — muse-project-modal-bacot

- **Tanggal:** 17 November 2026
- **Repo publik:** `muse-project-modal-bacot` — https://github.com/solpret/muse-project-modal-bacot
- **Ukuran:** 360 KB (280.764 byte), 44 file
- **Cakupan:** Project Modal Bacot — trading memecoin (BSC, kini off) +
  paper trading M3 Solana (track challenge ronde 2).

## Isi

| Bagian | Isi |
|---|---|
| `goals/modal-bacot-live-trading/` | Goal utama Modal Bacot |
| `goals/narrative-pulse-watch/` | Watch narasi BSC (sinyal discovery, bukan rekomendasi beli) |
| `goals/early-call-wallet-data-collection/` | Koleksi wallet early-caller untuk screening paper |
| `goals/bsc-paper-trading-validation/` | Validasi paper BSC ($1.000 virtual, 1% risiko) |
| `solana-trading/m3/` | Engine M3 (`m3_engine.py`) + trial JSON (`m3-trials/`) |
| `solana-trading/m3-ledger.json`, `repro_m3_logic.py` | Ledger ronde 2 + repro logika |
| `trading-challenge/` | Spec M3 Solana, evaluasi ronde 1, progres migrasi, trial log M3 |
| `skills/` | binance-trading-signal, binance-meme-rush, binance-wallet-tracker, hermes-memecoin-early-entry, cli-trader-memecoin, memecoin-hunter-autotrader, crypto-market-rank, dexscreener, rugcheck, treasury-trading |

## Yang sengaja TIDAK ikut / ada di tempat lain
- `m3-state.json` (state runtime sightings) — dibuang.
- Skrip tracked-wallet scan (`narrative-pulse/`) ada di tree free-bacot
  (satu salinan saja) — dipakai Modal Bacot untuk money-flow, tapi
  filenya tinggal di sana.
- `CHALLENGE.md` + scoreboard + `update_scoreboard.py` ada di `common/`
  (repo `muse-project-common`) — framework dipakai semua track paper.
- Ingest Solana (`solana-trading/infra/`) ada di `common/infra/`.

## Audit rahasia
Bersih (17 Nov 2026): 0 temuan bernilai — layak repo publik.
