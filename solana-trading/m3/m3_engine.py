#!/usr/bin/env python3
"""M3 — MODAL BACOT versi Solana (paper). SIMULATION ONLY.

Migrasi metode live Modal Bacot BSC -> Solana atas perintah user 14 Nov 2026
~21:11 WIB. Spesifikasi lengkap:
  ~/workspace/trading-challenge/m3-modal-bacot-solana-spec.md
Parameter challenge: CHALLENGE.md §5.3.

PAPER MURNI: tidak pernah sign, broadcast, memanggil baw, menyentuh
wallet/key, atau swap nyata. Satu-satunya "eksekusi" adalah penulisan
ledger virtual ~/workspace/solana-trading/m3-ledger.json (TERPISAH dari
ledger.json M1).

Identitas vs M1 BACOT DEGEN (tetap berbeda): discovery narasi (DexScreener
metas/boosts/profiles + GeckoTerminal trending + PumpPortal stream + sinyal
wallet tier-ab), skor berbobot 6 faktor (min 60 feed / 70 manual),
money-flow WAJIB (DexScreener buys share + volume growth + snapshot holder
RugCheck), konfirmasi entry dip/breakout, exit ladder 2x/4x.

Sumber data (gratis, tanpa key — semua terverifikasi jalan dari VM 14 Nov):
  - Discovery: DexScreener token-boosts/top+latest, metas/trending,
    token-profiles/latest; GeckoTerminal trending_pools + new_pools;
    infra pools.db (PumpPortal newToken/migrasi) + candidates.json.
  - Pair/harga/volume/txns: DexScreener tokens/v1/solana/{mint}
    (buys/sells m5/h1/h6/h24, liquidity, volume, fdv, pairCreatedAt).
  - Chart: GeckoTerminal OHLCV 5-menit.
  - Audit + holder: RugCheck report/summary (gerbang keras) + GoPlus Solana
    token_security (audit kedua, keyless — terverifikasi jalan 14 Nov;
    klaim lama "GoPlus Solana mati 2022" terbantah). Binance audit tidak
    ada di Solana. Helius DAS TIDAK dipakai (butuh API key signup).
  - Sell path: Jupiter Swap v1 quote (api.jup.ag/swap/v1/quote).
  - Wallet: infra/wallet_signal.py + wallets/wallet-signals.json.

Safety rails (TIDAK BOLEH dilonggarkan): audit RugCheck gerbang keras,
LP lock >= 50%, holder gates, kill-switch ekuitas < $700 (70% bankroll
$1.000), maks 3 posisi terbuka, maks 1 entry baru per run, maks deploy
30% bankroll. Unverified = BLOCK (fail-closed).

Bankroll paper $1.000, risiko 1% ($10)/trade. Drag: fee pool per dex
(bonding pump.fun 1%/sisi; PumpSwap/Raydium/Meteora AMM 0,25%/sisi),
slippage dari priceImpactPct quote Jupiter, gas 0,00001 SOL/leg.
"""
import json
import os
import sqlite3
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

WIB = timezone(timedelta(hours=7))
BASE = os.path.dirname(os.path.abspath(__file__))          # .../solana-trading/m3
SOL_DIR = os.path.dirname(BASE)                            # .../solana-trading
LEDGER_PATH = os.path.join(SOL_DIR, "m3-ledger.json")
STATE_PATH = os.path.join(BASE, "m3-state.json")
TRIALS_DIR = os.path.join(BASE, "m3-trials")
POOLS_DB = os.path.join(SOL_DIR, "infra", "pools.db")
CANDIDATES_PATH = os.path.join(SOL_DIR, "infra", "candidates.json")
WALLET_SIGNALS_PATH = os.path.join(SOL_DIR, "wallets", "wallet-signals.json")

SOL_MINT = "So11111111111111111111111111111111111111112"
GT = "https://api.geckoterminal.com/api/v2"
DS = "https://api.dexscreener.com"
RC = "https://api.rugcheck.xyz/v1/tokens"
GOPLUS = "https://api.gopluslabs.io/api/v1/solana/token_security"
JUP2 = "https://api.jup.ag/tokens/v2"
JUP = "https://api.jup.ag/swap/v1/quote"

BANKROLL_USD = 1000.0
RISK_USD = 10.0
MAX_SIZE_USD = 50.0
KILL_EQUITY_USD = 700.0
MAX_OPEN = 3
MAX_NEW_PER_RUN = 1
MAX_DEPLOY_PCT = 0.30
GAS_SOL_PER_LEG = 0.00001
MIN_SCORE_FEED = 60
MIN_SCORE_MANUAL = 70
HARD_STOP_PCT = 0.25
TIME_STOP_HOURS = 24
HOLD_MODE_MAX_HOURS = 72
MIN_HOLDERS = 50
MAX_TOP1_PCT = 25.0
MAX_TOP10_PCT = 60.0
MAX_CREATOR_PCT = 15.0
MIN_LP_LOCK_PCT = 50.0
MAX_RUGCHECK_SCORE = 30
MIN_CANDLES = 12
UNIVERSE_CAP = 40
# FIX evaluasi ronde 1 (15 Nov 2026, m3-evaluasi-ronde1-2026-11-15.md):
# sighting hampir tidak pernah muncul lagi di discovery (ukur 06:03 WIB:
# 3/35 sighting segar ada di discovery, 1/40 slot universe) sehingga
# entry window tidak pernah diuji. Karena itu sighting (punya baseline)
# dievaluasi DULU tiap run; slot fresh diisi discovery terurut prioritas.
# TIDAK ADA gerbang/ambang/skor yang berubah — hanya cakupan evaluasi.
SIGHTING_TTL_HOURS = 6
MAX_REEVAL_PER_RUN = 20
# prioritas sumber discovery utk slot fresh (0 = pertama): infra graduated
# dulu (punya pair/LP/holder/riwayat), jup_recent terakhir (umur menit,
# sering belum terindeks DexScreener -> no_pair_data).
SOURCE_PRIORITY = {"infra_pools": 0, "infra_funnel": 1, "gt_trending_pools": 1,
                   "gt_new_pools": 1, "ds_boost_top": 2, "ds_boost_latest": 2,
                   "ds_profile_latest": 3, "jup_recent": 4}
