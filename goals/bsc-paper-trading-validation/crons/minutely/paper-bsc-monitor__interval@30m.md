---
id: paper-bsc-monitor
title: Monitor validasi paper BSC
enabled: false
owner: goal:bsc-paper-trading-validation
mode: task
schedule:
  kind: interval
  timezone: Asia/Jakarta
  at: 2026-10-31T16:23:09
  every: 30m
delivery:
  - chat_id: dddf9010-ba6e-4f1b-9b2a-01f53f85e4e2
metadata:
  tags: [cron:automatic-interval-anchor]
  originating_chat_context_json: '{"chat_id":"dddf9010-ba6e-4f1b-9b2a-01f53f85e4e2","origin_provider":"main","chat_kind":"direct","event_kind":"message","require_mention":false,"device_id":"8be79870-67e5-4541-845f-63fb93d3f6d3"}'
  presentation_locale: id-ID
---
Monitor validasi paper BSC — PAPER ONLY, READ-ONLY. Otorisasi user 2026-10-31 ~15:47 WIB (fase paper dimulai) dan ~15:52 WIB (monitor tiap 30 menit, via tap).

ATURAN FASE (baca dulu tiap run): ~/workspace/ponyin-tools/paper-bsc-rules.md
LEDGER: ~/workspace/ponyin-tools/paper-bsc-trades.json
SKRIP: ~/workspace/ponyin-tools/paper_bsc.py (perintah stats dan add)
LOG SCREENING: ~/workspace/ponyin-tools/paper-bsc-screen-YYYY-MM-DD.md

TIAP RUN:
1. Baca stats ledger (paper_bsc.py stats). Catat progres: trade tertutup/100, hari berjalan/30.
2. POSISI PAPER TERBUKA: untuk tiap posisi open, ambil harga segar (DexScreener/GMGN/quote on-chain dari cadangan pair; jangan pakai harga basi). Terapkan exit sesuai aturan: ladder 50% di 2x, 25% di 4x, trailing 40% -> 15%, floor break-even di +10%, hard stop -25%, time stop 24 jam sejak entry, exit instan bila tax/owner/proxy/LP berubah (baca ulang parameter kontrak bila memungkinkan). Bila trigger kena: tutup sebagian/seluruh sesuai ladder, hitung PnL BERSIH (fee pool + tax kontrak + gas estimasi $0,05/trade + slippage), perbarui ledger menjadi closed dengan pnl_usd_net dan daftar exits. Bila harga tak terbaca, biarkan posisi terbuka dan coba lagi run berikut; jangan tutup paksa.
3. SCREENING KANDIDAT BARU: feed graduation (four.meme, Genius.fun, Flap.sh — Flap read-only saja, jangan connect/sign; bila Flap terlihat mencurigakan lagi, lewati), DexScreener BSC new pairs/trending, dan sinyal baru dari ~/workspace/narrative-pulse/state.json yang sudah dikonfirmasi aliran uang. Untuk tiap kandidat: verifikasi CA on-chain (name/symbol cocok). JANGAN paper-enter token yang CA-nya tidak terverifikasi — snapshot tanpa CA dilewati dengan alasan, bukan entry (pelajaran screening #1). Gerbang penuh: Sourcify, otoritas retained (mint/pause/blacklist/proxy admin), tax dari parameter kontrak (bukan quote), LP burn/lock, pool >= 50 BNB, konsentrasi, buy sim, konfirmasi entry (dip 15-30% atau breakout + retest dengan volume dan holder naik). HANYA bila SEMUA lolos: paper-enter dengan ukuran aturan (risiko 1% dari bankroll paper $1.000, cap 5% bankroll + 1-2% cadangan pool), catat entry price dari quote segar, stop/targets, bukti gerbang, dan timestamp. Token yang sudah ditolak dengan alasan decisive (BIBIAI: minter retained; RIKI: source tak terverifikasi + pool 4,62 WBNB + cerita dibantah CZ; VRQQ: identitas tak terverifikasi) TIDAK di-enter ulang tanpa bukti baru yang terverifikasi.
4. LAPORAN: DIAM bila tidak ada entry baru, exit baru, atau kriteria promosi terpenuhi. Laporkan bila: paper entry baru (token, CA, entry price, size, stop/targets, bukti gerbang singkat), posisi paper tertutup (PnL bersih + stats berjalan), atau kriteria promosi terpenuhi (>= 100 tertutup + >= 30 hari + expectancy bersih > 0 + profit factor > 1,5). Jangan pernah laporkan token sebagai ajakan beli.

GUARD (mengikat, tanpa kecuali): PAPER ONLY — jangan pernah menyentuh wallet, preview, transaksi, approval, swap, sign, atau connect wallet dari run ini. Jangan pernah mengarang harga, CA, atau hasil gerbang. Bila data kunci tak terbaca, catat dan lanjutkan; jangan memaksa entry. Tulis catatan run singkat ke ~/memory/YYYY-MM-DD.md (bukan ke MEMORY.md).
