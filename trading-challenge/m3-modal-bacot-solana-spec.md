# MODAL BACOT — Spesifikasi Versi Solana (M3-Solana)

**Perintah migrasi:** user 14 Nov 2026 ~21:11 WIB — semua metode ke Solana
(analisa, wallet, money-flow), riset dari berbagai sumber dengan akurasi
yang masuk akal untuk tujuannya. Pekerjaan unblock M3 versi BSC DIBATALKAN.
**Status:** PAPER dulu. Live Solana tetap terblokir (wallet agen 0 SOL).
**Ronde challenge:** FRESH 0/10 mulai 14 Nov 2026 ~21:11 WIB. Skor BSC lama
(0/10 trial terblokir) hanya konteks, tidak dibawa.

**Identitas yang dipertahankan (ini yang membedakan M3 dari M1 BACOT DEGEN):**
discovery narasi, skor berbobot 6 faktor, money-flow WAJIB, konfirmasi entry
dip/breakout, exit ladder 2x/4x. M1 tetap: discovery GeckoTerminal saja,
hard gate tanpa skor, tanpa money-flow, 2-sighting, stop/TP. Tidak ada trade
yang dihitung ganda.

**Sumber yang TERBUKTI jalan dari VM ini (diuji live 14 Nov 2026):**
GeckoTerminal, DexScreener (pairs, boosts, metas, profiles, search),
RugCheck (report + summary), Jupiter Swap v1 quote, PumpPortal WS
(newToken + migration, via infra), wallet-signals.json, infra pools.db +
prices.db + candidates.json.
**MATI / tidak bisa dipakai tanpa kunci:** Solscan public API (404),
GoPlus Solana (code 2022), Jupiter v6 + tokens.jup.ag (HTTP 000),
RPC publik getTokenLargestAccounts (429 persisten), GMGN (Cloudflare),
X search / twitterapi.io (402), PumpPortal trade stream (butuh API key +
wallet ≥0,02 SOL), Helius + Birdeye (free tier ada TAPI butuh API key dari
dashboard signup — tidak bisa dibuat dari VM; engine mendukung opsional
`HELIUS_API_KEY` bila suatu hari ada, tanpa itu tetap jalan).

---

## 1. Discovery narasi — BSC → Solana

| BSC (lama) | Solana (baru) | Status |
|---|---|---|
| Sinyal narasi (feed_loop / narrative-pulse) | **DexScreener metas/trending** — tag narasi (AI, Cat, …) + mcap/volume/tokenCount per meta. TERVERIFIKASI live | Jalan |
| Sinyal narasi | **DexScreener token-boosts/top + latest** — token yang sedang dipromosikan. CAVEAT JUJUR: Boost = sinyal BERBAYAR (multiplier trending score, siapa pun bisa beli). Dipakai HANYA sebagai feed discovery, TIDAK PERNAH sebagai bukti kualitas | Jalan, dengan caveat |
| Sinyal narasi | **DexScreener token-profiles/latest** — info berbayar + link website/X (link terbaca lewat API tanpa akses X) | Jalan |
| X search (candidate-triggered) | **TIDAK ADA pengganti yang membaca X dari VM** (402). Narasi diukur lewat metas/boosts/profiles/trending, bukan lewat X. Ini downgrade yang dicatat, bukan disembunyikan | Mati |
| GeckoTerminal trending 1 jam | **GeckoTerminal trending_pools + new_pools** (sudah dipakai M1) | Jalan |
| Holder bridge | **infra pools.db** — token baru PumpPortal + migrasi Raydium (daemon ingest jalan sejak 19:00 WIB) | Jalan |
| Tier-ab wallet | **wallet-signals.json + wallet_signal.py** (lihat §2) | Jalan |

**Aturan discovery:** kandidat masuk dari SALAH SATU jalur di atas. Sighting
pertama hanya snapshot (tidak langsung entry) — sama seperti BSC.

## 2. Wallet tracking tier-ab — BSC → Solana

- **BSC:** tracked wallets feed, entitas tier-ab.
- **Solana:** `~/workspace/solana-trading/wallets/wallet-signals.json` —
  9 sinyal terverifikasi (4 deployer sehat, 1 whale, 1 smart, 1 klaster
  cabal lemah; 2 factory deployer DIBLOKIR). Bukti migrasi terverifikasi via
  Jupiter `graduatedPool=True + graduatedAt` + enumerasi creatorTokens
  RugCheck. Contoh deployer terbaik GnYdutPAifmH3usS1cRzUjU1UjSxWPGx7de8TVUZkAYi
  (2/2 migrasi terverifikasi).
- **Peran sama seperti BSC:** discovery feed + input skor, TIDAK PERNAH
  entry sendiri. Wallet yang diblokir = 0 poin.
- **Batas jujur:** snapshot statis (dibuat 14 Nov); butuh refresh berkala
  (pekerjaan lanjutan, bukan blocker — engine baca file apa adanya, skor 0
  bila file tidak ada, lanjut normal seperti M1).

## 3. Audit — BSC → Solana