POOL_FEE = {"pumpfun": 0.01, "pumpswap": 0.0025, "raydium": 0.0025,
            "meteora": 0.0025, "orca": 0.0025}
DEFAULT_POOL_FEE = 0.0025

UA = {"User-Agent": "m3-solana-paper/1.0 (read-only research)"}


def now_wib():
    return datetime.now(WIB).strftime("%Y-%m-%dT%H:%M:%S+07:00")


def log(msg):
    print(f"[{now_wib()}] {msg}", flush=True)


def http_json(url, timeout=20):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        return {"_http_error": e.code}
    except Exception as e:
        return {"_error": str(e)}


def load_json(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return default


def save_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)
    os.replace(tmp, path)


def prune_sightings(state):
    """Hapus sighting berumur > SIGHTING_TTL_HOURS. Baseline basi
    melemahkan money-flow (vol h1 kini vs vol 8 jam lalu bukan sinyal yang
    sama), dan token yang 6 jam tidak masuk tidak akan masuk. Token yang
    kedaluwarsa boleh di-sighting ulang segar di run berikut. Kembalikan
    jumlah yang dihapus."""
    now = datetime.now(WIB)
    expired = []
    for mint, s in list(state.get("sightings", {}).items()):
        try:
            age = (now - datetime.fromisoformat(s["first_seen_wib"])
                   ).total_seconds() / 3600.0
        except Exception:
            continue
        if age > SIGHTING_TTL_HOURS:
            expired.append(mint)
    for mint in expired:
        del state["sightings"][mint]
    return len(expired)


# ---------------- harga SOL ----------------

def sol_price_usd():
    d = http_json(f"{GT}/simple/networks/solana/token_price/{SOL_MINT}")
    try:
        return float(d["data"]["attributes"]["token_prices"][SOL_MINT])
    except Exception:
        return 75.0


# ---------------- discovery ----------------

def discovery():
    """Kembalikan dict mint -> {pair, symbol, source} dari semua jalur."""
    out = {}

    def add(mint, pair, symbol, source):
        if not mint or mint == SOL_MINT:
            return
        e = out.setdefault(mint, {"pair": pair, "symbol": symbol, "sources": []})
        if pair and not e["pair"]:
            e["pair"] = pair
        if symbol and not e["symbol"]:
            e["symbol"] = symbol
        if source not in e["sources"]:
            e["sources"].append(source)

    # GeckoTerminal trending + new pools
    for kind in ("trending_pools", "new_pools"):
        d = http_json(f"{GT}/networks/solana/{kind}?page=1")
        for p in (d.get("data") or [])[:20]:
            a = p.get("attributes", {})
            rel = p.get("relationships", {})
            bt = (rel.get("base_token", {}).get("data", {}) or {}).get("id", "")
            mint = bt.replace("solana_", "") if bt.startswith("solana_") else ""
            add(mint, a.get("address"), a.get("name", "").split(" / ")[0], f"gt_{kind}")
        time.sleep(0.5)
    # DexScreener boosts top + latest (hanya solana)
    for kind in ("top", "latest"):
        d = http_json(f"{DS}/token-boosts/{kind}/v1")
        if isinstance(d, list):
            for b in d:
                if b.get("chainId") == "solana":
                    add(b.get("tokenAddress"), None, None, f"ds_boost_{kind}")
        time.sleep(0.5)
    # DexScreener token profiles latest (hanya solana)
    d = http_json(f"{DS}/token-profiles/latest/v1")
    if isinstance(d, list):
        for b in d:
            if b.get("chainId") == "solana":
                add(b.get("tokenAddress"), None, None, "ds_profile_latest")
    time.sleep(0.5)
    # DexScreener metas trending (catat saja — narasi yang sedang ramai)
    d = http_json(f"{DS}/metas/trending/v1")
    metas = []
    if isinstance(d, list):
        metas = [(m.get("slug"), m.get("tokenCount")) for m in d[:5]]
    # Jupiter Token API v2 /recent — token berumur menit (sebelum pair
    # DexScreener). Pair dari firstPool bila ada; audit flag Jupiter hanya
    # info (gerbang tetap RugCheck + GoPlus + money-flow DexScreener).
    d = http_json(f"{JUP2}/recent", timeout=25)
    if isinstance(d, list):
        for t in d[:30]:
            fp = t.get("firstPool") or {}
            pair = fp.get("id") if isinstance(fp, dict) else None
            add(t.get("id"), pair, t.get("symbol"), "jup_recent")
    time.sleep(0.5)
    # infra candidates.json (funnel M1 — sumber tambahan, dedupe)
    cand = load_json(CANDIDATES_PATH, {})
    for c in (cand.get("candidates") or [])[:20]:
        add(c.get("mint"), c.get("pair"), None, "infra_funnel")
    # infra pools.db — graduated 6 jam terakhir + ungraduated watch
    try:
        con = sqlite3.connect(f"file:{POOLS_DB}?mode=ro", uri=True, timeout=10)
        rows = con.execute(
            "SELECT mint, pair FROM pools WHERE status IN ('graduated','watch') "
            "ORDER BY last_seen_wib DESC LIMIT 20").fetchall()
        con.close()
        for mint, pair in rows:
            add(mint, pair, None, "infra_pools")
    except Exception as e:
        log(f"pools.db baca gagal: {e}")
    log(f"discovery: {len(out)} mint unik; metas trending: {metas}")
    return out


# ---------------- data pair / audit / chart ----------------

