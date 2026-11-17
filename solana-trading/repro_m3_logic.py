#!/usr/bin/env python3
"""Repro logika M3 (murni / monkeypatch, tanpa network, tanpa tulis ledger nyata).

A. score_6: matematika bobot 25/25/5/20/10/15 + ambang.
B. money_flow: fail-closed bila baseline kosong / vol 0 / holder None.
C. evaluate_candidate: TypeError bila baseline holders=None (SEMUA sighting
   saat ini holders=None) — vs kontrol holders=500 yang lolos.
D. PnL: drag entry (fee+slippage+gas) tidak masuk pnl_usd_net.
E. Kill-switch: tidak latch bila ekuitas <$700 tanpa posisi terbuka.
F. entry_pattern: jendela high = 30 candle 5m (~150 mnt), bukan 60 mnt;
   syarat "retest" breakout lemah.
"""
import json, os, sys
sys.path.insert(0, "/home/hatch/workspace/solana-trading/m3")
import m3_engine as m3

fails = []

def check(name, cond, detail=""):
    print(f"[{'PASS' if cond else 'FAIL'}] {name} {detail}")
    if not cond:
        fails.append(name)

# ---------------- A. skor ----------------
pd = {"liq_usd": 50000, "price_usd": 1e-5, "vol_h1": 20000}
rc = {"score_normalised": 5}
hg = {"holders": 1000, "top1": 5.0, "top10": 50.0, "creator_pct": 0.0}
mf = {"buys_share_h1": 0.8, "vol_growth": 4.0, "holder_growth": 0.0,
      "pattern": "dip"}
total, sub = m3.score_6(pd, rc, hg, 80.0, [1e-5]*30, mf, True, 1.0)
# manual: contract 100; distribution (100+100+70+100)/4=92.5; entry 100;
# liquidity 0.6*85+0.4*85=85; money_flow (100+100+40)/3=80; sell 100
exp = (100*25 + 92.5*25 + 100*5 + 85*20 + 80*10 + 100*15) / 100
check("A1 score_6 == hitung manual berbobot", abs(total - exp) < 0.05,
      f"got {total} exp {exp} sub={sub}")
check("A2 bobot berjumlah 100", 25+25+5+20+10+15 == 100)
check("A3 ambang feed 60 / manual 70 di kode",
      m3.MIN_SCORE_FEED == 60 and m3.MIN_SCORE_MANUAL == 70)

# ---------------- B. money-flow fail-closed ----------------
pd2 = dict(pd, txns={"h1": {"buys": 80, "sells": 20}})
check("B1 baseline None -> mf ok False",
      m3.money_flow(pd2, {"totalHolders": 1000}, None)["ok"] is False)
check("B2 baseline vol 0 -> vg 0 -> ok False",
      m3.money_flow(pd2, {"totalHolders": 1000},
                    {"vol_h1_usd": 0, "holders": 100, "liq_usd": 50000})["ok"] is False)
r = m3.money_flow(pd2, {"totalHolders": 1000},
                  {"vol_h1_usd": 5000, "holders": None, "liq_usd": 50000})
check("B3 baseline holders None -> hg 0, liq flat -> ok False",
      r["holder_growth"] == 0.0 and r["ok"] is False, f"r={r}")

# ---------------- C. evaluate_candidate holders=None ----------------
MINT = "TestMint11111111111111111111111111111111111111"
PAIR = "TestPair1111111111111111111111111111111111111"

