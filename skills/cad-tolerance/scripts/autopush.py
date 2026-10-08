#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""autopush.py — TU DONG commit + push len GitHub, va ghi PHAT HIEN MOI.

Dung:
  python scripts/autopush.py status                # xem co gi thay doi chua push
  python scripts/autopush.py push                  # commit + push neu co thay doi
  python scripts/autopush.py note "noi dung"       # ghi phat hien moi -> findings/ -> push
  python scripts/autopush.py watch --interval 1800 # tu push dinh ky (giay), Ctrl+C de dung
  python scripts/autopush.py --selftest

Nguyen tac:
  - Khong co thay doi -> khong lam gi (khong tao commit rong).
  - Push that bai (offline/khong co quyen) -> ghi log, KHONG crash, lan sau thu lai.
  - Moi lan chay ghi 1 dong vao logs/autopush.log.
"""
import argparse
import os
import subprocess
import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
LOGDIR = os.path.join(REPO, "logs")
LOGFILE = os.path.join(LOGDIR, "autopush.log")
FINDINGS = os.path.join(REPO, "findings")


def log(msg):
    os.makedirs(LOGDIR, exist_ok=True)
    line = "%s | %s" % (time.strftime("%Y-%m-%d %H:%M:%S"), msg)
    print(line)
    with open(LOGFILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def git(*args, check=False):
    p = subprocess.run(["git"] + list(args), cwd=REPO, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if check and p.returncode != 0:
        raise RuntimeError("git %s -> %s" % (" ".join(args), (p.stderr or "").strip()[:300]))
    return p


def changed_files():
    p = git("status", "--porcelain")
    return [l[3:].strip() for l in (p.stdout or "").splitlines() if l.strip()]


def do_push(msg=None, dry_run=False):
    files = changed_files()
    if not files:
        log("khong co thay doi — bo qua")
        return 0
    if dry_run:
        log("DRY-RUN: se commit %d file: %s" % (len(files), ", ".join(files[:10])))
        return 0
    if not msg:
        msg = "auto: cap nhat %d file (%s)" % (len(files), time.strftime("%Y-%m-%d %H:%M"))
    git("add", "-A")
    c = git("commit", "-m", msg)
    if c.returncode != 0:
        log("commit loi: %s" % (c.stderr or c.stdout or "").strip()[:200])
        return 1
    p = git("push", "origin", "HEAD")
    if p.returncode != 0:
        log("PUSH THAT BAI (se thu lai lan sau): %s" % (p.stderr or "").strip()[:200])
        return 1
    log("PUSH OK — %d file | %s" % (len(files), msg))
    return 0


def write_finding(text):
    os.makedirs(FINDINGS, exist_ok=True)
    day = time.strftime("%Y-%m-%d")
    path = os.path.join(FINDINGS, day + ".md")
    new = not os.path.exists(path)
    with open(path, "a", encoding="utf-8") as f:
        if new:
            f.write("# Phát hiện mới — %s\n\n> Dòng: `HH:MM | nội dung | nguồn (nếu có)`\n\n" % day)
        f.write("- %s | %s\n" % (time.strftime("%H:%M"), text.strip()))
    return path


def cmd_status(a):
    files = changed_files()
    print("Repo    : %s" % REPO)
    print("Thay doi: %d file" % len(files))
    for f in files[:30]:
        print("   ", f)
    p = git("status", "-sb")
    print(p.stdout.strip().splitlines()[0] if p.stdout.strip() else "")
    return 0


def cmd_push(a):
    return do_push(a.message, a.dry_run)


def cmd_note(a):
    path = write_finding(a.text)
    print("Da ghi phat hien -> %s" % path)
    return do_push(a.message or ("finding: " + a.text.strip()[:60]))


def cmd_watch(a):
    if a.interval < 60:
        print("interval toi thieu 60 giay.")
        return 1
    log("WATCH bat dau — push moi %d giay (Ctrl+C de dung)" % a.interval)
    try:
        while True:
            do_push()
            time.sleep(a.interval)
    except KeyboardInterrupt:
        log("WATCH dung theo yeu cau")
    return 0


def selftest():
    global LOGDIR, LOGFILE, FINDINGS
    import tempfile
    old = (LOGDIR, LOGFILE, FINDINGS)
    tmp = tempfile.mkdtemp(prefix="autopush_")
    LOGDIR, LOGFILE, FINDINGS = tmp, os.path.join(tmp, "autopush.log"), os.path.join(tmp, "findings")
    try:
        p = write_finding("Thu nghiem phat hien")
        assert os.path.exists(p), "phai tao file findings"
        t = open(p, encoding="utf-8").read()
        assert "Thu nghiem phat hien" in t and t.startswith("# Phát hiện mới"), "noi dung findings sai"
        p2 = write_finding("Dong thu hai")
        assert open(p2, encoding="utf-8").read().count("- ") == 2, "phai ghi them duoc dong moi (2 dong finding)"
        log("test log")
        assert os.path.exists(LOGFILE), "phai ghi log"
        assert changed_files() == [] or isinstance(changed_files(), list)
    finally:
        LOGDIR, LOGFILE, FINDINGS = old
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
    print("SELFTEST PASS")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Tu dong push repo len GitHub")
    sub = ap.add_subparsers(dest="cmd")
    s = sub.add_parser("status"); s.set_defaults(fn=cmd_status)
    p = sub.add_parser("push")
    p.add_argument("-m", "--message")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(fn=cmd_push)
    n = sub.add_parser("note")
    n.add_argument("text")
    n.add_argument("-m", "--message")
    n.set_defaults(fn=cmd_note)
    w = sub.add_parser("watch")
    w.add_argument("--interval", type=int, default=1800)
    w.set_defaults(fn=cmd_watch)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not getattr(a, "fn", None):
        ap.print_help()
        return 1
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
