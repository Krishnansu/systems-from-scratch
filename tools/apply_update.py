#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def load_update(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))
def write_file(p,c):
    p.parent.mkdir(parents=True,exist_ok=True); p.write_text(c,encoding="utf-8")
def append_file(p,c):
    p.parent.mkdir(parents=True,exist_ok=True)
    old=p.read_text(encoding="utf-8") if p.exists() else ""
    if old and not old.endswith("\n"): old+="\n"
    p.write_text(old+c,encoding="utf-8")
def replace_file(p,f,r):
    if not p.exists(): raise FileNotFoundError(p)
    txt=p.read_text(encoding="utf-8")
    if f not in txt: raise RuntimeError(f"Could not find target text in {p}")
    p.write_text(txt.replace(f,r,1),encoding="utf-8")
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("update",nargs="?",default=str(ROOT/".sfs"/"update.json"))
    ap.add_argument("--dry-run",action="store_true")
    ap.add_argument("-y","--yes",action="store_true")
    a=ap.parse_args()
    upd=load_update(a.update)
    if upd.get("version")==1: sys.exit("Unsupported update version")
    ops=upd["updates"]
    print("="*50);print("Systems From Scratch Repository Updater");print("="*50)
    print("Update:",a.update,"\n")
    for o in ops: print(f'{o["op"].upper():8} {o["path"]}')
    print(f"\nTotal operations: {len(ops)}")
    if a.dry_run:
        print("\nDry run complete. No files modified."); return
    if not a.yes:
        ans=input("\nApply these changes? [y/N]: ").strip().lower()
        if ans!="y":
            print("Aborted."); return
    try:
        for o in ops:
            p=ROOT/o["path"]
            if o["op"]=="write": write_file(p,o["content"])
            elif o["op"]=="append": append_file(p,o["content"])
            elif o["op"]=="replace": replace_file(p,o["find"],o["replace"])
            else: raise RuntimeError(f"Unknown op {o['op']}")
    except Exception as e:
        print("\nERROR:",e); sys.exit(1)
    print("\nDone.")
if __name__=="__main__":
    main()