def fake_http(url, timeout=20):
    if "tokens/v1/solana/" in url:
        return [{"chainId": "solana", "dexId": "raydium", "pairAddress": PAIR,
                 "quoteToken": {"symbol": "SOL"}, "liquidity": {"usd": 50000},
                 "priceUsd": "0.00001", "fdv": 100000, "marketCap": 100000,
                 "volume": {"h24": 100000, "h6": 50000, "h1": 20000},
                 "txns": {"h1": {"buys": 80, "sells": 20}},
                 "pairCreatedAt": 1763126400000,
                 "baseToken": {"symbol": "TEST"}, "info": {}}]
    if "report/summary" in url:
        return {"lpLockedPct": 80}
    if "/report" in url:
        return {"score_normalised": 5, "risks": [],
                "token": {"mintAuthority": None, "freezeAuthority": None},
                "token_extensions": {}, "rugged": False, "totalHolders": 1000,
                "topHolders": [{"owner": f"holder{i}", "pct": 5.0}
                               for i in range(10)],
                "creator": None, "markets": [{"lp": {"lpLockedPct": 80}}],
                "lockers": {}}
    if "gopluslabs" in url:
        return {"code": 1, "message": "ok", "result": {MINT: {
            "mintable": {"authority": [], "status": "0"},
            "freezable": {"authority": [], "status": "0"},
            "closable": {"authority": [], "status": "0"},
            "transfer_fee": {}, "holder_count": 1000}}}
    if "ohlcv" in url:
        closes = [0.00002]*10 + [0.00002 - i*5e-7 for i in range(20)]
        closes[-1] = 0.000015  # dip 25% dari high
        return {"data": {"attributes": {"ohlcv_list":
                [[1700000000+i*300, c, c, c, c, 100] for i, c in enumerate(closes)]}}}
    if "swap/v1/quote" in url:
        if "inputMint=So11" in url:
            return {"outAmount": "1000000", "priceImpactPct": "1"}
        return {"outAmount": "7000000", "priceImpactPct": "1"}
    return {"_http_error": 404}

m3.http_json = fake_http
info = {"symbol": "TEST", "sources": ["test"], "pair": PAIR}
state_none = {"sightings": {MINT: {"holders": None, "liq_usd": 40000,
                                   "vol_h1_usd": 5000, "price_usd": 1e-5}}}
try:
    res = m3.evaluate_candidate(MINT, info, state_none, 74.0, True)
    check("C1 baseline holders=None -> TIDAK TypeError (fix BUG-2)",
          res.get("skip") != "entry_holders_not_rising" or True,
          f"skip={res.get('skip')} pass={res.get('pass')}")
    check("C1b baseline holders=None -> bukan crash TypeError",
          "TypeError" not in str(res), f"res={res.get('skip') or res.get('pass')}")
except TypeError as e:
    check("C1 baseline holders=None -> TIDAK TypeError (fix BUG-2)", False,
          f"raise: {e}")
state_ok = {"sightings": {MINT: {"holders": 500, "liq_usd": 40000,
                                 "vol_h1_usd": 5000, "price_usd": 1e-5}}}
res2 = m3.evaluate_candidate(MINT, info, state_ok, 74.0, True)
check("C2 kontrol baseline holders=500 -> pass True",
      res2.get("pass") is True,
      f"pass={res2.get('pass')} skip={res2.get('skip')} score={res2.get('score')}")

# ---------------- D. PnL drag entry ----------------
m3.TRIALS_DIR = "/tmp/m3-trials-test"
os.makedirs("/tmp/m3-trials-test", exist_ok=True)
led = {"cash_usd": 1000.0, "positions": [], "trades": []}
pos = {"mint": MINT, "symbol": "TEST", "pair": PAIR, "dex": "raydium",
       "entry_time": m3.now_wib(), "entry_price_usd": 1e-5,
       "entry_liq_usd": 50000, "size_usd": 40.0, "tokens": 4000000,
       "peak_mult": 1.0, "sold_frac": 0.0, "sold_2x": False, "sold_4x": False,
       "realized_usd": 0.0, "fees_usd": 0.0, "slippage_pct": 0.01,
       "score": 90, "status": "open"}
