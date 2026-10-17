# Task 9.16 claim audit — blind reader B4: independent reads

Reader B4, the blind reader for the claims outside the workload dataset. Phase 1 of the blind re-read: the reader saw only `claims/outside-blind-topics.md` (the topic list and bibliographic entries) and nothing else in the repository while writing this file. Access date for every copy: 2026-10-17. All local copies are under `/private/tmp/claude-501/-Users-jiohin-Desktop-future-of-sw-LLM-driven-shceduling/43e369a1-b5c7-40a2-b57d-cc4fcdb568dc/scratchpad/blind/` (written `<scratch>/` below). Hashes are SHA-256 of the local file. Where a source could not be reached it says so; nothing below is reconstructed from memory.

Topic names: the topics file numbers its topics T-01 … T-20 (claims whose wording changed after their read) and S-01 … S-04 (random spot checks); each heading below gives the topic's subject next to its number.

---

## T-01 — Chambers et al., IMC 2005: session times on a busy Counter-Strike server

**Copy read.** www.usenix.org/legacy/event/imc05/tech/full_papers/chambers/chambers.pdf (14 pages, Proc. IMC '05, USENIX Association), `<scratch>/t01/chambers.pdf`, sha256 `6d9dea3b145f9513917b82a636702d966286bb3a17734c53280067d7be0a0c3a`.

**Passages.**
- p. 2, §2 Methodology, the trace: "we examined the activity of one of the busiest and longest running Counter-Strike servers in the country located at cs.mshmro.com [14, 15]. … The server averages more than 40,000 connections per week, has hosted more than 400,000 unique players within the last year, and has logged more than 60 player years in activity since its launch in August 2001."
- p. 4, §3.2 "Gamers have short attention spans": "Using the same trace, we extracted the total session time of each player session contained in the trace. Figure 2 plots the session time distributions of the trace in unit increments of a minute."
- p. 4, §3.2: "Figure 2(b) shows the cumulative density function for the session times of the trace. As the figure shows, more than 99% of all sessions last less than 2 hours."
- p. 4, §3.2: "Unlike the player patience data, session times can not be fitted with a simple negative exponential distribution. However, the data can be closely matched to a Weibull distribution …"
- p. 4, §3.2: "In this form, β is a shape parameter or slope of the distribution, η is a scale parameter, and γ is a location parameter. As the location of the distribution is at the origin, γ is set to zero, giving us the two-parameter form for the Weibull PDF."
- p. 4, §3.2: "Using a probability plotting method [22], we estimated the shape (β) and scale (η) parameters of the session time PDF. As Figure 2(a) shows, a Weibull distribution with β = 0.5, η = 20, and γ = 0 closely fits the PDF of measured session times for the trace."
- p. 4, Figure 2(a) legend: "Weibull β=0.5, η=20, γ=0"; x axis "Minutes".
- §3.4 player interest (p. 5): "Figure 5(a) shows that player session times are relatively constant halfway through their play history and fall off to just more than 50% of the initial session time before the player loses interest completely." (Figure 5(a) is titled "Average session time", y axis "Session time (in minutes)", plotted over normalised play history, no value given in text.)
- Search of the full text: the word "median" does not occur; no numeric mean or median of session time is stated in the text.

**Reading.** Session durations of the cs.mshmro.com trace are fitted with a two-parameter Weibull (shape β = 0.5, scale η = 20, location γ = 0); the unit of the plot is minutes (unit increments of a minute), so η = 20 is read as 20 minutes, though the text never writes "η = 20 minutes". More than 99% of sessions last less than 2 hours. The paper states no median or mean session time; any central value (for example the Weibull median 20·(ln 2)² ≈ 9.6 min or mean 20·Γ(3) = 40 min) would be derived, not stated.

---

## T-02 — Fiedler's game loop, mpv's audio output, Chromium's fake audio worker

### (1) Fiedler, "Fix Your Timestep!"
**Copy read.** gafferongames.com/post/fix_your_timestep/ (page dated "Jun 10, 2004"), `<scratch>/t02/fiedler.html`, sha256 `fbaf9d77e5960386776b42d9228d33192b6c43e02976defae3e6f1cf4fbf599f`.

**Passages.**
- § "Semi-fixed timestep": "… if your simulation is the most expensive part of your frame you could run into the so called “spiral of death”." / "So how do we avoid this? … If you can do this then your physics engine can “catch up” from any temporary spike by simulating more frames. Alternatively you can clamp at a maximum # of steps per-frame and the simulation will appear to slow down under heavy load."
- § "Free the physics": "the renderer produces time and the simulation consumes it in discrete dt sized steps." Code: `accumulator += frameTime; while ( accumulator >= dt ) { integrate( state, t, dt ); accumulator -= dt; t += dt; } render( state );`
- § "Free the physics": "This left over time is passed on to the next frame via the accumulator variable and is not thrown away."
- § "Free the physics": "if the display framerate is 50fps and the simulation runs at 100fps then we need to take two physics steps every display update."
- § "The final touch", final listing: `double frameTime = newTime - currentTime; if ( frameTime > 0.25 ) frameTime = 0.25;` then the same `while ( accumulator >= dt )` loop, then interpolation by `alpha = accumulator / dt` and one `render( state );` per loop iteration.

**Reading.** When more real time than one step has passed, the fixed-timestep loop runs as many whole dt steps as the accumulated time holds (floor(accumulator/dt)), carrying the remainder; it renders once per outer loop iteration. The final listing clamps the frame time added per iteration at 0.25 s (so at most 0.25/dt steps per frame, 25 at dt = 0.01); the text separately offers clamping a maximum number of steps per frame as an alternative to catching up.

### (2) mpv audio output, tag `v0.37.0` (`818ce7c51a6b9179307950e919983e0909942098`, verified by `git ls-remote` as the peeled tag)
**Copies read.** raw.githubusercontent.com/mpv-player/mpv/818ce7c5…/<path>:
- `audio/out/buffer.c` → `<scratch>/t02/mpv/audio_out_buffer.c`, sha256 `954b35dd2e8dab0c11ae4bdbc6a9ecbe8d0a7b1a2e98b79380235e7ab0e73b59`
- `audio/out/ao_null.c` → `<scratch>/t02/mpv/audio_out_ao_null.c`, sha256 `264d64ec92c8d0e5f68edbedf318cfa2dad2370695dfa3213dc03b78c02a6b76`
- `osdep/threads-posix.h` → `<scratch>/t02/mpv/osdep_threads-posix.h`, sha256 `0b0d426cee45954edb078a18ab61ee16d49c5d7c5dbde50a259d7e2b59ad37a1`

**Passages.**
- buffer.c:606–623 `ao_play_data`: `get_dev_state(ao, &state); if (p->streaming && !state.playing && !ao->untimed) goto eof; … int space = state.free_samples; if (!space) return false;`
- buffer.c:646: `samples = read_buffer(ao, planes, space, &got_eof, true);` then buffer.c:653: `if (!ao->driver->write(ao, planes, samples))`.
- buffer.c:674–681 (eof label): `MP_VERBOSE(ao, "audio end or underrun\n"); // Normal AOs signal EOF on underrun, untimed AOs never signal underruns. if (ao->untimed || !state.playing || ao->stream_silence) { p->streaming = state.playing && !ao->untimed; p->playing = false; } ao->wakeup_cb(ao->wakeup_ctx);`
- buffer.c:687–725 `playthread`: `retry = ao_play_data(ao); // Wait until the device wants us to write more data to it. // Fallback to guessing. … // Wake up again if half of the audio buffer has been played. // Since audio could play at a faster or slower pace, wake up twice // as often as ideally needed. timeout = MP_TIME_S_TO_NS(ao->device_buffer / (double)ao->samplerate * 0.25); … mp_cond_timedwait(&p->pt_wakeup, &p->pt_lock, timeout);`
- buffer.c:353–355 comment on `ao_start`: "Initiate playback. This moves from the stop/underrun state to actually playing … Plays all data in the queue, and goes into underrun state if no more data available."
- ao_null.c:212–216 defaults: `.bufferlen = 0.2, .outburst = 256, .speed = 1,`; ao_null.c:105–107: `int bursts = (int)(ao->samplerate * priv->bufferlen + 1) / priv->outburst; ao->device_buffer = priv->outburst * bursts + priv->latency;`
- ao_null.c:63–82 `drain`: buffered samples decrease by elapsed wall time, `if (priv->buffered < 0) priv->buffered = 0;`; ao_null.c:175–176 `state->free_samples = ao->device_buffer - priv->latency - priv->buffered; state->free_samples = state->free_samples / priv->outburst * priv->outburst;`; ao_null.c:196 `state->playing = priv->playing && priv->buffered > 0;`
- threads-posix.h:184–203 `mp_cond_timedwait`: relative timeout turned into an absolute `pthread_cond_timedwait` deadline.

**Reading.** Each wake-up the output thread writes the device's whole free space (null output: free space rounded down to 256-sample bursts), as much queued audio as is available up to that space. It waits a quarter of the device-buffer duration between wake-ups (null output: buffer ≈ 0.2 s, so ≈ 50 ms), or is woken earlier. When the device buffer has run empty (`state.playing` false), the code takes the underrun path ("audio end or underrun"): playback stops (`p->playing = false`) and the player is notified; nothing in buffer.c discards the queued audio, and `ao_start` later "plays all data in the queue". So at this layer audio due earlier is played later, not dropped; the null output's clock clamps at zero, so lost wall time is not credited back. What the player core does after the underrun signal is outside these files.

### (3) Chromium, tag `152.0.7977.82` (`d04cdb24d67b081f6cf80200ffc5233f44b61109`, verified by `git ls-remote`)
**Copies read.** chromium.googlesource.com/chromium/src/+/d04cdb24…/<path>?format=TEXT:
- `media/base/fake_audio_worker.cc` → `<scratch>/t02/chromium/fake_audio_worker.cc`, sha256 `eddbc3edff85e6e5a4617974b148776fa02c4b10ecd71c46ec95bada22381e5b`
- `media/audio/fake_audio_output_stream.cc` → `<scratch>/t02/chromium/fake_audio_output_stream.cc`, sha256 `850fd29ea0bd837b8d9b190f0179707859da4727d9485e6df4bfd768043f6823`
- `media/audio/audio_output_resampler.cc` → `<scratch>/t02/chromium/audio_output_resampler.cc`, sha256 `14a802796c84311a83aa16c3b973113ad788c90f9a29169256abe0015f18c436`

**Passages.**
- fake_audio_worker.cc:163–182 `DoRead`: `read_time = first_read_time_ + FramesToTime(frames_elapsed_, …); frames_elapsed_ += frames_per_read_; … // Note: Even if we're late, this callback must be called. In many cases we // are driving an underlying "samples consumed" based clock with these // calls. if (worker_cb_) worker_cb_.Run(read_time, now);`
- fake_audio_worker.cc:184–193: `// If we're behind, find the next nearest ontime interval. Note, we could be // behind many intervals (e.g., if the system is resuming from sleep). if (next_read_time <= now) { frames_elapsed_ = TimeToFrames(now - first_read_time_, …); frames_elapsed_ = ((frames_elapsed_ / frames_per_read_) + 1) * frames_per_read_; next_read_time = …; }`
- fake_audio_worker.cc:198–201: `PostDelayedTaskAt(…, worker_task_cb_.callback(), next_read_time, base::subtle::DelayPolicy::kPrecise);`
- fake_audio_output_stream.cc:68–75 `CallOnMoreData`: `const auto delay = fixed_data_delay_ + std::max(base::TimeDelta(), ideal_time - now); callback_->OnMoreData(delay, now, {}, audio_bus_.get());`
- audio_output_resampler.cc:321–325: "// Fallback is available for low latency streams only."; :342–381 (Windows only) fall back to non-offload then to high-latency output; :383–394: `DLOG(ERROR) << "Unable to open audio device in high latency mode.  Falling " << "back to fake audio output."; // Finally fall back to a fake audio output device. output_params_ = input_params_; output_params_.set_format(AudioParameters::AUDIO_FAKE);`

**Reading.** A late callback still runs exactly once (one buffer per late wake-up); if the next deadline is already past, the worker skips forward to the next whole interval after now, so missed intervals are not run. Chromium uses this fake output as the last fallback when a low-latency output stream cannot be opened on the real device (on Windows after the non-offload and high-latency attempts).

---

## T-03 — Periodic tasks whose activation time has passed; rt-app's units

### rt-app at `d6f8be41107642fd6ab41bc1ab3bb01a486fd00e` (2026-06-10, "Merge pull request #151 …"; github.com/scheduler-tools/rt-app, git clone)
**Copies.** `doc/tutorial.txt` → `<scratch>/t03/rtapp-copies/tutorial.txt` sha256 `a3e8823ebae6fda9893327637a48ab195f98206b00ad857a8cc736414d9ee3e7`; `src/rt-app.c` → `<scratch>/t03/rtapp-copies/rt-app.c` sha256 `61431c72171ee3234e8c7f0dfc2b7f7354beebd8d8850a4e30f5837616666eb8`; `src/rt-app_parse_config.c` → `<scratch>/t03/rtapp-copies/rt-app_parse_config.c` sha256 `850fdc1ade6ed8f8813af491f62d00d0dd924cfba0c1666cbda5e09774341fc3`.

**Passages.**
- tutorial.txt:36: "* duration : Integer. Duration of the use case in seconds. All the threads will be killed once the duration has elapsed. if -1 has been set, the use case will run indefinitly …"
- tutorial.txt:156: "* delay: Integer. Initial delay before a thread starts execution. The unit is usec."
- tutorial.txt:221–235: "* dl-runtime : Integer: … Default value is 0. The unit is usec." / "* dl-period : Integer. … Default value is runtime. The unit is usec." / "* dl-deadline : Integer. … Default value is period. The unit is usec."
- tutorial.txt:350–351: "* run : Integer. Emulate the execution of a load. The duration is defined in usec …"; :361 "* runtime : Integer. The duration is define in usec."; :366–367 "* sleep : Integer. Emulate the sleep of a task. The duration is defined in usec."
- tutorial.txt:447–452: "* timer : Object. Emulate the wake up of the thread by a timer. … Sleep duration starts at the beginning of the sleep event whereas timer duration starts at the end of the last use of the timer. … The initial starting time of the timer is set during the 1st use of the latter." (The timer object's `period` key has no unit stated in the timer paragraph; examples use 20000, 30000; the log columns list "c_period: sum of the timer(s) period(s) [us]", tutorial.txt:789.)
- tutorial.txt:507–509: "Timers can work with a "relative" or an "absolute" reference. By default they work in "relative" mode …"
- tutorial.txt:518–537: ""relative" mode means that the reference for setting the next timer event is relative to the end of the current phase. … Third activation of Timer0 is missed, since r0 executed for more that 20ms. However the next phase is not affected as Timer0 was set considering the instant of time when the misbehaving r0 finished executing."
- tutorial.txt:548–567: ""absolute" mode means that the reference for setting the next timer event is fixed and always consider the starting time of the first phase. … the next phase (and potentially other subsequent phases) _will_ be affected. … 4th Timer0 is still missed because the reference didn't change. In this example 5th activation of r0 then managed to recover …"
- rt-app.c:574–596: `t_period = usec_to_timespec(event->duration); … rdata->res.timer.t_next = timespec_add(&rdata->res.timer.t_next, &t_period); clock_gettime(CLOCK_MONOTONIC, &t_now); … if (timespec_lower(&t_now, &rdata->res.timer.t_next)) { clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, &rdata->res.timer.t_next, NULL); … } else { if (rdata->res.timer.relative) clock_gettime(CLOCK_MONOTONIC, &rdata->res.timer.t_next); ldata->wu_latency = 0UL; }`
- rt-app_parse_config.c:213 `data->res.timer.relative = 1;`; :857 `data->duration = get_int_value_from(obj, "period", TRUE, 0);`; :861–863 `tmp = get_string_value_from(obj, "mode", TRUE, "relative"); if (!strncmp(tmp, "absolute", …)) rdata->res.timer.relative = 0;`

**Reading.** rt-app timer, activation already passed: no sleep in either mode; relative mode (the default) re-anchors the next activation to "now"; absolute mode keeps the old reference, so later timer events also return without sleeping until the schedule is caught up (accumulate / catch up). Units: run, runtime, sleep, delay, dl-runtime, dl-period, dl-deadline in microseconds and Integer; the timer period is passed through `usec_to_timespec` (microseconds) and parsed as an int, its unit not written in the timer paragraph; the global duration is an Integer in seconds.

### interbench at `e612a65ce941028ddea804e6b45ccde2750720d2` (2016-10-24; version string `INTERBENCH_VERSION "0.31"`, interbench.c:25)
**Copies.** `interbench.c` → `<scratch>/t15/interbench.c` sha256 `a381b94085427cda4169466d3833c272fe4e9672cfbad74a64897621db7f2191`; `interbench.8` → `<scratch>/t15/interbench.8` sha256 `31bc88e508bb7f81cc01a4ef632fbee4f4acb908082140427acba11ca2ee92ee`.

**Passages.**
- interbench.c:398–411 `periodic_schedule`: `if (interval_usecs && current_time > deadline + interval_usecs) { /* We missed the deadline even before we consumed cpu */ … intervals = (current_time - deadline) / interval_usecs + 1; tb->missed_deadlines += intervals; … deadline += intervals * interval_usecs; tb->missed_burns += intervals; goto bypass_burn; }`
- interbench.c:418–437: "/* If we meet the deadline we move the deadline forward, otherwise we consider it a missed deadline and dropped frame etc. */" … `deadline += intervals * interval_usecs;`
- interbench.8:186–195: "… some deadlines were so late … that some redraws were dropped entirely to catch up. In X terms this would translate into jerky movement, in audio it would be a skip, and in video it would be a dropped frame. … This is because redraws are dropped in order to catch up usually by these sorts of applications."

**Reading.** interbench's periodic loads (audio, video, X) skip: when behind, the deadline is advanced past now by whole intervals, the skipped intervals are counted as missed deadlines/burns, and their work is not run.

### Teper et al., arXiv:2408.03696v1 (7 Aug 2024)
**Copy.** arxiv.org/pdf/2408.03696v1 → `<scratch>/t03/teper-2408.03696v1.pdf`, sha256 `26bde904e5fd547813fc6c6a5a0906e20cb3307c4f7dc0a0a7438d51219c0754` (12 pages).

**Passage.** p. 3 (§ on the default ROS 2 executor): "The mechanism of the default executor for timers is as follows: Each timer stores its next activation time at which it will be eligible for execution. At the moment at which the executor determines if a timer is eligible, it checks whether the current time is greater than or equal to the activation time of the timer. If so, a job of that timer is sampled, and the next activation time point is determined by increasing the current activation time by the minimal multiple of the timer period, such that it is greater than the current time. As a result, the executor may skip timer jobs if the time between two polling points is longer than the period of the timer …"

**Reading.** ROS 2's default executor skips to the next activation after now (one job sampled, missed ones skipped), keeping the original phase.

### Lipari & Palopoli, arXiv:1512.01978v1 (7 Dec 2015)
**Copy.** arxiv.org/pdf/1512.01978v1 → `<scratch>/t03/lipari-1512.01978v1.pdf`, sha256 `b12b9b96b5297c09be94451a324a5c2455fb2f24a25bd7959bc042c067a44085` (24 pages).

**Passages.**
- §2.1 "Hard real-time tasks", Listing 1 "Structure of a periodic thread in Linux" (p. 5): `clock_gettime(CLOCK_REALTIME, &next); while (1) { // Job execution // Check deadline miss … if (timespec_cmp(&now, &dline) > 0) pthread_exit(0); // Wait until next period timespec_add_us(&next, ps->period_us); clock_nanosleep(CLOCK_REALTIME, TIMER_ABSTIME, &next, NULL); }`
- Text after Listing 1: "At the end of the execution, we check if the deadline has been missed, in which case we abort the thread. Otherwise the thread suspends itself waiting for the next periodic activation (at time next)."
- §3.1 "Soft real-time tasks" (p. 10): "As an alternative, we can decide to skip future instances …" and "In Listing 2 we show an example of how to combine these techniques by using SCHED_DEADLINE for budget control, and by skipping all late instances if a deadline has been missed (lines 18-20)." Listing 2: `while (timespec_cmp(&now, &next) > 0) { // Skip late instances timespec_add_us(&next, ps->dline_us); }`

**Reading.** The reference periodic thread (Listing 1) advances `next` by one period from the previous activation and sleeps with an absolute deadline; if `next` is already past, `clock_nanosleep` returns at once, so late activations run back-to-back (accumulate) — but this listing aborts the thread on any deadline miss. The soft real-time variant (Listing 2) skips all late instances (note it advances by `dline_us`, not `period_us`).

### mpv default video output, tag `v0.37.0`
**Copies.** `DOCS/man/options.rst` → `<scratch>/t02/mpv/DOCS_man_options.rst` sha256 `f7fedcc5cd5bd0f8c76413417e78f4a3318ab306f864571eb87ef9321cc316a4`; `video/out/vo.c` → `<scratch>/t02/mpv/video_out_vo.c` sha256 `2a59dbf041a2386860a063c553d062c5db53d35991bf1a2da50e1c216825d9fb`.

**Passages.**
- options.rst:1134–1151: "``--framedrop=<mode>`` Skip displaying some frames to maintain A/V sync on slow systems … <vo> Drop late frames on video output (default). This still decodes and filters all frames, but doesn't render them on the VO. … In audio sync. mode, this drops frames that are outdated at the time of display. … frame dropping stops if the effective framerate is below 10 FPS."
- vo.c:886–895: `// "normal" strict drop threshold. in->dropped_frame = duration >= 0 && end_time < now; … // Even if we're hopelessly behind, rather degrade to 10 FPS playback, // instead of just freezing the display forever. in->dropped_frame &= now - in->prev_vsync < MP_TIME_MS_TO_NS(100);`

**Reading.** mpv's default (`--framedrop=vo`) drops a frame whose display interval has already ended (skip), except it renders at least every 100 ms (≥ 10 fps).

---

## T-04 — GStreamer's sinks and late buffers

**Copies.** gitlab.freedesktop.org/gstreamer/gstreamer, commit `83e7df9168dd73f5dcd1caa60195a9d9dce558b4` (2026-09-23, "tfliteinference: Fix caps handling …", via GitLab API). The monorepo paths are `subprojects/gstreamer/libs/gst/base/gstbasesink.c` → `<scratch>/t04/gstbasesink.c` sha256 `43a7223ce9ab63dc0bae4868f0660d6bf3e4e3201cf883eaee21cac2addd14c7`; `subprojects/gst-plugins-base/gst-libs/gst/video/gstvideosink.c` → `<scratch>/t04/gstvideosink.c` sha256 `cbaceaada60cad03ecf75d397eb529d82ede5d15d5dd57cbdb7134e62b65c30c`.

**Passages.**
- gstbasesink.c:118–129: "The #GstBaseSink:max-lateness property affects how the sink deals with buffers that arrive too late in the sink. A buffer arrives too late in the sink when the presentation time (as a combination of the last segment, buffer timestamp and element base_time) plus the duration is before the current time of the clock. If the frame is later than max-lateness, the sink will drop the buffer without calling the render method. This feature is disabled if sync is disabled, the #GstBaseSinkClass::get_times method does not return a valid start time or max-lateness is set to -1 (the default)."
- gstbasesink.c:300: `#define DEFAULT_MAX_LATENESS -1`; :461–464: `"max-lateness", "Max Lateness", "Maximum number of nanoseconds that a buffer can be late before it " "is dropped (-1 unlimited)"`.
- gstbasesink.c:3197–3216 `gst_base_sink_is_too_late`: `if (GST_CLOCK_TIME_IS_VALID (rstop)) max_lateness += rstop; … if ((late = rstart + jitter > max_lateness)) { … /* !!emergency!!, if we did not receive anything valid for more than a * second, render it anyway so the user sees something */ if (… rstart - priv->last_render_time > GST_SECOND) { late = FALSE; …`
- gstbasesink.c:4108–4112: `dropped: { priv->dropped++; GST_DEBUG_OBJECT (basesink, "buffer late, dropping");`
- gstvideosink.c:174–178: `/* 20ms is more than enough, 80-130ms is noticeable */ gst_base_sink_set_processing_deadline (GST_BASE_SINK (videosink), 15 * GST_MSECOND); gst_base_sink_set_max_lateness (GST_BASE_SINK (videosink), 5 * GST_MSECOND); gst_base_sink_set_qos_enabled (GST_BASE_SINK (videosink), TRUE);`

**Reading.** Threshold: `max-lateness`, measured past the buffer's end (stop) time; base-sink default −1 (never drop: a late buffer is rendered); the video sink sets 5 ms, so a video frame whose end is more than 5 ms past is dropped without rendering — except that if nothing was rendered for more than one second it is rendered anyway.

---

## T-05 — LAVD talk slides, Open Source Summit North America 2024

**Copy.** static.sched.com/hosted_files/ossna2024/9b/scx-lavd-oss-na24.pdf (30 pages), `<scratch>/t05/scx-lavd-oss-na24.pdf`, sha256 `e62d69cd401021f8bfedadde2c4de62b01383facaa83acce7d218af3b6402475`. Figures read from 150–400 dpi renders (`<scratch>/t05/s11-11.png`, `crop11-11.png`, `s14-14.png`, `s16-16.png`).

**Passages.**
- Slide 1: "Optimizing Scheduler for Linux Gaming / Changwoo Min / changwoo@igalia.com / April 17, 2024". (No venue named on the slide; the URL path is "ossna2024".)
- Slide 10: "We collect and analyze all scheduling activities while playing games."
- Slide 12 "Task scheduling and CPU utilization": "Around 300 tasks are scheduled while running a game. ○ Around 90% are long-living tasks; only 10% of tasks are terminated. ● Top 30-40 most frequently scheduled tasks take 95% of scheduling. ○ Around half of them are system tasks -- especially, wine, graphics, and audio servers, taking 30--40% of scheduling. ○ There are 15-20 game-specific tasks, which takes 60-70% scheduling. ● CPU utilization is moderately high -- around 65-95%, but not overloaded (i.e., no 100%)."
- Slide 14 "What makes scheduling happen?": "Preemption (e.g., timer interrupt) takes only 25-30% of scheduling. ● 70-75% of scheduling is initiated by waiting system calls – such as epoll, pipe_read, futex_wait, etc. ● In this case, a task is first scheduled out waiting for an event then it is scheduled in when the event is notified." Pie chart "Call stacks which triggered scheduling in a game": largest slice "sched_preempt (28.78%)", then "ioctl (13.25%)", "alloc (7.95%)", "unlock (7.28%)", "syscall (6.76%)", "futex_wait (5.94%)" …
- Slide 11 "Analyzed a lot of scheduling traces", panel "- 30.00 percentile of waker-waiter": nodes `wineserver[5789/0]` and `redDispatcher1…7[6345…6351/6340]`, `wine_xinput_hid[6597/6340]`; edges labelled `epoll (109665)`, `epoll (107855)`, `epoll (105654)` (redDispatcher3/7/6 → wineserver) and `pipe_read (…)` / `epoll (…)` pairs between wineserver and each of wine_xinput_hid, redDispatcher5, redDispatcher1, redDispatcher4, redDispatcher2.
- Slide 16 "Tasks are tightly linked in a graph — Task graphs of top 50 percentile of waiter-wakers": nodes `swapper[0/0]`, `SteamControlle[4908/4788]`, `winedevice.exe[7284/7273]`, `Task worker thr[7825…7828/7781]`, `dxvk-cs[7922/7781]`, `dxvk-submit[7920/7781]`, `winepulse_mainl[7991/7781]`, `winepulse_timer[7993/7781]`, `FAudio_AudioCli[7992/7781]`, `pipewire-pulse[1707/1703]`, `pipewire-pulse[1703/0]`, `pipewire[1214/1204]`; edges `sleep (…)` (swapper → SteamControlle, winedevice.exe; Task worker thr → winedevice.exe), `futex_wait (…)` (four Task worker threads → dxvk-cs; dxvk-cs → dxvk-submit; winepulse_mainl → winepulse_timer; winepulse_timer → FAudio_AudioCli), `poll`/`epoll` between winepulse_mainl, winepulse_timer, pipewire-pulse[1703/0], pipewire-pulse[1707/1703], pipewire[1214/1204].

**Reading.** Speaker Changwoo Min (Igalia address), 17 April 2024. "Around 300 tasks" are scheduled while a game runs — the slides do not say whether that is one game process or the whole system; the deck says it collected "all scheduling activities while playing games", and the graphs include system processes. "Around half … are system tasks" is said of the top 30-40 most frequently scheduled tasks, not of all ~300. Scheduling initiators: preemption 25–30%, waiting system calls 70–75%. No slide gives a number of schedules per wake-up; slide 14 only says a task is scheduled out while waiting, then scheduled in when notified. The figures link threads of one game process (tgid 6340 on slide 11; tgid 7781 on slide 16) with other processes (wineserver; pipewire, pipewire-pulse, winedevice.exe, SteamController, swapper) through epoll, pipe_read, futex_wait, poll and sleep.

---

## T-06 — Who develops LAVD, and Valve's role

### LWN
**Copy.** lwn.net/Articles/1051430/ → `<scratch>/t06/lwn-1051430.html`, sha256 `4a7b994f2e866490c36c3add7dffcb784f4e197e04fc642d545565b55c871af8` (By Jake Edge, January 7, 2026).
**Passages.** "At the 2025 Linux Plumbers Conference (LPC), held in Tokyo in mid-December, Changwoo Min led a session on what he has learned while developing the "latency-criticality aware virtual deadline" (LAVD) scheduler, which is aimed at gaming workloads." / "Min said that he has been developing LAVD as part of his work at Igalia on SteamOS and the Steam Deck." / "… including one about adapting LAVD to be the default scheduler for Meta's production fleet." The word "Valve" does not occur in the article text.

### scx at `v1.1.3` (`c8728c6b6a3fde451f0f10b95f99aad7a32a750a`, peeled tag verified by `git ls-remote`)
**Copy.** sparse clone of `scheds/rust/scx_lavd/` at `<scratch>/t06/scx/`; `README.md` → `<scratch>/t06/scx_lavd_README.md` sha256 `8e4f48c103d082585d4dfea98c436818bff6530632725f65108393451f3bb65f`.
**Passages.** Cargo.toml:4 `authors = ["Changwoo Min <changwoo@igalia.com>", "Igalia"]`; src/main.rs:3–4 "// Copyright (c) 2024 Valve Corporation. // Author: Changwoo Min <changwoo@igalia.com>"; src/bpf/main.bpf.c:180–181 " * Copyright (c) 2023, 2024 Valve Corporation. * Author: Changwoo Min <changwoo@igalia.com>" (same header in every source file). README: "`scx_lavd` is initially motivated by gaming workloads."

### SteamOS release notes (Steam news, app 1675200)
**Copy.** Steam Web API `api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=1675200&count=300&maxlength=0` → `<scratch>/t06/steamnews-1675200.json`, sha256 `c05f8de95ac88f779c249d368e3a319e63b7a5ef9cc579a896878d571684142b`. (The `docs/references.md` entry the topic points to was not opened in this phase; the notes were found by searching Valve's own feed for "LAVD".)
**Passages.** Item "SteamOS 3.8" (gid 1835871199302299, 2026-06-18, author "nya"): "SteamOS 3.8.10 has just been released for all users with the following changes: … These notes contain all changes since the previous SteamOS 3.7 stable release." … under **Developer**: "Initial support for LAVD CPU scheduler via `steamosctl set-cpu-scheduler lavd`". The same line appears in "SteamOS 3.8.0 Preview: Second Clutch" (2026-03-19).

**Reading.** Developer: Changwoo Min, at Igalia (LWN quoting Min; scx author lines). Work done "on SteamOS and the Steam Deck" (Min, as reported by LWN). Valve's role: holds the copyright on the scx_lavd sources (source headers); LWN says nothing about Valve; no source read calls Valve a sponsor or employer. SteamOS: from 3.8.10 stable (18 June 2026; first in the 3.8.0 Preview) "initial support", selected by the user through `steamosctl set-cpu-scheduler lavd` — not stated as default (Valve's own notes).

---

## T-07 — Steam Deck's display refresh

**Copies.** "The SteamOS 3.2 Update" (gid 4437747060827905309, 2022-05-26) via `api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=1675200&count=50&maxlength=0&enddate=1654041600` → `<scratch>/t07/steamnews-1675200-to2022-06.json`, sha256 `a04189840d732a82b22632aac777ad54355c8da85959198d073edf399f6ef5ba` (the store page itself is JavaScript-rendered; the API returns the post body). Tech specs www.steamdeck.com/en/tech/deck → `<scratch>/t07/techspecs.html`, sha256 `eb0d1f2e1506543088eb9743e62a7e029e07bfed3bc7e6737c31c3280f062936`.

**Passages.**
- SteamOS 3.2 post, "Refresh Rate": "The default is 60Hz (which can be frame-limited to 60, 30, and 15fps), but you can now slide it down to 40Hz (with frame limits at 40, 20, and 10fps). Or any number (integer) between those two settings."
- Same post, footnote: "So 30hz = 33.33 ms/frame, and 60hz = 16.66ms/frame. Meanwhile, 40hz is 25 ms/frame."
- Tech specs, Display (current page, LCD model): "Refresh rate 60Hz".

**Reading.** Default 60 Hz with limits 60/30/15 fps; frame times stated by Valve: 60 Hz 16.66 ms, 30 Hz 33.33 ms, 40 Hz 25 ms; 15 fps (66.7 ms) is not written out.

---

## T-08 — Gregg's `perf sched` example

**Copy.** www.brendangregg.com/perf.html ("Last Updated: 29-Jul-2020") → `<scratch>/t08/perf.html`, sha256 `a60d127603220a9f74776ed9c370a3ffc2d69383366f44241d3460ab434e99a4`.

**Passages (§6.7 Scheduler Analysis).**
- "# perf sched record -- sleep 1 … [ perf record: Captured and wrote 1.886 MB perf.data (13502 samples) ]"
- "That's 1.9 Mbytes for one second, including 13,502 samples. … (this example is an 8 CPU server running a software build)."
- Header: "# captured on: Sun Feb 26 19:40:00 2017 … # os release : 4.10-virtual … # nrcpus online : 8".
- `perf sched latency` rows (Task | Runtime ms | Switches): "cat:(6) | 12.002 ms | 6", "ar:17043 | 3.191 ms | 1", "rm:(10) | 20.955 ms | 10", "objdump:(6) | 35.870 ms | 8", ":17008:17008 | 462.213 ms | 50", "grep:(7) | 21.655 ms | 11", "fixdep:(6) | 81.066 ms | 8", "mv:(10) | 30.249 ms | 14", "ld:(3) | 14.353 ms | 6", "recordmcount:(7) | 14.629 ms | 9", "svstat:17067 | 1.862 ms | 1", "cc1:(21) | 6013.457 ms | 1138", "gcc:(18) | 43.596 ms | 40", "ps:17073 | 27.158 ms | 4", then "[...]".

**Reading.** One second of scheduler events on an 8-CPU server during a software build (Linux 4.10, captured 26 Feb 2017); the summary is truncated with "[...]"; cc1 dominates (21 processes, 6013 ms runtime, 1138 switches).

---

## T-09 — Chromium's process model

**Copy.** chromium/src at `2ea968713a3de13a38d992a99b21102409b5dd1f` (committed 2026-09-13), `docs/process_model_and_site_isolation.md` → `<scratch>/t09/process_model_and_site_isolation.md`, sha256 `5a371fa56628822f38946d32ef5ce291e07ff74c1fb5a53b1eaac0249fe41bab`.

**Passages.**
- § Full Site Isolation (site-per-process): "_Used on: Desktop platforms (Windows, Mac, Linux, ChromeOS)._ In (one-)site-per-process mode, each process is locked to documents from a single site."
- § Abstractions: "Note that the user may visit multiple instances of a given principal in the browser, sometimes in unrelated tabs (i.e., separate browsing context groups). These separate instances do not need synchronous access to each other and can safely run in separate processes."
- § Process Reuse, Soft Process Limit: "On desktop platforms, Chromium sets a "soft" process limit based on the memory available on a given client. … Chromium makes an attempt to start randomly reusing same-site processes when over this limit. For example, if the limit is 100 processes and the user has 50 open tabs to `example.com` and 50 open tabs to `example.org`, then a new `example.com` tab will share a process with a random existing `example.com` tab, while a `chromium.org` tab will create a 101st process."
- § Process Locks: "a special "allow-any-site" value for processes allowed to host multiple sites"; "Full Site Isolation requires all processes to be locked, once content has been loaded in the process".

**Reading.** On desktop, a renderer process holds documents of one site only; one site can occupy many processes (separate instances run in separate processes; same-site reuse happens over the soft limit or by aggressive reuse for iframes).

---

## T-10 — Firefox tab and window telemetry (GLAM)

**Copies.** POST `glam.telemetry.mozilla.org/api/v1/data/` with `{"query":{"channel":"release","probe":<probe>,"product":"fog","app_id":"release","aggregationLevel":"version","os":"Linux","ping_type":"metrics"}}` (the API rejects the query without `app_id`): `browser_engagement_max_concurrent_tab_count` → `<scratch>/t10/glam-browser_engagement_max_concurrent_tab_count.json` sha256 `6fec1e163fc86646349b33630cb900ec8700c9fe681d975dab6cbe83b7434d68`; `…_window_count` → `<scratch>/t10/glam-browser_engagement_max_concurrent_window_count.json` sha256 `7fae93354d8666bc01cab7403453c120c1c2c53b75a90ba5cfa5821c9dbacc34`. Metric definitions: mozilla-firefox/firefox at `cf51949351fa0f0333d1db4d77a3184ed59da99c` (2026-09-26), `browser/modules/metrics.yaml` → `<scratch>/t10/metrics.yaml` sha256 `490fff8a449ddc3d89cac7e007e88234851e3408e1124980a948193380252b16`.

**Passages.**
- metrics.yaml:251–258: "max_concurrent_tab_count: type: quantity description: > The count of maximum number of tabs open during a subsession, across all windows, including tabs in private windows and restored at startup."
- metrics.yaml:290–295: "max_concurrent_window_count: … The count of maximum number of browser windows open during a subsession. This includes private windows and the ones opened when starting the browser."
- API response, fields per row: `version, ping_type, os, build_id, …, client_agg_type, total_users, sample_count, histogram, percentiles, non_norm_percentiles`. Versions served on 2026-10-17: 155, 156, 157 only; client aggregation types `sum, max, avg, count, min`; percentiles served `0.1, 1, 5, 25, 50, 75, 95, 99, 99.9`.
- Tab count, `client_agg_type = max`, median (percentile 50): 155 → 4.49 (3,328,490 clients), 156 → 4.49 (3,099,132), 157 → 3.8 (1,595,009). p95: 39.35, 33.18, 33.18; p99: 176.79, 148.86, 175.87.
- Tab count, `sum`, median: 12.23, 12.2, 8.74; `avg` median 2.72 in all three.
- Window count, `max`, median: 1, 1, 1; p95: 3.85, 4, 2.97; p99: 6.46, 6.56, 5.94.

**Reading.** The tab count is across all windows (per subsession maximum). The served data cover only the three current release versions (155–157, Linux, metrics ping); the median depends on which per-client aggregation is chosen; with the per-client maximum it is 4.49 tabs for 155 and 156 and 3.8 for 157 (157 has about half the clients), and 1 window in all three. Values are histogram bucket boundaries (exponential buckets), not exact counts.

---

## T-11 — The SWELL Knowledge Work dataset

**Copies.** The ACM DOI page and PDF returned HTTP 403 (bot block). Read instead: the authors' camera-ready PDF linked from the dataset site, cs.ru.nl/~skoldijk/Papers/ICMI 2014 paper_final_cr.pdf → `<scratch>/t11/koldijk-icmi2014-final-cr.pdf` (6 pages), sha256 `a10bffe9ea55cb66af6a8e7c2b61fbc5dfeffb3ebef57db8ef0f41cc6c1e5720`; dataset site cs.ru.nl/~skoldijk/SWELL-KW/Dataset.html → `<scratch>/t11/swellkw-dataset.html` sha256 `9f3df722d7d45e019f1815d700a042262d16096b102f4f3af7775f28b7cc2a75`; DANS Data Station version 4.0 metadata (`ssh.datastations.nl/api/datasets/:persistentId/versions/4.0?persistentId=doi:10.17026/dans-x55-69zp`) → `<scratch>/t11/dans.json` sha256 `577703cb7adf4c2921172384f9da5c6c32762d1dec9ae8903fe2791b29ec2594`; one raw uLog file from that version (datafile 171730, `a_pp16_c3_uLog_20121015_154051.xml`) → `<scratch>/t11/a_pp16_c3_uLog_20121015_154051.xml` sha256 `80a9ab64555238c1a3fb80bd64ead54766b615496fe1d476a7b8f36e54b451fa`.

**Passages.**
- Paper §3.7 Participants (p. 4): "25 students participated in our experiment, of which 8 were female and 17 male. The average age was 25 (standard deviation 3.25). Most participants were native Dutch. They were interns from TNO and students from Delft University of Technology who were approached by advertising."
- §3.1 Design (p. 3): "Neutral: … After a maximum of 45 minutes the participant was asked to stop …"; "Time pressure: the time to finish all tasks was 2/3 of the time the participant needed in the neutral condition (and maximally 30 minutes)."; "Interruptions: 8 emails were sent to the participant during the task."
- §3.2 Tasks: "The participants performed knowledge worker tasks on a desktop computer in a controlled lab setting. We asked them to write reports and make presentations on predefined topics (in English)."
- §3.3 Procedure: "The experiment was divided into three blocks for the different stressor conditions, each taking approximately one hour. Each of the experimental blocks started with a relaxation phase of about 8 minutes …"; "… the total experiment took about 3 hours."
- §3.4 Apparatus (p. 4): "Participants performed their tasks on a computer (Dell Latitude E6400) with Windows 7 Professional with a 17 inch screen and mouse and keyboard … Office 2010 … As a browser, Internet Explorer was used …"
- §3.5 Sensors: "Computer interactions were logged with the key-logging application uLog (version 3.2.5, by Noldus Information Technology), which ran as a background application on the users’ computer."
- §4 raw data: "The computer logging software recorded detailed timestamped information in XML format about each computer event. Examples of computer events are mouse clicks, mouse scrolls and application changes."
- The paper states no recording year and no timestamp resolution. DANS file names date the recordings: e.g. `PP1_C2_uLog_20120918_142524…`, `pp23_1-11-2012_c2…`, `PP25 7-11-2012` (September–November 2012).
- uLog XML event (one file, my own inspection): `<EventType>Keyboard</EventType><EventAction>character</EventAction><TimeStamp>2012-10-15T13:50:08.908276Z</TimeStamp> … <Milliseconds>908</Milliseconds> … <KeyboardValue>p</KeyboardValue><Control> … <ControlApplication>iexplore</ControlApplication><ControlWindowText>http://www.google.nl/ - Windows Internet Explorer</ControlWindowText>`. Event kinds in that file include Keyboard/character, Keyboard/special key, Mouse/clicked, Other/Window Activated, Other/Application started. Successive timestamps in that file differ by multiples of about 15.6 ms (my observation, not a source statement).

**Reading.** 25 students/interns (TNO, TU Delft), lab setting, Windows 7 desktop, recorded autumn 2012 (from DANS file names; the paper gives no year); three ~1-hour blocks, ~3 hours total; tasks: writing reports and presentations, e-mail, information search. uLog records per event a timestamp (written to 100 ns digits plus a milliseconds field), the key value, the application and the window text; the paper states no resolution.

---

## T-12 — Proton

**Copy.** github.com/ValveSoftware/Proton branch `proton_9.0` (head `2c620c0fd7c2c424f6bd91898602bdc4d4260468` on 2026-10-17), `README.md` → `<scratch>/t12/README.md`, sha256 `67d272bfa00c86bc620f10461f91c68041a34aca30d450e576eac3626a532d5b`.

**Passages.** README:4–6 "**Proton** is a tool for use with the Steam client which allows games which are exclusive to Windows to run on the Linux operating system. It uses Wine to facilitate this." README:8 "**Most users should use Proton provided by the Steam Client itself.**" README:175–181 install a local build into `~/.steam/root/compatibilitytools.d/` and "restart the Steam client for it to pick up on a new tool." No section documents running Proton without the Steam client.

**Reading.** Proton is described as a tool for use with the Steam client; the README documents no client-less use.

---

## T-13 — SteamCMD

**Copy.** developer.valvesoftware.com/wiki/SteamCMD returns an Anubis bot challenge to scripted clients (and HTTP 403 to WebFetch). Read instead: Internet Archive capture `web.archive.org/web/20261016064157id_/https://developer.valvesoftware.com/wiki/SteamCMD` (captured 2026-10-16; page footer "This page was last edited on 25 July 2026, at 08:54.") → `<scratch>/t13/steamcmd-wayback-20261016064157.html`, sha256 `6fd301401cfcca233af67ce259debbd3cde0d0a407a0b4a1471cbbb0b831afd8`.

**Passages.**
- Lead: "The Steam Console Client or SteamCMD is a command-line version of the Steam Client. Its primary use is to install and update various dedicated servers available on Steam using a command-line interface."
- § SteamCMD Login → Anonymous: "To download most game servers, you can login anonymously using login anonymous"; → With a Steam Account: "Some servers require you to login with a Steam Account."
- § Known Issues, "ERROR! Failed to install app "xxxxxx" (No subscription)": "If you get the "No subscription" error, the game/server you are trying to download either requires a login or that you have purchased the game. You will therefore have to log in with a Steam username and password. If that doesn't help, you may need to purchase a copy of the game on Steam first."

**Reading.** SteamCMD's stated primary use is dedicated servers; anonymous login suffices for most game servers; game content that requires ownership needs a logged-in account that has purchased the game.

---

## T-14 — CpsMark+ sensitivity tables

**UNREACHABLE.** DOI 10.1016/j.tbench.2023.100084 → ScienceDirect (pii S2772485923000017) returns HTTP 403 to curl and to WebFetch (bot block); the Elsevier API without a key returns metadata only (`<scratch>/t14/cpsmark.xml`, sha256 `ddbde2101f396385060ba273abb64c2e6e3029b1660801a1199badcba1066ad9`, confirms open access CC BY-NC-ND 4.0, cover date October 2022); the Internet Archive's 2023-01-14 capture of the article page (`<scratch>/t14/sd-wayback-20230114130231.html`, sha256 `63c919c0526b21a95bad7394783af5f2b837cbae723a42be0fbac5fc7636f135`) does not contain the body text or tables; OpenAlex and Semantic Scholar list no repository copy. Table 4 and the module-level sensitivities were not read. Nothing is recorded for this topic.

---

## T-15 — interbench's Burn load

**Copies.** As in T-03 (interbench at `e612a65`, `<scratch>/t15/interbench.c`, `<scratch>/t15/interbench.8`).

**Passages.**
- interbench.8:120–121: ".B Burn: A configurable number of threads fully cpu bound (4 by default)."; interbench.8:12: "\fB\-L\fR Use cpu load of with burn load (default: 4)". Man page header: ".TH interbench "8" "March 2006" "Interbench 0.31"".
- interbench.c:1436 (usage text): `" -L\tUse cpu load of <int> with burn load (default: detected processors)\n"`; interbench.c:1520: `ud.cpu_load = sysconf(_SC_NPROCESSORS_ONLN);`
- interbench.c:614–632: `/* Have ud.cpu_load threads burn cpu continuously */ void emulate_burn(struct thread *th) { … for (i = 0 ; i < ud.cpu_load ; i++) create_pthread(&burnthreads[i], NULL, burn_thread, (void*)(long) t); wait_sem(s); post_sem(&th->sem.stopchild); for (…) join_pthread(burnthreads[i], NULL); }`
- interbench.c:595–611 `burn_thread`: `while (1) { burn_loops(ud.loops_per_ms); if (!trywait_sem(s)) { post_sem(s); break; } }`

**Reading.** Burn = `cpu_load` threads, each looping `burn_loops` (pure CPU) continuously, checking a stop semaphore after each ~1 ms of loops; they stop when the benchmark posts the stop semaphore at the end of the run. Thread count: the man page says 4 by default; the 0.31 code's default is the number of online processors (the usage text agrees with the code).

---

## T-16 — González & Mark, CHI 2004

**Copy.** ACM PDF returned HTTP 403. Read the author-hosted copy ics.uci.edu/~gmark/CHI2004.pdf (8 pages, CHI 2004 paper layout, "CHI 2004 | Paper", Volume 6, Number 1, pp. 113–120) → `<scratch>/t16/gonzalez-mark-chi2004.pdf`, sha256 `988981bfff2408ba2158cf6bcc8bc24c4b1eed9e9cfd3490c69044ea88dcfac4`. Tables read from page renders `<scratch>/t16/pg-4.png`, `pg-5.png`.

**Passages.**
- Abstract: "People average about three minutes on a task and somewhat more than two minutes using any electronic tool or paper document before switching tasks. … People worked in an average of ten different working spheres. Working spheres are also fragmented; people spend about 12 minutes in a working sphere before they switch to another."
- Method (p. 3): "Fourteen people were observed over a seven-month period. … For the next three days formal data collection was done …"
- p. 3: "We coded our data into events that we defined as any continuous use of a device or engagement in an interaction with other individuals …"
- p. 116, text: "What was most surprising to us was that people spend on the average slightly over three minutes on an event (leaving out formal meetings, unknown, and personal events) before another event is initiated."
- p. 116, Table 2 "Average continuous time spent on events before switching (hour:min:sec)": row "All events except “Formal meetings” and “Other”" Avg. Time/Event "0:03:08 (0:02:27)"; row "All events total" "0:08:55 (0:13:23)"; "Other (unknown, personal)" "0:17:27"; "Formal meetings" "0:41:47".
- p. 116, Table 3: "All devices" Avg. Time/Event "0:02:11 (0:01:52)"; text "People spent an average of 2 min. 11 sec. working with any device or paper before they switched to another device or event."
- p. 117, Table 4 "Avg. no. of working spheres (WS) per person, and avg. time spent in each WS per day": row "Central and Peripheral WS only" Avg. Time/segment "0:11:28 (0:10:54)"; row "All" "0:13:49 (0:16:14)"; Metawork "0:06:22"; Personal "0:48:38"; Unknown "0:12:00".
- p. 117, text: "Table 4 shows that the actual average duration of a working sphere segment is quite short (11 min, 28 sec.)."
- p. 117, Table 5 "Avg. time per WS segment without “nonsignificant” disruptions": "Both / All 0:12:18 (0:11:53)"; text: "a segment was considered as “continuous” even if people turned to another working sphere for less than two minutes."

**Reading.** Event average 3 min 08 s covers all event types except formal meetings and "other" (unknown, personal); with all events it is 8 min 55 s. Working-sphere segment average 11 min 28 s covers central and peripheral spheres only (excluding metawork, personal, unknown); 13 min 49 s with all; "about 12 minutes" in the abstract matches the 12 min 18 s figure that ignores disruptions under two minutes. 14 informants, 3 days each.

---

## T-17 — ananicy-cpp's rule matching and CachyOS's default install

**Copies.**
- ananicy-cpp, gitlab.com/ananicy-cpp/ananicy-cpp, tag `v1.2.0` = `cf5ac2eb7b9660794f26f274975066f33359c63e` (2026-03-26): `src/platform/linux/process.cpp` → `<scratch>/t17/process.cpp` sha256 `9256c305d21591c887c4e038faa39ebc722135c849de87bd8a942a2d7984fa20`; `src/rules.cpp` → `<scratch>/t17/rules.cpp` sha256 `9a56344d6baca144a626e0a78be7b5617d865fe338fcc540d820b8416f17770b`; `src/platform/linux/priority.cpp` → `<scratch>/t17/priority.cpp` sha256 `32c0996f97a1d78f1576357fa2683caf0387189d7faf682af65306edc56eaa22`.
- cachyos-settings: CachyOS-PKGBUILDS master at `3933fa84c42affc0646eddc6723a48d7ca6a90d5` (head on 2026-10-17; the topic names no commit), `cachyos-settings/PKGBUILD` → `<scratch>/t17/cachyos-settings-PKGBUILD` sha256 `13451f633724b71a355c9e196de3d0f190029e006166c68791f270fb29d1e1c4`; `cachyos-settings.install` → `<scratch>/t17/cachyos-settings.install` sha256 `806cd2b00996f0baf914ed5ce427fa760f0484a0eed8ac31214e04313fd53f5f`.
- CachyOS desktop ISO of 2026-08-09: the ISO image itself was not downloaded. Read instead its build repository CachyOS-Live-ISO at `d876de294c45533c58fb03f4917e962abffc8f36` ("changelog: 2608 release", 2026-08-09), `archiso/packages_desktop.x86_64` → `<scratch>/t17/packages_desktop.x86_64-d876de29` sha256 `4b19b2e25dab56438d1f2675295f5d4a4d5514721b1f092c7ae3196a4001d0e9`; and the installer CachyOS/cachyos-calamares branch `cachyos` at its last commit before 2026-08-10, `f1c20a500e14448e36991f1b9d3ebae153827761` (2026-06-28): `src/modules/pacstrap/pacstrap.conf` → `<scratch>/t17/pacstrap.conf-f1c20a50` sha256 `b920979a788b4bf683ad4078c7a998ae8149de1c2aa04a1e125b8104f48595c7`; `src/modules/netinstall/netinstall.yaml` → `<scratch>/t17/netinstall.yaml-f1c20a50` sha256 `3c87f6acddf41a6f472dd76f33e42cfb74d0638d401089aec735f8fa5263a66a`.
- CachyOS/ananicy-rules at `03ef03fbf7e834385377432ccecaedd32e3414bb` (2026-09-08): `00-types.types` (sha256 of `git show` output `667d89cb61a949ac9b6595f2f318dc452b65c735d8cd6d4fcd5f934dc940591d`), `README.md` (`0886ec1f23a1ef772e676ba65bc13961ce7942bec6e0dc9d0936a4f60b16b7ed`), 361 `.rules` files; clone at `<scratch>/t17/ananicy-rules`.

**Passages.**
- process.cpp:193–257 `get_command_from_pid`: "// Cmdline method" `cmdline = get_cmdline_from_pid(pid); if (!cmdline.empty()) { auto exe_name_begin = cmdline[0].find_last_of('/'); … return cmdline[0].substr(exe_name_begin + 1); … return cmdline[0]; }` then "// Exe method" (`read_symlink("/proc/{pid}/exe")`, filename, " (deleted)" stripped; skipped after 5 permission failures) then "// Comm method" (`/proc/{pid}/comm`).
- process.cpp:60–65 (events from the BPF probe): `std::string &&command = get_command_from_pid(e->pid); if (command.ends_with(".exe")) { std::replace(…, '\\', '/'); … command = cmd_path.filename().string(); }`
- rules.cpp:70–72 program rules keyed by `"name"`; rules.cpp:181–196 `get_rule(name)`: exact `m_program_rules.contains(name)`, else regex rules (`name_regex`); :198–205 a rule's `type` is merged in, the rule's own fields overriding the type's.
- PKGBUILD: `depends=( zram-generator ananicy-cpp cachyos-ananicy-rules inxi "systemd>=256" iw wireless-regdb )`.
- cachyos-settings.install: `SERVICES=("ananicy-cpp" "systemd-resolved" "systemd-oomd")` … `post_install() { echo "Enabling services..."; for service in "${SERVICES[@]}"; do systemctl enable "$service"; done …`
- pacstrap.conf (installer base packages): `basePackages: - base - base-devel … - cachyos-settings …`; netinstall.yaml group "CachyOS Packages" (`selected: true`, `critical: true`) lists `cachyos-settings`.
- packages_desktop.x86_64 at the 2608 release (live ISO package list), line 27: `cachyos-settings`.
- ananicy-rules README: "**Don't use absolute paths for the executables. Process name alone is enough.**"

**Reading.** ananicy-cpp matches rules against the basename of `argv[0]` (from `/proc/<pid>/cmdline`), falling back to the `/proc/<pid>/exe` basename and only last to `comm`; the primary name is not truncated (the 15-character `comm` limit applies only to the last fallback); Windows `.exe` paths are cut to the file name. CachyOS's installer puts `cachyos-settings` in the base packages, which depends on `ananicy-cpp` and `cachyos-ananicy-rules` and enables the `ananicy-cpp` service in its post-install hook, so a default install has ananicy-cpp with the CachyOS rules installed and enabled (read from the installer and package sources, not from the ISO image).

---

## T-18 — GitHub-hosted runners

**Copies.** docs.github.com/en/actions/reference/limits → `<scratch>/t18/limits.html` sha256 `b2d7e72916e92c25b15bfe39f294dad721f6afeccb95c900fba351a6087df272`; docs.github.com/en/actions/reference/runners/github-hosted-runners → `<scratch>/t18/runners.html` sha256 `0b096d8bc7844425cc8bf858e01e5d929a17fb0685e86edf77aaeb855fe41b72`.

**Passages.**
- Limits table: "All GitHub-hosted runners | Job execution time | 6 hours | Each job in a workflow can run for up to 6 hours of execution time. If a job reaches this limit, the job is terminated and fails." (Self-hosted: 5 days.)
- Runners reference, "Standard GitHub-hosted runners for public repositories": "Linux | 4 | 16 GB | 14 GB | x64 | ubuntu-latest, ubuntu-24.04, ubuntu-22.04, ubuntu-26.04"; also "Linux | 1 | 5 GB | 14 GB | x64 | ubuntu-slim" and "Linux | 4 | 16 GB | 14 GB | arm64 | ubuntu-24.04-arm …". Private repositories: "Linux | 2 | 8 GB | 14 GB | x64 | ubuntu-latest …".

**Reading.** 6 hours per job; standard Linux x64 runner for public repositories: 4 CPUs, 16 GB RAM, 14 GB SSD (private repositories: 2 CPUs, 8 GB).

---

## T-19 — Coetzee et al.'s build-system preprint

**Copy.** arxiv.org/pdf/1203.2704v1 → `<scratch>/t19/coetzee-1203.2704v1.pdf` (11 pages), sha256 `637cbce65f2ceceed18434f59efadbfd54dc3bdcfdc85ee5f6cb75fd4ae882b9`.

**Passages (section "Preliminary experimental results", p. 9).**
- "Three prototype build systems were constructed. In the first, a ptrace-based prototype that could only perform full builds, a pessimistic locking scheme was used … Given enough concurrent processes, this build scaled to 85% the time of a parallel make build of the Linux kernel."
- "A variant of this prototype used binary rewriting based on Jockey [12] … In practice, even with caching, the system added too much overhead to be practical due to the Linux kernel build’s enormous number of short-lived processes like cp and mkdir."
- §5.2 (earlier): "load-time rewriting is too expensive for short-lived processes, necessitating on-disk caching of instrumented binaries."

**Reading.** Workload: a parallel make build of the Linux kernel. The text calls its processes an "enormous number of short-lived processes" and names cp and mkdir; no count is given.

---

## T-20 — Game Mode documentation on recognising a game

**Copies.**
- Microsoft Learn: learn.microsoft.com/en-us/windows/win32/gamemode/ returns 404; the API index learn.microsoft.com/en-us/windows/win32/api/_gamemode/ → `<scratch>/t20/learn.microsoft.com_en-us_windows_win32_api__gamemode_.html` sha256 `8c551083a545b625e11aa952c1b46272beb3fde285050e240effd6b98c4ebbff`, whose "Game Mode" programming-guide link leads to learn.microsoft.com/en-us/previous-versions/windows/desktop/gamemode/game-mode-portal → `<scratch>/t20/learn_previous-versions_gamemode_game-mode-portal.html` sha256 `4304eaa1f8b7d59c724eecdd507ac98a7db6e16c5fdbc08f1a5dc982b289d964`.
- Xbox Support "Game Mode" (support.xbox.com/en-US/help/games-apps/game-setup-and-play/use-game-mode-gaming-on-pc): **unreachable** — the page is rendered by JavaScript; curl gets an empty shell (`<scratch>/t20/support.xbox.com_…html`, sha256 `b2963ce7f76ceb33e11a4a775d6718ee402247220b698ef9194e44dedfaed734`) and WebFetch sees only the title "XBOX Support".
- Apple Support "Use Game Mode" support.apple.com/en-us/105118 (Published Date: September 14, 2026) → `<scratch>/t20/support.apple.com_en-us_105118.html` sha256 `99173c1124d432687fc3234e155d697f6c60f6436f57bb05799554cbbffb83f9`.
- Apple Developer `LSSupportsGameMode`: the page is JavaScript-rendered; its DocC JSON developer.apple.com/tutorials/data/documentation/bundleresources/information-property-list/lssupportsgamemode.json → `<scratch>/t20/lssupportsgamemode.json` sha256 `43b79fc8c54e6fa9bd1adae5afd68cefd034d98a739aee2d96dece831f3945f0` (introduced iOS/iPadOS 18.6, macOS 26.0).

**Passages.**
- Microsoft game-mode-portal: "Important: The Game Mode APIs are deprecated in Windows 10, version 1809 and later." / "Game Mode works by default for most Windows games, requiring no action or opt-in by the customer, and no work by the game developer." / "By using the expandedResources capability, you can explicitly declare that the game will work with Game Mode. As part of launching the game, the process will go into Game Mode with a set of defaults …" / "This capability is granted on a per-title basis; contact your account manager for more information." / "Note: The app must be in the foreground and have focus before exclusive resources are granted."
- Apple Support 105118, Requirements: "Mac with Apple silicon and macOS Sonoma 14 or later and a game that supports macOS full-screen mode." / "When your game enters full screen, Game Mode automatically turns on for that game. Quitting the game automatically turns Game Mode off." The page does not say how macOS decides an app is a game (no category, list or key mentioned).
- Apple Developer LSSupportsGameMode: abstract "A Boolean value indicating whether the app supports Game Mode." Body: "Game Mode turns on automatically when you launch a game, and minimizes background activity for smoother gameplay and more consistent frame rates. Set this key to YES to make Game Mode available when your app is running. For games that aren’t resource intensive enough to benefit from Game Mode, set this key to NO to turn off Game Mode for your app. If you don’t include this key in your Info.plist, Game Mode might not turn on for your game." No mention of an application category.

**Reading.** Microsoft's page says Game Mode works by default for "most Windows games" without stating how Windows recognises a game; the only mechanism it documents is a developer declaration (the `expandedResources` capability, granted per title). Apple's support page gives no recognition rule beyond "your game" entering full screen; the developer key `LSSupportsGameMode` is a declaration by the app, and without it Game Mode "might not turn on". Neither vendor's pages read here state a list, a heuristic or a category. The Xbox Support page could not be read.

---

## S-01 — Field & Welsh 2007, "Bootstrapping Clustered Data"

**Copies.** doi.org → academic.oup.com/jrsssb/article/69/3/369/7109361: HTTP 403 to curl; the ANU repository copy is restricted (HTTP 401 on the bitstream); OpenAlex lists the article as closed access. Read only the publisher-deposited abstract from Crossref, api.crossref.org/works/10.1111/j.1467-9868.2007.00593.x → `<scratch>/s01/crossref.json` sha256 `125af6ea9691a8c7bb86015b174432539a34ef249830aefe496dac74e8fab92e`. **Full text unreachable.**

**Passage (Summary).** "Various bootstraps have been proposed for bootstrapping clustered data from one-way arrays. … extending the theory from functions of the sample mean to include functions of the between and within sums of squares and non-parametric bootstraps to include model-based bootstraps. We determine that the consistency of variance estimates for a bootstrap method depends on the choice of model with the residual bootstrap giving consistency under the transformation model whereas the cluster bootstrap gives consistent estimates under both the transformation and the random-effect model. In addition we note that the criteria based on the distribution of the bootstrap observations are not really useful in assessing consistency."

**Reading.** From the abstract only: data structure one-way arrays (clustered data); the cluster bootstrap gives consistent variance estimates under both the transformation and the random-effect models. The asymptotic regime (number of clusters, cluster size) and the simulation design and findings are not in the abstract and could not be read.

---

## S-02 — Brodersen et al. 2010, balanced accuracy

**Copy.** kaybrodersen.github.io/publications/Brodersen_2010b_ICPR.pdf (4 pages, ICPR 2010 pp. 3121–3124) → `<scratch>/s02/Brodersen_2010b_ICPR.pdf`, sha256 `ab6d144f596e95f180b284ce83a4a3fbb0c58874db671bfe2cfeb755f4e86c75`.

**Passages.**
- §III "The posterior balanced accuracy" (p. 3122): "This observation motivates the use of a different generalizability measure: the balanced accuracy, which can be defined as the average accuracy obtained on either class. Based on a confusion matrix [predicted+/−, actual +/−: TP FP / FN TN] the balanced accuracy (before we adopt a probabilistic viewpoint) is given by ½ (TP/P + TN/N). If the classifier performs equally well on either class, this term reduces to the conventional accuracy … if the conventional accuracy is high only because the classifier takes advantage of an imbalanced test set, then the balanced accuracy, as desired, will drop to chance."
- Same page: "If desired, this symmetry assumption can be dropped, yielding c × TP/P + (1−c) × TN/N, where c ∈ [0, 1] is the cost associated with the misclassification of a positive example."
- §V Discussion (p. 3124): "The notions of the posterior distribution of both the accuracy and the balanced accuracy can be generalized in a natural way to a multiclass setting. Specifically, the posterior of the relative fractions of class frequencies in the test data can be estimated by replacing the Beta distribution by the Dirichlet distribution."

**Reading.** Defined for two classes as the mean of the per-class accuracies, ½(TP/P + TN/N), from the confusion-matrix counts (P and N are not spelled out; they read as the actual positives and negatives). For more than two classes the paper gives no point formula, only the remark that the posterior generalises via a Dirichlet distribution.

---

## S-03 — The Cargo Book

**Copies.** doc.rust-lang.org/cargo/commands/cargo-build.html → `<scratch>/s03/cargo-build.html` sha256 `cc3858cb5974e41ae7247b180e4533f973280b30e274a79326f488253d93ca49`; doc.rust-lang.org/cargo/guide/why-cargo-exists.html → `<scratch>/s03/why-cargo-exists.html` sha256 `10fabdb2e75bd1ae8177ef03cca9aab5e9420acd505422320f93cb9ee07d55a4` (the stable book as served 2026-10-17; no version printed).

**Passages.**
- cargo-build(1): "NAME cargo-build — Compile the current package … DESCRIPTION Compile local packages and all of their dependencies."
- Why Cargo Exists: "Crates are compiled using the Rust compiler, rustc." / "Cargo is the Rust package manager." / "To accomplish this goal, Cargo does four things: … Fetches and builds your package’s dependencies. Invokes rustc or another build tool with the correct parameters to build your package. …" / "Rather than invoke rustc directly, you can instead invoke something generic such as cargo build and let cargo worry about constructing the correct rustc invocation."

**Reading.** `cargo build` compiles the local packages and all their dependencies; Cargo is the package manager that invokes rustc (or another build tool) with the right parameters.

---

## S-04 — Ananicy and ananicy-cpp

**Copies.** Ananicy: GitHub API for Nefelim4ag/Ananicy (2026-10-17): `"archived": true`, `pushed_at 2023-03-21T15:03:42Z`; last commit `1e2cc9a62ba3b6793e59da66aa0039f89e1ad49f` "Add rule for git-annex", authored 2021-10-07T15:36:35Z (Alex Dewar), committed 2023-03-21T15:03:42Z (Timofey Titovets). `README.md` at that commit → `<scratch>/s04/Ananicy-README.md` sha256 `7879441e10863035f42421925356910a9bbcc3040fc76346abb349e3bdc6b8d2`. ananicy-cpp: as T-17, plus `README.md` at `3554447c1ca495478bd00e002078847dfd2205d6` (2026-08-18) → `<scratch>/t17/README-3554447c.md` sha256 `603e16e86a3037f986669abd231c67b294a2cfd63e04dfe87839a012da7cbb39`.

**Passages.**
- Ananicy README (at the last commit): "Ananicy (ANother Auto NICe daemon) — is a shell daemon created to manage processes' IO and CPU priorities, with community-driven set of rules for popular applications … It's mainly for desktop usage." The README does not itself state that the project is unmaintained; the archived flag comes from GitHub's repository metadata.
- ananicy-cpp matching: as T-17 (argv[0] basename, then exe basename, then comm).
- ananicy-cpp README@3554447c, "Supported attributes": "`nice: [-20-19]`: Set the nice value of the process." / "`latency_nice: [-20-19]` …" / "`sched: {"fifo", "rr", "normal", "batch", "idle"}`: Set the scheduling policy." / "`ioclass: {"best-effort", "realtime", "idle", "none"}`: Define the IO scheduling policy." / "`oom_score_adj` …", "`cgroup` …", "`type`: Set the type of the rule. All options defined in the type will be used as if written explicitly in the rule, although you can override each option if needed."; "### Types … It must be defined in a `.types` file. `{"type": "my_type", "nice": 19, "other_parameter": "value"}`".
- priority.cpp:41–51 (v1.2.0) `set_priority`: iterates `/proc/{pid}/task` and calls `setpriority(PRIO_PROCESS, tid, nice_value)` for every thread; `set_latency_nice` likewise per thread; `set_io_priority`: `ioprio_set(IOPRIO_WHO_PROCESS, pid, io_prio)` (the pid only); `set_sched`: `sched_setscheduler(pid, sched, &param)` (the pid only).
- CachyOS ananicy-rules `00-types.types`: `{ "type": "Game", "nice": -5, "ioclass": "best-effort", "sched": "normal" }`.

**Reading.** Upstream Ananicy is archived; its last commit was committed 2023-03-21 (authored 2021-10-07). In ananicy-cpp a rule's name is matched against the untruncated basename of argv[0] (comm only as last fallback). A type can carry any rule attribute — nice (applied to every thread), latency_nice (every thread), ioclass/ionice and sched (applied through the pid, i.e. the main thread), oom_score_adj, cgroup, cpuset.
