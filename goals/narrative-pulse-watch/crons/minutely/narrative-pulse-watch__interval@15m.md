---
id: narrative-pulse-watch
title: Pemantau narasi memecoin BSC
enabled: false
owner: goal:narrative-pulse-watch
mode: task
schedule:
  kind: interval
  timezone: Asia/Jakarta
  at: 2026-10-31T15:29:58
  every: 15m
timeout_secs: 900
delivery:
  - chat_id: dddf9010-ba6e-4f1b-9b2a-01f53f85e4e2
metadata:
  tags: [cron:automatic-interval-anchor]
  originating_chat_context_json: '{"chat_id":"dddf9010-ba6e-4f1b-9b2a-01f53f85e4e2","origin_provider":"main","chat_kind":"direct","event_kind":"message","require_mention":false,"device_id":"8be79870-67e5-4541-845f-63fb93d3f6d3"}'
  presentation_locale: id-ID
---
Pemantau narasi memecoin BSC — READ-ONLY, laporan hanya bila ada sinyal awal baru. Otorisasi pengguna 2026-10-31 ~15:14 WIB (tap "Ya, aktifkan pemantau narasi berkala"). PERLUASAN disetujui pengguna 2026-10-31 ~20:33 WIB ("Sekarang lanjutkan perluas pemantauan narasi"): lapisan KOL + lapisan wallet ditambahkan di bawah, tanpa mengubah aturan diam, jendela, atau larangan. PERBAIKAN DISCOVERY disetujui pengguna 2026-11-01 ~08:52 WIB ("Setujui semua perbaikan discovery"): fast layer + browser dipangkas di bawah; gerbang keras, ambang skor, dan aturan diam TIDAK berubah.

FAST LAYER (baru, tiap run, didahulukan):
- Jalankan dulu `python3 ~/workspace/narrative-pulse/fast_discovery.py` (read-only, API GeckoTerminal BSC new_pools 3 halaman, ~3 detik, tanpa browser). Hasilnya hanya snapshot first-seen di `~/workspace/narrative-pulse/fast_discovery_state.json`.
- Token dari fast layer BUKAN sinyal, BUKAN kandidat, dan BUKAN rekomendasi dengan sendirinya. Ia baru menjadi reported_signal bila JUGA muncul di sumber narasi, di log holder Mode B, atau di sinyal tier-ab dalam jendela yang sama — aturan konvergensi multi-sumber tetap berlaku.

X SEARCH (baru, disetujui pengguna 2026-11-01 ~11:46 WIB, tap "Ya, sambungkan X search ke narasi"):
- Setelah fast layer, jalankan `python3 ~/workspace/narrative-pulse/x_narrative.py` (read-only, API twitterapi.io via konektor custom.twitterapi yang sudah terhubung dan teruji live; kunci tidak pernah ditampilkan atau dicatat).
- Skrip ini HANYA memeriksa token fast layer yang pertama kali terlihat dalam 30 menit terakhir dan belum pernah diperiksa, maksimal 2 token per run (urutan volume h24 tertinggi), 1 halaman search per token (query = alamat kontrak persis, bukan nama/simbol, agar tidak tertukar token bersimbol sama).
- Anggaran dipaksakan skrip sendiri: cap harian 3.000 kredit (~200 tweet/hari); bila cap tercapai skrip berhenti tanpa memanggil API. Jangan mengakali cap, jangan menambah token per run, jangan mengikuti cursor ke halaman berikut.
- Hasil skrip adalah SATU sumber narasi: X-HIT (minimal 2 penulis berbeda menyebut CA dalam 24 jam terakhir) + fast layer = reported_signal menurut aturan konvergensi multi-sumber yang sudah ada, klasifikasi "alert saja" kecuali money-flow terkonfirmasi lewat jalur yang sudah ada. X-MISS bukan sinyal dan bukan penolakan — catat saja di state.
- X search TIDAK PERNAH mengonfirmasi money-flow, TIDAK mengubah gerbang keras, skor, second-sighting, sizing, atau aturan diam, dan TIDAK PERNAH memicu trade. Bila skrip gagal (X-ERROR, kunci bermasalah, cap tercapai), catat "X search tidak tersedia" dan lanjutkan dengan sumber lain; jangan pernah mengarang hasil discussion.
- Bukti per token tersimpan di ~/workspace/narrative-pulse/x_narrative_state.json (CA, jumlah tweet, penulis, URL tweet terbaru, estimasi kredit).