def pair_data(mint):
    """DexScreener tokens/v1 — pilih pair SOL likuiditas terbesar."""
    d = http_json(f"{DS}/tokens/v1/solana/{mint}")
    if not isinstance(d, list):
        return None
    best = None
    for p in d:
        qt = (p.get("quoteToken") or {}).get("symbol")
        if qt != "SOL":
            continue
        liq = (p.get("liquidity") or {}).get("usd") or 0
        if best is None or liq > best["_liq"]:
            p["_liq"] = liq
            best = p
    if best is None:
        return None
    tx = best.get("txns") or {}
    return {
        "pair": best.get("pairAddress"),
        "dex": (best.get("dexId") or "").lower(),
        "price_usd": float(best.get("priceUsd") or 0),
        "liq_usd": float(best.get("liquidity", {}).get("usd") or 0),
        "fdv": float(best.get("fdv") or 0),
        "mcap": float(best.get("marketCap") or 0),
        "vol_h24": float((best.get("volume") or {}).get("h24") or 0),
        "vol_h6": float((best.get("volume") or {}).get("h6") or 0),
        "vol_h1": float((best.get("volume") or {}).get("h1") or 0),
        "txns": tx,
        "created_at": best.get("pairCreatedAt"),
        "symbol": (best.get("baseToken") or {}).get("symbol"),
        "info": best.get("info") or {},
    }


def rugcheck(mint):
    d = http_json(f"{RC}/{mint}/report")
    time.sleep(1.5)  # pola M1: hormati rate limit RugCheck
    if not isinstance(d, dict) or d.get("_error") or d.get("_http_error"):
        return None
    return d


def rugcheck_summary(mint):
    d = http_json(f"{RC}/{mint}/report/summary")
    time.sleep(1.0)
    if not isinstance(d, dict) or d.get("_error") or d.get("_http_error"):
        return None
    return d


def goplus(mint):
    """GoPlus Solana token_security (audit kedua, keyless). Result keyed by mint."""
    d = http_json(f"{GOPLUS}?contract_addresses={mint}", timeout=25)
    time.sleep(0.5)
    if not isinstance(d, dict) or d.get("_error") or d.get("_http_error"):
        return None
    return d


def goplus_gates(d, mint):
    """Gerbang keras audit kedua GoPlus. Fail-closed: code != 1 atau result
    kosong = unverified (blokir); code 2 partial = blokir, bukan lolos.
    Aturan blokir dari field live (BONK + mint M1, 14 Nov): mintable /
    freezable / closable aktif (status "1") atau transfer fee non-empty.
    Kembalikan (lolos, alasan, ringkasan)."""
    if d is None:
        return False, "goplus_unavailable", {}
    if d.get("code") != 1:
        return False, f"goplus_code_{d.get('code')}", {}
    inner = ((d.get("result") or {}).get(mint) or {})
    if not inner:
        return False, "goplus_empty_result", {}
    for field in ("mintable", "freezable", "closable"):
        v = inner.get(field) or {}
        if isinstance(v, dict) and str(v.get("status")) == "1":
            return False, f"goplus_{field}_live", {}
    tf = inner.get("transfer_fee")
    if isinstance(tf, dict) and tf:
        return False, "goplus_transfer_fee", {}
    summ = {"mintable": (inner.get("mintable") or {}).get("status"),
            "freezable": (inner.get("freezable") or {}).get("status"),
            "closable": (inner.get("closable") or {}).get("status"),
            "holder_count": inner.get("holder_count")}
    return True, "ok", summ


def chart_candles(pair, limit=30):
    """GeckoTerminal OHLCV 5-menit -> list close (terurut naik)."""
    d = http_json(
        f"{GT}/networks/solana/pools/{pair}/ohlcv/minute?aggregate=5&limit={limit}")
    try:
        closes = [float(c[4]) for c in d["data"]["attributes"]["ohlcv_list"]]
        return closes
    except Exception:
        return []


def jupiter_quote(input_mint, output_mint, amount_lamports):
    url = (f"{JUP}?inputMint={input_mint}&outputMint={output_mint}"
           f"&amount={amount_lamports}&slippageBps=100")
    d = http_json(url, timeout=25)
    time.sleep(2.0)  # limiter Jupiter lite (dibagi semua komponen)
    if not isinstance(d, dict) or d.get("_error") or d.get("_http_error"):
        return None
    return d


def wallet_score(mint, top_holders, creator):
    """Skor wallet tier-ab (bonus info; 0 bila file/modul tidak ada)."""
    try:
        sys.path.insert(0, os.path.join(SOL_DIR, "infra"))
        import wallet_signal
        sig = wallet_signal.load_signals(WALLET_SIGNALS_PATH)
        return wallet_signal.score_mint(mint, top_holders or [], creator,
                                        signals=sig)
    except Exception:
        return {"score": 0, "matched": [], "blocked": False}


# ---------------- gates & skor ----------------

def audit_gates(rc):
    """Gerbang keras audit RugCheck. Kembalikan (lolos, alasan, ringkasan)."""
    if rc is None:
        return False, "rugcheck_unavailable", {}
    risks = rc.get("risks") or []
    if any((r.get("level") or "").lower() == "danger" for r in risks):
        return False, "rugcheck_danger_risk", {}
    score = rc.get("score_normalised")
    if score is None or score > MAX_RUGCHECK_SCORE:
        return False, f"rugcheck_score_{score}", {}
    tok = rc.get("token") or {}
    if tok.get("mintAuthority") is not None:
        return False, "mint_authority_live", {}
    if tok.get("freezeAuthority") is not None:
        return False, "freeze_authority_live", {}
    ext = rc.get("token_extensions") or {}
    tfc = ext.get("transferFeeConfig")
    if tfc is not None:
        return False, "transfer_fee_present", {}
    if rc.get("rugged"):
        return False, "rugged", {}
    summary = {
        "score_normalised": score,
        "risks": [r.get("name") for r in risks],
        "total_holders": rc.get("totalHolders"),
        "creator": rc.get("creator"),
    }
    return True, "ok", summary


