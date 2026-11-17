---
id: holder-candidate-watch
title: Pemantau kandidat holder early-call
enabled: true
owner: goal:early-call-wallet-data-collection
mode: task
schedule:
  kind: interval
  timezone: Asia/Jakarta
  at: 2026-10-31T20:30:43
  every: 2h
delivery:
  - chat_id: dddf9010-ba6e-4f1b-9b2a-01f53f85e4e2
metadata:
  tags: [cron:automatic-interval-anchor]
  originating_chat_context_json: '{"chat_id":"dddf9010-ba6e-4f1b-9b2a-01f53f85e4e2","origin_provider":"main","chat_kind":"direct","event_kind":"message","require_mention":false,"device_id":"8be79870-67e5-4541-845f-63fb93d3f6d3"}'
  presentation_locale: id-ID
---
Pemantau berkala kandidat holder early-call — READ-ONLY, tanpa koneksi wallet, tanpa signing, tanpa pembelian, tanpa follow/copy-trade. Otorisasi pengguna 2026-10-31 ~18:29 WIB ("Ya, buatkan pemantau berkala untuk kandidat"). Zona waktu Asia/Jakarta. Bahasa laporan: Bahasa Indonesia.

TUJUAN UTAMA (koreksi pengguna 2026-10-31 ~18:35 WIB — ini yang paling penting): dompet-dompet yang dikumpulkan BUKAN tentang koin-koin lama itu sendiri. Dompet-dompet ini adalah KOMPAS ARAH UANG: sinyal yang dicari adalah ke token baru mana uang mereka masuk lebih awal — ke mana arah uang tertuju. Koin-koin lama (MSX, COOL, ok, 旺财) hanyalah jejak yang membuktikan dompet-dompet itu pernah masuk lebih awal; status hold pada koin lama BUKAN produk pemantauan ini.

HASIL RUN BUKAN LAPORAN RUTIN UNTUK PENGGUNA (instruksi 2026-10-31 ~18:32 WIB): hasil run adalah bahan analisis internal Muse untuk melanjutkan proyek — pengumpulan wallet early buyer sebagai pertimbangan analisis eksekusi trading memecoin (fase paper; otomasi live TIDAK dipersenjatai). Karena itu run ini SENYAP ke chat kecuali satu pengecualian di bawah.

MODE B — AKTIF SEJAK 2026-10-31 ~20:31 WIB (login GMGN terverifikasi 20:23–20:31 WIB via jalur email, sesi bertahan melalui pemuatan halaman wallet verifikasi; diaktifkan atas perintah pengguna "Holder monitor modeb lanjutkan" + "Coba login GMGN lagi"):
Fokus run adalah aktivitas dompet, bukan hold koin lama:
1. Selesaikan dulu alamat lengkap kandidat dari halaman token (GMGN menampilkan alamat lengkap lewat tautan saat login) — dompet yang alamat lengkapnya belum terverifikasi tidak bisa diikuti dan tetap dicatat sebagai belum bisa diikuti.
2. Untuk tiap dompet terpantau beralamat lengkap (prioritas: 0x8e966a9f17beab1ea50039434c2a14ad9e09b8d6 dan kandidat lain yang alamat lengkapnya sudah terverifikasi), baca halaman aktivitas dompetnya dan catat setiap PEMBELIAN AWAL BARU: dompet, CA token baru (hanya bila terverifikasi on-chain/GMGN), waktu beli pertama, ukuran beli, dan — bila dapat diverifikasi — apakah beli itu mendahului lonjakan sosial token tersebut.
3. Catat tiap temuan sebagai "money-flow signal" di log + state: arah uang = token-token baru yang dimasuki lebih awal oleh dompet-dompet terpantau, beserta dompet mana dan kapan. Inilah produk pemantauan ini.
4. Sinyal arah uang adalah lapisan DISCOVERY untuk screening paper, bukan rekomendasi beli dan bukan bukti: satu dompet membeli tidak melewati gerbang screening; kandidat paper dari sinyal ini tetap harus lolos seluruh gerbang + konfirmasi money-flow + konfirmasi entry. Data GMGN adalah agregat (data sekunder), bukan bukti on-chain mentah — nyatakan itu di log bila relevan.
5. CATATAN RAPUH SESI: sesi GMGN di browser ini pernah hilang dua kali pada 2026-10-31 (logout ~19:34 WIB setelah login 19:05–19:17 WIB). Bila suatu run mendapati halaman wallet login-gated, catat sebagai login-gated dan lanjut — jangan pernah mencoba login sendiri, dan jangan klaim sinyal arah uang dari run itu; run berikutnya yang login tersedia kembali melanjutkan Mode B.

