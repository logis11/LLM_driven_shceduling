#!/usr/bin/env bash
# tools.sh — what the runner has: perf for its kernel, perf_event_paranoid,
# tracefs, /dev/uinput, sound devices and modules, audio servers, replay tools.
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"
export DEBIAN_FRONTEND=noninteractive
rec kernel "$(uname -r)"; rec os "$(. /etc/os-release; echo "$PRETTY_NAME")"
python3 "$TOOLS/../runner_spec.py" > "$OUT/spec.json"; rec spec.rc "$?"
sudo apt-get update > /dev/null 2>&1
run_rec apt.policy.linux-tools apt-cache policy "linux-tools-$(uname -r)" linux-tools-azure linux-tools-common
sudo apt-get install -y linux-tools-common "linux-tools-$(uname -r)" > "$OUT/apt.perf.log" 2>&1; rec apt.perf_exact.rc "$?"
if ! perf --version > /dev/null 2>&1; then sudo apt-get install -y linux-tools-azure >> "$OUT/apt.perf.log" 2>&1; rec apt.perf_azure.rc "$?"; fi
rec perf.version "$(perf --version 2>&1 | head -1)"
rec perf_event_paranoid "$(cat /proc/sys/kernel/perf_event_paranoid)"
rec kptr_restrict "$(cat /proc/sys/kernel/kptr_restrict)"
run_rec perf.sched.record.user perf sched record -o "$OUT/perf.user.data" -- sleep 1
run_rec perf.sched.record.sudo sudo perf sched record -a -o "$OUT/perf.sudo.data" -- sleep 3
run_rec perf.sched.timehist.sudo sudo perf sched timehist -i "$OUT/perf.sudo.data"
rec perf.timehist.rows "$(wc -l < "$OUT/perf.sched.timehist.sudo.out")"
rec tracefs.mounted "$(mount | grep -c tracefs)"
rec tracefs.readable_sudo "$(sudo ls /sys/kernel/tracing/ > /dev/null 2>&1 && echo 1 || echo 0)"
run_rec trace_cmd.policy apt-cache policy trace-cmd bpftrace
rec dev.uinput "$([ -e /dev/uinput ] && echo 1 || echo 0)"
rec dev.input "$(ls /dev/input 2>/dev/null | tr '\n' ' ')"
rec dev.snd "$(ls /dev/snd 2>/dev/null | tr '\n' ' ')"
rec lsmod.snd "$(lsmod | grep -c '^snd')"
run_rec modprobe.snd_dummy sudo modprobe snd-dummy
run_rec modprobe.uinput sudo modprobe uinput
rec dev.uinput.after_modprobe "$([ -e /dev/uinput ] && echo 1 || echo 0)"
rec config.uinput "$(grep -E 'CONFIG_INPUT_UINPUT|CONFIG_SND=' /boot/config-"$(uname -r)" 2>/dev/null | tr '\n' ' ')"
run_rec apt.policy.replay apt-cache policy xdotool ydotool evemu-tools python3-xlib
sudo apt-get install -y --no-install-recommends xdotool evemu-tools pulseaudio pipewire pipewire-pulse wireplumber pulseaudio-utils alsa-utils > "$OUT/apt.audio.log" 2>&1; rec apt.audio.rc "$?"
run_rec aplay.l aplay -l
run_rec pactl.info.before pactl info
pulseaudio --start --exit-idle-time=-1 > "$OUT/pulse.log" 2>&1; rec pulseaudio.start.rc "$?"; sleep 2
run_rec pactl.info.pulse pactl info
run_rec pactl.sinks pactl list short sinks
pulseaudio --kill 2>/dev/null; sleep 1
XDG_RUNTIME_DIR=/run/user/$(id -u) ; export XDG_RUNTIME_DIR; mkdir -p "$XDG_RUNTIME_DIR" 2>/dev/null
(pipewire > "$OUT/pipewire.log" 2>&1 &); (wireplumber > "$OUT/wireplumber.log" 2>&1 &); (pipewire-pulse > "$OUT/pipewire-pulse.log" 2>&1 &); sleep 3
run_rec pw.cli.ls pw-cli ls Node
run_rec pw.top pw-top -b -n 2
rec finished_utc "$(date -u +%FT%TZ)"
finish_report