def holder_gates(rc):
    """Gerbang keras distribusi. Kembalikan (lolos, alasan, metrik)."""
    if rc is None:
        return False, "rugcheck_unavailable", {}
    holders = rc.get("totalHolders") or 0
    if holders < MIN_HOLDERS:
        return False, f"holders_{holders}<{MIN_HOLDERS}", {}
    top = rc.get("topHolders") or []
    top1 = float((top[0].get("pct") if top else 0) or 0)
    top10 = float(sum(float(h.get("pct") or 0) for h in top[:10]))
    creator = rc.get("creator")
    creator_pct = 0.0
    for h in top:
        if creator and h.get("owner") == creator:
            creator_pct = float(h.get("pct") or 0)
    if top1 > MAX_TOP1_PCT:
        return False, f"top1_{top1:.1f}>{MAX_TOP1_PCT}", {}
    if top10 > MAX_TOP10_PCT:
        return False, f"top10_{top10:.1f}>{MAX_TOP10_PCT}", {}
    if creator_pct > MAX_CREATOR_PCT:
        return False, f"creator_{creator_pct:.1f}>{MAX_CREATOR_PCT}", {}
    return True, "ok", {"holders": holders, "top1": top1, "top10": top10,
                         "creator_pct": creator_pct,
                         "creator": creator, "top_holders": top}


def lp_gate(rc, summ):
    """LP lock >= 50% ATAU lockers non-empty; fallback per-market bila
    summary = 0 (perbaikan M1 14 Nov)."""
    pct = None
    if summ and summ.get("lpLockedPct") is not None:
        pct = float(summ["lpLockedPct"])
    if pct is not None and pct > 0:
        return (pct >= MIN_LP_LOCK_PCT, pct, "summary")
    # fallback: max lpLockedPct per-market
    markets = (rc or {}).get("markets") or []
    per = [float(m.get("lp", {}).get("lpLockedPct") or 0) for m in markets]
    pct2 = max(per) if per else 0.0
    if pct2 > 0:
        return (pct2 >= MIN_LP_LOCK_PCT, pct2, "per_market")
    lockers = (rc or {}).get("lockers") or {}
    if lockers:
        return True, 100.0, "lockers"
    return False, 0.0, "none"


def score_6(pd, rc, hg, lp_pct, closes, mf, sell_ok, impact_pct):
    """Skor berbobot 6 faktor (0-100 per faktor). Bobot BSC tidak berubah."""
    sub = {}
    # contract (25)
    s = rc.get("score_normalised") or 0
    sub["contract"] = 100 if s <= 10 else (80 if s <= 20 else 60)
    # distribution (25)
    h = hg
    c_h = 100 if h["holders"] >= 500 else (85 if h["holders"] >= 200 else
                                           (70 if h["holders"] >= 100 else 55))
    c_t1 = 100 if h["top1"] <= 10 else (85 if h["top1"] <= 15 else
                                        (70 if h["top1"] <= 20 else 55))
    c_t10 = 100 if h["top10"] <= 30 else (85 if h["top10"] <= 40 else
                                          (70 if h["top10"] <= 50 else 55))
    c_c = 100 if h["creator_pct"] <= 5 else (85 if h["creator_pct"] <= 10 else 70)
    sub["distribution"] = (c_h + c_t1 + c_t10 + c_c) / 4.0
    # entry (5)
    sub["entry"] = 100 if mf.get("pattern") in ("dip", "breakout") else 50
    # liquidity (20)
    liq = pd["liq_usd"]
    c_l = 100 if liq >= 100000 else (85 if liq >= 50000 else
                                     (70 if liq >= 20000 else
                                      (55 if liq >= 10000 else 30)))
    c_lp = 100 if lp_pct >= 90 else (85 if lp_pct >= 75 else 70)
    sub["liquidity"] = 0.6 * c_l + 0.4 * c_lp
    # money_flow (10)
    bs = mf.get("buys_share_h1", 0)
    vg = mf.get("vol_growth", 0)
    hg_g = mf.get("holder_growth", 0)
    c_bs = 100 if bs >= 0.70 else (80 if bs >= 0.60 else (60 if bs >= 0.55 else 0))
    c_vg = 100 if vg >= 3 else (80 if vg >= 2 else (60 if vg >= 1.5 else 0))
    c_hg = 100 if hg_g >= 0.10 else (80 if hg_g >= 0.05 else (60 if hg_g >= 0.02 else 40))
    sub["money_flow"] = (c_bs + c_vg + c_hg) / 3.0
    # sell_path (15)
    if not sell_ok:
        sub["sell_path"] = 0
    elif impact_pct is None:
        sub["sell_path"] = 70
    elif impact_pct <= 5:
        sub["sell_path"] = 100
    elif impact_pct <= 10:
        sub["sell_path"] = 70
    else:
        sub["sell_path"] = 40
    w = {"contract": 25, "distribution": 25, "entry": 5, "liquidity": 20,
         "money_flow": 10, "sell_path": 15}
    total = sum(sub[k] * w[k] for k in w) / 100.0
    return round(total, 1), {k: round(v, 1) for k, v in sub.items()}


def money_flow(pd, rc, baseline):
    """Ukur money-flow vs baseline sighting pertama. Kembalikan dict +
    lolos (aturan §4 spec)."""
    tx = (pd.get("txns") or {}).get("h1") or {}
    buys = float(tx.get("buys") or 0)
    sells = float(tx.get("sells") or 0)
    tot = buys + sells
    bs = (buys / tot) if tot > 0 else 0.0
    vol_h1 = pd["vol_h1"]
    base_vol = (baseline or {}).get("vol_h1_usd") or 0
    vg = (vol_h1 / base_vol) if base_vol and base_vol > 0 else 0.0
    holders = (rc or {}).get("totalHolders") or 0
    base_h = (baseline or {}).get("holders") or 0
    hg = ((holders - base_h) / base_h) if base_h and base_h > 0 else 0.0
    base_liq = (baseline or {}).get("liq_usd") or 0
    liq_g = ((pd["liq_usd"] - base_liq) / base_liq) if base_liq and base_liq > 0 else 0.0
    ok = bs >= 0.60 and vg >= 2.0 and (hg >= 0.05 or liq_g >= 0.02)
    return {"buys_share_h1": round(bs, 3), "buys_h1": buys, "sells_h1": sells,
            "vol_h1_usd": vol_h1, "vol_growth": round(vg, 2),
            "holders": holders, "holder_growth": round(hg, 3),
            "liq_growth": round(liq_g, 3), "ok": ok, "pattern": None}


