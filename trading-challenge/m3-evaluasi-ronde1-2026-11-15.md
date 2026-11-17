# Evaluasi Ronde 1 M3 MODAL BACOT Solana — 15 Nov 2026

**Perintah:** user 15 Nov 2026 ~05:58 WIB ("evaluasi dan mulai ulang challenge paper nya").
**Aturan berdiri yang mengikat pekerjaan ini:** user 15 Nov 2026 ~06:03 WIB —
tiap ronde berakhir (gagal ATAU lolos) evaluasi menyeluruh dulu, perbaiki,
lalu challenge ulang ronde fresh, untuk setiap model (M1/M2/M3). Bila sudah
konsisten 2 ronde berturut-turut, lapor + konfirmasi user dulu sebelum lanjut.
**Scope:** M3 saja. M1 dan M2 TIDAK disentuh.

## 1. Fakta ronde 1 (terverifikasi dari sumber primer)

| Fakta | Nilai |
|---|---|
| Ronde 1 mulai | 14 Nov 2026 ~21:11 WIB (migrasi BSC → Solana) |
| Ronde 1 berakhir | 15 Nov 2026 ~06:0x WIB (evaluasi ini) |
| Trial tertutup | **0 / 10** (ledger `m3-ledger.json`: kas $1.000, 0 posisi, 0 trade) |
| Kill switch | false, ekuitas $1.000 |
| Run cron 15-menit | ~34 run, semua exit 0, durasi ~2 menit/run |
| Sighting tercatat | 67 di `m3-state.json` (21:18 WIB 14 Nov → 05:55 WIB 15 Nov) |
| Entry | **0** — metode BELUM TERUJI, bukan lolos/gagal |

## 2. Corong evaluasi per run (6 run sampel, 240 kandidat dievaluasi)

| Run | Kandidat | no_pair_data | RugCheck danger | holder/top1 | chart <12 | Sampai skor/money-flow |
|---|---|---|---|---|---|---|
| Dry-run 21:17, 14 Nov | 20 | 8 | 11 | 0 | 0 | 1 (skor 76,2; gagal money-flow = sighting pertama, tanpa baseline) |
| 23:55, 14 Nov | 40 | 26 | 8 | 0 | 0 | 0 |
| 00:53, 15 Nov | 40 | 26 | 6 | ~2 | 2 | 0 |
| 02:54, 15 Nov | 40 | 31 | 6 | 2 | 1 | 0 |
| 03:08, 15 Nov | 40 | 25 | 11 | 3 | 1 | 0 |
| Dry-run 06:00, 15 Nov (evaluasi ini) | 40 | 27 | 8 | 5 | 0 | 0 |
| **Total** | **240** | **143 (59,6%)** | **50 (20,8%)** | **~12** | **4** | **1** |

**Bacaan:** ~80% kandidat mati di dua kaki pertama. Hanya 1 dari 240
kandidat yang pernah mencapai tahap skor/money-flow — dan itu pun sighting
pertama yang memang tidak bisa entry (tanpa baseline, money-flow gagal
oleh konstruksi). Artinya: **ronde 1 tidak pernah menguji metode sama
sekali** — bukan metodenya yang kalah, melainkan corongnya yang tidak
pernah mengantar kandidat ke gerbang penentu.

## 3. Akar masalah (dengan bukti)

### Akar #1 — Sighting hampir tidak pernah dievaluasi ulang (CACAT STRUKTURAL, utama)
Entry HANYA mungkin untuk kandidat yang punya baseline (sighting pertama)
DAN muncul lagi di universe run berikutnya. Pengukuran langsung 06:03 WIB
(panggil `discovery()` + interseksi dengan state):
- Discovery: 50 mint unik — hanya **3 dari 67 sighting** ada di dalamnya
  (3 dari 35 sighting segar ≤6 jam; ketiganya dari `infra_pools`).
