---
id: baw-hyperevm-support-watch
title: Cek berkala dukungan baw untuk HyperEVM (999)
enabled: false
owner: goal:modal-bacot-live-trading
mode: task
schedule:
  kind: daily
  timezone: '@user.current'
  time: 09:37:00
delivery:
  - chat_id: dddf9010-ba6e-4f1b-9b2a-01f53f85e4e2
metadata:
  tags: [cron:flexible-time]
  originating_chat_context_json: '{"chat_id":"dddf9010-ba6e-4f1b-9b2a-01f53f85e4e2","origin_provider":"main","chat_kind":"direct","event_kind":"message","require_mention":false,"device_id":"8be79870-67e5-4541-845f-63fb93d3f6d3"}'
  presentation_locale: id-ID
---
CEK BERKALA DUKUNGAN BAW UNTUK HYPEREVM (chain 999) — disetujui user 2026-11-08 ~08:55 WIB (tap "Ya, cek berkala apakah baw sudah support HyperEVM"). READ-ONLY TOTAL: tidak pernah sign, preview tx nyata, kirim, swap, bridge, connect wallet, atau export private key.

KONTEKS: HYPE 0,0698936191466399 milik wallet agent 0xeb237F6f9FB4e826739F0954e9768914F28b2c2E terkunci di HyperEVM (chain 999) sejak bridge Relay BSC→HyperEVM 2026-11-08 07:29 WIB. Jalan pulang (HyperEVM→BNB BSC) mentok karena baw tidak mendukung chain 999: `baw wallet chains` 2026-11-08 ~08:56 WIB hanya mengembalikan 7 chain (8453 Base, 56 BSC, 1 Ethereum, 137 Polygon, 4663 Robinhood, CT_501 Solana, 42161 Arbitrum) — TANPA 999 dan tanpa 99901. Wallet agent juga tidak bisa dioperasikan manual dari aplikasi Binance (user 2026-11-08 ~08:54 WIB), dan WalletConnect manual gagal. Export private key darurat TIDAK PERNAH dipakai (irreversible, mematikan baw).

TIAP RUN (harian):
1. Jalankan `~/workspace/.baw-cli/bin/baw wallet chains --json` dan periksa apakah `binanceChainId` "999" muncul di daftar.
2. Verifikasi saldo HYPE wallet agent tetap utuh via RPC HyperEVM https://rpc.hyperliquid.xyz/evm (eth_getBalance 0xeb237F6f9FB4e826739F0954e9768914F28b2c2E, bandingkan dengan 0,0698936191466399; hex acuan 0xf84fe0554d4a21).
3. Catat hasil di ~/workspace/goals/modal-bacot-live-trading/hidden_files/baw-hyperevm-support-state.json (tanggal run, daftar chain, 999 ada/tidak, saldo HYPE, sudah-dilaporkan-atau-belum).

LAPOR KE CHAT UTAMA HANYA BILA:
- Chain 999 MUNCUL di `baw wallet chains` (dukungan baru) — laporkan SEKALI (dedupe via state file), dengan isi: baw kini mendukung HyperEVM, saldo HYPE terverifikasi, dan bahwa langkah bridge pulang tetap butuh keputusan user (rute + jumlah) — JANGAN mengeksekusi bridge apa pun di run ini.
- Saldo HYPE BERUBAH/BERKURANG tanpa perintah user — laporkan sekali sebagai anomali.
SELAIN ITU DIAM (run rutin tanpa perubahan tidak menghasilkan laporan). Bila `baw wallet chains` gagal (mis. sesi baw kedaluwarsa) tulis "tidak terverifikasi", JANGAN laporkan sebagai "belum support" dan JANGAN coba re-login (butuh QR tap user). Bila dukungan 999 sudah dilaporkan sekali, run berikutnya tetap diam sampai user memerintahkan lain atau menonaktifkan job ini.
