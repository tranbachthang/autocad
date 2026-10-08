#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Goi y CAP CHINH XAC (IT) + DO NHAM (Ra) cho be mat chi tiet may.

Dung:
  python rait.py suggest "lo lap o lan" --size 25
  python rait.py suggest "mat lam kin dau" --size 40 --process "phay tinh"
  python rait.py it --size 25 --grade 7          # tra tri so dung sai
  python rait.py ra --process "mài tinh"         # Ra dat duoc cua phuong phap
  python rait.py list                            # liet ke bang chuc nang
  python rait.py --selftest
"""
import argparse
import csv
import os
import sys
import unicodedata

try:                     # console Windows hay dung cp1252 -> khong in duoc dau tieng Viet
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")


def nodau(s):
    s = unicodedata.normalize("NFD", str(s).lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s.replace("đ", "d")


def load_csv(name):
    rows = []
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        for line in f:
            if line.startswith("#"):
                continue
            if not line.strip():
                continue
            rows.append(line)
    return list(csv.DictReader(rows))


IT_TABLE = load_csv("iso286_it.csv")
SURFACES = load_csv("surface_ra.csv")
PROCESSES = load_csv("process_ra.csv")


def it_value(d_um, grade):
    """Tri so dung sai (µm) cua cap IT<grade> cho kich thuoc danh nghia d_um (mm)."""
    for r in IT_TABLE:
        lo, hi = float(r["size_over_mm"]), float(r["size_to_mm"])
        if lo < d_um <= hi:
            return float(r["IT%d" % grade])
    return None


def find_surface(text):
    """Tim dong bang chuc nang khop nhieu keyword nhat."""
    t = nodau(text)
    best, best_hits = None, 0
    for r in SURFACES:
        hits = sum(1 for k in r["keywords"].split("|") if nodau(k) in t)
        if hits > best_hits:
            best, best_hits = r, hits
    return best, best_hits


def find_by_key(text, rows):
    t = nodau(text)
    best, best_hits = None, 0
    for r in rows:
        hits = sum(1 for k in r["keywords"].split("|") if nodau(k) in t)
        if hits > best_hits:
            best, best_hits = r, hits
    return best, best_hits


def deviation(prefix, it_um):
    """Sai lech gioi han CHI cho mien H (lo co ban) va h (truc co ban)."""
    if prefix == "H":        # lỗ cơ bản: EI = 0
        return "0 / +%.3f" % (it_um / 1000.0)
    if prefix == "h":        # trục cơ bản: es = 0
        return "0 / -%.3f" % (it_um / 1000.0)
    return None


def cmd_suggest(a):
    print("Mo ta dua vao : %s" % a.feature)
    row, hits = find_surface(a.feature)
    if not row:
        print("KHONG khop chuc nang nao trong bang.")
        print("-> Them tu khoa vao data/surface_ra.csv, hoac nap tai lieu rieng bang learn.py roi tra lai.")
        return 1
    (grade, ra_lo, ra_hi) = (int(row["IT"].replace("IT", "")), float(row["Ra_min"]), float(row["Ra_max"]))
    fits = [x for x in row["kieu_lap"].split("|") if x != "-"]
    ra_txt = "Ra %.2g - %.2g um (▽%.2g)" % (ra_lo, ra_hi, ra_hi)
    print("Chuc nang     : %s" % row["nhom"])
    print("Cap chinh xac : IT%d" % grade)
    print("Do nham goi y : %s" % ra_txt)
    print("Mien dung sai : %s" % (" | ".join(fits) if fits else "khong yeu cau (be mat tu do)"))
    print("Ghi chu        : %s" % row["ghi_chu"])

    dim = None
    if a.size:
        dim = float(a.size)
        it_um = it_value(dim, grade)
        if it_um is None:
            print("CANH BAO: kich thuoc %.3g mm nam ngoai bang ISO 286 (0-500 mm)." % dim)
        else:
            print("Tri so dung sai: %s um  (%.3f mm)  [ISO 286-1]" % (
                int(it_um) if it_um == int(it_um) else it_um, it_um / 1000.0))
            sym = fits[0] if fits else ""
            dev = deviation(sym[:1], it_um) if sym else None
            tail = "  (%s)" % dev if dev else "  (tra bang ISO 286-2 cho mien '%s')" % sym
            print("GHI TREN BAN VE: ⌀%.3g%s%s  %s" % (dim, sym, tail, ra_txt))

    if a.process:
        prow, phits = find_by_key(a.process, PROCESSES)
        if not prow:
            print("CANH BAO: khong nhan ra phuong phap '%s'." % a.process)
        else:
            p_lo, p_hi = float(prow["Ra_min"]), float(prow["Ra_max"])
            p_it = int(prow["IT_tot_nhat"].replace("IT", ""))
            print("Phuong phap   : %s -> Ra %.2g - %.2g um, dat tot nhat IT%d" % (
                prow["phuong_phap"], p_lo, p_hi, p_it))
            if ra_lo < p_lo:
                print("  ✗ CANH BAO: yeu cau Ra %.2g CHAT hon kha nang cua '%s' (tot nhat Ra %.2g)." % (
                    ra_lo, prow["phuong_phap"], p_lo))
                print("    -> Phai them buoc tinh hon (vd mài/nghiền) hoac ha yeu cau xuong Ra %.2g." % p_hi)
            if grade < p_it:
                print("  ✗ CANH BAO: yeu cau IT%d CHAT hon kha nang cua '%s' (tot nhat IT%d)." % (
                    grade, prow["phuong_phap"], p_it))
            if ra_lo >= p_lo and grade >= p_it:
                print("  ✓ Phuong phap nay DU suc dat yeu cau nay.")
    return 0


def cmd_it(a):
    v = it_value(float(a.size), int(a.grade))
    if v is None:
        print("Kich thuoc %.3g mm ngoai bang (0-500 mm)." % float(a.size))
        return 1
    print("IT%d cho ⌀%.4g mm = %s um = %.3f mm" % (
        int(a.grade), float(a.size), int(v) if v == int(v) else v, v / 1000.0))
    return 0


def cmd_ra(a):
    row, _ = find_by_key(a.process, PROCESSES)
    if not row:
        print("Khong nhan ra phuong phap '%s'." % a.process)
        return 1
    print("%s: Ra %.2g - %.2g um, dat tot nhat IT%d. %s" % (
        row["phuong_phap"], float(row["Ra_min"]), float(row["Ra_max"]),
        int(row["IT_tot_nhat"].replace("IT", "")), row["ghi_chu"]))
    return 0


def cmd_list(a):
    print("== Theo CHUC NANG be mat ==")
    for r in SURFACES:
        print("  %-42s IT%-3s Ra %.2g-%.2g  %s" % (
            r["nhom"], r["IT"].replace("IT", ""), float(r["Ra_min"]), float(r["Ra_max"]), r["kieu_lap"]))
    print("== Theo PHUONG PHAP gia cong ==")
    for r in PROCESSES:
        print("  %-28s Ra %.2g-%.2g  toi da IT%s" % (
            r["phuong_phap"], float(r["Ra_min"]), float(r["Ra_max"]), r["IT_tot_nhat"].replace("IT", "")))
    return 0


def selftest():
    assert it_value(25, 7) == 21, "IT7 18-30 phai = 21um"
    assert it_value(25, 6) == 13, "IT6 18-30 phai = 13um"
    assert it_value(50, 7) == 25, "IT7 30-50 phai = 25um"
    assert it_value(2, 7) == 10, "IT7 0-3 phai = 10um"
    row, hits = find_surface("lo lap o lan")
    assert row and "ổ lăn" in row["nhom"], "phai khop o lan"
    row2, _ = find_surface("mat lam kin dau")
    assert row2 and "kín" in row2["nhom"], "phai khop lam kin"
    p, _ = find_by_key("phay tho", PROCESSES)
    assert p and p["phuong_phap"] == "Phay thô"
    assert deviation("H", 21) == "0 / +0.021"
    assert deviation("h", 13) == "0 / -0.013"
    print("SELFTEST PASS")
    return 0


def main():
    p = argparse.ArgumentParser(description="Goi y Ra/IT cho be mat chi tiet may")
    sub = p.add_subparsers(dest="cmd")
    s = sub.add_parser("suggest", help="goi y cho mot be mat")
    s.add_argument("feature")
    s.add_argument("--size", type=float, help="kich thuoc danh nghia (mm)")
    s.add_argument("--process", help="phuong phap gia cong du kien")
    s.set_defaults(fn=cmd_suggest)
    t = sub.add_parser("it", help="tra tri so dung sai")
    t.add_argument("--size", type=float, required=True)
    t.add_argument("--grade", type=int, required=True)
    t.set_defaults(fn=cmd_it)
    r = sub.add_parser("ra", help="Ra dat duoc cua phuong phap")
    r.add_argument("--process", required=True)
    r.set_defaults(fn=cmd_ra)
    l = sub.add_parser("list", help="liet ke bang")
    l.set_defaults(fn=cmd_list)
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest:
        return selftest()
    if not getattr(a, "fn", None):
        p.print_help()
        return 1
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