# tiru potongan kas saat entry di run() (fix BUG-3: field entry drag di pos)
entry_drag = 40*0.0025 + 40*0.01 + 0.00001*74.0
led["cash_usd"] = round(1000 - 40 - entry_drag, 4)
pos["fees_usd"] = round(entry_drag, 4)
pos["entry_drag_usd"] = round(entry_drag, 4)
pos["entry_fee_usd"] = round(40*0.0025, 4)
pos["entry_slip_usd"] = round(40*0.01, 4)
pos["entry_gas_usd"] = round(0.00001*74.0, 4)
m3.settle_exit(led, pos, 2e-5, "test_2x", 74.0, 1.0)  # jual semua di 2x
trade = m3.finalize_trade(led, pos, "test_2x")
true_pnl = round(led["cash_usd"] - 1000.0, 4)
check("D1 pnl laporan == pnl kas sebenarnya (fix BUG-3)",
      abs(trade["pnl_usd_net"] - true_pnl) < 0.01,
      f"laporan={trade['pnl_usd_net']} kas-nyata={true_pnl} drag={entry_drag:.5f}")
check("D1b pnl == +38.4986 (bukan +38.9993)",
      abs(trade["pnl_usd_net"] - 38.4986) < 0.01,
      f"pnl={trade['pnl_usd_net']}")
bd = trade["pnl_breakdown"]
check("D2 pnl_breakdown angka nyata (bukan 0.0)",
      abs(bd["gas_usd"] - 0.0015) < 0.001 and abs(bd["slippage_usd"] - 1.2) < 0.01
      and abs(bd["fees_usd"] - 0.3) < 0.01 and abs(bd["entry_drag_usd"] - 0.5007) < 0.01,
      f"bd={bd}")

# ---------------- E. kill-switch latch ----------------
captured = {}
def fake_load(path, default):
    if "m3-ledger" in path:
        return dict(captured.get("ledger", {}))
    return {"sightings": {}}
def fake_save(path, obj):
    if "m3-ledger" in path:
        captured["ledger"] = json.loads(json.dumps(obj))
m3.load_json = fake_load
m3.save_json = fake_save
m3.sol_price_usd = lambda: 74.0
m3.discovery = lambda: {}
m3.pair_data = lambda mint: {"price_usd": 1e-5, "liq_usd": 50000}
m3.rugcheck = lambda mint: None

captured["ledger"] = {"bankroll_start_usd": 1000.0, "cash_usd": 699.0,
                      "positions": [], "trades": [], "kill_switch": False}
m3.run(dry_run=False)
check("E1 ekuitas $699 tanpa posisi -> kill_switch TETAP False (celah latch)",
      captured["ledger"].get("kill_switch") is False,
      f"kill_switch={captured['ledger'].get('kill_switch')}")
# kontrol positif: ada posisi, ekuitas <700 -> latch True + posisi tertutup
pos2 = dict(pos, mint=MINT, symbol="TEST", pair=PAIR, entry_time=m3.now_wib(),
            entry_price_usd=1e-5, size_usd=40.0, sold_frac=0.0,
            realized_usd=0.0, fees_usd=0.0, status="open", peak_mult=1.0)
captured["ledger"] = {"bankroll_start_usd": 1000.0, "cash_usd": 650.0,
                      "positions": [pos2], "trades": [], "kill_switch": False}
m3.run(dry_run=False)
check("E2 kontrol: ekuitas $690 + 1 posisi -> kill_switch True, posisi 0",
      captured["ledger"].get("kill_switch") is True and
      len(captured["ledger"].get("positions", [])) == 0,
      f"kill={captured['ledger'].get('kill_switch')} pos={len(captured['ledger'].get('positions', []))}")

# ---------------- F. entry_pattern ----------------
closes_flat = [0.00002] + [0.000016]*29  # high 150 mnt lalu, 60 mnt terakhir datar
pat, why = m3.entry_pattern(closes_flat)
check("F1 high 150-mnt lalu dihitung sbg 'dip' (spec: high 60 mnt)",
      pat == "dip", f"pat={pat} {why}")
closes_jump = [0.00001]*27 + [0.00001, 0.00001, 0.000013]
pat2, why2 = m3.entry_pattern(closes_jump)
check("F2 breakout tanpa retest nyata tetap lolos (syarat retest lemah)",
      pat2 == "breakout", f"pat={pat2} {why2}")

print()
print("HASIL:", "SEMUA PASS (temuan terkonfirmasi)" if not fails else f"GAGAL: {fails}")
sys.exit(1 if fails else 0)
