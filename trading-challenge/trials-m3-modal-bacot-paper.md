# Log Trial — M3 MODAL BACOT (paper, aturan metode live)

**Metode:** aturan live Modal Bacot (arming-scope 2026-10-31 + revisi 2026-11-06;
paper $1.000 bankroll, risiko 1% = $10/trade). Detail parameter persis di
CHALLENGE.md §5.3.
**Definisi trial:** 1 paper trade lengkap entry → exit; menang =
`pnl_usd_net` > 0 sesudah fee + tax + gas $0,05 + slippage.
**Sumber kebenaran:** `~/workspace/ponyin-tools/paper-bsc-trades.json` +
log ini (bukti gerbang per trial).
**Status: TERBUKA tapi TERBLOKIR (0/10 trial — bukan 0 menang).**
Syarat buka blokir (CHALLENGE.md §5.3.4): (a) user mengaktifkan kembali
screening/feed BSC untuk keperluan paper, ATAU (b) parent menjalankan satu
pass screening pasca-graduation manual dengan bukti gerbang lengkap per
kandidat.

## Alasan blokir (per 14 Nov 2026 ~20:38 WIB)
1. Feed discovery (feed_loop.py / narrative-pulse) NONAKTIF — BSC trading
   dimatikan atas perintah user 14 Nov ~18:15 WIB.
2. Kaki money-flow Ankr MATI (401 sejak 9 Nov). Pengganti yang sah bila
   dipakai: seri GoPlus (holder count) + volume DexScreener — harus dicatat
   sebagai catatan metode, bukan diasumsikan sama dengan kaki Ankr.
3. Pencarian X kehabisan kredit (402).
4. Tidak ada mesin entry paper otomatis — `paper_bsc.py` hanya pencatat
   ledger (`stats` + `add`). Mesin live (`live_loop.py` /
   `live_executor.py`) TIDAK PERNAH dijalankan untuk challenge.

## Checklist gerbang per trial (gagal satu = TIDAK ada trial)
- [ ] Discovery: sinyal narasi/tier-ab terkonfirmasi money-flow, ATAU
  screening pasca-graduation (four.meme / Flap.sh / Genius.fun + trending)
- [ ] Audit Binance: hasil disclosed (hasResult=false = tidak ada hasil,
  bukan lolos); RISK hit = STOP
- [ ] Audit GoPlus: bersih (bukan honeypot/blacklist/pausable/dll)
- [ ] Skor 6 faktor ≥70 (bobot: contract 25, distribution 25, entry 5,
  liquidity 20, money_flow 10, sell_path 15)
- [ ] Money-flow: tracked inflow ATAU holder kumulatif ≥5% DAN pool ≥2%
  sejak sighting pertama
- [ ] Konfirmasi entry: dip 15–30% ATAU breakout+retest, DAN volume ≥2x,
  DAN holder naik
- [ ] Exit ditulis SEBELUM entry: ladder 50% @2x, 25% @4x, trailing
  40%→15%, floor BE +10%, hard stop −25%, time stop 24 jam
- [ ] Drag tercatat: fee pool, tax token, gas $0,05, slippage

## Format trial JSON (untuk `update_scoreboard.py add`)
```json
{
  "token": "0x...",
  "symbol": "XXX",
  "pair": "0x...",
  "entry_time": "2026-11-14T21:00:00+07:00",
  "entry_usd": 10.0,
  "entry_price_usd": 0.00000123,
  "size_usd": 10.0,
  "exit_time": "2026-11-14T23:00:00+07:00",
  "exit_reason": "ladder_2x / trailing / hard_stop_-25% / time_stop_24h / ...",
  "pnl_usd_net": 1.23,
  "pnl_breakdown": {"fees_usd": 0.05, "tax_usd": 0.0, "gas_usd": 0.05, "slippage_usd": 0.02},
  "gates": {"audit_binance": true, "audit_goplus": true, "score": 72, "money_flow": true, "entry_confirmation": true},
  "discovery": "narrative signal 2026-11-14 / screening four.meme"
}
```
Field `gates` wajib berisi kelima kunci dengan nilai truthy — bila satu
saja false/hilang, updater MENOLAK trial (gagal satu gerbang = tidak ada
trial).

## Ronde 1 (terbuka + terblokir, 0/10)
| # | Token | Entry → Exit | Alasan exit | PnL net (USD) | Hasil |
|---|---|---|---|---|---|
| _belum ada trial — menunggu buka blokir_ | | | | | |
