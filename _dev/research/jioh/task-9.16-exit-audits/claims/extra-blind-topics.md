# Extra blind topics — sources whose only record is the citation index's passage

Written by the 9.16 lead from the cite lines alone; no repository wording or value.

## `kalibera-ismm13`
- Entry: Kalibera, T., & Jones, R. (2013). Rigorous Benchmarking in Reasonable Time. *Proc. 2013 International Symposium on Memory Management (ISMM '13)*, Seattle, ACM, 63–74. DOI 10.1145/2464157.2464160. Author's accepted manuscript, Kent Academic Repository: kar.kent.ac.uk/33611/45/p63-kaliber.pdf (accessed 2026-09-19).
- Topic: At which level repetitions should be made when an experiment has several levels of random variation; how many repetitions, and whether a minimum or an on-line stopping rule is given (§3, §9.3, §11, §12).

## `georges-oopsla07`
- Entry: Georges, A., Buytaert, D., & Eeckhout, L. (2007). Statistically Rigorous Java Performance Evaluation. *Proc. 22nd Annual ACM SIGPLAN Conference on Object-Oriented Programming Systems, Languages and Applications (OOPSLA '07)*, Montréal, ACM, 57–76. DOI 10.1145/1297027.1297033. Author-hosted PDF: dri.es/files/oopsla07-georges.pdf (accessed 2026-09-19).
- Topic: How a confidence interval over independent runs is formed for small samples; whether a fixed count or a stopping criterion on the interval's width is given, and any cap on runs (§4.3, §6.2.1).

## `maricq-osdi18`
- Entry: Maricq, A., Duplyakin, D., Jimenez, I., Maltzahn, C., Stutsman, R., & Ricci, R. (2018). Taming Performance Variability. *Proc. 13th USENIX Symposium on Operating Systems Design and Implementation (OSDI '18)*, Carlsbad, USENIX Association, 409–425. No DOI (the Zenodo DOI 10.5281/zenodo.1435969 is its dataset). Open access: www.usenix.org/system/files/osdi18-maricq.pdf (accessed 2026-09-19).
- Topic: What the paper finds about performance variability across repeated runs on one server and across servers with nominally identical hardware (§2).

## `chow-aoms65`
- Entry: Chow, Y. S., & Robbins, H. (1965). On the Asymptotic Theory of Fixed-Width Sequential Confidence Intervals for the Mean. *The Annals of Mathematical Statistics*, 36(2), 457–462. DOI 10.1214/aoms/1177700156. Project Euclid (subscription; the article PDF, a JSTOR scan, served to a fetch of the DOI's `.pdf` path on 2026-09-25).
- Topic: What the fixed-width sequential procedure is, what coverage it guarantees and under what limit; any finite-sample coverage figures the paper reports and for which population and rule (eq. (3), p. 461).

## `cochran-st77`
- Entry: Cochran, W. G. (1977). *Sampling Techniques* (3rd ed.). New York: John Wiley & Sons. xvi + 428 pp. ISBN 0-471-16240-X. Read in the Wiley Eastern authorized reprint (New Delhi, sixth reprint June 1989), scanned by the Digital Library of India: archive.org/details/in.ernet.dli.2015.121816 (accessed 2026-09-26).
- Topic: What the text says about sample size for estimating a mean to a given relative precision, ratio estimates, and two-stage or cluster sampling (§6.3, §6.5, §9A.1).

## `feller-ipta50`
- Entry: Feller, W. (1950). *An Introduction to Probability Theory and Its Applications*, Volume One. New York: John Wiley & Sons; London: Chapman & Hall. Read in the second printing (May 1951), scanned by the Digital Library of India: archive.org/details/dli.ernet.5666 (accessed 2026-09-27).
- Topic: What the text gives for the number of successes in Bernoulli trials and its limit as the trials grow and the success probability shrinks (§12.4 and the binomial/Poisson chapters).

## `glean`
- Entry: Mozilla. Glean SDK, `glean-core/src/scheduler.rs`. github.com/mozilla/glean, branch `main` at commit 25b0fb2 (2026-09-25); the file last changed in commit 8fe5d82 (2025-08-08). MPL-2.0 per the file's header (accessed 2026-09-28).
- Topic: When the metrics-ping scheduler fires each day, in which time zone, and the name the thread it spawns carries.

## `systemd-ubuntu`
- Entry: Ubuntu source package `systemd` 255.4-1ubuntu8.17 (noble), its packaging: `debian/systemd.postinst`, `debian/rules` (`override_dh_installsystemd`), `debian/systemd.links`, `debian/systemd.install`; and its source: `src/core/main.c`, `src/core/manager.c`, `man/machine-id.xml`, `presets/90-systemd.preset`. git.launchpad.net/ubuntu/+source/systemd, branch `ubuntu/noble-updates`, tag `import/255.4-1ubuntu8.17` (commit 080f998) (accessed 2026-09-26 and 2026-10-01).
- Topic: Which units the package's maintainer scripts enable by default on a new install, and whether systemd-networkd is among them.

## `netplan`
- Entry: Ubuntu source package `netplan.io` 1.1.2-8ubuntu1~24.04.3 (noble), `src/generate.c`. git.launchpad.net/ubuntu/+source/netplan.io, branch `ubuntu/noble-updates` (accessed 2026-09-26).
- Topic: Under which condition the netplan generator enables systemd-networkd.

## `livecd-rootfs`
- Entry: Ubuntu `livecd-rootfs` 24.04.101, the image build of Ubuntu 24.04's desktop, `live-build/functions` (`configure_network_manager`, called from `live-build/lb_chroot_layered` and `live-build/auto/build`). git.launchpad.net/livecd-rootfs, branch `ubuntu/noble` (accessed 2026-09-26).
- Topic: What network configuration the Ubuntu 24.04 desktop image build writes, and which renderer it names.

## `gh-artifact-retention`
- Entry: GitHub Docs, "Managing GitHub Actions settings for a repository", section "Configuring the retention period for checks, workflow runs, commit statuses, artifacts, and logs in your repository". docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository (accessed 2026-10-16; the page's markdown body as docs.github.com/api/article/body serves it, SHA-256 `3708ce2284c723d39be96d4d148d2cc09e8c9e16b68b7c0ab28b59053296e2c2`).
- Topic: The default retention period for workflow artifacts and logs, and the configurable range for public and private repositories.

## `fqcodel-rfc18`
- Entry: Hoeiland-Joergensen, T., McKenney, P., Taht, D., Gettys, J., & Dumazet, E. (2018). The Flow Queue CoDel Packet Scheduler and Active Queue Management Algorithm. RFC 8290, IETF stream, Experimental, January 2018. DOI 10.17487/RFC8290. www.rfc-editor.org/rfc/rfc8290.txt and www.rfc-editor.org/info/rfc8290 (accessed 2026-09-20).
- Topic: What the RFC says the algorithm is for, and its status (Experimental or otherwise).

## The kernel's `sched_waking` tracepoint
- Entry: Linux kernel source, `kernel/sched/core.c`, tag v6.17.
- Topic: where in the wakeup path the `sched_waking` tracepoint fires relative to the task's switch-out and the `sched_wakeup` tracepoint.

## The Linux kernel's top-level Makefile and `-pipe`
- Entry: Linux kernel source, top-level `Makefile` and `arch/x86/Makefile`, tag v6.17 (and the tag the 9.6 compile slice built).
- Topic: whether the kernel build passes `-pipe` to the compiler.
