---
id: slime-today-watch
title: Slime.today Flap launch watch
enabled: false
owner: goal:narrative-pulse-watch
mode: task
schedule:
  kind: interval
  timezone: Asia/Jakarta
  at: 2026-11-06T20:48:33
  every: 30m
delivery:
  - chat_id: dddf9010-ba6e-4f1b-9b2a-01f53f85e4e2
metadata:
  tags: [cron:automatic-interval-anchor]
  originating_chat_context_json: '{"chat_id":"dddf9010-ba6e-4f1b-9b2a-01f53f85e4e2","origin_provider":"main","chat_kind":"direct","event_kind":"message","require_mention":false,"device_id":"8be79870-67e5-4541-845f-63fb93d3f6d3"}'
  presentation_locale: id-ID
---
SLIME.TODAY FLAP LAUNCH WATCH — READ-ONLY, laporan hanya bila ada launch BARU yang LULUS (graduated), dengan TANDA WARNA gate.

Sumber: API JSON publik slime.today (tanpa login/akun), terminal data Flap Pool Launch BSC. BUKAN situs proyek token SLIME — token SLIME tidak ada di data ini, jangan pernah laporkan token SLIME dari sumber ini.

TIAP RUN (30 menit):
1. Jalankan: python3 ~/workspace/narrative-pulse/slime-today-pull.py
   Skrip menarik /api/launches?chain=56 (cursor pagination, semua launch), /api/stats, /api/saltlocks; menyimpan snapshot ke ~/workspace/narrative-pulse/slime-today/latest.json dan membandingkan dengan previous.json (baseline run sebelumnya). Skrip sudah menerapkan STAGE A (filter data, lihat bawah) dan mencetak baris 🟢 PASS / 🔴 STAGEA-REJECT untuk tiap launch baru.
2. Baca output skrip + latest.json. Yang dihitung BARU = token yang TIDAK ada di previous.json.

STAGE A — filter data (dikerjakan skrip, ambang dari gerbang MODAL BACOT / BACOT DEGEN yang sudah dikenal; diuji 2026-11-06: 5 dari 69 launch lulus):
- graduated=1, isTest=0.
- mcap_usd $3.000–$1.000.000 (bawah ≈ floor kelulusan, atas = batas wajar; mcap absurd seperti TEST ~$1,6T otomatis gugur).
- pool_value_usd ≥ $10.000 (≈ POOL_MIN_BNB 14,5).
- pool_value_usd / mcap_usd ≥ 2% (LIQ_MCAP_MIN).
- tax_buy_bps ≤ 200 dan tax_sell_bps ≤ 200 (TAX_MAX 2%).
- Creator dengan ≥3 launch dan 0 lulus (launcherStats) = pola launcher mencurigakan, gugur.
- Aturan OG nama sama: bila ada ≥2 token bersimbol sama, hanya yang paling awal (ts terkecil) yang lolos; sisanya copy, gugur.
- Gagal Stage A = 🔴 TIDAK MEMENUHI (lihat TANDA WARNA).

STAGE B — verifikasi (worker, HANYA untuk yang lolos Stage A — jumlahnya sedikit, ~1 per jam):
- B1 GoPlus (skill goplus-security / API publik): honeypot = gagal 🔴; tax on-chain tidak cocok / >2% = gagal 🔴; blacklist / pausable / selfdestruct / ownerChangeBalance / canTakeBackOwnership = gagal 🔴; mintable / hidden-owner / proxy = 🟡 catatan (bukan gagal keras).
- B2 Audit Binance (skill query-token-audit): hit RISK spesifik (isHit + riskType RISK) atau riskAlert non-null = gagal 🔴; hasResult=false = 🟡 catatan (tanpa hasil, BUKAN lolos).
- B3 LP on-chain: dead-burn ≥50% ATAU lock kontrak (mis. PinkLock) + tidak ada wallet bebas >5% LP — bila tidak ada keduanya = gagal 🔴.
- B4 Holder: holder ≥50 bila terbaca; top wallet bebas >5% = gagal 🔴; data holder tidak terbaca = 🟡 catatan.
- B5 Money-flow — DIUKUR SEGAR TIAP RUN, jangan pakai log basi (perbaikan 2026-11-06 ~20:24 WIB atas catatan user: standar money-flow sulit dipenuhi bila sumbernya tidak rutin di-update): ambil DexScreener pair PCS token itu (https://api.dexscreener.com/latest/dex/tokens/<CA>, pilih pair pancakeswap): money-flow TERKONFIRMASI bila buys > sells pada h1 DAN h6 (net-buy dua jendela). Bila DexScreener tidak terbaca, pakai pertumbuhan holder Ankr (holder naik vs run sebelumnya dan tidak ada wallet bebas >5% baru). Bila buys ≤ sells di h1/h6 → money-flow TIDAK terkonfirmasi = 🟡 catatan ("alert saja", bukan priority). JANGAN pakai wallet-watchlist (masih kosong) atau log tier-ab (login-gated sejak run 50, basi) sebagai sumber money-flow job ini — keduanya tidak rutin ter-update dan itulah yang membuat standar ini sulit dipenuhi.

TANDA WARNA — klasifikasi akhir tiap launch baru yang lulus:
- 🟢 BERSIH: lolos Stage A + semua Stage B tanpa catatan. Kandidat discovery terkuat.
- 🟡 LULUS SEBAGIAN: lolos Stage A + lolos semua hard gate Stage B, tapi ada ≥1 catatan 🟡 (audit tanpa hasil, mintable/hidden-owner/proxy, holder tidak terbaca, money-flow belum terkonfirmasi). Dilaporkan dengan catatan kekurangannya ditulis jelas.
- 🔴 TIDAK MEMENUHI: gagal Stage A, ATAU gagal satu hard gate Stage B (honeypot, RISK, LP tidak burn/lock, top holder >5%, tax >2%).

PELAPORAN ke chat utama:
- Laporkan 🟢 dan 🟡 saja, sekali per launch, dengan tanda warnanya di depan + simbol, alamat kontrak, mcap, pool, floor, pajak, creator, dan untuk 🟡: daftar catatan yang kurang. Bila ada beberapa dalam satu run, laporkan semuanya sekali dalam satu pesan.
- 🔴 TIDAK dilaporkan ke chat — hanya dicatat di log harian ~/memory/YYYY-MM-DD.md + state (sesuai pilihan user: laporkan yang lulus saja).
- DIAM bila: tidak ada launch baru, tidak ada yang 🟢/🟡, atau hanya perubahan mcap/harga launch lama.
- Bila fetch gagal: catat di log harian + diam (jangan laporkan kegagalan satu run ke chat; run berikutnya mencoba lagi).

ATURAN LAPORAN: laporan ini discovery saja — BUKAN rekomendasi beli, BUKAN sinyal trade, dan TIDAK pernah memicu eksekusi. Launch 🟢/🟡 tetap harus lolos seluruh gerbang screening MODAL BACOT sebelum jadi kandidat, dan otomasi live tetap tidak dipersenjatai dari job ini. Jangan ubah MEMORY.md dari run ini. State/snapshot hanya di ~/workspace/narrative-pulse/slime-today/.
