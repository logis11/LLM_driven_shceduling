#!/bin/bash
# dejadup-session.sh <mode> <out dir> — the Déjà Dup campaign's session (9.10 D112–D118; method §2, §3). Run by run.sh
# inside the chroot, as the user, under a session bus of its own (dbus-run-session), with DISPLAY, XDG_RUNTIME_DIR,
# DD_KEYRING_PW and DD_FOLDER in its environment. Every mode records Déjà Dup's settings as it leaves them.
#   first    the keyring unlocked; the location written as Déjà Dup's location page stores it (D114); the first
#            backup by `deja-dup --backup`, its assistant worked from the harness CPUs (dejadup_first.py); then the
#            password the keyring holds for Déjà Dup (D117) and Déjà Dup's cache folder
#   week     "Back Up Automatically" on; last-backup and last-run 8 days back (D118)
#   monitor  the keyring unlocked; deja-dup-monitor started, as the session's autostart would (D112); the script then
#            waits on it, so the session lives until run.sh stops it after the phase
#   read     the settings, Déjà Dup's cache folder and the drive's files, after the phase
MODE="$1"; L="$2"
settings() { gsettings list-recursively org.gnome.DejaDup > "$L/dejadup.settings.$1.txt" 2>&1; }
unlock() {   # the default layer's gnome-keyring (D117): the login keyring unlocked, or made, with the design password
  printf '%s' "$DD_KEYRING_PW" | gnome-keyring-daemon --unlock --components=secrets > "$L/keyring.$MODE.unlock.txt" 2>&1
  echo "keyring_unlock_rc=$?"
  gnome-keyring-daemon --start --components=secrets > "$L/keyring.$MODE.start.txt" 2>&1
  echo "keyring_start_rc=$?"
}
items() {   # the Secret Service's items for Déjà Dup's schema (CommonUtils.vala store_passphrase: owner, type)
  gdbus call --session --dest org.freedesktop.secrets --object-path /org/freedesktop/secrets \
    --method org.freedesktop.Secret.Service.SearchItems "{'owner': 'deja-dup', 'type': 'passphrase'}" > "$L/keyring.items.$1.txt" 2>&1
  echo "keyring_items_rc=$?"
}
cache() { ls -laR "$HOME/.cache/deja-dup" > "$L/dejadup.cache.$1.txt" 2>&1; }
env | sort > "$L/dejadup.env.$MODE.txt"
case "$MODE" in
  first)
    unlock
    gsettings set org.gnome.DejaDup backend "'local'"; echo "set_backend_rc=$?"
    gsettings set org.gnome.DejaDup.Local folder "'$DD_FOLDER'"; echo "set_folder_rc=$?"
    settings first-before
    t0=$(date +%s)
    deja-dup --backup > "$L/dejadup.first.log" 2>&1; echo "first_rc=$?"
    echo "first_s=$(( $(date +%s) - t0 ))"
    settings first-after; items first; cache first ;;
  week)
    gsettings set org.gnome.DejaDup periodic true; echo "set_periodic_rc=$?"
    T="$(date -u -d '8 days ago' +%Y-%m-%dT%H:%M:%S.%6NZ)"; echo "week_back=$T"
    gsettings set org.gnome.DejaDup last-backup "'$T'"; echo "set_last_backup_rc=$?"
    gsettings set org.gnome.DejaDup last-run "'$T'"; echo "set_last_run_rc=$?"
    settings week ;;
  monitor)
    unlock; items monitor; settings monitor-before
    /usr/libexec/deja-dup/deja-dup-monitor > "$L/dejadup.monitor.log" 2>&1 &
    echo "monitor_pid=$!"
    wait ;;
  read)
    settings after; cache after
    find "$HOME/.cache/deja-dup" -maxdepth 2 -type f -size -1M ! -name '*.sigtar*' ! -name '*.manifest*' \
      -exec sh -c 'for f; do echo "== $f"; tail -c 20000 "$f"; done' _ {} + > "$L/dejadup.cache-files.after.txt" 2>&1 ;;
esac
