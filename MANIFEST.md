# MANIFEST — muse-project-modal-bacot

- **Tanggal:** 20 November 2026
- **Repo publik:** `muse-project-modal-bacot` — https://github.com/solpret/muse-project-modal-bacot
- **Ukuran:** 278 KB (284.546 byte), 46 file
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

## Pembaruan 2026-11-20 (sejak 17 Nov)
- Trading DIHENTIKAN user 19 Nov 18:22 WIB: cron M3 15 menit dihapus
  (`paper-trading-m3-solana-15m__interval@15m.md`), diganti cron 30 menit;
  GOAL.md + `m3_engine.py` + `baw-hyperevm-support-state.json` diperbarui.
- `trading-challenge/` dihapus dari tree ini (20 Nov): isinya duplikat —
  CHALLENGE.md/scoreboard/update_scoreboard.py identik dengan
  `common/trading-challenge-framework/`, trial M1/M2 identik dengan
  bacot-degen; varian `update_scoreboard.py.AUDITF-PATCHED` dipindah ke
  common. Framework tinggal di EXACTLY SATU tempat.
- Pemecahan repo: TIDAK diperlukan — tree 278 KB; tidak ada file >90 MB.

## Audit rahasia
Bersih (20 Nov 2026, `audit-secret-2026-11-20.txt` di folder induk):
0 temuan bernilai — layak repo publik.
