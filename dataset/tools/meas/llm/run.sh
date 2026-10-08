#!/usr/bin/env bash
# llm/run.sh <repeat> [full|dry] — the 9.12 latency repeat (research-slice changelog D31; method
# _dev/research/jioh/task-9.12-related-work-prose/campaign/method.md). llama.cpp built from source at a pinned
# commit; two pinned GGUF files, a 3B and an 8B at Q4_K_M; for each, llama-server on every CPU of the runner, its
# load time, then request.py's recognizer-shaped requests (a warm-up, then the `system`-only and the full proposal
# schema alternated, each evaluating the whole prompt), then llama-bench's prompt and generation rates.
# Writes report.json, requests.<model>.jsonl, bench.<model>.json and the logs.
set -u
export PROBE_OUT="${MEAS_OUT:-/tmp/meas}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEAS="$(cd "$HERE/.." && pwd)"
source "$MEAS/probe/common.sh"        # OUT, KV, rec, finish_report
REPEAT="$1"; MODE="${2:-full}"
LLAMA_SHA=bd4eeaa047006cb1fe71999fbd11134b5836e167
# name|repository|revision|file|sha256
MODELS="qwen2.5-3b|Qwen/Qwen2.5-3B-Instruct-GGUF|7dabda4d13d513e3e842b20f0d435c732f172cbe|qwen2.5-3b-instruct-q4_k_m.gguf|626b4a6678b86442240e33df819e00132d3ba7dddfe1cdc4fbb18e0a9615c62d
llama3.1-8b|bartowski/Meta-Llama-3.1-8B-Instruct-GGUF|bf5b95e96dac0462e2a09145ec66cae9a3f12067|Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf|7b064f5842bf9532c91456deda288a1b672397a54fa729aa665952863033557c"
if [ "$MODE" = dry ]; then N_REQ=2; BENCH="-p 128 -n 16 -r 1"; else N_REQ=5; BENCH="-p 512 -n 64 -r 3"; fi
NPROC="$(nproc)"

rec family costs; rec job llm; rec repeat "$REPEAT"; rec mode "$MODE"; rec started_utc "$(date -u +%FT%TZ)"
python3 "$MEAS/runner_spec.py" > "$OUT/spec.json"
source "$MEAS/machine_gate.sh"
rec machine.model "$(machine_model)"; rec machine.wanted "${MEAS_CPU_MODEL:-}"
if ! machine_gate "${MEAS_CPU_MODEL:-}"; then
  rec gate wrong-machine; rec finished_utc "$(date -u +%FT%TZ)"; finish_report
  echo "machine gate: wanted '${MEAS_CPU_MODEL}', drew '$(machine_model)' — stopping before any measurement" >&2
  exit 0
fi
rec gate open
rec kernel "$(uname -r)"; rec nproc "$NPROC"; rec mem_total "$(sed -n 's/^MemTotal: *//p' /proc/meminfo)"
grep -m1 -o -w -E 'avx512f|avx2' /proc/cpuinfo | sort -u | tr '\n' ' ' > "$OUT/cpuflags.txt"; rec cpu.flags "$(cat "$OUT/cpuflags.txt")"
df -h / /mnt /tmp > "$OUT/df.txt" 2>&1
DIR=/tmp/llm
if [ -d /mnt ] && sudo mkdir -p /mnt/llm 2>/dev/null && sudo chown "$(id -u):$(id -g)" /mnt/llm; then DIR=/mnt/llm; fi
mkdir -p "$DIR"; rec llm.dir "$DIR"

sudo apt-get update > "$OUT/apt.update.log" 2>&1; rec apt.update.rc "$?"
sudo apt-get install -y --no-install-recommends cmake build-essential libcurl4-openssl-dev libssl-dev > "$OUT/apt.build.log" 2>&1; rec apt.build.rc "$?"
rec cmake.version "$(cmake --version | head -1)"; rec gcc.version "$(gcc --version | head -1)"
SRC="$DIR/llama.cpp"; mkdir -p "$SRC"
( cd "$SRC" && git init -q && git fetch -q --depth 1 https://github.com/ggml-org/llama.cpp "$LLAMA_SHA" && git checkout -q FETCH_HEAD ) > "$OUT/git.log" 2>&1
rec llama.sha "$(git -C "$SRC" rev-parse HEAD 2>/dev/null)"
t0=$(now_us)
( cd "$SRC" && cmake -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build --config Release -j "$NPROC" --target llama-server llama-bench ) > "$OUT/build.log" 2>&1
rec llama.build.rc "$?"; rec llama.build_s "$(( ($(now_us) - t0) / 1000000 ))"
BIN="$SRC/build/bin"
grep -E "GGML_(NATIVE|AVX[0-9A-Z_]*|FMA|F16C|BMI2)|CMAKE_BUILD_TYPE" "$SRC/build/CMakeCache.txt" > "$OUT/cmakecache.txt" 2>/dev/null
rec llama.version "$("$BIN/llama-server" --version 2>&1 | tr '\n' ' ' | head -c 200)"

echo "$MODELS" | while IFS='|' read -r name repo rev file sha; do
  M="$DIR/$file"
  t0=$(now_us)
  curl -sSL --retry 3 -o "$M" "https://huggingface.co/$repo/resolve/$rev/$file"; rec "model.$name.curl.rc" "$?"
  rec "model.$name.download_s" "$(( ($(now_us) - t0) / 1000000 ))"
  rec "model.$name.bytes" "$(stat -c %s "$M" 2>/dev/null)"
  got="$(sha256sum "$M" | cut -d' ' -f1)"; rec "model.$name.sha256" "$got"
  if [ "$got" != "$sha" ]; then rec "model.$name.verified" 0; continue; fi
  rec "model.$name.verified" 1
  sync; echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null   # every repeat loads the model from disk
  t0=$(now_us)
  "$BIN/llama-server" -m "$M" -t "$NPROC" -c 4096 -np 1 --host 127.0.0.1 --port 8080 > "$OUT/server.$name.log" 2>&1 &
  SPID=$!
  up=0
  for _ in $(seq 1 600); do
    if curl -sf http://127.0.0.1:8080/health > /dev/null 2>&1; then up=1; break; fi
    kill -0 "$SPID" 2>/dev/null || break
    sleep 0.2
  done
  rec "server.$name.up" "$up"; rec "server.$name.load_ms" "$(( ($(now_us) - t0) / 1000 ))"
  if [ "$up" = 1 ]; then
    python3 "$HERE/request.py" http://127.0.0.1:8080 "$HERE" "$N_REQ" > "$OUT/requests.$name.jsonl" 2> "$OUT/requests.$name.err"
    rec "requests.$name.rc" "$?"
  fi
  kill "$SPID" 2>/dev/null; wait "$SPID" 2>/dev/null
  # shellcheck disable=SC2086
  "$BIN/llama-bench" -m "$M" -t "$NPROC" $BENCH -o json > "$OUT/bench.$name.json" 2> "$OUT/bench.$name.err"
  rec "bench.$name.rc" "$?"
  rm -f "$M"
done

rec finished_utc "$(date -u +%FT%TZ)"
finish_report
