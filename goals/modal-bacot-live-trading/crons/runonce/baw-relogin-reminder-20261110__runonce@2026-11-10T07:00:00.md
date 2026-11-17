---
id: baw-relogin-reminder-20261110
title: Pengingat login ulang baw (sesi kedaluwarsa 08:34)
enabled: true
owner: goal:modal-bacot-live-trading
mode: task
schedule:
  kind: runonce
  timezone: Asia/Jakarta
  at: 2026-11-10T07:00:00
delivery:
  - chat_id: dddf9010-ba6e-4f1b-9b2a-01f53f85e4e2
metadata:
  originating_chat_context_json: '{"chat_id":"dddf9010-ba6e-4f1b-9b2a-01f53f85e4e2","origin_provider":"main","chat_kind":"direct","event_kind":"message","require_mention":false,"device_id":"8be79870-67e5-4541-845f-63fb93d3f6d3"}'
  presentation_locale: id-ID
---
Pengingat satu kali (user setuju 2026-11-09 ~08:15 WIB): sesi baw kedaluwarsa Selasa 2026-11-10 ~08:34 WIB.

Saat run ini jalan (~07:00 WIB):
1. Cek status sesi live (`baw wallet status`).
2. Ingatkan user di chat utama: sesi baw segera kedaluwarsa (~08:34 WIB hari ini), scan QR untuk login ulang sebelum klaim AGC Mode B ~09:24 WIB dan sebelum eksekusi live apa pun. Bila sesi ternyata masih hidup dan kedaluwarsanya jauh dari 08:34, sampaikan apa adanya — tetap ingatkan untuk siap scan QR.
3. JANGAN login ulang sendiri — login butuh QR tap user. Jangan preview/mint/swap/sign apa pun dari job ini. Ini hanya pengingat.