- Universe-40: hanya **1 sighting**.
- Dry-run 06:00: dari 40 kandidat, **39 sighting pertama + 1 re-evaluasi**.
- Komposisi universe-40: `jup_recent` 30 + `infra_pools` 10; GT
  trending/new, boosts, profiles menyumbang 0 mint unik baru (duplikat
  jup_recent); `metas trending: []` (kaki narasi kosong saat itu).

Feed discovery bergerak ke token yang lebih baru tiap 15 menit; sighting
kemarin tidak pernah muncul lagi. Akibatnya entry window (dip + volume
2× + holder naik — kondisi sesaat) praktis tidak pernah diuji. Ini cacat
cakupan evaluasi, BUKAN ambang yang terlalu ketat.

### Akar #2 — Universe dibanjiri token yang tidak bisa dievaluasi
`no_pair_data` 25–31 dari 40 per run (62–78%): token berumur menit dari
`jup_recent` (30 slot universe) + GT new_pools yang belum terindeks
DexScreener, atau pair non-SOL. `pair_data` mengembalikan None →
fail-closed oleh desain (money-flow butuh data DexScreener). Bukan bug
`pair_data` — endpoint terbukti jalan (13/40 kandidat tiap run punya
pair; kandidat di akhir run tetap terbaca → bukan rate-limit). Masalahnya
adalah **urutan universe**: `UNIVERSE_CAP=40` terisi menurut urutan
insertion discovery (GT → boosts → profiles → jup_recent → funnel →
pools), sehingga sumber yang paling bisa dievaluasi (`infra_pools`,
graduated, 369 token tersedia) berada PALING AKHIR dan biasanya terpotong.

### Akar #3 — Gerbang audit RugCheck bersifat dinamis
Token yang lolos saat sighting sering gagal saat dievaluasi ulang —
diuji live 15 Nov ~06:00 WIB pada 5 sighting:
- `5EaWWo8L…`: sighting 05:55 (skor 20, tanpa danger) → re-evaluasi
  06:01 SUDAH gagal `audit_rugcheck_danger_risk` (6 menit kemudian).
- `AUfKbxEb…`: skor 33 + danger "Low Liquidity" kini (lolos saat
  sighting 22:10).
- `HtpL2Ubh…`: skor 69 + 3 danger konsentrasi kini (lolos saat sighting
  00:56).
- `7mEhH5gs…`: skor 1, tanpa risk, tapi `lpLockedPct` summary 46,6%
  (<50%) kini (lolos saat sighting 22:26).
- `BWJfBNeX…`: skor 1, tanpa risk, LP 87,3% — masih lolos kini.

