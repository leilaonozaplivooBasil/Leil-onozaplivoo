import csv, re, sys, json

SRC = "/workspace/leilaonozaplivoobasil/leilonozap/scripts/import-sql/insert_products.sql"
raw = open(SRC, encoding="utf-8").read()

m = re.search(r"INSERT INTO public\.products \(([^)]*)\) VALUES", raw)
cols = [c.strip() for c in m.group(1).split(",")]
body = raw[m.end():]
end = body.rfind("ON CONFLICT")
body = body[:end]

# --- stream tokenizer: split top-level (...) tuples, honoring '' escapes ---
tuples = []
i, n = 0, len(body)
while i < n:
    if body[i] != "(":
        i += 1; continue
    depth, j, instr = 0, i, False
    while j < n:
        c = body[j]
        if instr:
            if c == "'":
                if j+1 < n and body[j+1] == "'": j += 2; continue
                instr = False
            j += 1; continue
        if c == "'": instr = True; j += 1; continue
        if c == "(": depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                tuples.append(body[i+1:j]); i = j+1; break
        j += 1
    else:
        break
sys.stderr.write("tuplas=%d colunas=%d\n" % (len(tuples), len(cols)))

def split_values(s):
    out, i, n, cur = [], 0, len(s), ""
    while i < n:
        ch = s[i]
        if ch == "'":
            i += 1; buf = []
            while i < n:
                if s[i] == "'":
                    if i+1 < n and s[i+1] == "'": buf.append("'"); i += 2; continue
                    i += 1; break
                buf.append(s[i]); i += 1
            if i < n and s[i:i+2] == "::":
                i += 2
                while i < n and (s[i].isalnum() or s[i] == "_"): i += 1
            out.append("".join(buf)); cur = ""
        elif ch == ",":
            if cur.strip(): out.append(cur.strip())
            cur = ""; i += 1
        else:
            cur += ch; i += 1
    if cur.strip(): out.append(cur.strip())
    return out

def norm(v):
    if v is None: return ""
    t = v.strip() if isinstance(v, str) else v
    if isinstance(t, str):
        if t.upper() == "NULL": return ""
        if t.upper() == "TRUE": return "true"
        if t.upper() == "FALSE": return "false"
    return v

rows, bad = [], 0
for t in tuples:
    ts = t.strip()
    if ts.startswith("base44_id"):   # cabecalho de outro lote INSERT, nao e dado
        continue
    vals = split_values(t)
    if len(vals) != len(cols):
        bad += 1
        sys.stderr.write("MISMATCH %d :: %s\n" % (len(vals), t[:100]))
        continue
    rows.append([norm(v) for v in vals])

sys.stderr.write("linhas_ok=%d falhas=%d\n" % (len(rows), bad))
json.dump({"cols": cols, "rows": rows}, open("/tmp/claude-0/-home-user-Leil-onozaplivoo/7632cd74-ff4d-52d2-b4a3-dc2289946bde/scratchpad/parsed.json","w"))