def entry_pattern(closes):
    """Dip 15-30% dari high 60m ATAU breakout+retest. Kembalikan pola."""
    if len(closes) < MIN_CANDLES:
        return None, "too_few_candles"
    last = closes[-1]
    high60 = max(closes)
    dip = (high60 - last) / high60 if high60 > 0 else 0
    if 0.15 <= dip <= 0.30:
        return "dip", f"dip_{dip:.0%}"
    prev_high = max(closes[:-3]) if len(closes) > 3 else high60
    if last > prev_high and closes[-2] <= prev_high * 1.02:
        return "breakout", "breakout_retest"
    if dip < 0.15:
        return None, f"dip_too_small_{dip:.0%}"
    return None, f"dip_too_deep_{dip:.0%}"


# ---------------- ledger / state ----------------

def init_ledger():
    return {"bankroll_start_usd": BANKROLL_USD, "cash_usd": BANKROLL_USD,
            "positions": [], "trades": [], "created_wib": now_wib(),
            "kill_switch": False}


def settle_exit(led, pos, exit_price_usd, reason, sol_usd, frac):
    """Jual `frac` dari ukuran AWAL posisi pada harga exit. Kembalikan
    (proceeds_usd_net, fees_usd)."""
    dex = pos.get("dex") or ""
    fee_rate = POOL_FEE.get(dex, DEFAULT_POOL_FEE)
    gross = pos["size_usd"] * frac * (exit_price_usd / pos["entry_price_usd"])
    fee = gross * fee_rate
    slip = gross * pos.get("slippage_pct", 0.005)
    gas = GAS_SOL_PER_LEG * sol_usd
    net = gross - fee - slip - gas
    pos["realized_usd"] = pos.get("realized_usd", 0.0) + net
    pos["fees_usd"] = pos.get("fees_usd", 0.0) + fee + slip + gas
    # FIX AUDIT BUG-3: lacak komponen drag exit terpisah (untuk breakdown nyata).
    pos["exit_fee_usd"] = pos.get("exit_fee_usd", 0.0) + fee
    pos["exit_slip_usd"] = pos.get("exit_slip_usd", 0.0) + slip
    pos["exit_gas_usd"] = pos.get("exit_gas_usd", 0.0) + gas
    pos["sold_frac"] = pos.get("sold_frac", 0.0) + frac
    led["cash_usd"] = round(led["cash_usd"] + net, 4)
    return net, fee + slip + gas


def finalize_trade(led, pos, reason):
    pos["status"] = "closed"
    pos["exit_reason"] = reason
    pos["exit_time"] = now_wib()
    # FIX AUDIT BUG-3: pnl = realized - size - entry_drag. Sebelumnya
    # entry drag (fee+slip+gas saat masuk) tidak dipotong — pnl dilaporkan
    # terlalu tinggi persis sebesar entry drag (mis. entry $40 @2x:
    # +$38,9993 dilaporkan vs +$38,4986 kas nyata). Breakdown kini angka
    # nyata dari komponen yang dilacak, bukan hardcoded 0.0.
    entry_drag = pos.get("entry_drag_usd", 0.0)
    pnl = round(pos.get("realized_usd", 0.0) - pos["size_usd"] - entry_drag, 4)
    trade = {
        "token": pos["mint"], "symbol": pos.get("symbol"), "pair": pos["pair"],
        "status": "closed", "entry_time": pos["entry_time"],
        "entry_usd": pos["size_usd"],
        "entry_price_usd": pos["entry_price_usd"],
        "exit_time": pos["exit_time"], "exit_reason": reason,
        "pnl_usd_net": pnl,
        "pnl_breakdown": {
            "fees_usd": round(pos.get("entry_fee_usd", 0.0)
                              + pos.get("exit_fee_usd", 0.0), 4),
            "gas_usd": round(pos.get("entry_gas_usd", 0.0)
                             + pos.get("exit_gas_usd", 0.0), 4),
            "slippage_usd": round(pos.get("entry_slip_usd", 0.0)
                                  + pos.get("exit_slip_usd", 0.0), 4),
            "entry_drag_usd": round(entry_drag, 4)},
        "gates": pos.get("gates", {}), "discovery": pos.get("discovery", ""),
        "score": pos.get("score"),
    }
    led["trades"].append(trade)
    led["positions"] = [p for p in led["positions"] if p is not pos]
    # trial JSON untuk update_scoreboard.py add
    trial = dict(trade)
    trial["trial_id"] = f"m3-{pos['mint'][:12]}-{pos['exit_time']}"
    trial["win"] = pnl > 0
    with open(os.path.join(TRIALS_DIR, trial["trial_id"] + ".json"), "w") as f:
        json.dump(trial, f, indent=1)
    log(f"CLOSED {pos.get('symbol')} {reason} pnl_net=${pnl}")
    return trade


