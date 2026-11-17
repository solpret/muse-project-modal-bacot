# Log Trial — M3 MODAL BACOT Solana (paper, aturan live yang dimigrasikan)

**Metode:** MODAL BACOT versi Solana (migrasi atas perintah user 14 Nov 2026
~21:11 WIB). Spesifikasi lengkap:
`m3-modal-bacot-solana-spec.md`; parameter di CHALLENGE.md §5.3.
**Definisi trial:** 1 paper trade lengkap entry → exit; menang =
`pnl_usd_net` > 0 sesudah fee pool + slippage + gas 0,00001 SOL/leg.
**Sumber kebenaran:** `~/workspace/solana-trading/m3-ledger.json` (TERPISAH
dari `ledger.json` M1) + log ini (bukti gerbang per trial).
**Status: TERBUKA — ronde 1 fresh 0/10 trial** (mulai 14 Nov 2026 ~21:11 WIB).
Ronde BSC lama (0/10 trial, terblokir) ditutup tanpa trial — hanya konteks.

## Checklist gerbang per trial (gagal satu = TIDAK ada trial)
- [ ] Discovery: narasi (meta/boost/trending/profiles) / wallet tier-ab /
  PumpPortal stream, ATAU screening pasca-graduation
- [ ] Audit RugCheck: report ada, score_normalised ≤30, tanpa risk "danger",
  mintAuthority null, freezeAuthority null, transferFee 0%, rugged false
- [ ] Skor 6 faktor ≥70 (bobot: contract 25, distribution 25, entry 5,
  liquidity 20, money_flow 10, sell_path 15)
- [ ] Money-flow: buys share h1 ≥60% DAN volume h1 ≥2× sighting pertama DAN
  (holder +5% ATAU likuiditas +2% sejak sighting)
- [ ] Konfirmasi entry: dip 15–30% ATAU breakout+retest, DAN volume ≥2x,
  DAN holder naik
- [ ] Exit ditulis SEBELUM entry: ladder 50% @2x, 25% @4x, trailing
  40%→15%, floor BE +10%, hard stop −25%, time stop 24 jam
- [ ] Drag tercatat: fee pool per dex, slippage (quote Jupiter), gas
  0,00001 SOL/leg

## Method fix audit 14 Nov ~22:05 WIB (BUKAN tuning — ronde 0/10, 0 trade)
- **BUG-1:** urutan argumen `score_mint` salah → skor wallet selalu 0, gate factory tidak pernah aktif. Diperbaiki (kaki D) + terverifikasi repro 7/7.
- **BUG-2:** sighting `holders=None` → TypeError di konfirmasi entry (8/8 sighting beku). Diperbaiki: sighting hanya bila holders terisi + refresh baseline + defensif `or 0`.
- **BUG-3:** `pnl_usd_net` tidak memotong entry drag (+$38,9993 vs +$38,4986 kas nyata). Diperbaiki: pnl = realized − size − entry_drag + breakdown komponen nyata. Repro: pnl == 38.4986.
- **GoPlus** audit kedua (gerbang keras, fail-closed) + **Jupiter `/recent`** discovery tambahan. Detail: CHALLENGE.md §5.3.1a.

## Trial ronde 1
_Belum ada trial tertutup._

### Penutup ronde 1 — 15 Nov 2026 ~06:0x WIB (closed_untested)
- **Hasil: 0/10 trial, 0 menang, 0 kalah — metode BELUM TERUJI, bukan
  lolos/gagal.** ~34 run cron 15-menit, semua exit 0; 67 sighting tercatat;
  0 entry. Corong (6 run sampel, 240 kandidat): no_pair_data 143 (59,6%),
  RugCheck danger 50 (20,8%); hanya 1 kandidat mencapai skor/money-flow
  (76,2, lolos skor — gagal money-flow karena sighting pertama).
- **Akar masalah:** (1) sighting tidak pernah dievaluasi ulang — ukur
  06:03 WIB discovery hanya memuat 3/67 sighting, universe-40 hanya 1;
  (2) universe dibanjiri token tanpa pair (jup_recent 30/40 slot);
  (3) gerbang RugCheck dinamis (lolos saat sighting, gagal menit kemudian);
  (4) chart <12 candle untuk token segar.
- **Perbaikan (method v2, didokumentasikan di
  m3-evaluasi-ronde1-2026-11-15.md + CHALLENGE.md §5.3.1b):** FIX-1
  universe sighting-first (≤20 sighting/run, TTL 6 jam); FIX-2 prioritas
  discovery infra-graduated dulu, jup_recent terakhir; FIX-3 log cakupan.
  TIDAK ADA gerbang/ambang yang dilonggarkan.
- Rekor ronde 1 disimpan utuh di scoreboard (status `closed_untested`).

## Trial ronde 2 (method v2 sighting-first — FRESH 0/10)
**Mulai:** 15 Nov 2026 ~06:1x WIB. **Status: TERBUKA.**
**Method:** MODAL BACOT Solana v2 (sighting-first) — lihat CHALLENGE.md
§5.3.1b. Bankroll $1.000, risiko 1% ($10), skor ≥60 feed, money-flow
wajib, konfirmasi dip/breakout, exit ladder 2x/4x. Safety rails TIDAK
berubah (audit RugCheck+GoPlus, LP lock ≥50%, holder gates, kill-switch
<$700). Ledger direset $1.000/0/0; state sightings dipertahankan (35 segar).
_Belum ada trial tertutup di ronde 2._
