#!/usr/bin/env bash
# cut_windows.sh N — cut the recorded-input windows 1..N with the committed rules and commit the new ones (9.5 D26).
# SWELL-KW (word, ie, outlook) by campaign/build_windows.py, 136M Keystrokes by probe/aalto_streams.py. Every committed
# window must come out byte-identical, and every committed index entry unchanged, or nothing is written. A window with
# no events (the recording ended) is not committed. SWELL-KW's uLog files are fetched once into $MEAS_LOOP_WORK/swell
# (DANS data files listed in probe/swell-ulog-files.json, sizes checked); 136M reads by HTTP range into its cache.
set -euo pipefail
N=${1:?usage: cut_windows.sh N}
cd "$(dirname "$0")/../../../.."
W=${MEAS_LOOP_WORK:-$HOME/.cache/meas-loop}; SCOPE=${MEAS_LOOP_SCOPE:-jioh/phase-9}
CERT=${SSL_CERT_FILE:-/etc/ssl/cert.pem}   # the development Mac's python.org builds carry no CA bundle
ST=dataset/meas/streams
mkdir -p "$W/swell/xml" "$W/aalto"
python3 -c "
import json
for f in json.load(open('dataset/tools/meas/probe/swell-ulog-files.json'))['files']: print(f['id'], f['name'], f['bytes'])" |
while read -r id name bytes; do
  f="$W/swell/xml/$name"
  [ -f "$f" ] && [ "$(wc -c < "$f" | tr -d ' ')" = "$bytes" ] && continue
  curl -sfL -o "$f" "https://ssh.datastations.nl/api/access/datafile/$id"
  [ "$(wc -c < "$f" | tr -d ' ')" = "$bytes" ] || { echo "size mismatch: $name"; exit 1; }
done
[ -d "$W/swell/ext" ] || python3 dataset/tools/meas/probe/swell_streams.py "$W/swell/ext" "$W"/swell/xml/*.xml > "$W/swell/ext.log"
rm -rf "$W/swell/win$N" "$W/aalto/out$N"
python3 dataset/tools/meas/campaign/build_windows.py "$W/swell/ext" dataset/tools/meas/probe/swell-ulog-files.json "$W/swell/win$N" --repeats "$N" | tail -3 | cut -c1-160
SSL_CERT_FILE=$CERT python3 dataset/tools/meas/probe/aalto_streams.py "$W/aalto/cache" "$W/aalto/out$N" --repeats "$N" | tail -1
bad=0
for f in "$ST"/*-r*.jsonl; do
  b=$(basename "$f"); src="$W/swell/win$N/$b"; case $b in aalto-*) src="$W/aalto/out$N/$b";; esac
  cmp -s "$f" "$src" || { echo "CHANGED: $b"; bad=1; }
done
python3 - "$W" "$N" "$ST" <<'PY'
import json, sys
W, N, ST = sys.argv[1:]
o, n = json.load(open(f"{ST}/windows.json")), json.load(open(f"{W}/swell/win{N}/windows.json"))
a, b = json.load(open(f"{ST}/aalto-windows.json")), json.load(open(f"{W}/aalto/out{N}/aalto-windows.json"))
ok = (o["rule"] == n["rule"] and all(o["windows"][k] == n["windows"][k] for k in o["windows"])
      and a["rule"] == b["rule"] and all(a["windows"][k] == b["windows"][k] for k in a["windows"])
      and all(b["sha256"].get(k) == v for k, v in a["sha256"].items()))
print("committed windows and index entries unchanged:", ok)
sys.exit(0 if ok else 1)
PY
[ $bad = 0 ] || exit 1
new=()
for app in word ie outlook; do
  f="$W/swell/win$N/$app-r$N.jsonl"
  if [ -s "$f" ] && [ ! -f "$ST/$app-r$N.jsonl" ]; then cp "$f" "$ST/"; new+=("$ST/$app-r$N.jsonl"); fi
done
if [ ! -f "$ST/aalto-r$N.jsonl" ]; then cp "$W/aalto/out$N/aalto-r$N.jsonl" "$ST/"; new+=("$ST/aalto-r$N.jsonl"); fi
cp "$W/swell/win$N/windows.json" "$W/aalto/out$N/aalto-windows.json" "$ST/"
paths=(${new[@]+"${new[@]}"} "$ST/windows.json" "$ST/aalto-windows.json")   # only these: the index is shared
git add "${paths[@]}"
git diff --cached --quiet -- "${paths[@]}" && { echo "window $N already committed"; exit 0; }
git commit -q -m "feat($SCOPE): stimulus window $N — SWELL-KW and 136M cut by the committed rules; earlier windows byte-identical (9.5 D26)" -- "${paths[@]}"
git pull -q --rebase --autostash && git push -q && git log --oneline -1