Skor aditif, risiko danger, dan LP% berubah seiring perdagangan. Jendela
entry memang pendek — makin memperkuat perlunya re-evaluasi CEPAT dan
BERULANG (akar #1), bukan pelonggaran gerbang.

### Akar #4 — Kandidat yang lolos audit mati di chart <12 candle
1–2/run gagal `chart_2-3_candles<12`: token butuh ≥60 menit candle 5-menit
untuk konfirmasi dip/breakout. Token segar dari discovery berumur menit.
Tanpa re-evaluasi (akar #1), token yang di-sighting umur 10 menit tidak
pernah dicek lagi saat umurnya 60+ menit dan SUDAH punya candle.

## 4. Yang BUKAN akar masalah (dengan bukti — sengaja TIDAK diubah)

- **Skor 6-faktor (≥60 feed / ≥70 manual):** hanya 1 kandidat pernah
  mencapainya (76,2 — LOLOS). Bukan blocker. TIDAK diturunkan.
- **Money-flow (buys ≥60% + vol ≥2× + holder +5%/liq +2%):** hanya
  pernah diuji 1× (sighting pertama, gagal oleh konstruksi). Belum ada
  bukti ia memblokir apa pun. TIDAK dilonggarkan.
- **Konfirmasi entry (dip 15–30% / breakout+retest):** tidak pernah
  diuji dalam 8,5 jam. TIDAK diubah.
- **Sell path (quote Jupiter beli + jual-balik):** tidak pernah diuji.
  TIDAK diubah.
- **LP lock ≥50%:** hipotesis awal "token bonding-curve gagal LP"
  TERBANTAH — RugCheck melaporkan `pump_fun_amm lpLockedPct=100`,
  summary 87–100% untuk token sighting. Gerbang ini lolos untuk token
  graduated/bonding. (LP% bisa hanyut <50% seiring waktu — efek dinamis
  akar #3, bukan cacat gerbang.) TIDAK diubah.
- **Audit GoPlus (kedua):** tidak pernah tercapai di run sampel (kandidat
  mati sebelumnya). TIDAK diubah.
- **Gate wallet factory:** tidak pernah terpicu di run sampel. TIDAK diubah.
- **Kill switch / cron / bug mesin:** kill switch false; cron jalan
  tiap 15 menit exit 0; perbaikan BUG-1/2/3 (14 Nov ~22:05) terverifikasi
  masih ada di kode (urutan argumen `score_mint` benar; sighting hanya
  bila holders terisi; pnl memotong entry drag). TIDAK ada bug baru
  ditemukan.

## 5. Perbaikan yang diterapkan (ronde 2, method v2)

Semua perbaikan adalah **perbaikan cakupan evaluasi + observabilitas** —
TIDAK ADA gerbang keamanan, ambang skor, ambang money-flow, LP lock,
holder gate, kill-switch, sizing, atau exit yang dilonggarkan/diubah.
File: `~/workspace/solana-trading/m3/m3_engine.py` (py_compile OK).

### FIX-1 — Universe sighting-first (utama)
`run()` kini membangun universe sebagai: **sighting dari state dulu**
(umur ≤6 jam, terbaru dulu, maks 20/run) + discovery fresh sesudahnya,
total tetap maks 40. Sighting adalah satu-satunya kandidat yang BISA
entry (punya baseline); tanpa ini entry window tidak pernah diuji.
Sighting dicatat di info dengan `sources=["sighting"]`; semua gerbang
tetap berlaku penuh saat re-evaluasi.

### FIX-2 — Prioritas sumber discovery untuk slot fresh
Slot fresh diurutkan: `infra_pools` (0) → `infra_funnel`/`gt_*` (1) →
`ds_boost_*` (2) → `ds_profile_latest` (3) → `jup_recent` (4, terakhir).
Graduated (punya pair/LP/holder/riwayat) didahulukan; token berumur menit
yang belum terindeks tidak lagi menghabiskan slot pertama.

### FIX-3 — TTL sighting 6 jam + observabilitas
`prune_sightings()`: sighting berumur >6 jam dihapus tiap run (baseline
basi melemahkan money-flow; token kedaluwarsa boleh di-sighting ulang
segar). Sighting lama pra-fix BUG-2 (`holders=None`, 21:18–21:54 WIB 14
Nov) ikut terhapus oleh TTL ini. Log run kini mencatat
`reevaluasi N, sighting baru M` + komposisi universe, supaya evaluasi
berikutnya bisa melihat cakupan langsung.

### Yang sengaja TIDAK diubah
Lihat §4. Bila ronde 2 menunjukkan kandidat mencapai money-flow/skor/
entry-pattern lalu gugur di sana, ambang-ambang itu DIEVALUASI ULANG
dengan data trial — bukan sekarang, tanpa bukti.

## 6. Transisi ronde (scoreboard)

- **Ronde 1: DITUTUP sebagai `closed_untested` — 0/10 trial, 0 menang,
  0 kalah, win rate null.** Alasan: tidak ada trial yang bisa diuji
  (metode belum teruji, bukan lolos/gagal). Rekor ronde 1 TETAP disimpan
  utuh, tidak dihapus/diubah.
- **Ronde 2: DIBUKA sebagai ronde perbaikan ke-1 dari maks 3**
  (`fix_rounds_used` M3 = 1/3), status open, 0/10.
  - `method_version`: "MODAL BACOT Solana v2 (sighting-first, 15 Nov 2026)"
  - `method_changes`: "FIX-1 universe sighting-first (reevaluasi ≤20 sighting/run, TTL 6 jam); FIX-2 prioritas discovery infra-graduated dulu, jup_recent terakhir; FIX-3 log cakupan reevaluasi. TIDAK ADA gerbang/ambang yang dilonggarkan (skor ≥60, money-flow, LP ≥50%, holder gates, kill-switch $700, audit RugCheck+GoPlus tetap)."
- **Ledger direset** ke kas $1.000, 0 posisi, 0 trade (atomik; memang
  sudah $1.000/0/0 — reset menandai awal ronde 2). **State sightings
  TIDAK dihapus**: 35 sighting segar (≤6 jam) adalah bahan bakar FIX-1 —
  ronde 2 langsung bisa menguji entry window; sighting basi (>6 jam)
  terhapus otomatis oleh TTL di run berikut. Menghapus state justru
  menunda entry pertama tanpa alasan.
- **Cron M3 15-menit TIDAK dijeda/diubah** — tetap jalan; run berikut
  membaca state fresh dengan aturan baru.

## 7. Verifikasi pasca-restart

- `py_compile m3_engine.py` OK.
- Dry-run pasca-fix (lihat §8 di bawah — diisi sesudah run): universe
  harus menunjukkan `reevaluasi sighting ~20, fresh ~20`; log harus
  menunjukkan baris SKIP (re-evaluasi) bukan hanya SIGHTING; sighting
  >6 jam harus terhitung kedaluwarsa.
- `update_scoreboard.py sync` sesudah transisi: 0 trial baru (M1/M2/M3
  tidak berubah), scoreboard.md ter-render ulang dengan ronde 2 M3 open.

## 8. Hasil verifikasi pasca-restart (dry-run + run live v2)

**Dry-run pasca-fix — 15 Nov 06:07:57–06:10:23 WIB, exit 0, ~2,5 menit:**
- `sighting kedaluwarsa (> 6 jam): 32 dihapus` — TTL pruning bekerja
  (67 → 35 sighting di memori; dry-run tidak menyimpan, tapi logika
  terbukti).
- `universe: 40 kandidat (reevaluasi sighting 20, fresh 20)` — komposisi
  sesuai desain (sebelum fix: 39 sighting pertama + 1 re-evaluasi).
- **20 baris SKIP (re-evaluasi) + 20 baris SIGHTING (fresh)** — cakupan
  re-evaluasi naik dari 1/40 (2,5%) menjadi 20/40 (50%).
- **Pertama kali dalam sejarah challenge ada kandidat re-evaluasi yang
  mencapai gerbang money-flow:** `SKIP EwUVBpdM: money_flow_fail` —
  lolos audit+holder+LP+GoPlus+chart+skor, lalu gugur di money-flow.
  Corong kini mengantar kandidat ke gerbang penentu.
- Skip run ini: danger 14, no_pair_data 17, top1 5, chart 2, holders 1,
  money-flow 1. **0 entry** — gerbang bekerja sebagaimana mestinya;
  yang diperbaiki adalah kandidat MENCAPAI gerbang, bukan gerbangnya.
- `py_compile m3_engine.py` OK. `update_scoreboard.py sync` sesudah
  transisi: 0 trial baru (M1/M2/M3 tidak berubah); scoreboard.md
  ter-render ulang (M3 ronde 2 open 0W/0L, fix_used=1).

**Run live v2 pertama (manual, perintah cron yang sama, paper-only) —
15 Nov 06:10:41–06:13:41 WIB, exit 0, ~3 menit:**
- `sighting kedaluwarsa (> 6 jam): 32 dihapus` — pruning TERSIMPAN:
  state 67 → **36 sighting** (35 segar + 1 baru).
- `discovery: 76 mint unik; universe: 40 kandidat (reevaluasi sighting
  20, fresh 20)` — komposisi sesuai desain.
- **DUA kandidat re-evaluasi mencapai `money_flow_fail`** (EwUVBpdM,
  Bv8gmCuY) — corong kini berulang kali mengantar kandidat ke gerbang
  penentu (dry-run sebelumnya: 1).
- 0 entry, ledger kas $1.000, 0 posisi, 0 trade. Skip: danger 16,
  no_pair_data 14, money_flow 2, chart 2, top1/top10/holders 6.
- **Kesimpulan verifikasi:** perbaikan aktif di jalur live, state
  fresh terbaca bersih, tidak ada error. Run cron 15-menit berikutnya
  (06:23:46 WIB) melanjutkan dari state ini tanpa intervensi.

## 9. Kaki saldo — kriteria lolos baru + uji ketahanan sizing/exit M3

**Aturan baru (user 15 Nov ~06:05 WIB, dicatat di CHALLENGE.md §1/§4
+ `scoreboard.json pass_bar.balance_leg` + diimplementasikan di
`update_scoreboard.py finish_round_if_complete`):** ronde lolos HANYA bila
(a) ≥8/10 menang DAN (b) PnL bersih ronde > 0 (ekuitas akhir > ekuitas
awal; dihitung dari jumlah `pnl_usd_net` / `realized_sol` /
`net_vs_hodl_usd` atas 10 trial ronde). Jumlah kemenangan saja TIDAK
cukup. Bila satu trial tidak punya field PnL-nya → net tidak
terverifikasi → ronde TIDAK lolos (fail-closed). Diuji sintetis 4/4:
8W net +179 → lolos; 8W net −74 → GAGAL kaki saldo; 8W net None → gagal;
7W net +143,5 → gagal kaki menang.

**Pelajaran M1 ronde 1 (yang memicu aturan ini):** posisi 0,024/0,08 SOL
= 30% bankroll per trade; stop −15% nominal tidak melindungi saat harga
gap antar poll 15 menit — 2 kalah (−98%, −51,5%) menghabiskan saldo
sampai kill switch (ekuitas 0,052037 < 0,056 SOL).

**Uji ketahanan M3 (dari kode mesin, bukan asumsi):** sizing M3 =
min(risiko $10 / jarak stop 25%, maks $50, 2% cadangan pool) = **$40
per trade** (4% dari bankroll $1.000; skip bila < $5). Maks 3 posisi
terbuka, maks deploy 30% ($300) — 3 × $40 = $120 (12%), cap tidak pernah
mengikat. Exit: ladder 50% @2x, 25% @4x, trailing 40%→15%, floor BE
+10%, hard stop −25%, time stop 24 jam, hold mode (peak ≥4x) trailing
15% + maks 72 jam.
- Kalah normal (hard stop −25%): −$10 + drag ~$0,20–0,80 ≈ **−$10,50**
  per trade. 2 beruntun ≈ −$21 → ekuitas $979.
- Kalah gap-wipe ala M1 (token −100% antar poll): −$40 + drag ≈
  **−$41** per trade. 2 beruntun ≈ −$82 → ekuitas $918 — jauh di atas
  kill-switch $700.
- Worst case absolut satu ronde (10 gap-wipe): −$410 → $590 < $700 —
  kill switch BISA kena, tapi ronde itu sudah 0/10 menang (gagal di kaki
  menang juga).
- **Ronde 8-menang:** 2 kalah terburuk −$82. Kemenangan ladder tipikal
  +$20–50 bersih per trade (50% @2x ≈ +$20, 25% @4x ≈ +$30, minus drag
  ~$1–2). 8 menang × ~$20+ = +$160 ≫ $82 → **kaki saldo lolos dengan
  nyaman dalam semua skenario realistis**. Kaki saldo HANYA menggagalkan
  kasus patologis yang memang dimaksud aturan ini: 8 menang debu
  (mis. exit break-even +$0–2 tiap trade = +$0–16 total) + 2 kalah
  gap-wipe (−$82) → net negatif → TIDAK lolos meski 8/10.
- **Kesimpulan:** sizing 1% risiko + posisi 4% bankroll M3 secara
  struktural melindungi saldo dari 2 kekalahan beruntun — berbeda dari
  M1 (30% bankroll/trade). Kaki saldo tidak mengubah kelayakan metode
  M3; ia hanya memblokir kemenangan-kemenangan kecil yang tidak menutup
  kerugian. Tidak ada perubahan sizing/exit yang diperlukan dari uji ini.
