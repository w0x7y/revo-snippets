"""Expand every snippet in snippets/revo.json and run the result with revo.

usage: python3 tools/check.py [path/to/revo]   (default: revo on PATH)

Expansion: ${N:default} -> default, $N / ${N} -> the value for N. FILLS overrides a
tab stop's value, PRE/POST wrap the snippet so it is a runnable program.
"""
import json
import re
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path

TOKEN = re.compile(r"\$\{(\d+):([^}]*)\}|\$\{(\d+)\}|\$(\d+)")


def expand(body, fills=None):
    fills = fills or {}
    defaults = {}
    for m in TOKEN.finditer(body):
        if m.group(1) is not None:
            defaults.setdefault(int(m.group(1)), m.group(2))

    def value(m):
        n = int(next(g for g in (m.group(1), m.group(3), m.group(4)) if g is not None))
        return fills.get(n, defaults.get(n, ""))

    return TOKEN.sub(value, body)


# prefix -> (prelude, postlude, fills, mode)
CASES = {
    "hdr": ("", "", {}, "run"),
    "fn": ("", "\nprint(name())", {}, "run"),
    "fna": ("", "", {}, "run"),
    "mres": ('const expr = number("42")\nprint(', "\n)", {}, "run"),
    "match": ("const x = 5\nconst cond = :true\nprint(", "\n)", {}, "run"),
    "rok": ("const value = 1\nprint(", ")", {}, "run"),
    "rerr": ("print(", ")", {}, "run"),
    "fnr": ("const cond = :false\nconst value = 1\n", "\nprint(name())", {}, "run"),
    "fori": ("const n = 3\n", "", {0: "print(i)"}, "run"),
    "forin": ("const items = {1, 2}\n", "", {0: "print(x)"}, "run"),
    "ife": ("const cond = :true\n", "", {}, "run"),
    "doc": ("", "\nfn f() 1\nprint(f())", {}, "run"),
    "docm": ("", "\nfn f() 1\nprint(f())", {}, "run"),
    "test": ("const cond = :true\n", "", {}, "test"),
    "suite": ("", "", {0: "expect(:true)?"}, "test"),
    "eq": ('test "t" do\nconst actual = 1\nconst expected = 1\n', "\nend", {}, "test"),
    "class": ("", "\nprint(Name.new(1):method())", {2: "x", 3: "x = x", 0: "self.x"}, "run"),
    "tobj": ("", "\nc:inc()\nprint(c.n)", {0: "self.n += 1"}, "run"),
    "mfn": ("const o = {\nv = 1,\n", "\n}\nprint(o:name())", {0: "self.v"}, "run"),
    "iterm": ("const t = set_meta({10, 20}, {\n", "\n})\nfor x in t print(x)", {}, "run"),
    "blk": ("const cond = :true\nconst value = 1\nconst r = ", "\nprint(r)", {}, "run"),
    "loopl": ("const cond = :true\nconst value = 1\nconst r = ", "\nprint(r)", {}, "run"),
    "union": ("", "\nconst s: Shape = {:point}\nprint(s)", {}, "run"),
    "des": ("", "\nprint(a, b)", {0: "{1, 2}"}, "run"),
    "imp": ("", "\nprint(alias.double(2), mod.double(1))", {1: "./mod", 3: "./mod"}, "run"),
    "spawnj": ("fn worker() 42\n", '\nprint("joined")', {}, "run"),
    "jobs": ("fn worker(x) x * 2\nconst items = {1, 2}\n", '\nprint("joined")', {}, "run"),
    "tcpserve": ("", "", {2: "18091"}, "serve"),
    "tcpconn": ("", "", {}, "compile"),
    "readf": ("", "\nprint(text)", {}, "run"),
    "writef": ("", '\nprint(fs.open("out.txt")?:read()?)', {}, "run"),
    "stdin": ("", "", {0: 'print("got", line)'}, "stdin"),
    "chanp": ("const value = 42\n", '\nprint("received")', {}, "run"),
    "itmap": ("const xs = {1, 2}\nprint(", ")", {}, "run"),
    "itfilter": ("const xs = {1, 2}\nconst cond = :true\nprint(", ")", {}, "run"),
    "itreduce": ("const xs = {1, 2}\nprint(", ")", {}, "run"),
    "dbg": ("const x = {a = 1}\n", "", {}, "run"),
    "timeit": ("", "", {}, "run"),
    "proc": ("", "\nprint(name!(42))", {}, "run"),
    "procv": ("", "\nprint(name!(1, 2, 3))", {}, "run"),
    "ext": ("", "", {}, "compile"),
    "ffifn": ("", '\nprint(strlen("hello"))', {}, "run"),
    "cli": ("", "", {0: "print(args.flags, args.positionals)"}, "args"),
}


def serve_check(revo, path, cwd):
    proc = subprocess.Popen([revo, path], cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        for _ in range(50):
            try:
                with socket.create_connection(("127.0.0.1", 18091), timeout=2) as s:
                    s.sendall(b"ping\n")
                    reply = s.recv(64).decode()
                return (0 if reply == "ping\n" else 1), f"echo reply: {reply!r}"
            except ConnectionRefusedError:
                time.sleep(0.1)
        return 1, "server never accepted"
    finally:
        proc.kill()


def run(revo, path, mode, cwd):
    cmd = {
        "run": [revo, path],
        "test": [revo, "--test", path],
        "compile": [revo, "compile", path, path + "o"],
        "stdin": [revo, path],
        "args": [revo, path, "-v", "in.txt"],
    }[mode]
    stdin = "a\nb\n" if mode == "stdin" else None
    p = subprocess.run(cmd, cwd=cwd, input=stdin, capture_output=True, text=True, timeout=10)
    return p.returncode, (p.stdout + p.stderr).strip()


def main():
    revo = sys.argv[1] if len(sys.argv) > 1 else "revo"
    snippets = json.loads((Path(__file__).parent.parent / "snippets" / "revo.json").read_text())
    with tempfile.TemporaryDirectory() as tmp:
        sys.exit(check(snippets, str(Path(revo).resolve()) if "/" in revo else revo, Path(tmp)))


def check(snippets, revo, work):
    (work / "mod.rv").write_text("pub fn double(n) n * 2\n")
    (work / "file.txt").write_text("file contents\n")
    prefixes = {s["prefix"] for s in snippets.values()}
    assert prefixes == set(CASES), f"untested: {prefixes - set(CASES)}, stale: {set(CASES) - prefixes}"

    failed = 0
    for name, s in snippets.items():
        pre, post, fills, mode = CASES[s["prefix"]]
        src = pre + expand("\n".join(s["body"]), fills) + post + "\n"
        path = work / f"{s['prefix']}.rv"
        path.write_text(src)
        if mode == "serve":
            rc, out = serve_check(revo, str(path), work)
        else:
            rc, out = run(revo, str(path), mode, work)
        ok = rc == 0 and "error:" not in out.lower() and "fail" not in out.lower()
        failed += not ok
        last = out.splitlines()[-1] if out else ""
        print(f"{'PASS' if ok else 'FAIL'} {s['prefix']:<9} [{mode}] {last[:70]}")
        if not ok:
            print("   " + out.replace("\n", "\n   ")[:1500])
    print(f"\n{len(snippets) - failed}/{len(snippets)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    main()
