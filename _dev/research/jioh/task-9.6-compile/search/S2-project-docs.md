# S2 — primary project and vendor documentation and source code (T1, T3, T4, T5, T6, T7)

Reader S2, research slice 9.6 "Compile", stage 2 search. Access date for everything: 2026-09-16. Source copies were saved under `sources/S2-NN/` (gitignored; not relied on below — every passage is quoted and every copy identified by URL/commit/tag and SHA-256). Every line-numbered locator is `file:line` in the copy identified in the candidate's "copy read" block. Where I computed anything myself (a grep count, a git-log search) it is labelled "reader's own" with the command.

Network notes: outbound HTTPS goes through the session proxy. `www.gnu.org` was unreachable throughout (curl exit 35, "Recv failure: Connection reset by peer", HTTP 000, three attempts incl. `--retry 3`); the GNU make manual was therefore read from `doc/make.texi` in the make source tree at tag 4.4.1 instead of the html_node pages. `git.sesse.net` (plocate) returned "CONNECT tunnel failed, response 502" (three URLs). `github.com` HTML/patch URLs and the GitHub MCP tool returned 403 / "not configured for this session" for repositories other than this project; `raw.githubusercontent.com`, `git clone`, `git ls-remote`, `git.kernel.org` (`/patch/` and man-pages `plain/`), `gitlab.archlinux.org` raw, `gitlab.gnome.org` raw, `code.videolan.org` raw, `deb.debian.org`, `src.fedoraproject.org`, `docs.fedoraproject.org`, `wiki.archlinux.org`, `wiki.gentoo.org`, `www.debian.org`, `gcc.gnu.org`, `ffmpeg.org`, `docs.python.org`, `kernel-team.pages.debian.net`, `make.mad-scientist.net` all worked.

## 1. Search log

One row per query/fetch. "Venue" is the site or tool; "hits followed" names the files that became candidate copies; dead ends give the HTTP status (or curl exit code).