- **Binance audit: TIDAK BISA dimigrasikan.** API audit Binance hanya
  EVM/BSC; tidak ada padanan Solana. Dihapus dari gerbang M3-Solana,
  dicatat sebagai perubahan metode.
- **GoPlus: MATI di Solana** (code 2022 "main chain is not supported",
  terverifikasi 14 Nov). Dihapus.
- **Satu-satunya audit: RugCheck** (report + summary, gratis, tanpa key).
  Gerbang keras (SEMUA harus lolos, unverified = BLOCK):
  report ada; `score_normalised` ≤ 30; tanpa risk level "danger";
  `mintAuthority` null; `freezeAuthority` null; transferFee 0%
  (Token-2022 `transferFeeConfig` null); `rugged` false.
- **CAVEAT JUJUR (temuan riset):** skor RugCheck bersifat aditif dan bisa
  menyesatkan — dalam satu pengujian independen, BONK (token mapan) dapat
  96/100 sementara memecoin umur 2 menit dapat 1/100. Karena itu skor
  HANYA satu input; bobot keputusan ada di authorities / risks / LP lock.
- **Cross-check ideal (opsional):** Helius DAS `getAsset` untuk
  mint/freeze authority on-chain — butuh API key (free tier 1M kredit/bln,
  tanpa kartu, tapi signup dashboard). Engine membaca `HELIUS_API_KEY` bila
  ada; tanpa itu, RugCheck saja + dokumentasi.

## 4. Money-flow — BSC → Solana

- **BSC:** Ankr tracked inflow ATAU pertumbuhan kumulatif holder ≥5% DAN
  pool ≥2% sejak sighting pertama (revisi P1 2026-11-06).
- **Ankr MATI (401).** Pengukuran native-Solana (semua gratis, terverifikasi):
  - **(a) DexScreener txns** — buys vs sells per jendela (m5/h1/h6/h24) +
    volume. Tekanan beli bersih = `buys/(buys+sells)`.
  - **(b) Snapshot holder RugCheck** dari waktu ke waktu — pertumbuhan
    holder % (state engine menyimpan snapshot per mint).
  - **(c) GeckoTerminal OHLCV** — pertumbuhan volume.
  - **TIDAK tersedia gratis:** PumpPortal trade stream (butuh key + wallet
    ≥0,02 SOL), Helius getTokenLargestAccounts (butuh key).
- **Aturan lolos money-flow (terjemahan P1, semangat sama):**
  `buys share h1 ≥ 60%` DAN `volume h1 ≥ 2× volume saat sighting pertama`
  DAN (`holder +5%` sejak sighting pertama, bila snapshot tersedia, ATAU
  `likuiditas +2%` sejak sighting). Ini perubahan pengukuran, dicatat
  sebagai catatan metode — bukan diasumsikan sama dengan kaki Ankr.

## 5. Konfirmasi entry — sama aturannya, sumber Solana

- **Dip 15–30% ATAU breakout + retest, DAN volume ≥2x, DAN holder naik.**
- Data: candle 5-menit GeckoTerminal (OHLCV, via prices.db / live),
  volume DexScreener txns, holder dari snapshot RugCheck.
- Dip diukur dari high 60 menit terakhir; breakout = close di atas high
  60 menit + retest yang bertahan.

## 6. Skor 6 faktor — bobot TETAP, pemetaan Solana

Bobot tidak berubah: contract 25, distribution 25, entry 5, liquidity 20,
money_flow 10, sell_path 15. Ambang: ≥70 (manual) / ≥60 (feed, provisional).

| Faktor (bobot) | BSC (sumber lama) | Solana (sumber baru) |
|---|---|---|
| contract (25) | Binance audit + GoPlus | RugCheck: score_normalised, risks, mint/freeze authority, transferFee, rugged |
| distribution (25) | GoPlus holder + top10 | RugCheck topHolders (top1 ≤25%, top10 ≤60%), creator ≤15%, totalHolders ≥50 |
| entry (5) | Chart BSC | Candle GeckoTerminal 5m (≥12 candle) + dump gates (drop 15m ≤−15% atau dari high 60m ≥30% = block) |
| liquidity (20) | PCS V2 reserve | DexScreener/GT liquidity USD + reserve SOL; LP lock RugCheck `lpLockedPct` ≥50% ATAU lockers non-empty (fallback per-market bila summary = 0, seperti perbaikan M1 14 Nov) |
| money_flow (10) | Ankr inflow / holder+pool kumulatif | §4 (DexScreener buys share + volume growth + holder snapshot) |
| sell_path (15) | Quote PCS + round-trip | Jupiter v1 quote SOL→token (out > 0) DAN jual-balik penuh token→SOL (out > 0). Gagal jual-balik = hard block (pola M1: `sim_sellback_fail`) |

## 7. Exit — aturan TETAP, pemicu Solana

Ladder 50% di 2x, 25% di 4x, trailing 40% → 15% (mengetat saat peak ≥2x,
aktif saat peak ≥+10%), floor break-even di +10%, hard stop −25%, time stop
24 jam. Hold mode (maks 72 jam, maks 10x, jual semua saat ATH) menangguhkan
ladder + time stop, TIDAK menangguhkan gate failure / hard stop / BE floor /
kill-switch.
**"Exit instan bila tax/owner/proxy/LP berubah" → terjemahan Solana:**
mint/freeze authority muncul, `transferFeeConfig` muncul (>0), risiko
RugCheck berubah jadi "danger", `lpLockedPct` runtuh, atau likuiditas
collapse >50%.