def manage_position(led, pos, sol_usd, dry_run):
    """Cek aturan exit untuk satu posisi terbuka. Kembalikan True bila
    posisi tertutup penuh."""
    pd = pair_data(pos["mint"])
    if pd is None or not pd["price_usd"]:
        log(f"exit {pos.get('symbol')}: harga tak terbaca, lewati")
        return False
    price = pd["price_usd"]
    mult = price / pos["entry_price_usd"]
    pos["peak_mult"] = max(pos.get("peak_mult", 1.0), mult)
    age_h = ((datetime.now(WIB) - datetime.fromisoformat(pos["entry_time"]))
             .total_seconds() / 3600.0)
    rem = 1.0 - pos.get("sold_frac", 0.0)
    if rem <= 0:
        return True
    # exit instan: otoritas/fee/LP berubah (cek RugCheck ulang)
    rc = rugcheck(pos["mint"])
    if rc is not None:
        tok = rc.get("token") or {}
        ext = rc.get("token_extensions") or {}
        bad = (tok.get("mintAuthority") is not None or
               tok.get("freezeAuthority") is not None or
               ext.get("transferFeeConfig") is not None or
               any((r.get("level") or "").lower() == "danger"
                   for r in (rc.get("risks") or [])))
        if bad:
            if not dry_run:
                settle_exit(led, pos, price, "instant_gate_fail", sol_usd, rem)
                finalize_trade(led, pos, "instant_gate_fail")
            return True
    # hold mode: sesudah 4x, sisa menunggangi trailing 15% / maks 72 jam
    hold = pos.get("peak_mult", 1.0) >= 4.0
    if hold and age_h >= HOLD_MODE_MAX_HOURS:
        if not dry_run:
            settle_exit(led, pos, price, "hold_mode_72h", sol_usd, rem)
            finalize_trade(led, pos, "hold_mode_72h")
        return True
    if hold:
        trail = 0.15
        if price <= pos["peak_mult"] * pos["entry_price_usd"] * (1 - trail):
            if not dry_run:
                settle_exit(led, pos, price, "trailing_hold", sol_usd, rem)
                finalize_trade(led, pos, "trailing_hold")
            return True
        return False
    # ladder
    if mult >= 2.0 and not pos.get("sold_2x"):
        if not dry_run:
            settle_exit(led, pos, price, "ladder_2x", sol_usd, 0.50)
        pos["sold_2x"] = True
        rem -= 0.50
    if mult >= 4.0 and not pos.get("sold_4x"):
        if not dry_run:
            settle_exit(led, pos, price, "ladder_4x", sol_usd, 0.25)
        pos["sold_4x"] = True
        rem -= 0.25
    if rem <= 0:
        if not dry_run:
            finalize_trade(led, pos, "ladder_complete")
        return True
    # trailing 40% -> 15% (15% saat peak >= 2x)
    if pos.get("peak_mult", 1.0) >= 1.10:
        trail = 0.15 if pos["peak_mult"] >= 2.0 else 0.40
        if price <= pos["peak_mult"] * pos["entry_price_usd"] * (1 - trail):
            if not dry_run:
                settle_exit(led, pos, price, "trailing", sol_usd, rem)
                finalize_trade(led, pos, "trailing")
            return True
    # floor break-even +10%
    if pos.get("peak_mult", 1.0) >= 1.10 and mult <= 1.0:
        if not dry_run:
            settle_exit(led, pos, price, "break_even_floor", sol_usd, rem)
            finalize_trade(led, pos, "break_even_floor")
        return True
    # hard stop -25%
    if mult <= (1 - HARD_STOP_PCT):
        if not dry_run:
            settle_exit(led, pos, price, "hard_stop_-25%", sol_usd, rem)
            finalize_trade(led, pos, "hard_stop_-25%")
        return True
    # time stop 24 jam
    if age_h >= TIME_STOP_HOURS:
        if not dry_run:
            settle_exit(led, pos, price, "time_stop_24h", sol_usd, rem)
            finalize_trade(led, pos, "time_stop_24h")
        return True
    # likuiditas collapse >50% vs entry
    if pd["liq_usd"] < pos.get("entry_liq_usd", pd["liq_usd"]) * 0.5:
        if not dry_run:
            settle_exit(led, pos, price, "liq_collapse", sol_usd, rem)
            finalize_trade(led, pos, "liq_collapse")
        return True
    return False


# ---------------- run utama ----------------