| # | Date | Venue | Query / exact URL(s) | Hits followed | Dead ends |
|---|------|-------|----------------------|---------------|-----------|
| 1 | 2026-09-16 | curl, proxy status | `$HTTPS_PROXY/__agentproxy/status`; probes `raw.githubusercontent.com/torvalds/linux/v6.6/scripts/Kbuild.include`, `www.gnu.org/software/make/manual/html_node/Parallel.html`, `gcc.gnu.org/onlinedocs/gcc/Overall-Options.html` | raw.githubusercontent.com 200, gcc.gnu.org 200 | www.gnu.org: curl exit 35, HTTP 000 |
| 2 | 2026-09-16 | raw.githubusercontent.com, torvalds/linux tag v6.6 | `scripts/Makefile.build`, `scripts/Kbuild.include`, `scripts/basic/fixdep.c`, `Makefile`, `scripts/Makefile.modpost`, `scripts/link-vmlinux.sh`, `Documentation/kbuild/makefiles.rst`, `Documentation/admin-guide/README.rst`, `Documentation/process/changes.rst`, `scripts/Makefile.lib`, `scripts/Makefile.modfinal`, `init/Kconfig`, `Documentation/scheduler/sched-design-CFS.rst`, `scripts/Makefile.host` | all 200 → S2-01 (and S2-13 for `init/Kconfig`) | — |
| 3 | 2026-09-16 | gcc.gnu.org/onlinedocs | `gcc/Overall-Options.html`, `gcc/Invoking-GCC.html`, `gcc/Developer-Options.html`, `gccint/Collect2.html`, `gcc/Link-Options.html`, `gcc/Preprocessor-Options.html`, `gcc/index.html` | all 200 → S2-02 | — |
| 4 | 2026-09-16 | git clone, github.com/mirror/make | `git clone --depth 1 --branch 4.4.1 https://github.com/mirror/make` | commit d66a65ad5a0e31b287f53930b0f09e31801f1613 → S2-03 (src/job.c, src/main.c, src/posixos.c, doc/make.texi) | — |
| 5 | 2026-09-16 | www.gnu.org (retry) | html_node `Parallel`, `Job-Slots`, `POSIX-Jobserver`, `Parallel-Disable`, `Options-Summary`, `Execution`, `Choosing-the-Shell`, `Recursion`, `Options_002fRecursion`, `Parallel-Output` with `--retry 3` | none | all HTTP 000 / curl exit 35 (connection reset); manual read from make.texi in S2-03 instead |
| 6 | 2026-09-16 | make.mad-scientist.net | `https://make.mad-scientist.net/papers/jobserver-implementation/` | 200 → S2-04 | — |
| 7 | 2026-09-16 | git clone, github.com/ninja-build/ninja | `git clone --depth 1 --branch v1.13.1` | commit 79feac0f3e3bc9da9effc586cd5fea41e7550051 → S2-05 (src/ninja.cc, src/util.cc, src/subprocess-posix.cc, doc/manual.asciidoc) | — |
| 8 | 2026-09-16 | raw.githubusercontent.com, rust-lang/cargo tag 0.89.0 | `src/doc/src/reference/config.md`, `src/doc/src/commands/cargo-build.md`, `src/cargo/core/compiler/job_queue/mod.rs` | all 200 → S2-06 | — |
| 9 | 2026-09-16 | raw.githubusercontent.com, Kitware/CMake tag v3.30.0 | `Help/envvar/CMAKE_BUILD_PARALLEL_LEVEL.rst`, `Help/manual/cmake.1.rst` | 200 → S2-07 | — |
| 10 | 2026-09-16 | raw.githubusercontent.com, guillemj/dpkg tag 1.22.11 | `man/dpkg-buildpackage.pod`, `scripts/Dpkg/BuildOptions.pm`, `scripts/dpkg-buildpackage.pl` | 200 → S2-08 | — |
| 11 | 2026-09-16 | www.debian.org | `doc/debian-policy/ch-source.html` (Policy v4.7.4.1, §4.9.1) | 200 → S2-08 | — |
| 12 | 2026-09-16 | kernel-team.pages.debian.net | `kernel-handbook/ch-common-tasks.html` | 200 → S2-08 | — |
| 13 | 2026-09-16 | raw.githubusercontent.com, rpm-software-management/rpm | `macros.in` at tags `rpm-4.19.0`, `rpm-4.18.0` (404), then `rpm-4.19.0-release` (200); `rpmio/macro.c` at `rpm-4.19.0-release` | 200 → S2-09 | tags without `-release` suffix: 404 |
| 14 | 2026-09-16 | docs.fedoraproject.org; src.fedoraproject.org | `en-US/packaging-guidelines/` ("Parallel Make" section); `rpms/redhat-rpm-config/raw/rawhide/f/macros` | 200 → S2-09 | redhat-rpm-config `macros` contains no `smp`/`ncpus` definition (reader's own grep, 0 hits) |
| 15 | 2026-09-16 | gitlab.archlinux.org raw; wiki.archlinux.org | `pacman/pacman/-/raw/v7.0.0/etc/makepkg.conf.in`; `title/Makepkg` | 200 → S2-10 | — |
| 16 | 2026-09-16 | wiki.gentoo.org | `wiki/MAKEOPTS`, `wiki/Handbook:AMD64/Working/Features`, `wiki/Handbook:AMD64/Installation/Base` | 200 → S2-11 (MAKEOPTS page) | Handbook Base page has no MAKEOPTS content relevant beyond the MAKEOPTS page |
| 17 | 2026-09-16 | git clone, github.com/dell/dkms | `git clone --depth 1 --branch v3.1.8` | commit eb06953aca4871ff110887cbee45d6f4d782b821 → S2-12 (dkms.in, dkms.8.in, dkms.service.in, dkms_autoinstaller.in, debian_kernel_postinst.d.in, redhat_kernel_install.d.in) | — |
| 18 | 2026-09-16 | raw.githubusercontent.com, torvalds/linux v6.6 | `Documentation/admin-guide/sysctl/kernel.rst`, `Documentation/scheduler/index.rst`, `Documentation/scheduler/sched-bwc.rst`, `kernel/sched/autogroup.c`, `kernel/sched/fair.c`, `kernel/sched/core.c`, `kernel/sched/features.h` | 200 → S2-13 | `sched_child_runs_first` and `autogroup` absent from sysctl/kernel.rst and scheduler/index.rst (reader's own grep) |
| 19 | 2026-09-16 | GitHub MCP `get_commit` torvalds/linux 5091faa449ee; github.com `.patch` URL | — | MCP: "Access denied: repository torvalds/linux is not configured for this session"; github.com/…/commit/5091faa449ee.patch: 403 |
| 20 | 2026-09-16 | git.kernel.org | `pub/scm/linux/kernel/git/torvalds/linux.git/patch/?id=5091faa449ee` | 200 → S2-13 | — |
| 21 | 2026-09-16 | raw.githubusercontent.com, sched-ext/scx main; git ls-remote | `README.md`, `scheds/rust/scx_rustland/README.md`, `scheds/rust/scx_lavd/README.md`, `scheds/rust/README.md`; HEAD pinned with `git ls-remote` | 200 → S2-13 | `scheds/c/README.md`: 404 |
| 22 | 2026-09-16 | git clone, github.com/ckolivas/interbench | `git clone --depth 1` (no tags used) | commit e612a65ce941028ddea804e6b45ccde2750720d2 → S2-14 | — |
| 23 | 2026-09-16 | git clone, github.com/Nefelim4ag/Ananicy; github.com/CachyOS/ananicy-rules | `--depth 1` (Ananicy); `--depth 50` then `--unshallow` (ananicy-rules) | 1e2cc9a62ba3b6793e59da66aa0039f89e1ad49f; 03ef03fbf7e834385377432ccecaedd32e3414bb → S2-15 | — |
| 24 | 2026-09-16 | git log (reader's own) in CachyOS/ananicy-rules | `git log --oneline --all -S'"gcc"'`, `-S'"name": "make"'`, `-S'"compiler"'`, `--grep=compil` | commits 9fbdadd7, b12d39a5, bf0bae3c, e9f84944, 5459ed81 → S2-15 | — |
| 25 | 2026-09-16 | raw.githubusercontent.com, coreutils/coreutils v9.4; coreutils/gnulib stable-202401 | `src/nproc.c`, `doc/coreutils.texi`, `lib/nproc.c` | 200 → S2-16 | — |
| 26 | 2026-09-16 | raw.githubusercontent.com, util-linux/util-linux v2.39; docs.python.org | `schedutils/taskset.1.adoc`; `3.12/library/os.html` | 200 → S2-17 | taskset.1.adoc has no "inherit"/"child" text (reader's own grep, 0 hits) |
| 27 | 2026-09-16 | ffmpeg.org; raw.githubusercontent.com FFmpeg/FFmpeg n7.0; code.videolan.org x264 | `ffmpeg-codecs.html`; `doc/codecs.texi`, `libavcodec/options_table.h`, `libavcodec/pthread.c`, `libavcodec/pthread_frame.c`, `libavcodec/pthread_internal.h`, `libavutil/cpu.c`, `fftools/ffmpeg_opt.c`; x264 `x264.c`, `encoder/encoder.c`, `common/cpu.c` at master (HEAD pinned via `git ls-remote`) | 200 → S2-18 | — |
| 28 | 2026-09-16 | raw.githubusercontent.com, Cisco-Talos/clamav clamav-1.3.1 | `etc/clamd.conf.sample`, `docs/man/clamd.conf.5.in`, `docs/man/clamscan.1.in`, `docs/man/clamd.8.in`, `docs/man/clamdscan.1.in` | 200 → S2-19 | clamscan.1.in: 0 occurrences of "thread" (reader's own grep) |
| 29 | 2026-09-16 | raw.githubusercontent.com, phoronix-test-suite/test-profiles master; phoronix-test-suite/phoronix-test-suite v10.8.4 | `pts/build-linux-kernel-1.15.0/{install.sh,pre.sh,test-definition.xml,downloads.xml}`; `pts-core/objects/phodevi/components/phodevi_cpu.php`, `pts-core/objects/client/pts_client.php` | 200 → S2-20 | `pts-core/objects/pts_test_execution.php`: 404 |
| 30 | 2026-09-16 | raw.githubusercontent.com, gcc-mirror/gcc releases/gcc-13.2.0 | `gcc/gcc.cc` | 200 → S2-02 | — |
| 31 | 2026-09-16 | raw.githubusercontent.com, pytorch/pytorch v2.4.0 | `docs/source/notes/cpu_threading_torchscript_inference.rst`, `torch/_C/__init__.pyi.in`, `aten/src/ATen/ParallelNative.cpp`, `aten/src/ATen/ParallelCommon.cpp`, `c10/core/thread_pool.cpp` | 200 → S2-21 | — |
| 32 | 2026-09-16 | git.sesse.net (plocate) | `?p=plocate;a=blob_plain;f=plocate-updatedb.service.in;hb=refs/tags/1.1.22` and `.timer`, `updatedb.8.in` | none | curl exit 56, "CONNECT tunnel failed, response 502" ×3 |
| 33 | 2026-09-16 | deb.debian.org pool | `pool/main/p/plocate/plocate_1.1.22.orig.tar.gz` (404), `plocate_1.1.23.orig.tar.gz` (200) | 200 → S2-22 | 1.1.22: 404 |
| 34 | 2026-09-16 | gitlab.gnome.org raw | `GNOME/tracker-miners/-/raw/3.7.3/src/miners/fs/tracker-main.c`, `…/src/libtracker-miners-common/tracker-sched.c`; tag pinned via `git ls-remote` | 200 → S2-22 | `src/miners/fs/tracker-miner-fs-3.service.in` at 3.7.3: 404 |
| 35 | 2026-09-16 | raw.githubusercontent.com mkerrisk/man-pages | `man2/sched_setaffinity.2` at `man-pages-6.7`, `man-pages-6.05`, `man-pages-6.04`, `man/man2/…` at `man-pages-6.7`, `master` | none | all 404 |
| 36 | 2026-09-16 | git.kernel.org man-pages | `pub/scm/docs/man-pages/man-pages.git/plain/man/man2/sched_setaffinity.2?h=man-pages-6.7` (404); `…/plain/man2/sched_setaffinity.2?h=man-pages-6.04` (200) | 200 → S2-23 | 6.7 path: 404 |
| 37 | 2026-09-16 | reader's own greps over S2-01 copies | `Documentation/admin-guide/README.rst` for `make -j`, `-j`, `jobs`, `parallel`; `Documentation/kbuild/makefiles.rst` for `-j`, `jobserver`, `fixdep`, `genksyms`, `objtool` | none for `-j`/jobserver in either file | establishes the T1/T4 "not found" for kernel admin docs |

Total searches/fetches logged: 37.

## 2. Candidates

### S2-01 — Linux kernel v6.6 kbuild sources and kbuild/admin documentation

**Citation.** Linus Torvalds et al., *Linux kernel*, tag `v6.6`, files `scripts/Makefile.build`, `scripts/Kbuild.include`, `scripts/Makefile.lib`, `scripts/basic/fixdep.c`, `Makefile`, `scripts/Makefile.modpost`, `scripts/Makefile.modfinal`, `scripts/link-vmlinux.sh`, `Documentation/kbuild/makefiles.rst`, `Documentation/admin-guide/README.rst`, `Documentation/process/changes.rst`.

**Copy read.** `https://raw.githubusercontent.com/torvalds/linux/v6.6/<path>` (tag v6.6), accessed 2026-09-16, saved under `sources/S2-01/<path>`. SHA-256:
- `scripts/Makefile.build` bbe901ed249056a20f0fae8ad43b2758223322a4d5ffb43f1ab331fe4c1e235a (513 lines)
- `scripts/Kbuild.include` 1c1781e3b4715263db145b420c701a1b563a5a61f394b753f64a756d6d568298 (279 lines)
- `scripts/Makefile.lib` 852f3ee60d6868046bea2dbcfe72e891291e87c42c82b70e34922fc07eb57316
- `scripts/basic/fixdep.c` c3533645894fe4d2dfa189525975a9e9960ebec00ebf402f51c9082f1a825180 (445 lines)
- `Makefile` e2c19bb5a1ef678d150dfc26f11bfa91e5a4458738f305f4abb7848ebeb2b399 (2055 lines)
- `scripts/Makefile.modpost` 7da18133253def95f80ae82b56d90907fc1cee94342a81af3480f5f35bcb89e4
- `scripts/Makefile.modfinal` 8c776b7318632c5accec8a49ea3119c00e6c0c7aa2883a8e628a0c2d776a731c
- `scripts/link-vmlinux.sh` 9bf1de01f85486403dc5055462ae6b8a624a8a37a980b8296ba7329dba18a67b
- `Documentation/kbuild/makefiles.rst` 04440fb7c290fefe9afa88cb78a55b20de3b48bc570df9c154f29921f01c3fa1
- `Documentation/admin-guide/README.rst` bd3df2b31678167cfd1cbcf7cef36f6a6150f23348694a5d9dc8edfdefe0c30b (339 lines)
- `Documentation/process/changes.rst` 7334a460683098c50195c6fda95ce637c9172c7ee20f38b75cc6bafb20dc1bb3
- `scripts/Makefile.host` 35635bf1604f6ef58574e67c5de5a31a880921ac47301465fec1d3ab7f47ece2 (fetched, not quoted)

**Verbatim passages.**

`Documentation/kbuild/makefiles.rst:21-24`:
> The top Makefile is responsible for building two major products: vmlinux
> (the resident kernel image) and modules (any module files).
> It builds these goals by recursively descending into the subdirectories of
> the kernel source tree.

`Documentation/kbuild/makefiles.rst:1042-1048`:
> 4) Recursively descend down in all directories listed in
>    init-* core* drivers-* net-* libs-* and build all targets.
>
>    - The values of the above variables are expanded in arch/$(SRCARCH)/Makefile.
>
> 5) All object files are then linked and the resulting file vmlinux is
>    located at the root of the obj tree.

`scripts/Kbuild.include:114` (how each directory is entered — a sub-make per directory):
> build := -f $(srctree)/scripts/Makefile.build obj

`scripts/Makefile.build:478-482` (the descend rule):
> PHONY += $(subdir-ym)
> $(subdir-ym):
> 	$(Q)$(MAKE) $(build)=$@ \
> 	need-builtin=$(if $(filter $@/built-in.a, $(subdir-builtin)),1) \
> 	need-modorder=$(if $(filter $@/modules.order, $(subdir-modorder)),1) \

`scripts/Makefile.build:146-148, 158-161` (the per-C-file command: one compiler driver invocation, optionally followed by objtool in the same shell):
> # C (.c) files
> # The C file is compiled and updated dependency information is generated.
> # (See cmd_cc_o_c + relevant part of rule_cc_o_c)
> …
> quiet_cmd_cc_o_c = CC $(quiet_modtag)  $@
>       cmd_cc_o_c = $(CC) $(c_flags) -c -o $@ $< \
> 		$(cmd_ld_single_m) \
> 		$(cmd_objtool)

`scripts/Makefile.lib:278, 280`:
> delay-objtool := $(or $(CONFIG_LTO_CLANG),$(CONFIG_X86_KERNEL_IBT))
> …
> cmd_objtool = $(if $(objtool-enabled), ; $(objtool) $(objtool-args) $@)

`scripts/Makefile.build:224-232` (the full per-object rule; every `$(call cmd,…)` is a further recipe line):
> define rule_cc_o_c
> 	$(call cmd_and_fixdep,cc_o_c)
> 	$(call cmd,checksrc)
> 	$(call cmd,checkdoc)
> 	$(call cmd,gen_objtooldep)
> 	$(call cmd,gen_symversions_c)
> 	$(call cmd,record_mcount)
> 	$(call cmd,warn_shared_object)
> endef

`scripts/Makefile.build:241-243`:
> # Built-in and composite module parts
> $(obj)/%.o: $(src)/%.c $(recordmcount_source) FORCE
> 	$(call if_changed_rule,cc_o_c)

`scripts/Kbuild.include:160` (what `$(call cmd,x)` expands to — a `set -e; …` shell fragment):
> cmd = @$(if $(cmd_$(1)),set -e; $($(quiet)log_print) $(delete-on-interrupt) $(cmd_$(1)),:)

`scripts/Kbuild.include:203-216` (compile, then run `fixdep`, then `rm`, all in one recipe line):
> # Execute command if command has changed or prerequisite(s) are updated.
> if_changed = $(if $(if-changed-cond),$(cmd_and_savecmd),@:)
>
> cmd_and_savecmd =                                                            \
> 	$(cmd);                                                              \
> 	printf '%s\n' 'savedcmd_$@ := $(make-cmd)' > $(dot-target).cmd
>
> # Execute the command and also postprocess generated .d dependencies file.
> if_changed_dep = $(if $(if-changed-cond),$(cmd_and_fixdep),@:)
>
> cmd_and_fixdep =                                                             \
> 	$(cmd);                                                              \
> 	scripts/basic/fixdep $(depfile) $@ '$(make-cmd)' > $(dot-target).cmd;\
> 	rm -f $(depfile)

`scripts/Kbuild.include:218-221`:
> # Usage: $(call if_changed_rule,foo)
> # Will check if $(cmd_foo) or any of the prerequisites changed,
> # and if so will execute $(rule_foo).
> if_changed_rule = $(if $(if-changed-cond),$(rule_$(1)),@:)

`scripts/basic/fixdep.c:2, 63-73`:
>  * "Optimize" a list of dependencies as spit out by gcc -MD
> …
>  * It is invoked as
>  *
>  *   fixdep <depfile> <target> <cmdline>
>  *
>  * and will read the dependency file <depfile>
>  *
>  * The transformed dependency snipped is written to stdout.
>  *
>  * It first generates a line
>  *
>  *   savedcmd_<target> = <cmdline>

`scripts/Makefile.build:163-172` (genksyms runs only under CONFIG_MODVERSIONS and only for objects that export symbols; the pipeline is `$(NM)`, `grep`, `$(CPP) … | genksyms`):
> ifdef CONFIG_MODVERSIONS
> # When module versioning is enabled the following steps are executed:
> # o compile a <file>.o from <file>.c
> # o if <file>.o doesn't contain a __export_symbol_*, i.e. does
> #   not export symbols, it's done.
> # o otherwise, we calculate symbol versions using the good old
> #   genksyms on the preprocessed source and dump them into the .cmd file.
> # o modpost will extract versions from that file and create *.c files that will
> #   be compiled and linked to the kernel and/or modules.

`scripts/Makefile.build:173-177, 130`:
> gen_symversions =								\
> 	if $(NM) $@ 2>/dev/null | grep -q ' __export_symbol_'; then		\
> 		$(call cmd_gensymtypes_$(1),$(KBUILD_SYMTYPES),$(@:.o=.symtypes)) \
> 			>> $(dot-target).cmd;					\
> 	fi
> …
> cmd_gensymtypes_c = $(CPP) -D__GENKSYMS__ $(c_flags) $< | $(genksyms)

`scripts/Makefile.build:347-348, 359-360` (assembly sources: also one `$(CC)` invocation):
> quiet_cmd_as_o_S = AS $(quiet_modtag)  $@
>       cmd_as_o_S = $(CC) $(a_flags) -c -o $@ $< $(cmd_objtool)
> …
> $(obj)/%.o: $(src)/%.S FORCE
> 	$(call if_changed_rule,as_o_S)

`scripts/Makefile.build:397-400` (per-directory archive: `rm`, `printf | xargs`, `$(AR)`):
> quiet_cmd_ar_builtin = AR      $@
>       cmd_ar_builtin = rm -f $@; \
> 	$(if $(real-prereqs), printf "$(obj)/%s " $(patsubst $(obj)/%,%,$(real-prereqs)) | xargs) \
> 	$(AR) cDPrST $@

`scripts/Makefile.build:427-428` (multi-object modules: one `$(LD) -r` per module):
> quiet_cmd_ld_multi_m = LD [M]  $@
>       cmd_ld_multi_m = $(LD) $(ld_flags) -r -o $@ @$(patsubst %.o,%.mod,$@) $(cmd_objtool)

`Makefile:1862-1865` (modpost is a separate sub-make after all directories are built):
> PHONY += modpost
> modpost: $(if $(single-build),, $(if $(KBUILD_BUILTIN), vmlinux.o)) \
> 	 $(if $(KBUILD_MODULES), modules_check)
> 	$(Q)$(MAKE) -f $(srctree)/scripts/Makefile.modpost

`Makefile:1844-1847`:
> modules: modpost
> ifneq ($(KBUILD_MODPOST_NOFINAL),1)
> 	$(Q)$(MAKE) -f $(srctree)/scripts/Makefile.modfinal
> endif

`scripts/Makefile.modpost:6-17`:
> # Stage one of module building created the following:
> # a) The individual .o files used for the module
> # b) A <module>.o file which is the .o files above linked together
> # c) A <module>.mod file, listing the name of the preliminary <module>.o file,
> #    plus all .o files
> # d) modules.order, which lists all the modules
>
> # Stage 2 is handled by this file and does the following
> # 1) Find all modules listed in modules.order
> # 2) modpost is then used to
> # 3)  create one <module>.mod.c file per module
> # 4)  create one Module.symvers file with CRC for all exported symbols

`scripts/Makefile.modfinal:25-26, 33-35` (per module: one more `$(CC)` for `.mod.c` and one `$(LD) -r` for the `.ko`):
> quiet_cmd_cc_o_c = CC [M]  $@
>       cmd_cc_o_c = $(CC) $(filter-out $(CC_FLAGS_CFI) $(CFLAGS_GCOV), $(c_flags)) -c -o $@ $<
> …
> quiet_cmd_ld_ko_o = LD [M]  $@
>       cmd_ld_ko_o +=							\
> 	$(LD) -r $(KBUILD_LDFLAGS)					\

`scripts/link-vmlinux.sh:1-8, 49-58` (final link: a shell script calling `$LD` directly, i.e. no compiler driver / collect2 for vmlinux):
> #!/bin/sh
> # SPDX-License-Identifier: GPL-2.0
> #
> # link vmlinux
> #
> # vmlinux is linked from the objects in vmlinux.a and $(KBUILD_VMLINUX_LIBS).
> # vmlinux.a contains objects that are linked unconditionally.
> # $(KBUILD_VMLINUX_LIBS) are archives which are linked conditionally
> …
> vmlinux_link()
> {
> 	local output=${1}
> 	local objs
> 	local libs
> 	local ld
> 	local ldflags
> 	local ldlibs
>
> 	info LD ${output}

`scripts/link-vmlinux.sh:169-183` (kallsyms: the link is repeated, each step adding `scripts/kallsyms`, `mksysmap`, and one `$(CC) -c` of a generated `.S`):
> kallsyms_step()
> {
> 	kallsymso_prev=${kallsymso}
> 	kallsyms_vmlinux=.tmp_vmlinux.kallsyms${1}
> 	kallsymso=${kallsyms_vmlinux}.o
> 	kallsyms_S=${kallsyms_vmlinux}.S
>
> 	vmlinux_link ${kallsyms_vmlinux} "${kallsymso_prev}" ${btf_vmlinux_bin_o}
> 	mksysmap ${kallsyms_vmlinux} ${kallsyms_vmlinux}.syms ${kallsymso_prev}
> 	kallsyms ${kallsyms_vmlinux}.syms ${kallsyms_S}
>
> 	info AS ${kallsyms_S}
> 	${CC} ${NOSTDINC_FLAGS} ${LINUXINCLUDE} ${KBUILD_CPPFLAGS} \
> 	      ${KBUILD_AFLAGS} ${KBUILD_AFLAGS_KERNEL} \
> 	      -c -o ${kallsymso} ${kallsyms_S}

`Documentation/process/changes.rst:36, 113`:
> GNU make               3.82             make --version
> …
> You will need GNU make 3.82 or later to build the kernel.

`Documentation/admin-guide/README.rst` — reader's own check: `grep -n -i -E 'make -j|-j|parallel|jobs' Documentation/admin-guide/README.rst` returns no line about parallel builds or `-j` (the only hits are "kernel-du-jour" and "coprocessor"). The v6.6 admin README does not recommend a `-j` level.

**Coverage.**
- T1: covers the *structure* of the process population per translation unit and per link: per `.c` one `$(CC)` driver invocation (which itself spawns `cc1` and `as` — see S2-02) plus, in the same recipe line, an optional `objtool` and then `scripts/basic/fixdep` and `rm`; per exporting object under CONFIG_MODVERSIONS, `$(NM)`, `grep`, `$(CPP)`, `genksyms`; per directory one sub-`make` and one `rm`/`printf`/`xargs`/`$(AR)` line; per multi-object module one `$(LD) -r`; after the tree, one `modpost` sub-make, then per module one `$(CC)` of `.mod.c` and one `$(LD) -r`; the vmlinux link is a `/bin/sh` script calling `$LD` repeatedly (kallsyms steps) plus `scripts/kallsyms`, `mksysmap`, one `$(CC) -c`. It gives no counts, lifetimes or CPU-time distributions; those depend on the configuration. Not an observation: no machine, no run.
- T3: covers how kbuild itself uses recursion (one sub-make per directory, `Makefile.modpost`/`Makefile.modfinal` as further sub-makes) — which is what make's jobserver must span. Not an observation.
- T4: does not cover a recommended `-j` (README.rst has none; makefiles.rst has none).
- T5, T6, T7: do not cover.
- One observation? No — source and documentation, no measurement.

### S2-02 — GCC manual (driver, subprocesses, collect2) and the GCC 13.2.0 driver source

**Citation.** *Using the GNU Compiler Collection (GCC)*, online manual for the development version 17.0.0, sections "3 GCC Command Options" (Invoking-GCC), "3.2 Options Controlling the Kind of Output" (Overall-Options), "3.13 Preprocessor Options"; *GNU Compiler Collection (GCC) Internals*, section "22 collect2"; and `gcc/gcc.cc` at tag `releases/gcc-13.2.0`.

**Copy read.** `https://gcc.gnu.org/onlinedocs/gcc/{index,Invoking-GCC,Overall-Options,Developer-Options,Link-Options,Preprocessor-Options}.html`, `https://gcc.gnu.org/onlinedocs/gccint/Collect2.html`, accessed 2026-09-16 (index.html states "version 17.0.0"); `https://raw.githubusercontent.com/gcc-mirror/gcc/releases/gcc-13.2.0/gcc/gcc.cc`. Saved under `sources/S2-02/`. SHA-256: index.html 64dad3d265d9d82fd2101a1d0657cc2faef4a9485720bd91c0fa334f11f6be73; Invoking-GCC.html bbef11bae35ab430205e801ce5934e51e4a76a79ccf61cac43b77bcd2fbf6c6e; Overall-Options.html 84e27e41f6745889fc3c98a0a03cf24c6f80409f52214b482c927d072b17e630; Developer-Options.html a2bfe5614823da357c80e1bfb34d9d037d826bbaae87adea05aa3a46a6e0cf04; Collect2.html 24d8c5924c980ea3c94c132df280f421ec85f632b222acf65af98032ea513d19; Link-Options.html b882b1eae24788f1454d686368ec488d77726add9ef4adb4fd5f6958bf1296c2; Preprocessor-Options.html 1c2878dd4eb6db32e9ecfbe8c314cb698cd70e08a6bdcb2b233b22b3b8c702be; gcc.cc c260c6321fb3852df326618d18642a3c795a8886c285db71acde6a97fd031b0a (11239 lines).

**Verbatim passages.**

Invoking-GCC.html, section "3 GCC Command Options", first paragraph:
> When you invoke GCC, it normally does preprocessing, compilation, assembly and linking. The “overall options” allow you to stop this process at an intermediate stage. For example, the -c option says not to run the linker. Then the output consists of object files output by the assembler.

Overall-Options.html, entry `-c`:
> Compile or assemble the source files, but do not link. The linking stage simply is not done. The ultimate output is in the form of an object file for each source file.

Overall-Options.html, entry `-v`:
> Print (on standard error output) the commands executed to run the stages of compilation. Also print the version number of the compiler driver program and of the preprocessor and the compiler proper.

Overall-Options.html, entries `-pipe` and `-wrapper`:
> -pipe
> --pipe
> Use pipes rather than temporary files for communication between the various stages of compilation. This fails to work on some systems where the assembler is unable to read from a pipe; but the GNU assembler has no trouble.
> -wrapper
> Invoke all subcommands under a wrapper program. The name of the wrapper program and its parameters are passed as a comma separated list.
> gcc -c t.c -wrapper gdb,--args
> This invokes all subprograms of gcc under ‘gdb --args’, thus the invocation of cc1 is ‘gdb --args cc1 …’.

Preprocessor-Options.html, entry `-no-integrated-cpp`:
> Perform preprocessing as a separate pass before compilation. By default, GCC performs preprocessing as an integrated part of input tokenization and parsing. If this option is provided, the appropriate language front end (cc1, cc1plus, or cc1obj for C, C++, and Objective-C, respectively) is instead invoked twice, once for preprocessing only and once for actual compilation of the preprocessed input.

gccint Collect2.html, section "22 collect2":
> GCC uses a utility called collect2 on nearly all systems to arrange to call various initialization functions at start time.
> The program collect2 works by linking the program once and looking through the linker output file for symbols with particular names indicating they are constructor functions. If it finds any, it creates a new temporary ‘.c’ file containing a table of them, compiles it, and links the program a second time including that file.
> …
> The program collect2 is installed as ld in the directory where the passes of the compiler are installed. When collect2 needs to find the real ld, it tries the following file names:

`gcc/gcc.cc:20-28` (releases/gcc-13.2.0):
> /* This program is the user interface to the C compiler and possibly to
> other compilers.  It is used because compilation is a complicated procedure
> which involves running several programs and passing temporary files between
> them, forwarding the users switches to those programs selectively,
> and deleting the temporary files at the end.
>
> CC recognizes how to compile each input file by suffixes in the file names.
> Once it knows which kind of compilation to perform, the procedure for
> compilation is specified by a string called a "spec".  */

`gcc/gcc.cc:1429-1442` (the default spec for a `.c` input: `cc1` once, then `%(invoke_as)`):
>   {"@c",
>    /* cc1 has an integrated ISO C preprocessor.  We should invoke the
>       external preprocessor if -save-temps is given.  */
>      "%{E|M|MM:%(trad_capable_cpp) %(cpp_options) %(cpp_debug_options)}\
>       %{!E:%{!M:%{!MM:\
>           %{traditional:\
> %eGNU C no longer supports -traditional without -E}\
>       %{save-temps*|traditional-cpp|no-integrated-cpp:%(trad_capable_cpp) \
> 	  %(cpp_options) -o %{save-temps*:%b.i} %{!save-temps*:%g.i} \n\
> 	    cc1 -fpreprocessed %{save-temps*:%b.i} %{!save-temps*:%g.i} \
> 	  %(cc1_options)}\
>       %{!save-temps*:%{!traditional-cpp:%{!no-integrated-cpp:\
> 	  cc1 %(cpp_unique_options) %(cc1_options)}}}\
>       %{!fsyntax-only:%(invoke_as)}}}}", 0, 0, 1},

`gcc/gcc.cc:1287-1292` (the assembler is a separate program `as`, fed a temp file or, with `-pipe`, a pipe):
> static const char *invoke_as =
> #ifdef AS_NEEDS_DASH_FOR_PIPED_INPUT
> "%{!fwpa*:\
>    %{fcompare-debug=*|fdump-final-insns=*:%:compare-debug-dump-opt()}\
>    %{!S:-o %|.s |\n as %(asm_options) %|.s %A }\
>   }";

`gcc/gcc.cc:882-884, 1136-1137, 1140-1142` (the link step runs `collect2` as the linker program, which in turn runs `ld`):
> #ifndef LINKER_NAME
> #define LINKER_NAME "collect2"
> #endif
> …
> /* We pass any -flto flags on to the linker, which is expected
>    to understand them.  In practice, this means it had better be collect2.  */
> …
> #define LINK_COMMAND_SPEC "\
> %{!fsyntax-only:%{!c:%{!M:%{!MM:%{!E:%{!S:\
>     %(linker) " \

`gcc/gcc.cc:5318-5324`:
>   if (save_temps_flag && use_pipes)
>     {
>       /* -save-temps overrides -pipe, so that temp files are produced */
>       if (save_temps_flag)
> 	warning (0, "%<-pipe%> ignored because %<-save-temps%> specified");
>       use_pipes = 0;
>     }

**Coverage.**
- T1: covers the per-translation-unit process structure of a GCC compile: `gcc` (driver) → `cc1` (or `cc1plus`) with integrated preprocessing → `as`; with `-pipe`, `cc1` and `as` are connected by a pipe (so they are concurrently alive), otherwise sequentially through a temporary file; a user-space link (`gcc -o`) runs `collect2` → `ld`, and `collect2` may link twice. Note for the kernel case: kbuild's vmlinux link calls `$LD` directly (S2-01), so `collect2` does not appear there; `$(CC) -c` still yields `cc1` + `as` per object. No counts, lifetimes or CPU-time distributions. Not an observation.
- T3, T4, T5, T6, T7: do not cover.
- One observation? No.

### S2-03 — GNU make 4.4.1 source (`src/job.c`, `src/main.c`, `src/posixos.c`) and the GNU make manual (`doc/make.texi`) at the same tag

**Citation.** Free Software Foundation, *GNU make* 4.4.1, source files `src/job.c`, `src/main.c`, `src/posixos.c`, and *GNU make manual* as `doc/make.texi` in the same tree (sections "Recipe Execution", "Parallel Execution", "Communicating Options to a Sub-make", "Summary of Options", "Sharing Job Slots with GNU make", "POSIX Jobserver Interaction").

**Copy read.** `git clone --depth 1 --branch 4.4.1 https://github.com/mirror/make` (mirror of git.savannah.gnu.org/git/make.git), commit `d66a65ad5a0e31b287f53930b0f09e31801f1613` (= tag 4.4.1), accessed 2026-09-16, saved under `sources/S2-03/repo/`, commit in `sources/S2-03/COMMIT.txt`. File sizes: `src/job.c` 3828 lines, `src/main.c` 3869 lines, `src/posixos.c` 896 lines. (Per-file SHA-256 is not separately meaningful for a git checkout; the commit hash identifies the content. `www.gnu.org` html_node pages were unreachable — search log #5.)

**Verbatim passages — the manual (`doc/make.texi`).**

`doc/make.texi:4079-4083` (one shell per recipe line):
> When it is time to execute recipes to update a target, they are
> executed by invoking a new sub-shell for each line of the recipe,
> unless the @code{.ONESHELL} special target is in effect
> (@pxref{One Shell, ,Using One Shell})  (In practice, @code{make} may
> take shortcuts that do not affect the results.)

`doc/make.texi:4333-4347`:
> GNU @code{make} knows how to execute several recipes at once.  Normally,
> @code{make} will execute only one recipe at a time, waiting for it to finish
> before executing the next.  However, the @samp{-j} or @samp{--jobs} option
> tells @code{make} to execute many recipes simultaneously.  You can inhibit
> parallelism for some or all targets from within the makefile (@pxref{Parallel
> Disable, ,Disabling Parallel Execution}).
>
> On MS-DOS, the @samp{-j} option has no effect, since that system doesn't
> support multi-processing.
>
> If the @samp{-j} option is followed by an integer, this is the number of
> recipes to execute at once; this is called the number of @dfn{job slots}.
> If there is nothing looking like an integer after the @samp{-j} option,
> there is no limit on the number of job slots.  The default number of job
> slots is one, which means serial execution (one thing at a time).

`doc/make.texi:4384-4390`:
> More precisely, when @code{make} goes to start up a job, and it already has
> at least one job running, it checks the current load average; if it is not
> lower than the limit given with @samp{-l}, @code{make} waits until the load
> average goes below that limit, or until all the other jobs finish.
>
> By default, there is no load limit.

`doc/make.texi:5117-5125`:
> The @samp{-j} option is a special case (@pxref{Parallel, ,Parallel Execution}).
> If you set it to some numeric value @samp{N} and your operating system
> supports it (most any UNIX system will; others typically won't), the
> parent @code{make} and all the sub-@code{make}s will communicate to
> ensure that there are only @samp{N} jobs running at the same time
> between them all.  Note that any job that is marked recursive
> (@pxref{Instead of Execution, ,Instead of Executing Recipes})
> doesn't count against the total jobs (otherwise we could get @samp{N}
> sub-@code{make}s running and have no slots left over for any real work!)

`doc/make.texi:9491-9499`:
> @item -j [@var{jobs}]
> @cindex @code{-j}
> @itemx --jobs[=@var{jobs}]
> @cindex @code{--jobs}
> Specifies the number of recipes (jobs) to run simultaneously.  With no
> argument, @code{make} runs as many recipes simultaneously as possible.
> If there is more than one @samp{-j} option, the last one is effective.
> @xref{Parallel, ,Parallel Execution}, for more information on how
> recipes are run.  Note that this option is ignored on MS-DOS.

`doc/make.texi:9525-9528`:
> Specifies that no new recipes should be started if there are other
> recipes running and the load average is at least @var{load} (a
> floating-point number).  With no argument, removes a previous load
> limit.  @xref{Parallel, ,Parallel Execution}.

`doc/make.texi:12283-12286, 12301-12304`:
> GNU @code{make} uses a method called the ``jobserver'' to control the
> number of active jobs across recursive invocations.  The actual
> implementation of the jobserver varies across different operating
> systems, but some fundamental aspects are always true.
> …
> Second, every command @code{make} starts has one implicit job slot
> reserved for it before it starts.  Any tool which wants to participate
> in the jobserver protocol should assume it can always run one job
> without having to contact the jobserver at all.

`doc/make.texi:12338-12343, 12363-12366`:
> On POSIX systems the jobserver is implemented in one of two ways: on systems
> that support it, GNU @code{make} will create a named pipe and use that for the
> jobserver.  In this case the auth option will have the form
> @code{--jobserver-auth=fifo:PATH} where @samp{PATH} is the pathname of the
> named pipe.  To access the jobserver you should open the named pipe path and
> read/write to it as described below.
> …
> In both implementations of the jobserver, the pipe will be pre-loaded with one
> single-character token for each available job.  To obtain an extra slot you
> must read a single character from the jobserver; to release a slot you must
> write a single character back into the jobserver.

**Verbatim passages — the source.**

`src/main.c:2188-2193` (default one slot; a child of a jobserver has `job_slots = 0` and relies on tokens):
>   if (jobserver_auth)
>     job_slots = 0;
>   else if (arg_job_slots == INVALID_JOB_SLOTS)
>     job_slots = 1;
>   else
>     job_slots = arg_job_slots;

`src/main.c:2210-2217`:
>   /* If we have >1 slot at this point, then we're a top-level make.
>      Set up the jobserver.
>
>      Every make assumes that it always has one job it can run.  For the
>      submakes it's the token they were given by their parent.  For the top
>      make, we just subtract one from the number the user wants.  */
>
>   if (job_slots > 1 && jobserver_setup (job_slots - 1, jobserver_style))

`src/posixos.c:146-147, 164, 195` (the jobserver is a FIFO by default, else a pipe):
> jobserver_setup (int slots, const char *style)
> {
> …
>       EINTRLOOP (r, mkfifo (fifo_name, 0600));
> …
>       EINTRLOOP (r, pipe (job_fds));

`src/job.c:1830-1835` (what make does when the cap is reached, non-jobserver case: block in `reap_children`):
>   /* Wait for a job slot to be freed up.  If we allow an infinite number
>      don't bother; also job_slots will == 0 if we're using the jobserver.  */
>
>   if (job_slots != 0)
>     while (job_slots_used == job_slots)
>       reap_children (1, 0);

`src/job.c:1838-1848, 1858-1860, 1881-1889` (jobserver case: first job uses the implicit token, further jobs block reading a token):
>   /* If we are controlling multiple jobs make sure we have a token before
>      starting the child. */
>
>   /* This can be inefficient.  There's a decent chance that this job won't
>      actually have to run any subprocesses: the command script may be empty
>      or otherwise optimized away.  It would be nice if we could defer
>      obtaining a token until just before we need it, in start_job_command.
>      To do that we'd need to keep track of whether we'd already obtained a
>      token (since start_job_command is called for each line of the job, not
>      just once).  Also more thought needs to go into the entire algorithm;
>      this is where the old parallel job code waits, so...  */
> …
>         /* If we don't already have a job started, use our "free" token.  */
>         if (!jobserver_tokens)
>           break;
> …
>         /* Get a token.  */
>         got_token = jobserver_acquire (waiting_jobs != NULL);
>
>         /* If we got one, we're done here.  */
>         if (got_token == 1)
>           {
>             DB (DB_JOBS, (_("Obtained token for child %p (%s).\n"),
>                           c, c->file->name));
>             break;
>           }

`src/posixos.c:612-615` (a token is one byte read from the pipe):
>   /* Set interruptible system calls, and read() for a job token.  */
>   set_child_handler_action_flags (1, timeout);
>
>   EINTRLOOP (got_token, read (job_rfd, &intake, 1));

`src/job.c:1137-1146` (token returned when the child is reaped):
>   /* If we're using the jobserver and this child is not the only outstanding
>      job, put a token back into the pipe for it.  */
>
>   if (jobserver_enabled () && jobserver_tokens > 1)
>     {
>       jobserver_release (1);
>       DB (DB_JOBS, (_("Released token for child %p (%s).\n"),
>                     child, child->file->name));
>     }
>
>   --jobserver_tokens;

`src/job.c:1628-1642` (`-l` handling):
>   /* If we are running at least one job already and the load average
>      is too high, make this one wait.  */
>   if (!c->remote
>       && ((job_slots_used > 0 && load_too_high ())
> #ifdef WINDOWS32
>           || process_table_full ()
> #endif
>           ))
>     {
>       /* Put this child on the chain of children waiting for the load average
>          to go down.  */
>       set_command_state (f, cs_running);
>       c->next = waiting_jobs;
>       waiting_jobs = c;
>       return 0;
>     }

`src/job.c:2104-2121` (on Linux `-l` compares the *running-task count* in `/proc/loadavg`, not the load average):
>               /* The syntax of /proc/loadavg is:
>                     <1m> <5m> <15m> <running>/<total> <pid>
>                  The load is considered too high if there are more jobs
>                  running than the requested average.  */
> …
>               if (p && ISDIGIT(p[1]))
>                 {
>                   unsigned int cnt = make_toui (p+1, NULL);
>                   DB (DB_JOBS, ("Running: system = %u / make = %u (max requested = %f)\n",
>                                 cnt, job_slots_used, max_load_average));
>                   return (double)cnt > max_load_average;
>                 }

`src/job.c:2709-2714` (when a shell is interposed between make and the compiler):
> /* Figure out the argument list necessary to run LINE as a command.  Try to
>    avoid using a shell.  This routine handles only ' quoting, and " quoting
>    when no backslash, $ or ' characters are seen in the quotes.  Starting
>    quotes may be escaped with a backslash.  If any of the characters in
>    sh_chars is seen, or any of the builtin commands listed in sh_cmds is the
>    first word of a line, the shell is used.

`src/job.c:2844-2850` (the character set and builtin list that force a shell on POSIX):
>   static const char *sh_chars = "#;\"*?[]&|<>(){}$`^~!";
>   static const char *sh_cmds[] =
>     { ".", ":", "alias", "bg", "break", "case", "cd", "command", "continue",
>       "eval", "exec", "exit", "export", "fc", "fg", "for", "getopts", "hash",
>       "if", "jobs", "login", "logout", "read", "readonly", "return", "set",
>       "shift", "test", "times", "trap", "type", "ulimit", "umask", "unalias",
>       "unset", "wait", "while", 0 };

`src/job.c:2340` (child creation):
>     pid = vfork ();

**Coverage.**
- T3: covers the dispatch mechanism precisely: default 1 slot; top-level make with `-jN` creates a FIFO (or pipe) pre-loaded with N−1 one-byte tokens; each make (including sub-makes) runs its first job on an implicit slot and blocks in `read()` on the FIFO for each further concurrent job; the token is written back when the child is reaped; when the cap is reached, `new_job` blocks in `reap_children(1,0)` (no jobserver) or in the token `read` (jobserver); with `-l`, on Linux it reads `/proc/loadavg`'s `<running>` field and refuses to start a job when that count exceeds the limit while at least one job is running; each recipe line gets its own `/bin/sh` unless make can exec the command directly (no shell metacharacters, first word not a shell builtin); kbuild's recipe lines contain `set -e;` and `;`, so (per this rule) every kbuild command runs under a shell. Number of live processes vs N: "there are only N jobs running at the same time between them all", recursive makes not counted; each job may be a shell plus its children. Make's own CPU cost per job: not covered. Not an observation.
- T4: covers the tool default (`-j` absent → serial; `-j` with no number → unlimited). No rationale for choosing N; no observation of user choices.
- T6 (single-core confinement): covers `-l` semantics under confinement only implicitly — the `<running>` count in `/proc/loadavg` is system-wide, not per affinity mask. No measurement.
- T1, T5, T7: do not cover.
- One observation? No.

### S2-04 — Paul D. Smith, "GNU make jobserver implementation" (make.mad-scientist.net)

**Citation.** Paul D. Smith, *GNU make: Jobserver implementation*, https://make.mad-scientist.net/papers/jobserver-implementation/ (web page, undated on the page as fetched).

**Copy read.** URL above, accessed 2026-09-16, saved as `sources/S2-04/jobserver-implementation.html`, SHA-256 97e67a1a3b88e192fc9a11d7e645c5104f59c16291a213bdc0e2abab41b02762 (53680 bytes).

**Verbatim passage** (section beginning of the page, paragraph starting "The idea is ingeniously simple"):
> The idea is ingeniously simple: the initial, top-level make creates a pipe and writes N one-byte tokens into the pipe.  That pipe is shared between that make and all submakes, and any time any make wants to run a job it first has to read a token from the pipe.  Once the job is complete, it writes the token back to the pipe.  Since there are only N tokens, you know that you will never invoke more than N jobs.

**Coverage.**
- T3: covers the design rationale of the jobserver (pipe with N tokens shared by all sub-makes). Consistent with S2-03. No CPU cost, no process counts. Not an observation.
- Other topics: do not cover.

### S2-05 — Ninja 1.13.1 source and manual

**Citation.** Ninja build system, tag `v1.13.1`, files `src/ninja.cc`, `src/util.cc`, `src/subprocess-posix.cc`, `doc/manual.asciidoc`.

**Copy read.** `git clone --depth 1 --branch v1.13.1 https://github.com/ninja-build/ninja`, commit `79feac0f3e3bc9da9effc586cd5fea41e7550051`, accessed 2026-09-16, saved under `sources/S2-05/repo/` (commit in `sources/S2-05/COMMIT.txt`).

**Verbatim passages.**

`src/ninja.cc:254-264` (the default `-j`):
> int GuessParallelism() {
>   switch (int processors = GetProcessorCount()) {
>   case 0:
>   case 1:
>     return 2;
>   case 2:
>     return 3;
>   default:
>     return processors + 2;
>   }
> }

`src/ninja.cc:241-243` (usage text):
> "  -j N     run N jobs in parallel (0 means infinity) [default=%d on this system]\n"
> "  -k N     keep going until N jobs fail (0 means infinity) [default=1]\n"
> "  -l N     do not start new jobs if the load average is greater than N\n"

`src/util.cc:861-868, 876-885` (processor count honours cgroup CPU quota and the affinity mask):
>   int cgroupCount = -1;
>   int schedCount = -1;
> #if defined(__linux__) || defined(__GLIBC__)
>   cgroupCount = ParseCPUFromCGroup();
> #endif
>   // The number of exposed processors might not represent the actual number of
>   // processors threads can run on. This happens when a CPU set limitation is
>   // active, see https://github.com/ninja-build/ninja/issues/1278
> …
> #elif defined(CPU_COUNT)
>   cpu_set_t set;
>   if (sched_getaffinity(getpid(), sizeof(set), &set) == 0) {
>     schedCount = CPU_COUNT(&set);
>   }
> #endif
>   if (cgroupCount >= 0 && schedCount >= 0) return std::min(cgroupCount, schedCount);
>   if (cgroupCount < 0 && schedCount < 0)
>     return static_cast<int>(sysconf(_SC_NPROCESSORS_ONLN));
>   return std::max(cgroupCount, schedCount);

`src/subprocess-posix.cc:132-134` (every command runs under `/bin/sh -c`):
>   const char* spawned_args[] = { "/bin/sh", "-c", command.c_str(), NULL };
>   err = posix_spawn(&pid_, "/bin/sh", &action, &attr,
>         const_cast<char**>(spawned_args), environ);

`doc/manual.asciidoc:184-188`:
> `ninja -h` prints help output.  Many of Ninja's flags intentionally
> match those of Make; e.g `ninja -C build -j 20` changes into the
> `build` directory and runs 20 build commands in parallel.  (Note that
> Ninja defaults to running commands in parallel anyway, so typically
> you don't need to pass `-j`.)

`doc/manual.asciidoc:191-222`:
> GNU Jobserver support
> ~~~~~~~~~~~~~~~~~~~~~
>
> Since version 1.13., Ninja builds can follow the
> https://https://www.gnu.org/software/make/manual/html_node/Job-Slots.html[GNU Make jobserver]
> client protocol. This is useful when Ninja is invoked as part of a larger
> build system controlled by a top-level GNU Make instance, or any other
> jobserver pool implementation, as it allows better coordination between
> concurrent build tasks.
>
> This feature is automatically enabled under the following conditions:
>
> - Dry-run (i.e. `-n` or `--dry-run`) is not enabled.
>
> - No explicit job count (e.g. `-j<COUNT>`) is passed on the command
>   line.
>
> - The `MAKEFLAGS` environment variable is defined and describes a valid
>   jobserver mode using `--jobserver-auth=SEMAPHORE_NAME` on Windows, or
>   `--jobserver-auth=fifo:PATH` on Posix.
>
> In this case, Ninja will use the jobserver pool of job slots to control
> parallelism, instead of its default parallel implementation.
>
> Note that load-average limitations (i.e. when using `-l<count>`)
> are still being enforced in this mode.
>
> IMPORTANT: On Posix, only the FIFO-based version of the protocol, which is
> implemented by GNU Make 4.4 and higher, is supported. Ninja will detect
> when a pipe-based jobserver is being used (i.e. when `MAKEFLAGS` contains
> `--jobserver-auth=<read>,<write>`) and will print a warning, but will
> otherwise ignore it.

**Coverage.**
- T3: covers ninja's dispatch: N concurrent `/bin/sh -c` children (each command always gets a shell), jobserver client mode since 1.13 (FIFO only), `-l` load check. No CPU-cost figure. Not an observation.
- T4: covers ninja's default parallelism: `nproc + 2` (2 on one CPU, 3 on two), where `nproc` is min(cgroup quota, affinity mask) — so under `taskset -c 0` the default is 2. No documented rationale beyond the code. Not an observation of user choices.
- T6 (single-core confinement): covers only what the default `-j` becomes under a one-CPU affinity mask (2). No measurement.
- T1, T5, T7: do not cover.
- One observation? No.

### S2-06 — Cargo 0.89.0 reference (`build.jobs`, `--jobs`) and job-queue source

**Citation.** The Cargo Book, "Configuration" (`build.jobs`) and "cargo build" (`--jobs`), and `src/cargo/core/compiler/job_queue/mod.rs`, Cargo tag `0.89.0`.

**Copy read.** `https://raw.githubusercontent.com/rust-lang/cargo/0.89.0/src/doc/src/reference/config.md` (SHA-256 ad41969fc77c7f810389b75d15e2833063dc2775e5fbe0a14c33ea7928b0ea78), `…/0.89.0/src/doc/src/commands/cargo-build.md` (dcc01685c12651843de1692460a7dc492b7e17b8c49860f331c4151bb4def628), `…/0.89.0/src/cargo/core/compiler/job_queue/mod.rs` (e3d2d773db84f5ce89a2aaa970b1fc0515d147c70658763d4a1bd8dd7ed33a70, 1237 lines); accessed 2026-09-16; saved under `sources/S2-06/`.

**Verbatim passages.**

`config.md:405-415`:
> #### `build.jobs`
> * Type: integer or string
> * Default: number of logical CPUs
> * Environment: `CARGO_BUILD_JOBS`
>
> Sets the maximum number of compiler processes to run in parallel. If negative,
> it sets the maximum number of compiler processes to the number of logical CPUs
> plus provided value. Should not be 0. If a string `default` is provided, it sets
> the value back to defaults.
>
> Can be overridden with the `--jobs` CLI option.

`cargo-build.md:396-402`:
> <dt class="option-term" id="option-cargo-build---jobs"><a class="option-anchor" href="#option-cargo-build---jobs"></a><code>--jobs</code> <em>N</em></dt>
> <dd class="option-desc">Number of parallel jobs to run. May also be specified with the
> <code>build.jobs</code> <a href="../reference/config.html">config value</a>. Defaults to
> the number of logical CPUs. If negative, it sets the maximum number of
> parallel jobs to the number of logical CPUs plus provided value. If
> a string <code>default</code> is provided, it sets the value back to defaults.
> Should not be 0.</dd>

`job_queue/mod.rs:31-56`:
> //! ## Jobserver
> //!
> //! As of Feb. 2023, Cargo and rustc have a relatively simple jobserver
> //! relationship with each other. They share a single jobserver amongst what
> //! is potentially hundreds of threads of work on many-cored systems.
> //! The jobserver could come from either the environment (e.g., from a `make`
> //! invocation), or from Cargo creating its own jobserver server if there is no
> //! jobserver to inherit from.
> //!
> //! Cargo wants to complete the build as quickly as possible, fully saturating
> //! all cores (as constrained by the `-j=N`) parameter. Cargo also must not spawn
> //! more than N threads of work: the total amount of tokens we have floating
> //! around must always be limited to N.
> //!
> //! It is not really possible to optimally choose which crate should build
> //! first or last; nor is it possible to decide whether to give an additional
> //! token to rustc first or rather spawn a new crate of work. The algorithm in
> //! Cargo prioritizes spawning as many crates (i.e., rustc processes) as
> //! possible. In short, the jobserver relationship among Cargo and rustc
> //! processes is **1 `cargo` to N `rustc`**. Cargo knows nothing beyond rustc
> //! processes in terms of parallelism[^parallel-rustc].
> //!
> //! We integrate with the [jobserver] crate, originating from GNU make
> //! [POSIX jobserver], to make sure that build scripts which use make to
> //! build C code can cooperate with us on the number of used tokens and
> //! avoid overfilling the system we're on.

**Coverage.**
- T3: covers cargo's dispatch (1 `cargo` to N `rustc`, GNU-make-compatible jobserver shared with rustc's codegen threads and build scripts; inherits a make jobserver from the environment). No CPU cost. Not an observation.
- T4: covers cargo's default: number of logical CPUs. Rationale: "fully saturating all cores". Not an observation of users.
- T1, T5, T6, T7: do not cover.

### S2-07 — CMake 3.30.0 `cmake --build --parallel` and `CMAKE_BUILD_PARALLEL_LEVEL`

**Citation.** Kitware, *CMake 3.30.0 documentation*, `Help/manual/cmake.1.rst` (Build Tool Mode, `--parallel`) and `Help/envvar/CMAKE_BUILD_PARALLEL_LEVEL.rst`.

**Copy read.** `https://raw.githubusercontent.com/Kitware/CMake/v3.30.0/Help/manual/cmake.1.rst` (SHA-256 aea8fb48fff51f116127d380aab56fc402b6e0db404e041b13f79c48645e3354) and `…/v3.30.0/Help/envvar/CMAKE_BUILD_PARALLEL_LEVEL.rst` (3fb60468407f021cb82533a55a36c5e3bd9c56154c41faf69ff58d7c15fb4353); accessed 2026-09-16; saved under `sources/S2-07/Help/`.

**Verbatim passages.**

`Help/manual/cmake.1.rst:629-640`:
> .. option:: -j [<jobs>], --parallel [<jobs>]
>
>   .. versionadded:: 3.12
>
>   The maximum number of concurrent processes to use when building.
>   If ``<jobs>`` is omitted the native build tool's default number is used.
>
>   The :envvar:`CMAKE_BUILD_PARALLEL_LEVEL` environment variable, if set,
>   specifies a default parallel level when this option is not given.
>
>   Some native build tools always build in parallel.  The use of ``<jobs>``
>   value of ``1`` can be used to limit to a single job.

`Help/envvar/CMAKE_BUILD_PARALLEL_LEVEL.rst:1-17`:
> CMAKE_BUILD_PARALLEL_LEVEL
> --------------------------
>
> .. versionadded:: 3.12
>
> .. include:: ENV_VAR.txt
>
> Specifies the maximum number of concurrent processes to use when building
> using the ``cmake --build`` command line
> :ref:`Build Tool Mode <Build Tool Mode>`.
> For example, if ``CMAKE_BUILD_PARALLEL_LEVEL`` is set to 8, the
> underlying build tool will execute up to 8 jobs concurrently as if
> ``cmake --build`` were invoked with the
> :option:`--parallel 8 <cmake--build --parallel>` option.
>
> If this variable is defined empty the native build tool's default number is
> used.

**Coverage.**
- T4: covers CMake's default (defers to the native tool: make → 1, ninja → nproc+2 per S2-03/S2-05). No rationale, no observation.
- T3: covers only that CMake passes the level to the native tool. Other topics: do not cover.

### S2-08 — Debian: dpkg-buildpackage 1.22.11 (`-j`, `parallel=`), Debian Policy §4.9.1, Debian kernel handbook

**Citation.** (a) dpkg 1.22.11, `man/dpkg-buildpackage.pod`, `scripts/dpkg-buildpackage.pl`, `scripts/Dpkg/BuildOptions.pm`; (b) *Debian Policy Manual* v4.7.4.1, §4.9.1 "debian/rules and DEB_BUILD_OPTIONS"; (c) *Debian Linux Kernel Handbook*, chapter 4 "Common kernel-related tasks", §4.5.1.

**Copy read.** `https://raw.githubusercontent.com/guillemj/dpkg/1.22.11/man/dpkg-buildpackage.pod` (SHA-256 f27efe854320d36fa72b706647370b65955544abb7b91b190998b1b3ee289a05), `…/1.22.11/scripts/dpkg-buildpackage.pl` (a0b863b4ad03208db43aefbc4ece942998f64a831e19af0539052432517cd0b1), `…/1.22.11/scripts/Dpkg/BuildOptions.pm` (28c3ffca8d99e2b664ce7ea21b1cc5c1d803ee5db0b3c2183528739e8fa96427); `https://www.debian.org/doc/debian-policy/ch-source.html` (7e418f4d2b595cb8e2db060c95606198951c0a0589a87cde91aded60c82d11a9; page header "Debian Policy Manual v4.7.4.1"); `https://kernel-team.pages.debian.net/kernel-handbook/ch-common-tasks.html` (d71b40b4ea5a5788f2a2504954af600fb154984e9282aac0682b9c0b4ac78133); accessed 2026-09-16; saved under `sources/S2-08/`.

**Verbatim passages.**

`man/dpkg-buildpackage.pod:340-362`:
> =item B<-j>, B<--jobs>[=I<jobs>|B<auto>]
>
> Specifies the number of jobs allowed to be run simultaneously
> (since dpkg 1.14.7, long option since dpkg 1.18.8).
> The number of jobs matching the number of online processors if B<auto> is
> specified (since dpkg 1.17.10), or unlimited number if I<jobs> is not
> specified.
> The default behavior is B<auto> (since dpkg 1.18.11) in non-forced mode
> (since dpkg 1.21.10), and as such it is always safer to use with any
> package including those that are not parallel-build safe.
> Setting the number of jobs to B<1> will restore serial execution.
>
> Will add B<parallel=>I<jobs> or B<parallel> to the B<DEB_BUILD_OPTIONS>
> environment variable which allows debian/rules files to opt-in to use this
> information for their own purposes.
> The I<jobs> value will override the B<parallel=>I<jobs> or
> B<parallel> option in the B<DEB_BUILD_OPTIONS> environment variable.
> Note that the B<auto> value will get replaced by the actual number of
> currently active processors, and as such will not get propagated to any
> child process.
> If the number of online processors cannot be inferred then
> the code will fallback to using serial execution (since dpkg 1.18.15),
> although this should only happen on exotic and unsupported systems.

`man/dpkg-buildpackage.pod:373-378`:
> =item B<--jobs-force>[=I<jobs>|B<auto>]
>
> This option (since dpkg 1.21.10) is equivalent to the B<--jobs> option
> except that it will enable forced parallel mode, by adding the B<make> B<-j>
> option with the computed number of parallel jobs to the B<MAKEFLAGS>
> environment variable.

`scripts/dpkg-buildpackage.pl:460-463, 471-487` (how "auto" is computed — `getconf _NPROCESSORS_ONLN`, i.e. online processors, not the affinity mask):
> # Default to auto if none of parallel=N, -J or -j have been specified.
> if (not defined $parallel and not $build_opts->has('parallel')) {
>     $parallel = 'auto';
> }
> …
> if (defined $parallel) {
>     if ($parallel eq 'auto') {
>         # Most Unices.
>         $parallel = qx(getconf _NPROCESSORS_ONLN 2>/dev/null);
>         # Fallback for at least Irix.
>         $parallel = qx(getconf _NPROC_ONLN 2>/dev/null) if $?;
>         # Fallback to serial execution if cannot infer the number of online
>         # processors.
>         $parallel = '1' if $?;
>         chomp $parallel;
>     }
>     if ($parallel_force) {
>         $ENV{MAKEFLAGS} //= '';
>         $ENV{MAKEFLAGS} .= " -j$parallel";
>     }
>     $build_opts->set('parallel', $parallel);
>     $build_opts->export();
> }

Debian Policy v4.7.4.1, §4.9.1, entry `parallel=n` (HTML rendered to text):
> parallel=n This tag means that the package should be built using up to n parallel processes if the package build system supports this.  [14] If the package build system does not support parallel builds, this string must be ignored. If the package build system only supports a lower level of concurrency than n, the package should be built using as many parallel processes as the package build system supports. It is up to the package maintainer to decide whether the package build times are long enough and the package build system is robust enough to make supporting parallel builds worthwhile.

Debian Policy v4.7.4.1, §4.9.1, example snippet and footnote 14:
> ifneq (,$(filter parallel=%,$(DEB_BUILD_OPTIONS)))
>     NUMJOBS = $(patsubst parallel=%,%,$(filter parallel=%,$(DEB_BUILD_OPTIONS)))
>     MAKEFLAGS += -j$(NUMJOBS)
> endif
> …
> [14] Packages built with make can often implement this by passing the -jn option to make.

Debian Linux Kernel Handbook, §4.5.1 (HTML rendered to text):
> $ export MAKEFLAGS=-j$(nproc)
> Enable parallel builds using one job per CPU by default.

**Coverage.**
- T4: covers the Debian packaging default (`-j auto` = number of online processors via `getconf _NPROCESSORS_ONLN`, opt-in through `DEB_BUILD_OPTIONS=parallel=N`; `--jobs-force` puts `-jN` into `MAKEFLAGS`), the policy's semantics of `parallel=n`, and the Debian kernel handbook's recommendation `-j$(nproc)` ("one job per CPU"). No rationale beyond "one job per CPU"; no observation of what users pick.
- T6 (single-core confinement): covers that dpkg's "auto" uses online processors, not the affinity mask (so a `taskset`-confined `dpkg-buildpackage` still computes the full count). No measurement.
- Other topics: do not cover. One observation? No.

### S2-09 — RPM 4.19.0 macros (`%_smp_mflags`, `%_smp_build_ncpus`, `%_smp_tasksize_proc`, `%{getncpus}`) and Fedora Packaging Guidelines "Parallel Make"

**Citation.** (a) rpm 4.19.0, `macros.in` and `rpmio/macro.c`; (b) Fedora Project, *Packaging Guidelines*, section "Parallel Make"; (c) Fedora `redhat-rpm-config` `macros` (rawhide) — checked, contains no SMP macro.

**Copy read.** `https://raw.githubusercontent.com/rpm-software-management/rpm/rpm-4.19.0-release/macros.in` (SHA-256 9e5cad241d807b4485047d3cdfdb6be3d282bb637471bf40ad6d798c158b605c), `…/rpm-4.19.0-release/rpmio/macro.c` (611e893de6c5b311c96c5e663acbe98a22db2b585594ee94cdb2698a80ecf1db, 2165 lines); `https://docs.fedoraproject.org/en-US/packaging-guidelines/` (c32360136bfe95827b9110a3b9e2aa519800ba1363330befddeafcf385009585); `https://src.fedoraproject.org/rpms/redhat-rpm-config/raw/rawhide/f/macros` (d32ef23a464a2582d275d01c43c3609c7d9e37af3c1ed7b8a22b668a775779ff); accessed 2026-09-16; saved under `sources/S2-09/`.

**Verbatim passages.**

`macros.in:731-752`:
> %__smp_use_ncpus() %([ -z "$RPM_BUILD_NCPUS" ] \\\
> 	&& RPM_BUILD_NCPUS="%{getncpus %{?1}}"; \\\
>         ncpus_max=%{?_smp_ncpus_max}; \\\
>         if [ -n "$ncpus_max" ] && [ "$ncpus_max" -gt 0 ] && [ "$RPM_BUILD_NCPUS" -gt "$ncpus_max" ]; then RPM_BUILD_NCPUS="$ncpus_max"; fi; \\\
>         echo "$RPM_BUILD_NCPUS";)
>
> # Maximum number of CPU's to use when building, 0 for unlimited.
> #%_smp_ncpus_max 0
>
> %_smp_build_ncpus %{__smp_use_ncpus:proc}
>
> %_smp_mflags -j${RPM_BUILD_NCPUS}
>
> # Maximum number of threads to use when building, 0 for unlimited
> #%_smp_nthreads_max 0
>
> %_smp_build_nthreads %{__smp_use_ncpus:thread}
>
> # Assumed task size of processes and threads in megabytes.
> # Used to limit the amount of parallelism based on available memory.
> %_smp_tasksize_proc 512
> %_smp_tasksize_thread %{_smp_tasksize_proc}

`macros.in:1064-1065`:
> # The "make" analogue, hiding the _smp_mflags magic from specs
> %make_build %{__make} %{_make_output_sync} %{?_smp_mflags} %{_make_verbose}

`rpmio/macro.c:612-627` (`getncpus` honours the affinity mask):
> static unsigned int getncpus(void)
> {
>     unsigned int ncpus = 0;
> #ifdef HAVE_SCHED_GETAFFINITY
>     cpu_set_t set;
>     if (sched_getaffinity (0, sizeof(set), &set) == 0)
> 	ncpus = CPU_COUNT(&set);
> #endif
>     /* Fallback to sysconf() if the above isn't supported or didn't work */
>     if (ncpus < 1)
> 	ncpus = sysconf(_SC_NPROCESSORS_ONLN);
>     /* If all else fails, there's always the one we're running on... */
>     if (ncpus < 1)
> 	ncpus = 1;
>     return ncpus;
> }

`rpmio/macro.c:1242-1261` (memory cap: available memory / 512 MB per process):
>     if (sizemacro) {
> 	unsigned int mcpus;
> 	unsigned long tasksize = rpmExpandNumeric(sizemacro);
>
> 	if (tasksize == 0)
> 	    tasksize = 512;
>
> 	if (mem == 0) {
> 	    mbErr(mb, 1, _("failed to get available memory for %s\n"), arg);
> 	    return;
> 	}
>
> 	mcpus = mem / tasksize;
> 	if (mcpus < ncpus)
> 	    ncpus = mcpus;
>     }
>
>     sprintf(buf, "%u", ncpus);
>     mbAppendStr(mb, buf);
> }

Fedora Packaging Guidelines, section "Parallel Make" (HTML rendered to text; page has no version string, accessed 2026-09-16):
> Parallel Make
> Whenever possible, invocations of make should be done as
> %make_build
> This generally speeds up builds and especially on SMP machines.
> Do make sure, however, that the package builds cleanly this way
> as some make files do not support parallel building.
> Therefore you should consider adding
> %_smp_mflags -j3
> to your ~/.rpmmacros file — even on UP machines — as this will expose most of these errors.

Reader's own check: `grep -n -i 'smp\|ncpus' rh-macros` over the fetched redhat-rpm-config `macros` returns nothing — Fedora inherits rpm's own definition above.

**Coverage.**
- T4: covers the RPM/Fedora default: `-j` = number of CPUs in the affinity mask (`sched_getaffinity` → `CPU_COUNT`), capped by available memory / 512 MB per process (`%_smp_tasksize_proc`), optionally by `%_smp_ncpus_max`; Fedora's guideline recommends `%make_build` and suggests `-j3` on UP machines to flush out parallel-unsafe makefiles. No observation of user choices.
- T6 (single-core confinement): covers that under a one-CPU affinity mask `%_smp_mflags` becomes `-j1`. No measurement.
- Other topics: do not cover.

### S2-10 — Arch Linux `makepkg.conf` (pacman 7.0.0) and ArchWiki "makepkg"

**Citation.** (a) pacman 7.0.0, `etc/makepkg.conf.in`; (b) ArchWiki, "makepkg", sections "Parallel compilation", "Running makepkg in a systemd control group", "Running with idle scheduling policy" (page footer: "last edited on 3 August 2026, at 10:04").

**Copy read.** `https://gitlab.archlinux.org/pacman/pacman/-/raw/v7.0.0/etc/makepkg.conf.in` (SHA-256 be73eff9cde70c3370575c900dbaaf443501df92f48b61ade4a1d69a02770f4e); `https://wiki.archlinux.org/title/Makepkg` (5a4edfbcdd69a7f941fa6e7533ab020a01d41fda05189e3205a5839ea9eb09ae); accessed 2026-09-16; saved under `sources/S2-10/`.

**Verbatim passages.**

`etc/makepkg.conf.in:45-46`:
> #-- Make Flags: change this for DistCC/SMP systems
> #MAKEFLAGS="-j2"

ArchWiki "makepkg", §"Parallel compilation" (HTML rendered to text):
> The make build system uses the MAKEFLAGS environment variable to specify additional options for make. The variable can also be set in the makepkg.conf file.
> Users with multi-core/multi-processor systems can specify the number of jobs to run simultaneously. This can be accomplished with the use of nproc(1) to determine the number of available processors, e.g. MAKEFLAGS="--jobs=$(nproc)".
> Some PKGBUILDs specifically override this with -j1, because of race conditions in certain versions or simply because it is not supported in the first place.

ArchWiki "makepkg", §"Running with idle scheduling policy":
> Package build process can lead to high CPU utilization, especially in case of #Parallel compilation. Under heavy CPU load, the system can issue a significant slowdown up to becoming unusable, even with the highest nice(1) value. User interface and foreground applications may stutter or even became unresponsive.
> This can be worked around by changing the scheduling policy to SCHED_IDLE before running makepkg. It ensures that package building process does not interfere with regular tasks and only utilizes remaining unused CPU time.
> …
> $ chrt -iap 0 $$

ArchWiki "makepkg", §"Running makepkg in a systemd control group":
> If the package you are building takes too many resources to build with your default make flags, which are otherwise set properly for most packages, you can try running it in its own control group. makepkg-cgAUR is a wrapper for makepkg that achieved this via systemd control groups (see systemd.resource-control(5)).

**Coverage.**
- T4: covers Arch's shipped default (`MAKEFLAGS` commented out, i.e. make's own default of 1; the template example is `-j2`) and the wiki's recommendation `--jobs=$(nproc)`. No observation of what users pick.
- T7 (process treatment): covers a distribution wiki's recommendation to run builds under `SCHED_IDLE` (`chrt -i 0`) and the stated motivation ("even with the highest nice(1) value" the desktop can become unusable). Not a measurement.
- Other topics: do not cover.

### S2-11 — Gentoo wiki "MAKEOPTS" (Portage defaults)

**Citation.** Gentoo Wiki, "MAKEOPTS" (page footer: "last edited on 1 July 2026, at 07:21").

**Copy read.** `https://wiki.gentoo.org/wiki/MAKEOPTS`, SHA-256 1fa2d48b559dbab6c3a1c4594d91e145e4f7f86ff3219067bcc3da5e22ed8455, accessed 2026-09-16, saved as `sources/S2-11/MAKEOPTS.html`. (Also fetched: `Handbook:AMD64/Working/Features` 53cea7109b0b960785416f4e55c33e962c6da5f814d985ba1c4bf070ea1eefd8 and `Handbook:AMD64/Installation/Base` 7a1725f080ac6cd8c1e9e310a78ec964a2ac0ec60d0b00450f4600da1a8298c4 — not quoted.)

**Verbatim passages** (HTML rendered to text).

Lead paragraph and tip:
> MAKEOPTS is a variable that defines and limits how many parallel make jobs can be launched from Portage. It can be set in the /etc/portage/make.conf configuration file.
> Tip Generally, the number of jobs specified in MAKEOPTS is less than or equal to the CPU's thread count or the size of RAM/2GB, whichever is smaller.

§"MAKEOPTS on a system-wide basis":
> The parallel jobs entry ensures that, when make is invoked, it knows how many parallel sessions it is allowed to trigger (when parallel sessions are possible of course). This is completely within the scope of that make command and has no influence on parallel installations (which is triggered through emerge with --jobs=X option). The recommended value is the number of logical processors in the CPU.
> …
> The make program creates parallel tasks based on the system's current load average and the --load-average limit. Since the load average is a damped value, the load-average jobs limitation can be sensibly set slightly above the number of available CPUs. For a machine with 4 physical cores with 2 threads per core, or 8 logical cores, MAKEOPTS could be set to:
> FILE /etc/portage/make.conf MAKEOPTS="--jobs 8 --load-average 9"
> Also, since Portage 3.0.31[1] and 3.0.53[2], --jobs and --load-average respectively default to the number of threads returned by nproc if MAKEOPTS is unset.
> Jobs should also be limited by RAM. Recent gcc versions can take 1.5 GB to 2 GB of RAM per job for large C++ codebases. For systems with 8 logical CPUs and only 4 GB RAM, MAKEOPTS should be lowered to -j2 so that the system can run the basics and also compile without hitting swap very often slowing things down.

**Coverage.**
- T4: covers Gentoo's default (`--jobs` and `--load-average` default to `nproc` since Portage 3.0.31 / 3.0.53), the recommendation (`-j` = logical processors, `-l` slightly above, capped by RAM/2 GB), with the stated rationale (load average is damped; gcc memory per job). No observation of what users pick. Other topics: do not cover.

### S2-12 — DKMS 3.1.8 (`dkms.in`, `dkms.8`, `dkms.service`, `dkms_autoinstaller`, kernel hooks)

**Citation.** Dell / DKMS project, *Dynamic Kernel Module Support* v3.1.8, files `dkms.in`, `dkms.8.in`, `dkms.service.in`, `dkms_autoinstaller.in`, `debian_kernel_postinst.d.in`, `redhat_kernel_install.d.in`.

**Copy read.** `git clone --depth 1 --branch v3.1.8 https://github.com/dell/dkms`, commit `eb06953aca4871ff110887cbee45d6f4d782b821`, accessed 2026-09-16, saved under `sources/S2-12/repo/` (commit in `sources/S2-12/COMMIT.txt`).

**Verbatim passages.**

`dkms.in:295-305`:
> # Find out how many CPUs there are so that we may pass an appropriate -j
> # option to make. Ignore hyperthreading for now.
> get_num_cpus()
> {
>     # use nproc(1) from coreutils 8.1-1+ if available, otherwise single job
>     if [[ -x /usr/bin/nproc ]]; then
>         nproc
>     else
>         echo "1"
>     fi
> }

`dkms.in:3203-3207`:
> # Default to -j<number of CPUs>
> parallel_jobs=${parallel_jobs:-$(get_num_cpus)}
>
> # Make sure we're not passing -j0 to make; treat -j0 as just "-j"
> [[ "$parallel_jobs" = 0 ]] && parallel_jobs=""

`dkms.in:782` (the default make command when `dkms.conf` gives none):
>     [[ ! $make_command ]] && make_command="make -C $kernel_source_dir M=$dkms_tree/$module/$module_version/build"

`dkms.in:1434-1439`:
>     local the_make_command
>     the_make_command="${make_command/#make/make -j$parallel_jobs KERNELRELEASE=$kernelver}"
>
>     invoke_command "$the_make_command" "Building module(s)" "$build_log" background || \
>         report_build_problem 10 "Bad return status for module build on kernel: $kernelver ($arch)" \
>         "Consult $build_log for more information."

`dkms.in:2905, 2911, 2913` (kernel install hook → autoinstall; intervening local declarations elided):
> kernel_postinst()
> …
>     have_one_kernel kernel_postinst
> …
>     autoinstall

`dkms.8.in:242-246`:
> .SY autoinstall
> .YS
> .IP "" 4
> Attempt to install the latest revision of all modules that have been installed for other kernel revisions.
> dkms_autoinstaller is a stub that uses this action to perform its work.

`dkms.8.in:420-427`:
> .B \-j number
> Run no more than
> .I number
> jobs in parallel; see the -j option of
> .I make(1).
> Defaults to the number of CPUs in the system, detected by
> .I nproc(1).
> Specify 0 to impose no limit on the number of parallel jobs.

`dkms.service.in` (whole file, 11 lines):
> [Unit]
> Description=Builds and install new kernel modules through DKMS
> Documentation=man:dkms(8)
> Before=network-pre.target graphical.target
>
> [Service]
> Type=oneshot
> RemainAfterExit=true
> ExecStart=@SBINDIR@/dkms autoinstall --verbose --kernelver %v
>
> [Install]
> WantedBy=multi-user.target

`debian_kernel_postinst.d.in` (whole file):
> #!/bin/sh
>
> # We're passed the version of the kernel being installed
> inst_kern=$1
>
> if [ -x @LIBDIR@/dkms_autoinstaller ]; then
>     exec @LIBDIR@/dkms_autoinstaller start "$inst_kern"
> fi

`dkms_autoinstaller.in:32-38`:
> 		if [ ! -d "$MODDIR/$kernel/build/include" ]; then
> 			echo "Automatic installation of modules for kernel $kernel was skipped since the kernel headers for this kernel do not seem to be installed."
> 		else
> 			dkms autoinstall --kernelver "$kernel"
> 			res=$?
> 			test $res = 0
> 		fi

`redhat_kernel_install.d.in:8-11`:
>     add)
>         dkms kernel_postinst --kernelver "$KERNEL_VERSION"
>         res=$?
>         ;;

**Coverage.**
- T5: covers what an autoinstall run does process-wise as far as the tool defines it: for each module needing a build, one `make -j$(nproc) KERNELRELEASE=<ver> -C <kernel-src> M=<build-dir>` (an out-of-tree kbuild run: per S2-01 that is a sub-make per module directory, per `.c` one `$(CC)` (+`cc1`, `as`) + `fixdep`, then `Makefile.modpost` and `Makefile.modfinal` sub-makes); `-j` defaults to `nproc` (which honours the affinity mask, S2-16), pre/post build scripts and `invoke_command` (background progress dots). Triggers: the boot service `dkms.service` (`dkms autoinstall --kernelver %v`, `Before=graphical.target`), the Debian `kernel/postinst.d` hook (→ `dkms_autoinstaller start`), the Fedora/RHEL `kernel/install.d` hook (→ `dkms kernel_postinst` → `autoinstall`). Does not cover: number of compiler processes (depends on the module), duration, CPU. Not an observation.
- T4: covers DKMS's own `-j` default = `nproc`. Other topics: do not cover.

### S2-13 — Linux scheduler: SCHED_AUTOGROUP help text and commit 5091faa449ee, `sched_child_runs_first` in v6.6, scheduler docs, and sched_ext/scx READMEs

**Citation.** (a) Linux v6.6 `init/Kconfig` (SCHED_AUTOGROUP), `kernel/sched/autogroup.c`, `kernel/sched/fair.c`, `Documentation/admin-guide/sysctl/kernel.rst`, `Documentation/scheduler/index.rst`; (b) Mike Galbraith, commit 5091faa449ee0b7d73bc296a93bca9540fc51d0a "sched: Add 'autogroup' scheduling feature: automated per session task groups", 2010-11-30; (c) sched-ext/scx repository `README.md` and `scheds/rust/scx_rustland/README.md`, `main` at commit dd211684716153e44d2405b6c895e3392de6ce3a.

**Copy read.** `https://raw.githubusercontent.com/torvalds/linux/v6.6/init/Kconfig` (SHA-256 6c5442c33760782fce0b93126f5a6966cf9fe3dab3d109827f473e7ddcc5ca7a, saved under `sources/S2-01/`), `…/v6.6/kernel/sched/autogroup.c` (5b2894921110e2797c78290447db3f1a984efff94971097167852400fce7c011), `…/v6.6/kernel/sched/fair.c` (7d259d533ffb439992969e5d1d20b27dc64c9203f5c09e09f839047cbd4e40bb, 13016 lines), `…/v6.6/Documentation/admin-guide/sysctl/kernel.rst` (d900982b3a0e91c9c658fc9d0a560d78adcf6d3dfb641202ee5c7d702880145d), `…/v6.6/Documentation/scheduler/index.rst` (c0915a5f61afbeefc3a52e0386dd3bd0fbd1a8c9a3bdc6009524fbc6da23ae4a); `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/patch/?id=5091faa449ee` (a37bdca3b53f4d6062746b66c141c161b198b237bb7a4c89e023e88a93dab43a); `https://raw.githubusercontent.com/sched-ext/scx/main/README.md` (b7ebada1f7b37a8e46494f0a6106b3d1c781845d9c6b5aa85e79a0220478d618) and `…/main/scheds/rust/scx_rustland/README.md` (9ad422e4abe89f179b2ccdf0fd94c675cf1e8a0f1cae20bf561ca48e8b3792a5), `main` HEAD = dd211684716153e44d2405b6c895e3392de6ce3a by `git ls-remote` at access time; all accessed 2026-09-16; saved under `sources/S2-13/`.

**Verbatim passages.**

`init/Kconfig:1261-1271` (v6.6):
> config SCHED_AUTOGROUP
> 	bool "Automatic process group scheduling"
> 	select CGROUPS
> 	select CGROUP_SCHED
> 	select FAIR_GROUP_SCHED
> 	help
> 	  This option optimizes the scheduler for common desktop workloads by
> 	  automatically creating and populating task groups.  This separation
> 	  of workloads isolates aggressive CPU burners (like build jobs) from
> 	  desktop applications.  Task group autogeneration is currently based
> 	  upon task session.

Commit 5091faa449ee, message lines 7-25 of the patch file:
> A recurring complaint from CFS users is that parallel kbuild has
> a negative impact on desktop interactivity.  This patch
> implements an idea from Linus, to automatically create task
> groups.  Currently, only per session autogroups are implemented,
> but the patch leaves the way open for enhancement.
>
> Implementation: each task's signal struct contains an inherited
> pointer to a refcounted autogroup struct containing a task group
> pointer, the default for all tasks pointing to the
> init_task_group.  When a task calls setsid(), a new task group
> is created, the process is moved into the new task group, and a
> reference to the preveious task group is dropped.  Child
> processes inherit this task group thereafter, and increase it's
> refcount.  When the last thread of a process exits, the
> process's reference is dropped, such that when the last process
> referencing an autogroup exits, the autogroup is destroyed.
>
> At runqueue selection time, IFF a task has no cgroup assignment,
> its current autogroup is used.

`kernel/sched/autogroup.c:7, 193-202` (v6.6; still enabled by default, created on setsid):
> unsigned int __read_mostly sysctl_sched_autogroup_enabled = 1;
> …
> void sched_autogroup_create_attach(struct task_struct *p)
> {
> 	struct autogroup *ag = autogroup_create();
>
> 	autogroup_move_group(p, ag);
>
> 	/* Drop extra reference added by autogroup_create(): */
> 	autogroup_kref_put(ag);
> }
> EXPORT_SYMBOL(sched_autogroup_create_attach);

`kernel/sched/fair.c:81-85, 147-154` (v6.6):
> /*
>  * After fork, child runs first. If set to 0 (default) then
>  * parent will (try to) run first.
>  */
> unsigned int sysctl_sched_child_runs_first __read_mostly;
> …
> static struct ctl_table sched_fair_sysctls[] = {
> 	{
> 		.procname       = "sched_child_runs_first",
> 		.data           = &sysctl_sched_child_runs_first,
> 		.maxlen         = sizeof(unsigned int),
> 		.mode           = 0644,
> 		.proc_handler   = proc_dointvec,
> 	},

Reader's own check: `grep -n sysctl_sched_child_runs_first kernel/sched/fair.c` in v6.6 returns only lines 85 and 150 — the variable is declared and exposed as a sysctl but referenced nowhere else in `fair.c` (no scheduling code reads it in v6.6). `grep -n -i 'child_runs_first\|autogroup' Documentation/admin-guide/sysctl/kernel.rst Documentation/scheduler/index.rst` returns nothing: neither sysctl is documented under `Documentation/` in v6.6.

scx `README.md:24-27`:
> - The following video is the [`scx_rustland`](https://github.com/sched-ext/scx/tree/main/scheds/rust/scx_rustland)
>   scheduler which makes most scheduling decisions in userspace `Rust` code showing
>   better FPS in terraria while kernel is being compiled. This doesn't mean that
>   `scx_rustland` is a better scheduler but does demonstrate how safe and easy it is to

scx `scheds/rust/scx_rustland/README.md:43-47`:
> The key takeaway of this demo is to demonstrate that , despite the overhead of
> running a scheduler in user-space, we can still obtain interesting results and,
> in this particular case, even outperform the default Linux scheduler (EEVDF) in
> terms of application responsiveness (FPS), while a CPU intensive workload
> (parallel kernel build) is running in the background.

**Coverage.**
- T6: covers (i) a kernel scheduler feature explicitly motivated by parallel kernel builds (autogroup: "parallel kbuild has a negative impact on desktop interactivity"; Kconfig: "isolates aggressive CPU burners (like build jobs) from desktop applications"), its mechanism (one task group per session, created on `setsid()`, inherited by children) and its default (enabled); (ii) `sched_child_runs_first`: present as a sysctl in v6.6 but unreferenced by the fair scheduler and undocumented; (iii) sched_ext's demonstration workload is "parallel kernel build" in the background of a game, with no `-j`, machine, config or process counts given. Does not cover process-lifetime distributions or single-core confinement. No observation with machine/subject/window named.
- T7: covers the kernel's own categorisation of "build jobs" as "aggressive CPU burners" (a design statement, not a measurement).
- T1, T3, T4, T5: do not cover.

### S2-14 — interbench (Con Kolivas): the "Compile" and "Burn" loads

**Citation.** Con Kolivas, *interbench — the Linux interactivity benchmark*, files `interbench.c`, `interbench.8`, `readme`, GitHub `ckolivas/interbench`, commit e612a65ce941028ddea804e6b45ccde2750720d2 (2016-10-24).

**Copy read.** `git clone --depth 1 https://github.com/ckolivas/interbench` (no release tag used; HEAD = e612a65ce941028ddea804e6b45ccde2750720d2, commit date Mon Oct 24 09:23:02 2016 +1100), accessed 2026-09-16, saved under `sources/S2-14/repo/`.

**Verbatim passages.**

`interbench.8:12`:
> \fB\-L\fR     Use cpu load of with burn load (default: 4)

`interbench.8:120-132` (identical text in `readme:84-96`):
> .B Burn:
> A configurable number of threads fully cpu bound (4 by default).
>
> .B Write:
> A streaming write to disk repeatedly of a file the size of physical ram.
>
> .B Read:
> Repeatedly reading a file from disk the size of physical ram (to avoid any
> caching effects).
>
> .B Compile:
> Simulating a heavy 'make -j4' compilation by running Burn, Write and Read
> concurrently.

`interbench.c:614-630`:
> /* Have ud.cpu_load threads burn cpu continuously */
> void emulate_burn(struct thread *th)
> {
> 	sem_t *s = &th->sem.stop;
> 	unsigned long i;
> 	long t;
> 	pthread_t burnthreads[ud.cpu_load];
>
> 	t = th->threadno;
> 	for (i = 0 ; i < ud.cpu_load ; i++)
> 		create_pthread(&burnthreads[i], NULL, burn_thread,
> 			(void*)(long) t);
> 	wait_sem(s);
> 	post_sem(&th->sem.stopchild);
> 	for (i = 0 ; i < ud.cpu_load ; i++)
> 		join_pthread(burnthreads[i], NULL);
> }

`interbench.c:770-772`:
> /* We emulate a compile by running burn, write and read threads simultaneously */
> void emulate_compile(struct thread *th)
> {

`interbench.c:1520-1521` (the actual default of the burn count in this revision is the online CPU count, not the man page's 4):
> 	ud.cpu_load = sysconf(_SC_NPROCESSORS_ONLN);
> 	sched_getaffinity(0, sizeof(ud.cpumask), &ud.cpumask);

`readme:130-136` (the author's example table; header columns in the readme are "Load", "Latency +/- SD (ms)", "Max Latency", "% Desired CPU", "% Deadlines Met"):
> None	  0.495 +/- 0.495         45		 100	         96
> Video	   11.7 +/- 11.7        1815		89.6	       62.7
> Burn	   27.9 +/- 28.1        3335		78.5	         44
> Write	   4.02 +/- 4.03         372		  97	       78.7
> Read	   1.09 +/- 1.09         158		99.7	         88
> Compile	   28.8 +/- 28.8        3351		78.2	       43.7
> Memload	   2.81 +/- 2.81         187		98.7	         85

**Coverage.**
- T7: covers how one classic interactivity benchmark *models* a compile: N always-runnable CPU-burning threads (N = online CPUs in the code; "4 by default" in the man page) plus one streaming writer and one streaming reader, run concurrently, i.e. a saturating batch job with no fork/exit churn. Not a process-population model of a real build.
- T6: covers a benchmark's compile-workload definition ("make -j4" emulation) used for scheduler evaluation; the readme table is one observation (latency of an "X"-like thread under each load) with no machine, kernel version or window named — the readme does not say on which machine or kernel the table was produced.
- T1, T3, T4, T5: do not cover.
- One observation? The readme table is one run (unnamed machine, unnamed kernel, 30 s per benchmark by the `-t` default); everything else is source.

### S2-15 — Ananicy (upstream) and CachyOS `ananicy-rules`: compiler and batch-job rules and their removal history

**Citation.** (a) Nefelim4ag/Ananicy, `README.md`, `ananicy.d/00-types.types`, `ananicy.d/00-default/compilers/*.rules`, `ananicy.d/00-default/clamd.rules`, commit 1e2cc9a62ba3b6793e59da66aa0039f89e1ad49f (2023-03-21); (b) CachyOS/ananicy-rules, `00-types.types`, `00-default/**/*.rules`, commit 03ef03fbf7e834385377432ccecaedd32e3414bb (2026-09-08), with its full git history (2762 commits).

**Copy read.** `git clone --depth 1 https://github.com/Nefelim4ag/Ananicy` (HEAD 1e2cc9a62ba3b6793e59da66aa0039f89e1ad49f) → `sources/S2-15/ananicy/`; `git clone --depth 50 https://github.com/CachyOS/ananicy-rules` then `git fetch --unshallow` (HEAD 03ef03fbf7e834385377432ccecaedd32e3414bb) → `sources/S2-15/cachyos/`; accessed 2026-09-16.

**Verbatim passages — upstream Ananicy (commit 1e2cc9a).**

`README.md:24-27`:
> I just wanted a tool for auto set programs nice in my system, i.e.:
> * Why do I get lag, while compiling kernel and playing games?
> * Why does dropbox client eat all my IO?
> * Why does torrent/dc client make my laptop run slower?

`README.md:68` (example rule):
> { "name": "gcc", "type": "Heavy_CPU", "nice": 19, "ioclass": "best-effort", "ionice": 7, "cgroup": "cpu90" }

`README.md:101`:
> 5. For CPU hungry backround task like compiling, just use `NICE=19`.

`ananicy.d/00-types.types:42`:
> {"type":"compiler", "nice":1}

`ananicy.d/00-types.types:103-111` (deprecated types, commented out):
> ########################
> ### Depricated types ###
> ########################
>
> #{"type":"Heavy_CPU", "nice":19, "ioclass":"best-effort", "ionice":7, "cgroup":"cpu90"}
>
> # BackGround CPU/IO Load
> # It's needed, but it must be as silent as possible
> #{"type":"BG_CPUIO", "nice":19, "ioclass":"idle", "sched":"idle", "cgroup":"cpu80" }

Shipped compiler rules (each file's single line as shown): `ananicy.d/00-default/compilers/gcc.rules:1` `{ "name": "gcc", "type": "compiler" }`; `compilers/g++.rules:1` `{ "name": "g++", "type": "compiler" }`; `compilers/make.rules:2` `{ "name":"make", "type":"compiler" }`; `compilers/meson.rules:2` `{ "name": "ninja", "type": "compiler" }`; `compilers/rust.rules:1-2` `{ "name": "cargo", "type": "compiler" }` / `{ "name": "rustc", "type": "compiler" }`; `compilers/javac.rules:1`, `compilers/go.rules:2` likewise. Batch jobs: `00-default/clamd.rules:2` `{ "name": "clamd", "type": "BG_CPUIO" }`; `00-default/clang-tidy.rules:1` `{ "name": "clang-tidy", "type": "BG_CPUIO" }`. Reader's own check: no rule names `cc1`, `cc1plus`, `as`, `ld` or `collect2` in either rule set (`grep -rn '"name": *"\(cc1\|cc1plus\|as\|ld\|collect2\)"'` over both trees: 0 hits).

**Verbatim passages — CachyOS ananicy-rules (commit 03ef03f).**

`00-types.types:4, 18, 22, 33`:
> { "type": "Game", "nice": -5, "ioclass": "best-effort", "sched": "normal" }
> …
> { "type": "LowLatency_RT", "nice": -12, "ioclass": "best-effort" }
> …
> { "type": "BG_CPUIO", "nice": 16, "ioclass": "idle", "sched": "idle" }
> …
> { "type": "Heavy_CPU", "nice": 9, "ioclass": "best-effort", "ionice": 7 }

Batch-job rules at HEAD: `00-default/Tools/ffmpeg.rules:2` `{ "name": "ffmpeg", "type": "Heavy_CPU" }`; `00-default/System Utilities & Maintenance/clamav.rules:2` `{ "name": "clamd", "type": "BG_CPUIO" }`; `00-default/DEs-and-WMs/plasma.rules:12,14` `{ "name": "baloo_file", "type": "BG_CPUIO" }` / `{ "name": "baloo_file_extractor", "type": "BG_CPUIO" }`; `00-default/Development & Programming/clang-tidy.rules:1` `{ "name": "clang-tidy", "type": "BG_CPUIO" }`; `00-default/Development & Programming/cmake.rules:2` `{ "name": "cmake-gui", "type": "BG_CPUIO" }`. Reader's own check at HEAD: `grep -rn -E '"name": ?"(gcc|cc1|g\+\+|clang|make|ninja|ld|rustc|cargo)"' 00-default/` → 0 hits — no compiler, make or linker rule is shipped.

History (reader's own: `git log --oneline --all -S'"gcc"'` and `git show --stat --format='%H%n%ad%n%an%n%B' <c>` in the unshallowed clone), five commits:

9fbdadd78ed6a0844f80ba5dba9de79b5d60c86d, Sat Sep 24 23:12:18 2022 +0200, Peter Jung (deletes `00-default/g++.rules`, `gcc.rules`, `make.rules`, `ninja.rules`):
> remove compiler rules, actually it could be useful to have at compile time a smooth desktop, but it gives also a extreme amount of overhead right now. Every process which gets spawned, will be adjusted from ananicy

b12d39a57ed6f4044587188eec28a9dd8119d2a1, Sun Sep 25 23:38:58 2022 +0200, Peter Jung, "add compilers" — added to `00-types.types`:
> +# Type: Compiler
> +{"type":"compiler", "nice":3, "latency_nice": 4 }

bf0bae3cfea5775b33365eee9b0ca5566445870a, Sun Feb 25 10:40:25 2024 +0100, Peter Jung:
> remove compiler processes to avoid freezes with BORE Scheduler
(removed rules for clang, clang++, cmake, gcc, g++, go, lld, mold, ld, ld.bfd, ld.mold, ld.lld, lto1-ltrans, cargo, rustc, rust-analyser and the type line `{ "type":"compiler", "nice": 9, "latency_nice": 9 }`)

e9f849440a023d753adff2b4a2e226f85f4946a4, Sat Apr 20 19:41:16 2024 +0530, Masum Reza, "Add compilers.rules (#80)":
> * Add compilers.rules
>
> C and C++, Go, Java, and Rust compilers are added
> Also added Bazel, Cmake, Ninja, and Meson build systems
>
> * compilers.rules: add linkers
> Change to uppercase Compiler
>
> * Change to 13 nice, is stable

5459ed81c0e006547b4f3a3bc40c00d31ad50aa9, Fri May 10 13:55:28 2024 +0200, Peter Jung:
> compiler: Drop them again, ananicy-cpp provides really noticeable cpu usage, when using these rules and they don't provide a real benefit at all
(removed `00-default/compilers.rules`, 22 name rules incl. `{ "name": "gcc", "type": "Compiler" }`, `{ "name": "make", "type": "Compiler" }`, `{ "name": "ld", "type": "Compiler" }`, and `{ "type":"Compiler", "nice": 13, "latency_nice": 13 }`)

**Coverage.**
- T7: covers whether shipped process-treatment catalogues assign compilers and batch jobs a class, and which: upstream Ananicy ships `compiler` = nice 1 for `gcc`, `g++`, `make`, `ninja`, `cargo`, `rustc`, `javac`, `go` (its README recommends nice 19 for "CPU hungry background task like compiling"), and `BG_CPUIO` (idle I/O class, SCHED_IDLE — deprecated/commented in the types file) for `clamd`/`clang-tidy`; CachyOS ships no compiler/make/linker rule at all after adding and removing them three times (2022: "extreme amount of overhead … Every process which gets spawned, will be adjusted"; Feb 2024: "avoid freezes with BORE Scheduler"; May 2024: "really noticeable cpu usage … don't provide a real benefit"), while it keeps `ffmpeg` = `Heavy_CPU` (nice 9), `clamd`/`baloo_file`/`baloo_file_extractor` = `BG_CPUIO` (nice 16, SCHED_IDLE, idle I/O). No rule in either set names `cc1`, `as`, `ld` (upstream) or `collect2`. The removal messages are statements by the maintainer, not measurements (no numbers).
- T6: covers indirectly that a per-exec rule engine finds a build's process churn costly ("every process which gets spawned") — again a statement, not a measurement.
- Other topics: do not cover. One observation? No.

### S2-16 — coreutils 9.4 `nproc` and gnulib `nproc.c` (does `nproc` honour the affinity mask?)

**Citation.** GNU coreutils 9.4, `src/nproc.c`, `doc/coreutils.texi` ("nproc invocation"); gnulib `lib/nproc.c` (branch `stable-202401`).

**Copy read.** `https://raw.githubusercontent.com/coreutils/coreutils/v9.4/src/nproc.c` (SHA-256 20e2d9da644856aac118a4fbba12d9db9e5bbc094a3569e1d9c727311450061f), `…/v9.4/doc/coreutils.texi` (6890fa80a0fc7a7a1157cfc6d3f420a9aa586c1495f1a20b31134ceb6b465298), `https://raw.githubusercontent.com/coreutils/gnulib/stable-202401/lib/nproc.c` (bf18f60b842058ecf70e472b34aa1586809e4f30a82f533ae17a863c8b0ed34e); accessed 2026-09-16; saved under `sources/S2-16/`.

**Verbatim passages.**

`src/nproc.c:58-59` (usage text):
> Print the number of processing units available to the current process,\n\
> which may be less than the number of online processors\n\

`doc/coreutils.texi:17082-17088`:
> Print the number of processing units available to the current process,
> which may be less than the number of online processors.
> If this information is not accessible, then print the number of
> processors installed.  If the @env{OMP_NUM_THREADS} or @env{OMP_THREAD_LIMIT}
> environment variables are set, then they will determine the minimum
> and maximum returned value respectively.  The result is guaranteed to be
> greater than zero.  Synopsis:

gnulib `lib/nproc.c:64-67, 128-137`:
> /* Return the number of processors available to the current process, based
>    on a modern system call that returns the "affinity" between the current
>    process and each CPU.  Return 0 if unknown or if such a system call does
>    not exist.  */
> …
> #elif HAVE_SCHED_GETAFFINITY_LIKE_GLIBC /* glibc >= 2.3.4 */
>   {
>     cpu_set_t set;
>
>     if (sched_getaffinity (0, sizeof (set), &set) == 0)
>       {
>         unsigned long count;
>
> # ifdef CPU_COUNT
>         /* glibc >= 2.6 has the CPU_COUNT macro.  */
>         count = CPU_COUNT (&set);

gnulib `lib/nproc.c:208-214, 222-229`:
>   /* On systems with a modern affinity mask system call, we have
>          sysconf (_SC_NPROCESSORS_CONF)
>             >= sysconf (_SC_NPROCESSORS_ONLN)
>                >= num_processors_via_affinity_mask ()
>      The first number is the number of CPUs configured in the system.
>      The second number is the number of CPUs available to the scheduler.
>      The third number is the number of CPUs available to the current process.
> …
>   if (query == NPROC_CURRENT)
>     {
>       /* Try the modern affinity mask system call.  */
>       {
>         unsigned long nprocs = num_processors_via_affinity_mask ();
>
>         if (nprocs > 0)
>           return nprocs;
>       }

**Coverage.**
- T6 (single-core confinement): covers that `nproc` (without `--all`) returns the count of CPUs in the calling process's affinity mask, so `make -j$(nproc)` under `taskset -c 0` yields `-j1`; likewise for DKMS (`nproc`, S2-12), rpm (`sched_getaffinity`, S2-09), ninja (S2-05); whereas dpkg's `getconf _NPROCESSORS_ONLN` (S2-08) and PTS's `/sys/devices/system/cpu/online` (S2-20) do not shrink under confinement. No measurement.
- T4: covers the semantics of the value every "`-j$(nproc)`" recommendation is based on. Other topics: do not cover.

### S2-17 — `taskset(1)` (util-linux 2.39) and Python 3.12 `os.cpu_count` / `os.sched_getaffinity` documentation

**Citation.** util-linux 2.39, `schedutils/taskset.1.adoc`; Python 3.12.14 documentation, `library/os.html`.

**Copy read.** `https://raw.githubusercontent.com/util-linux/util-linux/v2.39/schedutils/taskset.1.adoc` (SHA-256 c97d1fe3fdb2553e5c2b1a9f003c410b90bb9b6762e01211438d776ba5cd5da6); `https://docs.python.org/3.12/library/os.html` (b812ed995e58ba720d40c484407dbead446733630860279298686b7faed5f910; page states version 3.12.14); accessed 2026-09-16; saved under `sources/S2-17/`.

**Verbatim passages.**

`taskset.1.adoc:45`:
> The *taskset* command is used to set or retrieve the CPU affinity of a running process given its _pid_, or to launch a new _command_ with a given CPU affinity. CPU affinity is a scheduler property that "bonds" a process to a given set of CPUs on the system. The Linux scheduler will honor the given CPU affinity and the process will not run on any other CPUs. Note that the Linux scheduler also supports natural CPU affinity: the scheduler attempts to keep processes on the same CPU as long as practical for performance reasons. Therefore, forcing a specific CPU affinity is useful only in certain applications.   The affinity of some processes like kernel per-CPU threads cannot be set.

Python 3.12 `os.html`, entry `os.cpu_count()`:
> Return the number of logical CPUs in the system. Returns None if undetermined.
> This number is not equivalent to the number of logical CPUs the current process can use. len(os.sched_getaffinity(0)) gets the number of logical CPUs the calling thread of the current process is restricted to

**Coverage.**
- T6 (single-core confinement): covers the semantics of `taskset` (affinity bonds the process to the set; inheritance by children is documented in S2-23, not here — reader's own grep: `taskset.1.adoc` contains neither "inherit" nor "child") and that Python's `os.cpu_count()` ignores the affinity mask while `len(os.sched_getaffinity(0))` honours it — relevant to any build driver written in Python. No measurement. Other topics: do not cover.

### S2-18 — FFmpeg 7.0 `-threads` semantics and auto thread count; x264 thread-count default

**Citation.** FFmpeg n7.0: `doc/codecs.texi` (rendered at ffmpeg.org/ffmpeg-codecs.html), `libavcodec/options_table.h`, `libavcodec/pthread_frame.c`, `libavcodec/pthread_internal.h`, `libavutil/cpu.c`; x264 (VideoLAN) `encoder/encoder.c`, `common/cpu.c`, `x264.c` at `master` (HEAD 0480cb05fa188d37ae87e8f4fd8f1aea3711f7ee by `git ls-remote` at access time).

**Copy read.** `https://ffmpeg.org/ffmpeg-codecs.html` (SHA-256 2b71af17aab32132501eed3ee819ff1afa96a53c84b5b9cccc60c57ea58f35c6); `https://raw.githubusercontent.com/FFmpeg/FFmpeg/n7.0/doc/codecs.texi` (046759bcd56fddac91f24b24c936770270021ac583890eee5cbdc2d19a9d8b81), `…/n7.0/libavcodec/options_table.h` (46677edb6cbaed0a5c4cc170f3eedeb333cd110d13f127ef32abc946c9cb5854), `…/n7.0/libavcodec/pthread_frame.c` (607604372d2a6efa14b29ebbd69f016e19d3d9ad00d5e8bc71abadaab255d686), `…/n7.0/libavcodec/pthread_internal.h` (e5d5013d30492c3af0f5aabdd37db7fc7a40a862092bda8321d1c9d0ae73b83e), `…/n7.0/libavutil/cpu.c` (68a2871f13c48fbdc00e2d1cbd5f567dac4d33c898e90650d998208f9b9981ba); `https://code.videolan.org/videolan/x264/-/raw/master/encoder/encoder.c` (20a7290a727d7583f3f0fded5f427db6b4c84d934e86ca5df00e75a443a5e2c0), `…/master/common/cpu.c` (e850958f482b2f227ca4487855bb7530b3ca9b0ec436d521b3d3b4be27fbda5f), `…/master/x264.c` (fa4c8bc222972040cd7dbd7609da099d10131e7251c5c5c991da8648addcd8e9); accessed 2026-09-16; saved under `sources/S2-18/`.

**Verbatim passages.**

`doc/codecs.texi:669-679` (n7.0):
> @item threads @var{integer} (@emph{decoding/encoding,video})
> Set the number of threads to be used, in case the selected codec
> implementation supports multi-threading.
>
> Possible values:
> @table @samp
> @item auto, 0
> automatically select the number of threads to set
> @end table
>
> Default value is @samp{auto}.

`libavcodec/options_table.h:216-217`:
> {"threads", "set the number of threads", OFFSET(thread_count), AV_OPT_TYPE_INT, {.i64 = 1 }, 0, INT_MAX, V|A|E|D, .unit = "threads"},
> {"auto", "autodetect a suitable number of threads to use", 0, AV_OPT_TYPE_CONST, {.i64 = 0 }, INT_MIN, INT_MAX, V|E|D, .unit = "threads"},

`libavcodec/pthread_frame.c:843-850` (frame threading, auto count = cores + 1, capped):
>     if (!thread_count) {
>         int nb_cpus = av_cpu_count();
>         // use number of cores + 1 as thread count if there is more than one
>         if (nb_cpus > 1)
>             thread_count = avctx->thread_count = FFMIN(nb_cpus + 1, MAX_AUTO_THREADS);
>         else
>             thread_count = avctx->thread_count = 1;
>     }

`libavcodec/pthread_internal.h:26`:
> #define MAX_AUTO_THREADS 16

`libavutil/cpu.c:218-224` (`av_cpu_count` honours the affinity mask):
> #if HAVE_SCHED_GETAFFINITY && defined(CPU_COUNT)
>     cpu_set_t cpuset;
>
>     CPU_ZERO(&cpuset);
>
>     if (!sched_getaffinity(0, sizeof(cpuset), &cpuset))
>         nb_cpus = CPU_COUNT(&cpuset);

x264 `encoder/encoder.c:559-566`:
>     if( h->param.i_threads == X264_THREADS_AUTO )
>     {
>         h->param.i_threads = x264_cpu_num_processors() * (h->param.b_sliced_threads?2:3)/2;
>         /* Avoid too many threads as they don't improve performance and
>          * complicate VBV. Capped at an arbitrary 2 rows per thread. */
>         int max_threads = X264_MAX( 1, (h->param.i_height+15)/16 / 2 );
>         h->param.i_threads = X264_MIN( h->param.i_threads, max_threads );
>     }

x264 `common/cpu.c:645-648`:
>     if( sched_getaffinity( 0, sizeof(p_aff), &p_aff ) )
>         return 1;
> #if HAVE_CPU_COUNT
>     return CPU_COUNT(&p_aff);

**Coverage.**
- T7 (thread count of a video encode): covers the documented/coded defaults: FFmpeg's codec-level default is 1 thread, "auto" = min(affinity-CPUs + 1, 16) for frame-threaded codecs; x264's auto = 1.5 × affinity-CPUs (2 × for sliced threads), capped at (height/16)/2. Does not cover sustained utilisation or duration (no measurement). Not an observation.
- T6 (single-core confinement): covers that both auto counts follow `sched_getaffinity`, so under `taskset -c 0` FFmpeg frame threading falls to 1 thread and x264 to 1 (×3/2 → 1). Other topics: do not cover.

### S2-19 — ClamAV 1.3.1: `clamd` `MaxThreads`, `clamdscan --multiscan`, `clamscan`

**Citation.** Cisco-Talos/clamav, tag `clamav-1.3.1`: `etc/clamd.conf.sample`, `docs/man/clamd.conf.5.in`, `docs/man/clamd.8.in`, `docs/man/clamdscan.1.in`, `docs/man/clamscan.1.in`.

**Copy read.** `https://raw.githubusercontent.com/Cisco-Talos/clamav/clamav-1.3.1/<path>`; SHA-256: `etc/clamd.conf.sample` 3c01395b30b11240f7e0d9dec051281cecaf477763c3461824fd19e61bf0be6a, `docs/man/clamd.conf.5.in` 7643b2bc0d26bced6e56764d01f31722e690d7c97db9a010397dc36e9c5f6c86, `docs/man/clamd.8.in` 61f2a34de50d545f4c0b3d616496a824e520dc7d1f8c8d0e1d222b35d9df60a9, `docs/man/clamdscan.1.in` f116da4fb149ec2f836cf7eed7d28fcd472550734ea1a7d4da82e1fe7995b784, `docs/man/clamscan.1.in` 911b96261e5b608e7f40f1ac4e34440a4ad1b10ad51d3ae9c04359e243db6bb8; accessed 2026-09-16; saved under `sources/S2-19/`.

**Verbatim passages.**

`etc/clamd.conf.sample:147-149`:
> # Maximum number of threads running at the same time.
> # Default: 10
> #MaxThreads 20

`docs/man/clamd.conf.5.in:166-169`:
> \fBMaxThreads NUMBER\fR
> Maximum number of threads running at the same time.
> .br
> Default: 10

`docs/man/clamd.8.in:37-38`:
> \fBMULTISCAN file/directory\fR
> Scan file in a standard way or scan directory (recursively) using multiple threads (to make the scanning faster on SMP machines).

`docs/man/clamdscan.1.in:45-46`:
> \fB\-m, \-\-multiscan\fR
> In the multiscan mode clamd will attempt to scan the directory contents in parallel using available threads. This option is especially useful on multiprocessor and multi-core systems. If you pass more than one file or directory in the command line, they are put in a queue and sent to clamd individually. This means, that single files are always scanned by a single thread. Similarly, clamdscan will wait for clamd to finish a directory scan (performed in multiscan mode) before sending request to scan another directory. This option can be combined with \-\-fdpass (see below).

Reader's own check: `grep -c -i thread docs/man/clamscan.1.in` = 0 — the `clamscan` man page (the command used by the CI batch) has no thread option or threading statement.

**Coverage.**
- T7 (antivirus scan thread count): covers the daemon's documented thread cap (`MaxThreads`, default 10; parallel only in `MULTISCAN`/`--multiscan` mode, one thread per file), and that the standalone `clamscan` command documents no threading. Does not cover sustained utilisation or duration. Not an observation. Other topics: do not cover.

### S2-20 — Phoronix Test Suite `pts/build-linux-kernel-1.15.0` (how the benchmark invokes `make -j`)

**Citation.** phoronix-test-suite/test-profiles, `pts/build-linux-kernel-1.15.0/{install.sh,pre.sh,test-definition.xml}` (repository `master`, HEAD d2f1a150d388bd062737b445891edda0780f7e25 at access time); phoronix-test-suite v10.8.4 `pts-core/objects/phodevi/components/phodevi_cpu.php`, `pts-core/objects/client/pts_client.php`.

**Copy read.** `https://raw.githubusercontent.com/phoronix-test-suite/test-profiles/master/pts/build-linux-kernel-1.15.0/install.sh` (SHA-256 6e0f8dca7512e119a71c808a1017020682d3effdd253ec8ac596f5b823863513), `…/pre.sh` (3c38658cd1245d68b42345b5d008ad7ffabde07e1ecfd695b91f31daf84a7a64), `…/test-definition.xml` (32ee5c3a30035b576917d958c351ab2affc2a8d627f6be5abd986302fe37a851), `…/downloads.xml` (44152705720d25c258dd5296f5cc9fbf5ba8922600d40c848e9ece7c22a3deb3); `https://raw.githubusercontent.com/phoronix-test-suite/phoronix-test-suite/v10.8.4/pts-core/objects/phodevi/components/phodevi_cpu.php` (04b6afb4996471488f4b763b253f79065c3c7bb7206c70b4518dc2059973deb6), `…/v10.8.4/pts-core/objects/client/pts_client.php` (24bed3b52346c32c135d3cd81056751fbe0f977225c1032208e783cc1a89f5ec); accessed 2026-09-16; saved under `sources/S2-20/`.

**Verbatim passages.**

`install.sh` (whole file, 6 lines):
> #!/bin/sh
> echo "#!/bin/sh
> cd linux-6.1
> make -s -j \$NUM_CPU_CORES 2>&1
> echo \$? > ~/test-exit-status" > build-linux-kernel
> chmod +x build-linux-kernel

`pre.sh:1-15`:
> #!/bin/bash
> rm -rf linux-6.1
> tar -xf linux-6.1.tar.xz
> cd linux-6.1
> if [ -z "$@" ]
> then
> 	# This is for old PTS clients not passing anything per older old test profile configs that may be in suite...
> 	export LINUX_MAKE_CONFIG="defconfig"
> else
> 	export LINUX_MAKE_CONFIG="$1"
> fi
> echo "make $LINUX_MAKE_CONFIG"
> make "$LINUX_MAKE_CONFIG"
> make clean
> scripts/config --set-val CONFIG_WERROR n

`test-definition.xml:4-10`:
>     <Title>Timed Linux Kernel Compilation</Title>
>     <AppVersion>6.1</AppVersion>
>     <Description>This test times how long it takes to build the Linux kernel in a default configuration (defconfig) for the architecture being tested or alternatively an allmodconfig for building all possible kernel modules for the build.</Description>
>     <ResultScale>Seconds</ResultScale>
>     <Proportion>LIB</Proportion>
>     <SubTitle>Time To Compile</SubTitle>
>     <TimesToRun>3</TimesToRun>

`pts_client.php:360`:
> 			'NUM_CPU_CORES' => phodevi::read_property('cpu', 'core-count'),

`phodevi_cpu.php:109-123` (Linux: online CPU range from sysfs, not the affinity mask):
> 		else if(phodevi::is_linux())
> 		{
> 			$sl = phodevi::read_property('system', 'system-layer');
> 			if(is_file('/sys/devices/system/cpu/online') && ($sl == null || stripos($sl, 'lxc') === false))
> 			{
> 				$present = pts_file_io::file_get_contents('/sys/devices/system/cpu/online');
>
> 				if(isset($present[2]) && substr($present, 0, 2) == '0-')
> 				{
> 					$present = substr($present, 2);
>
> 					if(is_numeric($present))
> 					{
> 						$info = $present + 1;
> 					}

**Coverage.**
- T6: covers the exact compile workload of the most widely reported public kernel-build benchmark: Linux 6.1, `defconfig` (or `allmodconfig`), `make -s -j$NUM_CPU_CORES` with `NUM_CPU_CORES` = online CPUs (or the `NUM_CPU_CORES`/`PTS_NPROC` override), 3 runs, result in seconds. Does not cover process counts, lifetimes or CPU-time distributions, nor any result values (results live on openbenchmarking.org — S3 territory).
- T4: covers a benchmark tool's `-j` = online CPU count. Not an observation of user choices. Other topics: do not cover.

### S2-21 — PyTorch 2.4.0 CPU threading: default intra-op thread count

**Citation.** PyTorch v2.4.0, `docs/source/notes/cpu_threading_torchscript_inference.rst`, `aten/src/ATen/ParallelCommon.cpp`, `c10/core/thread_pool.cpp`.

**Copy read.** `https://raw.githubusercontent.com/pytorch/pytorch/v2.4.0/docs/source/notes/cpu_threading_torchscript_inference.rst` (SHA-256 66f2502d456c0dec966fecbfa371a58f94d7a810faed98ce536895afa81ba1a7), `…/v2.4.0/aten/src/ATen/ParallelCommon.cpp` (17eed5b7956f0757cd4b9390b8d0eea1713fc7ece4303f131c4b6c993d6496f1), `…/v2.4.0/c10/core/thread_pool.cpp` (82d1ec4dd35d56082cd75b1db49f4a7890ee2ac868ab8977e9093f9a47301eea); also fetched `aten/src/ATen/ParallelNative.cpp` (5cdf6878cb08e8675e218b4b14ce5672247b5f51399466e4523a0213b7640389) and `torch/_C/__init__.pyi.in`; accessed 2026-09-16; saved under `sources/S2-21/`.

**Verbatim passages.**

`cpu_threading_torchscript_inference.rst:96, 111-112`:
> | Inter-op parallelism   | ``at::set_num_interop_threads``,                          | Default number of threads: number of CPU cores.         |
> …
> For the intra-op parallelism settings, ``at::set_num_threads``, ``torch.set_num_threads`` always take precedence
> over environment variables, ``MKL_NUM_THREADS`` variable takes precedence over ``OMP_NUM_THREADS``.

`ParallelCommon.cpp:96, 103-105, 121`:
> int intraop_default_num_threads() {
> …
>   size_t nthreads = get_env_num_threads("OMP_NUM_THREADS", 0);
>   nthreads = get_env_num_threads("MKL_NUM_THREADS", nthreads);
>   if (nthreads == 0) {
> …
>     nthreads = TaskThreadPoolBase::defaultNumThreads();

`c10/core/thread_pool.cpp:9-21`:
> size_t TaskThreadPoolBase::defaultNumThreads() {
>   size_t num_threads = 0;
> #if !defined(__powerpc__) && !defined(__s390x__)
>   if (cpuinfo_initialize()) {
>     // In cpuinfo parlance cores are physical ones and processors are virtual
>     // ThreadPool should be defaulted to number of physical cores
>     size_t num_cores = cpuinfo_get_cores_count();
>     num_threads = cpuinfo_get_processors_count();
>     if (num_cores > 0 && num_cores < num_threads) {
>       return num_cores;
>     }
>     if (num_threads > 0) {
>       return num_threads;

**Coverage.**
- T7 (model-training thread count): covers the default intra-op pool size = physical core count (via cpuinfo, not the affinity mask) unless `OMP_NUM_THREADS`/`MKL_NUM_THREADS` are set; inter-op default = number of CPU cores. Does not cover utilisation or duration. Not an observation. Other topics: do not cover.

### S2-22 — File indexers' own scheduling: tracker-miner-fs 3.7.3 (SCHED_IDLE + nice 19) and plocate 1.1.23 `updatedb` timer/service (Nice=19, idle I/O)

**Citation.** (a) GNOME tracker-miners 3.7.3, `src/miners/fs/tracker-main.c`, `src/libtracker-miners-common/tracker-sched.c` (tag 3.7.3 = f70a377c6e1b816d8bb0d57c21c2d2217ceb5118); (b) plocate 1.1.23 (Steinar H. Gunderson), `plocate-updatedb.timer`, `plocate-updatedb.service.in`.

**Copy read.** `https://gitlab.gnome.org/GNOME/tracker-miners/-/raw/3.7.3/src/miners/fs/tracker-main.c` (SHA-256 511edaf49ecda04d787ba4bf60b62f66867f346e3e9b645381145b676ea3883c), `…/3.7.3/src/libtracker-miners-common/tracker-sched.c` (ea780d2ec0d900747eb6de50128f0d3fe0a736f53c40a80cea18f389a9d3e56e); `https://deb.debian.org/debian/pool/main/p/plocate/plocate_1.1.23.orig.tar.gz` (06bd3b284d5d077b441bef74edb0cc6f8e3f0a6f58b4c15ef865d3c460733783, extracted to `sources/S2-22/plocate/`); accessed 2026-09-16 (git.sesse.net unreachable, 502 — search log #32).

**Verbatim passages.**

`tracker-main.c:199-206, 216-219`:
> static void
> initialize_priority_and_scheduling (void)
> {
> 	/* Set CPU priority */
> 	tracker_sched_idle ();
>
> 	/* Set disk IO priority and scheduling */
> 	tracker_ioprio_init ();
> …
> 	TRACKER_NOTE (CONFIG, g_message ("Setting priority nice level to 19"));
>
> 	errno = 0;
> 	if (nice (19) == -1 && errno != 0) {

`tracker-sched.c:38-47`:
> tracker_sched_idle (void)
> {
> 	struct sched_param sp;
> 	int result, policy;
>
> 	result = pthread_getschedparam (pthread_self (), &policy, &sp);
>
> 	if (result == 0) {
> 		result = pthread_setschedparam (pthread_self(), SCHED_IDLE, &sp);
> 	}

`plocate-updatedb.timer:1-8`:
> [Unit]
> Description=Update the plocate database daily
>
> [Timer]
> OnCalendar=daily
> RandomizedDelaySec=1h
> AccuracySec=6h
> Persistent=true

`plocate-updatedb.service.in:1-10`:
> [Unit]
> Description=Update the plocate database
> ConditionACPower=true
>
> [Service]
> Type=oneshot
> ExecStart=@sbindir@/@updatedb_progname@
> LimitNOFILE=131072
> IOSchedulingClass=idle
> Nice=19

**Coverage.**
- T7 (process treatment of batch indexers): covers that tracker-miner-fs sets itself to `SCHED_IDLE` + nice 19 + idle I/O, and plocate's `updatedb` runs daily (randomised by up to 1 h, only on AC power) as a oneshot service with `Nice=19` and `IOSchedulingClass=idle`. Does not cover thread count, utilisation or duration. Not an observation. Other topics: do not cover.

### S2-23 — `sched_setaffinity(2)` man page (affinity inheritance across fork/exec)

**Citation.** Linux man-pages, `man2/sched_setaffinity.2`, release man-pages-6.04.

**Copy read.** `https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man2/sched_setaffinity.2?h=man-pages-6.04`, SHA-256 0a5fc10d55d70ddba87c181be18145fd61afe0a974bfbc5f6f5962610ff5d273, accessed 2026-09-16, saved as `sources/S2-23/sched_setaffinity.2`.

**Verbatim passage.** `sched_setaffinity.2:215-219`:
> A child created via
> .BR fork (2)
> inherits its parent's CPU affinity mask.
> The affinity mask is preserved across an
> .BR execve (2).

**Coverage.**
- T6 (single-core confinement): covers the basis on which `taskset -c 0 make -jN` confines every process of the build (make, shells, `gcc`, `cc1`, `as`, `fixdep`, sub-makes): the mask is inherited on fork and kept across exec. No measurement. Other topics: do not cover.

## 3. Not found

Established by the searches above (numbers refer to the search log); the reader's class is documentation and source, so "not found" here means no primary project or vendor document states it.

- **T1 — counts, lifetimes, CPU-time distributions per process.** No kbuild, GCC, binutils or make document gives the number of processes per build, per-process lifetimes, or a CPU-time distribution; the sources give only the *structure* (S2-01, S2-02, S2-03). Searches #2, #3, #4, #30 (kernel v6.6 kbuild files and docs; GCC manual and `gcc.cc`; make source). `Documentation/admin-guide/README.rst` and `Documentation/kbuild/makefiles.rst` contain no `-j`/jobserver text (#37).
- **T3 — make's own CPU cost per dispatched job.** Not stated anywhere in the make source or manual (#4, #5, #6); only the mechanism (token read/write, `vfork`, shell selection) is documented.
- **T4 — observations of the parallelism level users actually pick.** Every source gives a default or a recommendation (`nproc`, `nproc+2` for ninja, logical CPUs for cargo, online CPUs for dpkg, affinity-mask CPUs capped by memory for rpm, `-j2` template / `$(nproc)` wiki for Arch, `nproc` for Gentoo, `-j$(nproc)` for the Debian kernel handbook, `-j$NUM_CPU_CORES` for PTS); none reports what users choose (#7–#16, #29). The Fedora guideline's "-j3 … even on UP machines" is advice for exposing bugs, not a usage observation (#14). Kernel admin docs recommend no level (#37).
- **T5 — DKMS autoinstall duration, CPU, number of compiler processes.** The dkms sources document the make invocation (`-j$(nproc)`), the triggers and hooks, but no timing or process count (#17). No Ubuntu/Debian/Fedora vendor page with such numbers was found within budget; the Debian kernel-hook and Fedora `kernel/install.d` hook files are quoted from the dkms tree itself.
- **T6 — builds as a scheduler workload with reported `-j`, machines, process counts or lifetime distributions; single-core confinement observations.** The kernel documents autogroup's motivation (#20, #2) and the sched_ext README names "parallel kernel build" as a background load without any parameters (#21); `sched_child_runs_first` is present but unreferenced and undocumented in v6.6 (#18). No kernel or scx document reports process counts, lifetimes, `-j`, or a confined-vs-unconfined comparison. No vendor document on running builds under a CPU quota beyond the tool code that reads the affinity mask / cgroup quota (ninja #7, rpm #13, nproc #25, ffmpeg/x264 #27) and the man page on inheritance (#36). No study of Unix/Linux process-lifetime distributions is a documentation/source object (S1's territory).
- **T7 — sustained utilisation and duration of a saturating batch job.** Vendor docs give thread-count defaults/caps (ffmpeg/x264 #27, clamd `MaxThreads` #28, PyTorch physical cores #31, interbench "4 by default"/online CPUs #22) and scheduling-class treatment (ananicy sets #23–#24, tracker/plocate #34/#33, Arch wiki `SCHED_IDLE` #15), but no utilisation figures or durations. HandBrake CLI documentation was not fetched within budget (not searched — listed for completeness, not as an established absence).
