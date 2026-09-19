#!/usr/bin/env bash
# clamav_db.sh <dir> <daily> <main> <bytecode> — fetch the campaign's fixed ClamAV signature database into <dir> and
# check its versions (9.6 changelog D27). meas-build.yml caches <dir> under a key naming the three versions, so every
# repeat from repeat 9 on scans with the same database; a fetch that returns other versions fails, and nothing is cached.
set -euo pipefail
DIR="$1"; WANT_DAILY="$2"; WANT_MAIN="$3"; WANT_BYTECODE="$4"

sudo apt-get update -qq
sudo apt-get install -y -qq --no-install-recommends clamav clamav-freshclam > /dev/null
sudo systemctl stop clamav-freshclam || true   # the service holds freshclam's lock
sudo freshclam || echo "freshclam rc $? (the versions below decide)"
mkdir -p "$DIR"
pick() { local ext; for ext in cvd cld; do [ -f "$1/$2.$ext" ] && { echo "$1/$2.$ext"; return 0; }; done; return 1; }
for db in daily main bytecode; do
  f="$(pick /var/lib/clamav "$db")" || { echo "no $db database in /var/lib/clamav" >&2; exit 1; }
  cp "$f" "$DIR/"
done
chmod -R a+rX "$DIR"

version() { sigtool --info "$(pick "$DIR" "$1")" | sed -n 's/^Version: *//p'; }
have="daily $(version daily), main $(version main), bytecode $(version bytecode)"
want="daily $WANT_DAILY, main $WANT_MAIN, bytecode $WANT_BYTECODE"
echo "fetched: $have"
ls -la "$DIR"
[ "$have" = "$want" ] || { echo "want $want: the fixed database is no longer the current one" >&2; exit 1; }