def evaluate_candidate(mint, info, state, sol_usd, dry_run):
    """Satu kandidat: pair data -> audit -> holder -> LP -> chart ->
    money-flow -> skor -> sell path -> entry. Kembalikan dict hasil."""
    res = {"mint": mint, "symbol": info.get("symbol"),
           "sources": info.get("sources", []), "pair": info.get("pair")}
    pd = pair_data(mint)
    if pd is None or not pd["price_usd"]:
        res["skip"] = "no_pair_data"
        return res
    res.update({"pair": pd["pair"], "dex": pd["dex"], "price_usd": pd["price_usd"],
                "liq_usd": pd["liq_usd"], "fdv": pd["fdv"],
                "vol_h1": pd["vol_h1"]})
    rc = rugcheck(mint)
    ok, why, summ = audit_gates(rc)
    if not ok:
        res["skip"] = f"audit_{why}"
        return res
    ok, why, hg = holder_gates(rc)
    if not ok:
        res["skip"] = f"holder_{why}"
        return res
    summ_rc = rugcheck_summary(mint)
    lp_ok, lp_pct, lp_src = lp_gate(rc, summ_rc)
    if not lp_ok:
        res["skip"] = f"lp_lock_{lp_pct:.1f}%<{MIN_LP_LOCK_PCT}%"
        return res
    res["lp_pct"] = lp_pct
    res["lp_source"] = lp_src
    # Audit kedua GoPlus (method fix 14 Nov): hanya untuk kandidat yang
    # sudah lolos semua gerbang RugCheck.
    gp = goplus(mint)
    gok, gwhy, gsumm = goplus_gates(gp, mint)
    res["goplus"] = gsumm
    if not gok:
        res["skip"] = f"audit_goplus_{gwhy}"
        return res
    res["holders"] = hg["holders"]
    res["top1"] = hg["top1"]
    res["top10"] = hg["top10"]
    # chart
    closes = chart_candles(pd["pair"])
    if len(closes) < MIN_CANDLES:
        res["skip"] = f"chart_{len(closes)}_candles<12"
        return res
    pattern, pat_why = entry_pattern(closes)
    res["pattern"] = pattern
    res["pattern_detail"] = pat_why
    # money-flow vs baseline sighting
    baseline = state.get("sightings", {}).get(mint)
    mf = money_flow(pd, rc, baseline)
    mf["pattern"] = pattern
    res["money_flow"] = mf
    # skor (sell path dicek sesudah skor kasar — quote hanya bila skor cukup)
    score, sub = score_6(pd, rc, hg, lp_pct, closes, mf, True, None)
    res["score_pre"] = score
    res["subscores"] = sub
    if score < MIN_SCORE_FEED:
        res["skip"] = f"score_{score}<{MIN_SCORE_FEED}"
        return res
    # wallet tier-ab (bonus info, bukan gate)
    ws = wallet_score(mint, hg.get("top_holders"), hg.get("creator"))
    res["wallet"] = ws
    if ws.get("blocked"):
        res["skip"] = "wallet_blocked_factory"
        return res
    # sell path: Jupiter beli + jual-balik penuh
    size_sol = 0.01  # probe kecil untuk quote (bukan ukuran posisi)
    amount_lamports = int(size_sol * 1_000_000_000)
    q_buy = jupiter_quote(SOL_MINT, mint, amount_lamports)
    buy_ok = bool(q_buy and q_buy.get("outAmount"))
    impact = None
    sell_ok = False
    if buy_ok:
        try:
            impact = float(q_buy.get("priceImpactPct") or 0)
        except Exception:
            impact = None
        out_amt = int(q_buy["outAmount"])
        q_sell = jupiter_quote(mint, SOL_MINT, out_amt)
        sell_ok = bool(q_sell and q_sell.get("outAmount"))
    res["sell_path_ok"] = bool(buy_ok and sell_ok)
    res["price_impact_pct"] = impact
    if not (buy_ok and sell_ok):
        res["skip"] = "sell_path_fail"
        return res
    score, sub = score_6(pd, rc, hg, lp_pct, closes, mf, True, impact)
    res["score"] = score
    res["subscores"] = sub
    if score < MIN_SCORE_FEED:
        res["skip"] = f"score_{score}<{MIN_SCORE_FEED}"
        return res
    # money-flow gate + entry confirmation
    if not mf["ok"]:
        res["skip"] = "money_flow_fail"
        return res
    if pattern is None:
        res["skip"] = f"entry_pattern_{pat_why}"
        return res
    # volume >= 2x vs sighting pertama (bagian dari konfirmasi entry)
    if baseline is not None:
        base_vol = baseline.get("vol_h1_usd") or 0
        if base_vol and pd["vol_h1"] < 2 * base_vol:
            res["skip"] = "entry_vol_lt_2x"
            return res
        # FIX AUDIT BUG-2: baseline.get("holders") bisa None (key ada,
        # nilai None) -> TypeError. Pakai `or 0` (defensif).
        if hg["holders"] <= (baseline.get("holders") or 0):
            res["skip"] = "entry_holders_not_rising"
            return res
    res["pass"] = True
    res["slippage_pct"] = (impact / 100.0) if impact is not None else 0.005
    return res