MODE A — TIDAK LAGI AKTIF (riwayat, dipakai 2026-10-31 sampai login tersedia): selama login belum tersedia, run hanya membaca halaman token GMGN BSC berikut sebagai sinyal kesehatan interim (apakah dompet masih aktif/bertahan), dan log WAJIB menyebutnya interim, bukan sinyal arah uang:
1. MSX 0x23214ccbffb6ef479da64d1842b10b5525997777 — kandidat aktif: 0x52...708a, 0xca...1ad8, 0xd3...8727, 0x93...1a52.
2. COOL 0x21aeddf21ee854f20cb497b0430437c4ab367777 — kandidat aktif: 0xcc...4d0d.
3. ok 0xc853d8253f0d8346ca80f3f6af53e49a763e7777 — kandidat aktif: 0x8e...b8d6. Kandidat DROPPED (habis terjual per 2026-10-31 ~18:25 WIB): 0xa9...165f, 0x43...f622, 0x75...0488, 0x60...0ee3 — tetap dilirik bila muncul kembali sebagai pemegang (re-entry), catat di log bila terjadi.
4. 旺财 0x9d01d9ca91703b881dc0e585c6b746085b8f7777 — kaki kedua kandidat 0x8e...b8d6: periksa apakah bentuk 0x8e...b8d6 masih memegang di sana.
Jangan pernah mengklaim di log bahwa cek interim ini menunjukkan arah uang. Arah uang TIDAK DAPAT dihasilkan tanpa login — nyatakan batas ini apa adanya.

BASELINE TERAKHIR (cek 2026-10-31 ~18:13–18:25 WIB, tanpa login, MODE A):
- MSX: 0x52...708a 49,7% tersisa ($324,6); 0xca...1ad8 ~37,5% ($118,3); 0xd3...8727 100% ($134,4, tag Sniper tampil); 0x93...1a52 ~75% ($167,3, tag Sniper tampil).
- COOL: 0xcc...4d0d 32,4% tersisa ($1,659).
- ok: 0x8e...b8d6 100% tersisa ($3,92).
- 旺财: 0x8e...b8d6 100% ($6,646, beli $4,091) — terakhir terverifikasi batch 6, 2026-10-31 ~17:43 WIB, BELUM dicek ulang tanpa login.

TIAP RUN (berlaku untuk Mode B sekarang, Mode A sebagai riwayat):
1. Baca sumber yang sesuai modenya lewat browser (GMGN, BSC). Bila suatu halaman menuntut login padahal mode menuntutnya, catat sebagai login-gated dan lanjut — jangan pernah mencoba login sendiri.
2. Bandingkan dengan baseline di state file ~/workspace/narrative-pulse/holder-watch-state.json (buat bila belum ada; simpan % tersisa + nilai + tag per kandidat + streak tidak terbaca; di Mode B tambahkan daftar money-flow signal: dompet, CA token baru, waktu, ukuran). Perbarui state setiap run.
3. Tambahkan satu entri log ringkas ke ~/workspace/narrative-pulse/holder-watchlist.md setiap run (tanggal/waktu, perubahan saja bila ada; bila tidak ada perubahan, satu baris "tidak ada perubahan"). Di Mode A, tiap entri wajib memuat satu baris implikasi analisis interim (kandidat mana yang menguat/melemah sebagai sinyal early-call) dengan label jelas bahwa itu BUKAN sinyal arah uang. Di Mode B, tiap entri memuat sinyal arah uang yang ditemukan (atau "tidak ada pembelian awal baru").

METODOLOGI (wajib diingat tiap run): tanpa login, GMGN hanya merender ~100 baris pemegang teratas, terurut menurun berdasarkan nilai. Ketidakhadiran kandidat di 100 baris itu berarti habis terjual/keluar HANYA bila posisi kandidat cukup besar untuk berada di baris atas (posisi puluhan dolar saat ini akan berada di baris ~15–30); nyatakan batas ini di log bila mencatat kandidat hilang. Alamat terpotong TIDAK PERNAH dikonfirmasi sebagai wallet identik antar token — catat selalu sebagai kecocokan bentuk terpotong. Jangan pernah menaikkan status kandidat menjadi "tepercaya" atau mempromosikannya ke wallet-watchlist: promosi butuh pola ≥3 token + PnL terealisasi 30 hari + keputusan pengguna.

ATURAN PELAPORAN: JANGAN kirim laporan rutin ke chat. Semua temuan (termasuk money-flow signal di Mode B) HANYA dicatat di log + state, untuk analisis internal. SATU-SATUNYA pengecualian: bila sebuah dompet memenuhi SELURUH kriteria promosi (pola ≥3 token terverifikasi + PnL terealisasi 30 hari terverifikasi), laporkan SEKALI ke chat karena promosi butuh keputusan pengguna — itu bukan laporan rutin. Bila halaman tidak terbaca 4 run berturut-turut, catat di log/state saja dan terus pantau (jangan nonaktifkan cron, jangan laporkan ke chat).

LARANGAN: jangan login sendiri, jangan koneksi wallet, jangan sign, jangan beli/jual/follow, jangan mengubah MEMORY.md (observasi cukup di holder-watchlist.md + state file + log harian bila ada).
