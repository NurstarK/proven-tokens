#!/usr/bin/env python3
"""Base (chain 8453) version of survey/scan_tokens.py. Keyless: bytecode + storage from a public
Base RPC, source/ABI from Base Blockscout. Usage: python3 -I scan_base.py tokens_in.json out.json"""
import json, sys, time, urllib.request, os
RPC = "https://mainnet.base.org"
BS = "https://base.blockscout.com/api/v2"
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scan_tokens.py")
ns = {"__name__": "lib", "__file__": src_path}; os.environ.setdefault("ETHERSCAN_KEY", "unused")
_argv = sys.argv; sys.argv = [sys.argv[0]]
exec(open(src_path).read(), ns)  # reuse analyze() unchanged
sys.argv = _argv
analyze = ns["analyze"]

def get(url, data=None):
    for i in range(4):
        try:
            req = urllib.request.Request(url, data=data, headers={"User-Agent": "token-survey/1.0", "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=40) as r: return json.loads(r.read())
        except Exception as e: err = e; time.sleep(2 + 3 * i)
    raise err
def rpc(m, p): return get(RPC, json.dumps({"jsonrpc": "2.0", "id": 1, "method": m, "params": p}).encode()).get("result")
def call(addr, sel):
    try: return rpc("eth_call", [{"to": addr, "data": "0x" + sel}, "latest"])
    except Exception: return None

POWER = ("mint", "burn", "pause", "unpause", "blacklist", "freeze", "block", "deny", "rely", "ban",
         "setminter", "configureminter", "addminter", "upgrade", "rescue", "seize", "wipe", "transferownership",
         "renounceownership", "setfee", "settax", "setlimit", "grantrole", "revokerole", "crosschain", "bridge")

def source(addr):
    try: s = get(f"https://sourcify.dev/server/v2/contract/8453/{addr}?fields=compilation,abi")
    except Exception as e: return {"err": "not on Sourcify: " + repr(e)[:60]}
    abi = s.get("abi") or []; c = s.get("compilation") or {}
    fns = [f["name"] for f in abi if f.get("type") == "function" and f.get("stateMutability") not in ("view", "pure")]
    return {"name": c.get("name"), "compiler": c.get("compilerVersion"), "match": s.get("match"), "verified": bool(s.get("match")),
            "powers": sorted({f for f in fns if any(p in f.lower() for p in POWER)}), "writes": sorted(set(fns))}

def scan(r):
    a = r["addr"]
    r["code"] = analyze(rpc("eth_getCode", [a, "latest"]) or "0x"); r["code"].pop("sels")
    r["src"] = source(a)
    impl = ""
    code = rpc("eth_getCode", [a, "latest"]) or "0x"
    if code.startswith("0x363d3d373d3d3d363d73"): impl = "0x" + code[22:62]; r["clone"] = "EIP-1167"
    for slot in ("0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc",
                 "0x7050c9e0f4ca769c69bd3a8ef740bc37934f8e2c036e5a723fd8ee048ed3f8c3"):
        v = rpc("eth_getStorageAt", [a, slot, "latest"]) or "0x0"
        if impl: break
        if int(v, 16): impl = "0x" + v[-40:]; break
    if impl:
        r["impl_addr"] = impl; r["impl_src"] = source(impl)
        r["impl_code"] = analyze(rpc("eth_getCode", [impl, "latest"]) or "0x"); r["impl_code"].pop("sels")
        adm = rpc("eth_getStorageAt", [a, "0xb53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103", "latest"]) or "0x0"
        r["proxy_admin"] = "0x" + adm[-40:] if int(adm, 16) else None
    o = call(a, "8da5cb5b"); r["owner_now"] = ("0x" + o[-40:]) if o and len(o) >= 66 else None
    ts = call(a, "18160ddd"); r["total_supply_raw"] = int(ts, 16) if ts and ts != "0x" else None
    return r

rows = json.load(open(sys.argv[1])); out = []
for r in rows:
    try: out.append(scan(r))
    except Exception as e: r["error"] = repr(e)[:120]; out.append(r)
    print(r["sym"], r.get("code", {}).get("bytes"), r.get("impl_addr", ""), r.get("error", ""), file=sys.stderr)
    time.sleep(0.5)
json.dump(out, open(sys.argv[2], "w"), indent=1)
