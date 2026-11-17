---
id: paper-trading-m3-solana-15m
title: Paper trading M3 Solana (simulasi, 15 menit)
enabled: true
owner: goal:modal-bacot-live-trading
mode: task
schedule:
  kind: interval
  timezone: Asia/Jakarta
  at: 2026-11-14T21:38:46
  every: 15m
timeout_secs: 900
delivery:
  - chat_id: dddf9010-ba6e-4f1b-9b2a-01f53f85e4e2
metadata:
  tags: [cron:automatic-interval-anchor]
  originating_chat_context_json: '{"chat_id":"dddf9010-ba6e-4f1b-9b2a-01f53f85e4e2","origin_provider":"main","chat_kind":"direct","event_kind":"message","require_mention":false,"device_id":"8be79870-67e5-4541-845f-63fb93d3f6d3"}'
  presentation_locale: id-ID
---
PAPER TRADING M3 SOLANA — MODAL BACOT di Solana (paper only, uang virtual, TIDAK ADA eksekusi live/trade nyata). Disetujui user 14 Nov 2026 ~21:22 WIB (tap "Ya, pasang cron M3 15 menit"). Ronde 1 challenge fresh 0/10 (trial = trade paper yang TERTUTUP sesudah challenge mulai 14 Nov 20:34 WIB; metode versi Solana di ~/workspace/trading-challenge/m3-modal-bacot-solana-spec.md). Bankroll virtual $1.000, risiko 1% ($10), exit ladder 2x/4x, kill-switch ekuitas < $700. Mesin: ~/workspace/solana-trading/m3/m3_engine.py (ledger TERPISAH dari M1: ~/workspace/solana-trading/m3-ledger.json; state: ~/workspace/solana-trading/m3/m3-state.json).

TIAP RUN:
1. Cek proses: bila `m3_engine.py` sudah berjalan (pgrep), akhiri DIAM tanpa retry.
2. Jalankan `cd ~/workspace/solana-trading/m3 && python3 -u m3_engine.py` (satu siklus: kelola posisi → kill-switch → discovery → evaluasi → entry bila lolos semua gerbang; dry-run pertama 21:17 WIB: 20 kandidat, 0 entry).
3. Baca hasil run: ledger.json (kas, posisi open, trades tertutup) + m3-state.json (sightings).
4. LAPOR ke chat utama HANYA bila ada: entry baru, exit (ladder 2x/4x, stop, kill switch), kill switch aktif, atau alasan blokir BARU yang belum pernah dilaporkan. Sebutkan token (mint address), harga/entry, kas sesudah, dan alasan.
5. Bila tidak ada entry/exit/kill switch/alasan baru: DIAM (jangan kirim laporan rutin tiap run).
6. Bila run gagal (exit bukan 0, timeout, proses macet): catat singkat ke log harian ~/memory/YYYY-MM-DD.md + DIAM ke chat, kecuali gagal 3 run berturut-turut — laporkan sekali.
7. JANGAN pernah: trade live, sign, swap nyata, ubah ambang/gate di script, atau edit MEMORY.md. Observasi singkat ke log harian bila ada entry/exit.
