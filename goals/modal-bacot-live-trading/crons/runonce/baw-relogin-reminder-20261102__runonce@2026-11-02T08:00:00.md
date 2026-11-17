---
id: baw-relogin-reminder-20261102
title: Pengingat re-login wallet Modal Bacot 2026-11-02 08:00
enabled: true
owner: goal:modal-bacot-live-trading
mode: task
schedule:
  kind: runonce
  timezone: Asia/Jakarta
  at: 2026-11-02T08:00:00
delivery:
  - chat_id: dddf9010-ba6e-4f1b-9b2a-01f53f85e4e2
metadata:
  originating_chat_context_json: '{"origin_provider":"main","chat_kind":"direct","event_kind":"message","require_mention":false}'
  presentation_locale: id-ID
---
Pengingat satu kali re-login wallet Binance untuk Modal Bacot — BACA-SAJA, tanpa trade, tanpa login, tanpa signing. Dibuat 2026-11-01 malam karena pengingat 2026-11-02 08:00 WIB yang dijanjikan di chat 2026-11-01 ~18:03 WIB ternyata TIDAK ada dalam daftar cron live (daftar dicek 2026-11-01 ~18:30 WIB; watchdog trading-continuity-watch hanya melapor SETELAH sesi gagal, bukan pengingat pra-kedaluwarsa).

Langkah:
1. Baca live `~/workspace/.baw-cli/bin/baw wallet status --json`. JANGAN mengutip tanggal kedaluwarsa dari catatan lama — sesi bersifat activity-rolled, jadi hanya angka live yang berlaku.
2. Bila status CONNECTED dan sessionExpireTime live masih dalam ~36 jam ke depan (sekitar 2026-11-03): kirim SATU pengingat ke chat utama dalam Bahasa Indonesia: sesi wallet Modal Bacot akan kedaluwarsa sekitar tanggal live tersebut, re-login hanya bisa lewat tap QR user di aplikasi Binance, dan bila kedaluwarsa maka entry live berhenti sementara pemantauan baca-saja tetap jalan. Sebut tanggal live yang terbaca, bukan tanggal lama.
3. Bila sesi sudah diperbarui (expiry live sudah bergeser jauh melewati 2026-11-03) ATAU status sudah tidak CONNECTED: DIAM — tidak ada laporan. Kasus tidak CONNECTED adalah ranah watchdog per jam, bukan tugas ini.
4. Tugas ini satu kali saja; selesai setelah run ini, apa pun hasilnya.