TIAP RUN, periksa sumber narasi (baca-saja, tanpa login, tanpa connect wallet, tanpa tanda tangan) — DAFTAR DIPANGKAS agar run selesai dalam batas waktu:
- WAJIB tiap run: BlockBeats flash, feed graduation launchpad BSC (four.meme, Genius.fun — token yang baru graduate + holder growth-nya).
- OPSIONAL bila waktu tersisa: PANews Meme Daily, Odaily headlines, Sharpe.ai BNB meme narrative tracker, GMGN BSC trending (1h/6h) tampilan publik, DexScreener BSC trending/new pairs.
- DICOPOT dari sumber wajib: Jinse flash (buta 11 run berturut-turut; laporan butanya sudah pernah disampaikan sekali, jangan laporkan ulang kecuali ia pulih lalu buta lagi).
- Binance Square (tagar #bsc, #bnbmeme, #memeseason, #中文meme, Meme Rush rank) HANYA dipakai sebagai deep-check bila sudah ada kandidat dari fast layer / sumber wajib — bukan dibuka tiap run, karena tab ini pernah macet di persetujuan akses.
- Bila browser belum selesai menjelang batas waktu run, laporkan run sebagai tidak lengkap dan lanjutkan ke run berikutnya; jangan pernah mengklaim "tidak ada sinyal" dari run yang tidak selesai.

CARI SINYAL "AKAN RAMAI" (sinyal awal) — cirinya kecepatan, bukan besaran:
- Mention/velocity NAIK dari basis rendah, BUKAN sudah besar.
- Konvergensi multi-sumber dalam jendela singkat (muncul di >=2 sumber independen).
- Spillover China -> Inggris (muncul dulu di kanal China, belum di media Inggris).
- Disebut pertama kali oleh KOL berekan jejak, atau akumulasi smart-money / pertumbuhan holder MENDAHULUI lonjakan sosial.
- Graduation launchpad yang bersamaan dengan mention awal.

BEDAKAN DARI "SUDAH RAMAI" (jangan laporkan sebagai peluang entry):
perhatian puncak, posisi atas trending list, semua orang membicarakan,
harga sudah berlipat — itu zona distribusi. Bila menemukannya, cukup
catat sebagai distribution watch, bukan sinyal entry.

LAPISAN KOL — REFERENSI TAMBAHAN SAJA (aturan di ~/workspace/narrative-pulse/kol-ledger.md, berlaku sejak perluasan 2026-10-31):
- KOL adalah referensi tambahan, BUKAN lapisan discovery utama dan BUKAN penentu trade. Seruan KOL tidak pernah membuat kandidat sendiri, tidak pernah mengesampingkan gerbang keras, dan tidak menambah skor di luar faktor narasi yang sudah ada.
- Tiap run, bila sumber narasi menampilkan seruan KOL atas sebuah token/narasi, catat seruan itu di kol-ledger.md dengan: handle + platform, tanggal + jam seruan (WIB + UTC), token + CA HANYA bila CA sudah diverifikasi on-chain (nama/simbol cocok; CA dari sosial saja tidak pernah dicatat sebagai fakta), harga saat disebut, harga +24 jam dan +7 hari (diisi pada run berikutnya bila tersedia), pengungkapan berbayar / tidak berbayar / tidak diketahui, dan pemeriksaan pre-buy: apakah wallet yang terhubung dengan KOL membeli >30 menit sebelum seruan (ya / tidak / tidak terverifikasi — bila tidak dapat diverifikasi, tulis tidak terverifikasi, jangan menebak).
- Ledger dimulai KOSONG dan tetap kosong sampai seruan pertama tercatat dan terukur di sini — jangan pernah mengisi nama dari ingatan atau daftar vendor.
- Status "terpercaya" HANYA bila SEMUA terpenuhi: minimal 20 seruan terdokumentasi, hit rate terukur (harga +7 hari > harga saat disebut) yang dicatat bukan diklaim, NOL flag front-running, NOL bukti promosi berbayar yang tidak diungkapkan. Satu bukti front-running atau promosi berbayar tak diungkap = langsung dicopot dari status terpercaya, tetap tercatat sebagai flagged. Sampai syarat terpenuhi, statusnya "belum terverifikasi".
- Posisi KOL terhadap uang menentukan makna seruan: KOL membeli sebelum uang masuk = pemeriksaan front-running; KOL menyerukan setelah harga naik = sinyal telat, distribution watch saja, bukan sinyal awal.

LAPISAN WALLET — DISCOVERY SEJAJAR NARASI (aturan di ~/workspace/narrative-pulse/wallet-watchlist.md, berlaku sejak perluasan 2026-10-31):
- Tracking wallet adalah lapisan PENTING yang sejajar dengan narasi, bukan sekadar referensi. Sinyal wallet menemukan kandidat; gerbang keras yang memutuskan trade. Sinyal wallet tidak pernah mengesampingkan gerbang, tidak pernah menjadi pemicu trade sendiri, dan tidak pernah menggantikan verifikasi kontrak, tax, LP, atau konsentrasi.
- Tiap run, silangkan setiap kandidat narasi dengan DUA sumber wallet: (1) wallet-watchlist.md, dan (2) log money-flow signal pemantau holder Mode B (~/workspace/narrative-pulse/holder-watchlist.md). Bila kandidat yang sama dibeli lebih awal oleh wallet terpantau, naikkan klasifikasinya dari alert menjadi priority watchlist untuk gerbang penuh — tetap BUKAN rekomendasi beli.
- Prinsip money-flow (user 2026-10-31): narasi tanpa konfirmasi money-flow = alert saja, TIDAK PERNAH priority; narasi + money-flow = priority watchlist untuk gerbang penuh; volume mentah saja BUKAN konfirmasi (mudah dipalsukan lewat wash trading) — yang dihitung adalah akumulasi wallet terpantau, pertumbuhan holder nyata, dan inflow likuiditas.
- Sinyal satu wallet saja = alert saja, sama seperti sinyal satu sumber di lapisan narasi. Pembelian klaster (beberapa wallet terpantau membeli token baru yang sama dalam jendela singkat) lebih kuat daripada satu wallet, tetapi tetap discovery, bukan bukti.
- Penilaian di level KLASTER, bukan alamat tunggal: satu smart wallet hampir selalu mengendalikan banyak alamat (utama, fresh/satelit, akumulasi, distribusi). Keterkaitan KUAT = sumber pendanaan bersama, transfer langsung, atau pendanaan berantai; LEMAH = hanya co-buy tanpa koroborasi lain, dicatat sebagai "kemungkinan klaster", bukan fakta. Wallet fresh/satelit adalah sinyal LEBIH LEMAH (kemungkinan bundle), dicatat terpisah, tidak disamakan dengan wallet terpantau. On-chain menunjukkan APA dan KAPAN, bukan NIAT — jangan pernah menulis "terbukti insider".
- Daftar wallet-watchlist dimulai KOSONG dan tetap kosong sampai wallet pertama terukur di sini (profit terealisasi minimal 30 hari dari riwayat on-chain, minimal 10 trade terealisasi, perilaku holding tercatat, verifikasi ulang tiap bulan) — jangan pernah mengisi alamat dari daftar vendor atau ingatan. Karena itu, sampai ada wallet terpantau yang terverifikasi, lapisan ini TIDAK DAPAT mengonfirmasi money-flow; nyatakan itu apa adanya di state, jangan mengklaim konfirmasi yang tidak ada.
- Cron narasi ini TIDAK PERNAH login ke GMGN sendiri dan tidak mencoba login: konfirmasi wallet diambil dari log holder Mode B dan tampilan publik saja. Bila log holder login-gated atau basi, catat sebagai tidak terverifikasi dan lanjut — jangan memaksa konfirmasi.

ATURAN LAPORAN (diperbarui perluasan 2026-10-31, sisanya tidak berubah):
- DIAM bila tidak ada sinyal awal baru. Satu sinyal dilaporkan SEKALI
  saja, lalu dicatat di state file agar tidak diulang.
- Laporan sinyal berisi: nama token/narasi, kontrak BILA terverifikasi
  on-chain keberadaannya (jangan pernah percaya CA dari sosial saja),
  sumber + stempel waktu tiap sumber, indikator leading mana yang kena,
  KLASIFIKASI eksplisit: "alert saja" (narasi tanpa money-flow, atau
  seruan KOL belum terverifikasi saja) vs "priority watchlist"
  (narasi + money-flow terkonfirmasi wallet terpantau), STATUS KOL
  (belum terverifikasi / terpercaya / flagged / tidak ada), STATUS
  KONFIRMASI WALLET (terkonfirmasi wallet terpantau / satu wallet
  saja / tidak ada / tidak terverifikasi), dan penegasan eksplisit:
  gerbang keamanan BELUM dijalankan dan ini BUKAN rekomendasi beli.
- Narasi tidak pernah mengesampingkan gerbang keras. Monitor ini
  HANYA memberi makan pipeline screening; trade apa pun tetap butuh
  pipeline gerbang penuh; otomasi trading kini dipersenjatai dalam
  scope BSC wallet utama yang dikonfirmasi 2026-10-31 ~22:24 WIB
  (rubrik skor + funding BNB dikonfirmasi 2026-11-01 ~00:17 WIB);
  monitor ini sendiri tetap READ-ONLY dan tidak pernah mengeksekusi.
- Bila sumber kunci tidak terbaca 4 run berturut-turut, laporkan SEKALI
  sumber mana yang buta, lalu terus pantau.
- JANGAN PERNAH: mint, preview, eksekusi, approve, swap, sign, atau
  connect wallet dari run ini. JANGAN laporkan token sebagai ajakan beli.

STATE: ~/workspace/narrative-pulse/state.json (sinyal yang sudah
dilaporkan + stempel waktunya; sejak perluasan, tiap sinyal juga
mencatat status KOL dan status konfirmasi wallet-nya; buat folder bila perlu). Catatan run
singkat boleh ditambahkan ke log harian ~/memory/YYYY-MM-DD.md.

MANDAT ENTRI RUN (persetujuan pengguna 2026-11-02 ~06:47 WIB, tap "Ya, wajibkan entri run lengkap"): SETIAP run WAJIB menambahkan satu entri run lengkap ke daftar `runs` di ~/workspace/narrative-pulse/state.json, apa pun hasilnya — run lengkap, cek ringan, run tidak lengkap, run diam, maupun run yang gagal di tengah jalan. Entri memuat sekurang-kurangnya: stempel waktu run (WIB), jenis run (pulse penuh / cek ringan), sumber yang diperiksa, sumber yang dilewati + alasannya, hasil (sinyal baru / tidak ada sinyal / tidak lengkap / gagal + penyebabnya), dan kredit X yang dipakai bila X search berjalan. Penulisan entri run TIDAK BOLEH menghapus atau mengubah `reported_signals` maupun entri runs yang sudah ada; bila state.json tidak bisa dibaca, jangan menimpa dari kosong — laporkan kegagalan penulisan itu di laporan run. Entri run bukan laporan chat: aturan diam tetap berlaku — run diam tetap dicatat di `runs` tapi tidak mengirim pesan chat.

Ledger KOL: ~/workspace/narrative-pulse/kol-ledger.md.
Daftar wallet: ~/workspace/narrative-pulse/wallet-watchlist.md.
Log holder Mode B: ~/workspace/narrative-pulse/holder-watchlist.md.
Snapshot fast layer: ~/workspace/narrative-pulse/fast_discovery_state.json.
Bukti X search: ~/workspace/narrative-pulse/x_narrative_state.json.

JENDELA: run tiap 15 menit. Pulse PENUH di jendela alert
07:00-13:00 WIB dan 18:00-22:00 WIB (00:00-06:00 dan 11:00-15:00 UTC);
di luar jendela itu cukup cek ringan (BlockBeats flash + event
graduation) dan tetap diam kecuali sinyal multi-sumber yang kuat.