## 8. Sizing & drag — bankroll SAMA, satuan SOL

- Bankroll paper **$1.000**, risiko 1% (**$10**)/trade — sama seperti paper
  BSC, supaya ekonomi trial sebanding. Ukuran = min(risiko/jarak stop,
  5% bankroll = $50, 1–2% cadangan pool). Posisi didenominasi SOL pada harga
  entry (harga SOL live dari GeckoTerminal, hanya untuk konversi).
- Drag per trade (dicatat semua): fee pool menurut dex (bonding curve
  pump.fun 1%/sisi; PumpSwap/Raydium AMM 0,25%/sisi — dari `dexId`
  DexScreener), slippage dari `priceImpactPct` quote Jupiter, gas
  0,00001 SOL/leg (model M1). Tax token = 0 bila transferFee 0%
  (gerbang keras); bila >0, trade tidak terjadi.
- **Menang:** `pnl_usd_net` > 0 sesudah SELURUH drag.

## 9. Safety rails — TIDAK BOLEH dilonggarkan

Audit RugCheck (gerbang keras §3), LP lock ≥50%, holder gates (§6),
kill-switch ekuitas < $700 (70% bankroll awal) → tutup semua + berhenti,
maks 3 posisi terbuka, maks 1 entry baru per run, maks deploy 30% bankroll.
Tidak ada trade tanpa gerbang penuh. Tidak ada posisi di atas ukuran.

## 10. Mesin

`~/workspace/solana-trading/m3/m3_engine.py` — satu pass per run:
**universe sighting-first (§10a)** → pair data → audit RugCheck → skor
6 faktor → money-flow (§4) → konfirmasi entry (§5) → entry paper /
sighting → manajemen exit (§7) untuk posisi terbuka → tulis ledger
`~/workspace/solana-trading/m3-ledger.json` (TERPISAH dari `ledger.json` M1)
+ trial JSON tertutup ke `~/workspace/solana-trading/m3/m3-trials/` untuk
`update_scoreboard.py add --method m3-modal-bacot-paper --file <trial.json>`.
Mode `--dry-run` (evaluasi saja, tanpa tulis ledger). Cron 15-menit
`paper-trading-m3-solana-15m` aktif sejak 14 Nov 2026 ~21:22 WIB.

### 10a. Universe sighting-first (method v2, 15 Nov 2026)
Evaluasi ronde 1 (lihat `~/workspace/trading-challenge/
m3-evaluasi-ronde1-2026-11-15.md`) membuktikan sighting hampir tidak
pernah muncul lagi di discovery (ukur 06:03 WIB: 3/35 sighting segar ada
di discovery, 1/40 slot universe) sehingga entry window tidak pernah
diuji — 0 entry dalam ~8,5 jam padahal 67 sighting tercatat. Karena itu
tiap run mengevaluasi **sighting dari state dulu** (umur ≤6 jam, terbaru
dulu, maks 20/run — satu-satunya kandidat yang BISA entry karena punya
baseline), baru discovery fresh sesudahnya (total tetap maks 40/run).
Slot fresh diurutkan prioritas sumber: infra graduated dulu, `jup_recent`
terakhir (token berumur menit, sering belum terindeks DexScreener).
Sighting berumur >6 jam dihapus tiap run (baseline basi melemahkan
money-flow; boleh di-sighting ulang segar). TIDAK ADA gerbang/ambang/
skor yang berubah — hanya cakupan evaluasi. Ronde 1 ditutup
`closed_untested` (0 trial, bukan lolos/gagal); ronde 2 (v2) fresh 0/10.

## 11. Yang TIDAK bisa dilakukan di Solana (jujur)

1. **Narasi X** — tidak ada sumber gratis dari VM yang membaca X (402).
   Diganti metas/boosts/profiles/trending (§1).
2. **Audit Binance + GoPlus** — tidak ada di Solana; hanya RugCheck
   (+ Helius opsional bila user membuat API key gratis).
3. **Trade stream per-token real-time** — PumpPortal butuh key + wallet
   ≥0,02 SOL; diganti DexScreener txns + snapshot holder.
4. **Holder time-series** — tidak ada API gratis; pertumbuhan holder
   diukur dari snapshot berulang (sinyal lambat, butuh ≥2 sighting).
5. **Wallet signals refresh otomatis** — file statis 14 Nov; refresh
   berkala pekerjaan lanjutan.
6. **Token terlalu muda untuk DexScreener** — uji live 14 Nov: 8–12 dari
   20 kandidat discovery tidak punya pair SOL di DexScreener (belum
   terindeks) sehingga tidak bisa dievaluasi money-flow-nya. Ini
   fail-closed yang disengaja (money-flow wajib), bukan bug: kandidat
   seperti itu hanya bisa masuk sesudah terindeks + punya baseline.