def run(dry_run=False):
    log(f"M3-Solana run dimulai (dry_run={dry_run})")
    sol_usd = sol_price_usd()
    log(f"SOL=${sol_usd:.2f}")
    led = load_json(LEDGER_PATH, None) or init_ledger()
    state = load_json(STATE_PATH, {"sightings": {}})
    state.setdefault("sightings", {})
    if dry_run:
        log("DRY-RUN: tidak ada tulis ledger/state")
    # 1. kelola posisi terbuka dulu
    for pos in list(led.get("positions", [])):
        try:
            manage_position(led, pos, sol_usd, dry_run)
        except Exception as e:
            log(f"exit {pos.get('symbol')} error: {e}")
    # 2. kill-switch
    equity = led["cash_usd"]
    for pos in led.get("positions", []):
        pd = pair_data(pos["mint"])
        if pd and pd["price_usd"]:
            equity += pos.get("size_usd", 0) * (1 - pos.get("sold_frac", 0)) \
                * (pd["price_usd"] / pos["entry_price_usd"])
    log(f"ekuitas paper ${equity:.2f} (kas ${led['cash_usd']:.2f})")
    if equity < KILL_EQUITY_USD and led.get("positions"):
        log("KILL-SWITCH: ekuitas < $700 — tutup semua posisi")
        for pos in list(led.get("positions", [])):
            pd = pair_data(pos["mint"])
            if pd and pd["price_usd"] and not dry_run:
                settle_exit(led, pos, pd["price_usd"], "kill_switch",
                            sol_usd, 1.0 - pos.get("sold_frac", 0.0))
                finalize_trade(led, pos, "kill_switch")
        led["kill_switch"] = True
        if not dry_run:
            save_json(LEDGER_PATH, led)
        return
    if led.get("kill_switch"):
        log("kill-switch AKTIF — tidak ada entry baru")
        return
    # 3. discovery + universe sighting-first (FIX evaluasi ronde 1,
    #    15 Nov 2026 — lihat m3-evaluasi-ronde1-2026-11-15.md). Sighting
    #    (satu-satunya kandidat yang BISA entry karena punya baseline)
    #    dievaluasi dulu tiap run; slot fresh diisi discovery terurut
    #    prioritas sumber (infra graduated dulu, jup_recent terakhir).
    expired = prune_sightings(state)
    if expired:
        log(f"sighting kedaluwarsa (> {SIGHTING_TTL_HOURS} jam): "
            f"{expired} dihapus")
    sight_sorted = sorted(state["sightings"].items(),
                          key=lambda kv: kv[1].get("first_seen_wib", ""),
                          reverse=True)[:MAX_REEVAL_PER_RUN]
    disc = discovery()
    seen = {m for m, _ in sight_sorted}
    fresh = []

    def _prio(info):
        srcs = info.get("sources", []) or []
        return min((SOURCE_PRIORITY.get(s, 5) for s in srcs), default=5)

    for mint, info in sorted(disc.items(), key=lambda kv: _prio(kv[1])):
        if mint in seen:
            continue
        fresh.append((mint, info))
        if len(sight_sorted) + len(fresh) >= UNIVERSE_CAP:
            break
    universe = [(m, {"pair": s.get("pair"), "symbol": s.get("symbol"),
                     "sources": ["sighting"]}) for m, s in sight_sorted] + fresh
    log(f"universe: {len(universe)} kandidat "
        f"(reevaluasi sighting {len(sight_sorted)}, fresh {len(fresh)})")
    open_mints = {p["mint"] for p in led.get("positions", [])}
    entries = 0
    evaluated = []
    n_reeval = 0
    n_new_sight = 0
    for mint, info in universe:
        if mint in open_mints:
            continue
        if entries >= MAX_NEW_PER_RUN:
            break
        if len(led.get("positions", [])) + entries >= MAX_OPEN:
            break
        baseline = state["sightings"].get(mint)
        if baseline is not None:
            n_reeval += 1
        try:
            res = evaluate_candidate(mint, info, state, sol_usd, dry_run)
        except Exception as e:
            log(f"eval {mint[:8]} error: {e}")
            continue
        evaluated.append(res)
        # FIX AUDIT BUG-2: sighting HANYA bila holders terisi. Sebelumnya
        # sighting dicatat bila price_usd ada meski gerbang audit/holder
        # gagal -> holders=None -> baseline beku selamanya (konfirmasi
        # entry TypeError diam-diam). Bila baseline lama holders-nya None,
        # refresh saat evaluasi kini punya holders.
        if baseline is not None and baseline.get("holders") is None \
                and res.get("holders") is not None and not dry_run:
            baseline.update({"holders": res.get("holders"),
                             "liq_usd": res.get("liq_usd"),
                             "vol_h1_usd": res.get("vol_h1"),
                             "price_usd": res.get("price_usd")})
            log(f"SIGHTING-REFRESH {res.get('symbol') or mint[:8]}: "
                f"baseline holders terisi {res.get('holders')}")
        # sighting pertama: catat baseline, tidak entry
        if baseline is None:
            if (res.get("price_usd") is not None
                    and res.get("holders") is not None and not dry_run):
                n_new_sight += 1
                state["sightings"][mint] = {
                    "first_seen_wib": now_wib(),
                    "holders": res.get("holders"),
                    "liq_usd": res.get("liq_usd"),
                    "vol_h1_usd": res.get("vol_h1"),
                    "price_usd": res.get("price_usd"),
                    "pair": res.get("pair"),
                    "symbol": res.get("symbol"),
                    "discovery": ",".join(res.get("sources", [])),
                }
            log(f"SIGHTING {res.get('symbol') or mint[:8]} "
                f"score_pre={res.get('score_pre')} skip={res.get('skip')}")
            continue
        if not res.get("pass"):
            log(f"SKIP {res.get('symbol') or mint[:8]}: {res.get('skip')}")
            continue
        # ENTRY (paper)
        stop_dist = HARD_STOP_PCT
        size_usd = min(RISK_USD / stop_dist, MAX_SIZE_USD,
                       0.02 * res["liq_usd"])
        size_usd = round(size_usd, 2)
        if size_usd < 5:
            log(f"SKIP {res.get('symbol')}: ukuran ${size_usd} < $5")
            continue
        if led["cash_usd"] < size_usd:
            log("SKIP entry: kas tidak cukup")
            continue
        # deploy cap 30%
        deployed = sum(p.get("size_usd", 0) * (1 - p.get("sold_frac", 0))
                       for p in led.get("positions", []))
        if deployed + size_usd > MAX_DEPLOY_PCT * BANKROLL_USD:
            log("SKIP entry: deploy cap 30%")
            continue
        fee_rate = POOL_FEE.get(res.get("dex", ""), DEFAULT_POOL_FEE)
        entry_fee = size_usd * fee_rate
        slip_cost = size_usd * res.get("slippage_pct", 0.005)
        gas_cost = GAS_SOL_PER_LEG * sol_usd
        pos = {
            "mint": mint, "pair": res["pair"], "symbol": res.get("symbol"),
            "dex": res.get("dex"), "entry_time": now_wib(),
            "entry_price_usd": res["price_usd"],
            "entry_liq_usd": res["liq_usd"],
            "size_usd": size_usd,
            "tokens": size_usd / res["price_usd"],
            "peak_mult": 1.0, "sold_frac": 0.0, "sold_2x": False,
            "sold_4x": False, "realized_usd": 0.0, "fees_usd": 0.0,
            "slippage_pct": res.get("slippage_pct", 0.005),
            "score": res.get("score"), "subscores": res.get("subscores"),
            "gates": {"audit_rugcheck": True, "score": res.get("score"),
                      "money_flow": True, "entry_confirmation": True},
            "discovery": ",".join(res.get("sources", [])),
            "status": "open",
        }
        if not dry_run:
            led["cash_usd"] = round(led["cash_usd"] - size_usd - entry_fee
                                    - slip_cost - gas_cost, 4)
            pos["fees_usd"] = round(entry_fee + slip_cost + gas_cost, 4)
            # FIX AUDIT BUG-3: entry drag + komponen (untuk pnl bersih).
            pos["entry_drag_usd"] = round(entry_fee + slip_cost + gas_cost, 4)
            pos["entry_fee_usd"] = round(entry_fee, 4)
            pos["entry_slip_usd"] = round(slip_cost, 4)
            pos["entry_gas_usd"] = round(gas_cost, 4)
            led["positions"].append(pos)
        log(f"ENTRY {res.get('symbol')} ${size_usd} @ ${res['price_usd']:.8f} "
            f"skor={res.get('score')} mf={res.get('money_flow')} "
            f"pattern={res.get('pattern')}")
        entries += 1
    if not dry_run:
        save_json(LEDGER_PATH, led)
        save_json(STATE_PATH, state)
    log(f"run selesai: {len(evaluated)} dievaluasi "
        f"(reevaluasi {n_reeval}, sighting baru {n_new_sight}), "
        f"{entries} entry baru, "
        f"posisi open {len(led.get('positions', []))}, kas ${led['cash_usd']:.2f}")
    # ringkas alasan skip terbanyak
    from collections import Counter
    skips = Counter(r.get("skip", "pass") for r in evaluated)
    log(f"alasan skip: {dict(skips)}")


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    run(dry_run=dry)
