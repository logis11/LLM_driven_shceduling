# Stage 3, scope-card item 60 — vol-02's source quotations checked against copies

Three readers, 2026-10-09, each reading one span of `docs/guidebook/vol-02-related-work.md` (the file unchanged since `2f7c7b58`) against copies of its sources: chapters 2–3, 4–6, 7–8. Their reports follow verbatim. Copies fetched in this read are under `sources/V60/` (gitignored); every copy's SHA-256 and whether it equals the earlier record is in each report's copies table. Decision: changelog D53.


---

### Scope-card item 60 (research slice 9.12): source quotations in chapters 2 and 3 of `docs/guidebook/vol-02-related-work.md`

No repository file was edited. The new copies are under `_dev/research/jioh/task-9.12-related-work-prose/sources/V60/` (gitignored). Scratch text extractions and page crops are in `scratchpad/v60-ch23/`.

Method. Every entry in `vol02-quotes.json` whose section starts with `2.` or `3.` was checked: 92 lines in sections 2.2–2.6 and 3.2–3.4. Chapters 2 and 3 were also scanned for further block-quote lines carrying English. The only extra ones are the continuation lines 1119–1121 of the four-bullet quote at 1118, which are checked with it. The terminal-record code block at lines 1151–1156 is checked as an extra row. Each quote was matched against its copy, normalising whitespace, line-break hyphenation, ligatures (which `pdftotext` drops from the EEVDF report) and curly/straight quotes, with elisions treated as ordered fragments. OCR-scan passages and every formula or symbol were also read from rendered page images (`pdftoppm`): Corbató pp. 341 and 343, Liu & Layland p. 56, EEVDF report pp. 3, 6, 18 and 20, Miller p. 271. Markdown/reST markup (backticks, link brackets, `:kbd:`) is treated as formatting, not wording.

### 1. Copies

| Registry entry | Copy (URL / path) | SHA-256 | Equals record? |
|---|---|---|---|
| `corbato-sjcc62` | `task-9.12…/sources/S1-04/corbato62.pdf` (https://cseweb.ucsd.edu/classes/wi19/cse221-a/papers/corbato62.pdf) | `3e5f2a3b2561c5863da88ed6d19d6c587131416d68a35ce140e5ee92bf47841e` | yes (9.12 record S1-04) |
| `liu-jacm73` | `task-9.12…/sources/S1-10/liu-layland.pdf` (https://www.cs.ru.nl/~hooman/DES/liu-layland.pdf) | `de9fb72577ff1f45aa50ccae0774b248ef67ebe15c6b6e90b00e0ab377f2b927` | yes (S1-10) |
| `waldspurger-osdi94` | `task-9.12…/sources/S1-09/lottery.pdf` (https://www.waldspurger.org/carl/papers/lottery-osdi94.pdf) | `e704678ec0cf6064136794a23c1722ad32a24868259dcdf3a9ad8087d8f1b73a` | yes (S1-09; also the 9.11 record S1-03) |
| `eevdf-tr95` | `task-9.12…/sources/S1-05/eevdf-tr-95.pdf` (https://people.eecs.berkeley.edu/~istoica/papers/eevdf-tr-95.pdf) | `b44b71a76f6a4b27f1c476282732c69498c86e7ec253f3cdd96ca66684f2aa97` | yes (S1-05) |
| `miller-fjcc68` | `task-9.11…/sources/S1-01/Miller1968.pdf` (https://yusufarslan.net/sites/yusufarslan.net/files/upload/content/Miller1968.pdf) | `470bc40b3200c6e289d5e4fc276d6d3c416d5574079ef752da27aa366d6da990` | yes (9.11 record S1-01) |
| `nielsen-ue93` (local) | `task-9.11…/sources/S1-05/nngroup.html` (https://www.nngroup.com/articles/response-times-3-important-limits/) | `cd24ce28eaf2c4ded93a1a45ae9c2a939b896b30e9887ecd1d939c24785e43a8` (121 941 bytes) | **no**: the 9.11 record S1-05 gives `ee93bba73ca6307f8bdea3ba918d7959ef39a8c8cea6f43484b6ff078fc9ee83`, 120 613 bytes |
| `nielsen-ue93` (re-fetched) | `V60/nielsen-ue93/nngroup.html`, same URL, curl 2026-10-09 | `075f609c04027e55115b70e0936b270ed6258909e9b55fc1960cd5205c077fe3` (121 794 bytes) | **no** (the page is dynamic HTML). The quoted sentence and the line "Excerpt from Chapter 5 in my book Usability Engineering, from 1993" are word-identical in both copies |
| `shneiderman-csur84` | `task-9.11…/sources/S1-07/shneiderman.pdf` (https://www.cs.umd.edu/~ben/papers/Shneiderman1984Response.pdf) | `7ea65246d42600afcd94835ca8e42444ad49f376c38af26a12e1d6731851bd90` | yes (9.11 record S1-07) |
| `ghost-sosp21` (paper) | `task-9.12…/sources/S1-01/ghost.pdf` (https://cs.stanford.edu/~jhumphri/documents/ghost.pdf) | `c37d636045a45e2216e7047ba1fb9ffa4ed88fe54b09ee0ccc33435cacd35c91` | yes (S1-01) |
| ghOSt repository README (quoted as "저장소" — no registry entry or search record exists for it) | `V60/ghost-sosp21/ghost-userspace/README.md`, partial clone of https://github.com/google/ghost-userspace at HEAD `9ca0a1fb6ed88f0c4b0b40a5a35502938efa567f` (committed 2023-11-08) | `ebac49bb2f82a6f4ef17f133bee0285eb054ccbb4d73b623c4d5109c39e3e14a` | no record to compare |
| `schedext-docs` v6.12 | `V60/schedext-docs/sched-ext-v6.12.rst` from https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/scheduler/sched-ext.rst?h=v6.12 (raw.githubusercontent.com returned HTTP 429) | `b5a95750fb7e7d2778454b80e89c25d525ce739700b6528029ed7701613228e6` | yes (S2-01) |
| `schedext-docs` mainline | `V60/schedext-docs/sched-ext-7b63ef2d.rst` from the same git.kernel.org path `?id=7b63ef2d55f24519e7e9e5f4d15dbea03f126e40` | `3c96c6a67bfe6fcaaa5f02753cfe7547e3918312f586366389a219a1ae796113` | yes (S2-02) |
| `scx` v1.1.3 | `V60/scx/scx-v1.1.3`, partial clone of https://github.com/sched-ext/scx tag v1.1.3 = commit `c8728c6b6a3fde451f0f10b95f99aad7a32a750a` (S2-09's commit). `README.md` `b285939f…`, `OVERVIEW.md` `0a97538a…`, `scheds/rust/scx_lavd/README.md` `8e4f48c1…`; also `scx_rusty/README.md` `d0a6fd01adf9faa38998e75b873222cfd81b3a3037de5170e639dff74083eafe`, `scx_layered/README.md` `2d0aceed03537d442759b0faaf2f34522ab7eefcc96d5d444be597005ed30f81`, `scx_bpfland/README.md` `982ef58b7e3e4ef8ced70355f1a0f6a56128e4ff6fbeb1dec7ea3ec403acb28c`, `scx_flash/README.md` `28c7694d37d638d64ffe4e719e4b24a0b3c78d744254c8fe3b3a74be81dd8bcf` | listed | README, OVERVIEW and scx_lavd README: yes (S2-09). The other four READMEs: no hash in the record. The local clone `task-9.11…/sources/D-scx/scx-v1.1.3` holds only the top-level `.md` files; its README and OVERVIEW match too |
| `ostep` (supplementary only) | `task-9.11…/sources/S1-02/cpu-sched-mlfq.pdf` | `96241b4e6708991740560334a1f67516c3c68eb3e6a570af7b03cdb4b32918db` | yes (9.11 S1-02 = 9.12 S1-02) |

Not fetched: `sched-eevdf.rst` and `sched-design-CFS.rst`, because section 2.5 quotes neither (all of its quotes are from the EEVDF report).

### 2. Quotation rows

Verdicts: E = exact, D = differs, LW = locator wrong, NF = not found. Page numbers are printed pages.

### 2.2 — Corbató, Merwin-Daggett & Daley 1962 (all from the page images; ℓ, ℓ₀, 2^ℓ, ℓ′, ℓ″, w_p, w_q confirmed)

| Line | First words | Locator in copy | Verdict |
|---|---|---|---|
| 302 | "one is inevitably faced with the problem of system saturation where…" | p. 340, right column ("A Multi-Level Scheduling Algorithm") | E |
| 308 | "If the strategy near saturation is to execute the simple round-robin…" | p. 341, left | E |
| 314 | "a good design for the system is to have a saturation procedure…" | p. 340, right (preceded by "…alleviated if it is assumed that") | E |
| 324 | "The basis of the multi-level scheduling algorithm is to assign each…" | p. 341, left | E |
| 330 | "Programs are initially entered into a level ℓ₀, corresponding to their size…" | p. 341, left. "…" stands for formula (1). Source: "the bracket indicates "the integral part of"" | E |
| 340 | "Because a program is always operated for a time greater than…" | p. 341, right, conclusion 1 | E |
| 346 | "(Clearly, this fraction is adjustable in the formula for the initial level, ℓ₀.)" | p. 341, right | E |
| 350 | "The process starts with the time-sharing supervisor operating the program at…" | p. 341, left | E |
| 358 | "Ordinarily the time of a quantum, being the basic time unit…" | p. 341, left ("high-/speed" broken at the line end; "high-speed" is the compound) | E |
| 364 | "q = 16 m.s. (based on 1% switching overhead)" | p. 343, left. The guidebook's locator at line 362 ("IBM 7090에 대해") is right: "apply the multi-level scheduling algorithm bounds to the contemporary IBM 7090. The following approximate values are obtained:" | E |
| 372 | "and then if the program is not completed (i.e. has not made…" | p. 341, left | E |
| 380 | "If there are no programs entering the system at levels lower than ℓ…" | p. 341, left | E |
| 386 | "If during the execution of the 2^ℓ quanta of a program at level ℓ…" | p. 341, left | E |
| 392 | "Similarly, if a program of size w_p at level ℓ, during operation…" | p. 341, right | E |
| 398 | "One systematic method of handling this case is to modify the scheduling…" | p. 343, left | E |
| 404 | "Whenever a program must be removed from high-speed memory, a program…" | p. 343, left ("high-/speed" and "end-/of-the-queue" broken at the line ends) | E |
| 412 | "It is an important feature of the algorithm that long runs must…" | p. 341, right, conclusion 3 "Long Runs" | E |
| 416 | "In the multi-level algorithm the level classification procedure for programs is entirely…" | p. 342, left, conclusion 5 "Highest Serviced Level" | E |

Other locators checked in 2.2:
- Line 408, "다섯 개의 결론" (five conclusions): right. There are five numbered conclusions: 1 Computational Efficiency, 2 Response Time, 3 Long Runs, 4 Multi-level vs. Single-level Response Times, 5 Highest Serviced Level.
- Line 426, pp. 335–344: right. The printed numbers 335 and 344 are on the first and last pages of the scan.
- Not checked: the "MIT가 공개한 저자 감수 전사본" (the author-reviewed transcript published by MIT) that line 426 says the symbols were confirmed against. That transcript was not in the brief. The symbols were confirmed here from the scan's page images instead.

### 2.3 — Liu & Layland 1973

| Line | First words | Locator | Verdict |
|---|---|---|---|
| 442 | "each task must be completed before the next request for it occurs" | p. 48, §3, assumption (A2), the second of five (A1)–(A5). Matches line 440 | E |
| 454 | "the deadline driven scheduling algorithm is feasible if and only if (C₁/T₁)…" | p. 56, Theorem 7. Matches line 452. The "…" is the formula's own "+ · · · +", checked on the page image | E |
| 464 | "may be as low as 70 percent for large task sets" | p. 46, Abstract. Matches line 462 | E |

### 2.4 — Waldspurger & Weihl 1994

| Line | First words | Locator | Verdict |
|---|---|---|---|
| 490 | "the resource consumption rates of active computations are proportional to the relative…" | p. 1, §1 Introduction. Matches line 488 ("첫 절", the first section) | E |
| 500 | "With a scheduling quantum of 10 milliseconds (100 lotteries per second)…" | p. 2, right column, within §2.2 "Lotteries" (the guidebook gives no locator). The quote ends at "accuracy"; the sentence continues "while maintaining a fixed proportion of scheduler overhead." | E |

### 2.5 — Stoica & Abdel-Wahab, EEVDF technical report TR-95-22

| Line | First words | Locator | Verdict |
|---|---|---|---|
| 530 | "Revised January 26, 1996." | p. 1, starred footnote under the abstract. "TR-95-22" is on the same page. Matches line 528 | E |
| 540 | "While in general the proportional share schedulers tend to be more flexible…" | p. 2, §1 Introduction | E |
| 548 | "Although real-time based schedulers provide better support for multimedia, they cannot…" | p. 2, §1 | E |
| 554 | "our algorithm provides a unified approach for scheduling continuous media, interactive…" | p. 3, §1 | E |
| 562 | "Similarly to [31] and [23] we define the system virtual time as V(t)…" | p. 6, §3 "The EEVDF Algorithm", Eq. (5), checked on the image | E |
| 568 | "We note that the virtual time increases at a rate inverse proportional…" | p. 6, §3 | E |
| 574 | "Intuitively, the flow of the virtual time changes to 'accommodate' all active…" | p. 6, §3 (the source uses double quotes around accommodate) | E |
| 582 | "Based on the client share and on the service time that the…" | p. 3, §1 | **D**. Source (image checked): "…the scheduler associates to each client's request a *virtual eligible time* and a *virtual deadline* which are the corresponding starting and finishing times of servicing the request in the fluid-flow model." The guidebook writes "virtual **dead line**", splitting "deadline" into two words |
| 588 | "A request is said to be eligible if its virtual eligible time…" | p. 3, §1 | E |
| 594 | "The algorithm simply allocates a new time quantum to the client that…" | p. 3, §1 | E |
| 600 | "We note that while the concept of virtual deadline is also employed…" | p. 3, §1. "[…]" stands for "[23, 31, 29, 30]" | E |
| 608 | "Due to quantization, in a system in which the resource is allocated…" | p. 4, **§2 "Assumptions"** | E (see the locator finding at line 558 below) |
| 618 | "Since the service time lag determines both the throughput accuracy and the…" | p. 5, §2 | E |
| 626 | "we show that in steady conditions our algorithm guarantees that the difference…" | p. 1, Abstract ("Mainly, we show…"). Matches line 624 | E |
| 632 | "Theorem 1 The lag of any active client k in a steady system…" | p. 18, Theorem 1, Eq. (35), image checked: "−r_max < lag_k(d) < max(r_max, q)" | E |
| 638 | "Corollary 2 Consider a steady system and a client k such that…" | p. 20, Eq. (42), image checked: "−q < lag_k(t) < q." | E |
| 642 | "Lemma 5 Given any steady system with time quanta of size q…" | p. 20 | E |
| 652 | "Definition 2 An interval is said to be steady if all the…" | p. 13 | E |

**Locator wrong, line 558 (applies to the run of quotes at 562–608).** The line reads "논문의 서론에 네 개가 한 문단에 다 나옵니다" (in the paper's introduction, all four [virtual time, virtual eligible time, virtual deadline, lag] appear in one paragraph). The introduction paragraph on p. 3 does mention "the notion of virtual time", the virtual eligible time, the virtual deadline and eligibility. But the word "lag" does not occur anywhere in pp. 1–3. Lag is defined on p. 4 in §2 "Assumptions" (quote 608: "…is called service time lag"), and virtual time is formally defined on p. 6 in §3 "The EEVDF Algorithm" (quote 562).

### 2.6 — Miller 1968, Nielsen (NN/g excerpt), Shneiderman 1984

| Line | First words | Source and locator | Verdict |
|---|---|---|---|
| 678 | "should be immediate and perceived as a part of the mechanical action…" | Miller p. 271, "Topic 1. Response to control activation" (image) | E |
| 684 | "the delay between depressing the key and the visual feedback should be…" | Miller p. 271, still under Topic 1 (image; the OCR's "key'" is a scan artefact) | E |
| 688 | "this delay in feedback may be far too slow for skilled keyboard…" | Miller p. 271 ("(Note that this delay…") | E |
| 698 | "0.1 second is about the limit for having the user feel that…" | NN/g excerpt, both HTML copies. The source names "[Miller 1968; Card et al. 1991]" just before the quote, which bears out line 700 | E |
| 708 | "approximately 0.1–0.5 second" | Shneiderman p. 268: "Long [1976] studied delays of approximately 0.1-0.5 second in the time for a keystroke to produce a character on an impact printer." | E |
| 712 | "unskilled and skilled typists worked more slowly and made more errors with…" | Shneiderman p. 268 | E |

Locator findings in 2.6:
- **Locator wrong, line 674**: "열여덟 가지 주제로 나누고" (divides into eighteen topics). Miller p. 269: "The seventeen types of response category and response time cited in the next section of this report are certainly not exhaustive of all the possibilities." The topics run from Topic 1 to Topic 17; Topic 17 is on p. 276 and there is no Topic 18. Line 676 ("첫 번째 주제가 'Response to control activation'", the first topic) is right.
- Line 696, "5장 'Usability Heuristics'의 응답 시간 절" (the response-time section of chapter 5, "Usability Heuristics"): the number is borne out ("Excerpt from Chapter 5 in my book Usability Engineering, from 1993"). The title "Usability Heuristics" appears nowhere in either copy, so it cannot be checked from these copies. The registry entry `nielsen-ue93` already says "its title not verified". The text quoted is the author's web excerpt, not the printed book.
- Line 672, Miller pp. 267–277: consistent with the scan (pp. 268–277 printed, p. 271 for Topic 1).

### 3.2 — ghOSt (paper, SOSP '21, pp. 588–604; and the ghost-userspace README)

Paper pages: PDF page n is printed page 587+n. Line 859's "첫 쪽에 588쪽, 마지막 쪽에 604쪽" (588 on the first page, 604 on the last) is right.

| Line | First words | Source and locator | Verdict |
|---|---|---|---|
| 867 | "We present ghOSt, our infrastructure for delegating kernel scheduling decisions to userspace…" | Paper p. 588, Abstract, sentences 1–2. Line 865 calls it "초록 첫 문장" (the abstract's first sentence), but the quote is the first two sentences | E (locator nuance only) |
| 873 | "ghOSt is a general-purpose delegation of scheduling policy implemented on top of…" | README lines 3–6 | E |
| 875 | (the same text as 873) | README lines 3–6. **Line 875 is a verbatim duplicate block quote of line 873** | E |
| 887 | "ghOSt's kernel side is implemented as a scheduling class, akin to…" | Paper p. 591, §3 "Design", ghOSt overview | **D** (cross-references only). Source: "…the kernel exposes thread state to the agents via messages and status words **(§3.1)**. The agents then instruct the kernel on scheduling decisions via transactions and system calls **(§3.2)**." Both parentheticals are dropped without an elision mark |
| 893 | "Agents must be able to schedule both their local CPU (per-CPU case)…" | Paper p. 593, §3.2 | E |
| 901 | "Programmers use any language to develop and optimize policies, which are modified…" | Paper p. 588, Abstract. Matches line 899 | E |
| 907 | "With ghOSt, scheduling strategies — previously requiring extensive kernel modification — can…" | Paper p. 589, §1 Introduction. Matches line 905 | E |
| 911 | "Programmers can use any language or tools to develop policies, which can…" | README lines 6–7. Matches line 909 | E |
| 917 | "ghOSt supports policies for a range of scheduling objectives, from µs-scale latency…" | README lines 7–10. The guidebook names no source right before it; it follows the README framing of line 909 | E |
| 925 | "the Shinjuku request scheduler optimized highly dispersive workloads – workloads with a…" | Paper p. 588, §1 | **D** (citation markers only). Source: "For example, the Shinjuku request scheduler **[25]** optimized … The Tableau scheduler for virtual machine workloads **[23]** demonstrated … The Caladan scheduler **[21]** focused on…" Three citation brackets are dropped without an elision mark (elsewhere the guidebook marks such drops with "[…]", e.g. line 600) |
| 931 | "Designing, implementing, and deploying new scheduling policies across a large fleet is…" | Paper p. 588, §1 | **D** (citation marker only). Source: "…severely impede performance due to unintended side effects **[33]**. Even when successful…" |
| 937 | "Prior attempts to improve performance and reduce complexity in the kernel by…" | Paper p. 588, §1 | E |
| 941 | "Non-disruptive updates and fault isolation. OS upgrades on a large fleet…" | Paper p. 591, §2.1 "Design Goals", the fifth requirement (line 939's "다섯 개 … 마지막", the last of five, is right). "[…]" is in order | E |
| 949 | "ghOSt supports multiple concurrent policies on a single machine using enclaves. A…" | Paper p. 591, §3 ("Partitioning the machine.") | **D** (citation marker only). Source: "…such as per-NUMA-socket or per-AMD-CCX **[40]**. Enclaves also help…" (the "[…]" correctly stands for "as depicted in Fig. 2.") |
| 955 | "ghOSt uses **enclaves** to group agents and the threads that they…" | README lines 175–178 (the bold is in the source) | E |
| 957 | "Enclaves provide an easy way to partition the machine to support co-location…" | README lines 185–187 | E |
| 965 | "ghOSt enables rapid deployment, since updating the scheduling policy (i.e., the agents)…" | Paper p. 595, §3.4. "[…]" stands for "Similarly, we want to minimize interruptions for client virtual machines." | E |
| 971 | "ghOSt achieves dynamic upgrades by either (a) replacing the agents while keeping…" | Paper p. 595, §3.4 | E |
| 975 | "When you want to upgrade a policy, the agents in the new process…" | README lines 194–197 | E |
| 981 | "The new agent extracts the state of all threads in the enclave…" | Paper p. 595, §3.4 | E |
| 993 | "One of ghOSt's design goals is enabling easy adoption on existing systems…" | Paper p. 595, §3.4 | **D** (cross-reference only). Source: "…a lower priority **(§2)** than the default scheduler class — typically CFS — …" |
| 999 | "Destroying the enclave kills all the agents in that enclave, keeping other…" | Paper p. 595, §3.4 | E |
| 1003 | "ghOSt also recovers from scheduler failures (e.g., crashes, malfunctions, etc.) without…" | README lines 201–207 | E |
| 1007 | "Scheduling bugs in ghOSt or in any other kernel scheduler have system-wide…" | Paper p. 595, §3.4 ("ghOSt watchdog.") | E |
| 1032 | "We show that ghOSt's overheads are small and range from 265 ns…" | Paper p. 589, §1. Matches line 1030 (the sentence ends "(Fig. 5).") | E |
| 1042 | "ghOSt is competitive with Shinjuku for µs-scale tail workloads, even though its…" | Paper p. 597, §4.2 | E |
| 1048 | "Fig. 6c shows that when we co-locate a batch application with a…" | Paper p. 597, §4.2 | **D**. Source: "…the batch application cannot get any CPU resources even when the **RockDB** load is low." The source's misspelling is silently corrected to "RocksDB", with no [sic] or brackets |
| 1054 | "we deploy in production MicroQuanta, a custom, soft real-time scheduler that guarantees…" | Paper p. 597, §4.3 (the "597" inside the extracted text is the page number) | E |
| 1060 | "leading to comparable and in some cases 5-30% better tail latency than…" | Paper p. 589, §1. Matches line 1058 | E |
| 1064 | "For 64B messages, ghOSt performs similar or 10% better than the baseline…" | Paper p. 598, §4.3 | E |
| 1076 | "ghOSt leads to about 40-45% reduction in tail latency for query types…" | Paper p. 599, §4.4 | E |
| 1080 | "Prior to socket- and CCX-aware optimizations, the ghOSt policy led to nearly…" | Paper p. 599, §4.4 | **D** (the fragments are out of order). The guidebook gives "Prior to … B and C. […] The NUMA and CCX optimizations were critical … respectively." In the source the second sentence comes first, in the "CFS vs. ghOSt" paragraph: "Both CFS and ghOSt consider NUMA socket and CCX placement. The NUMA and CCX optimizations were critical in achieving parity with CFS as they delivered 27% and 10% throughput improvements, respectively." The first comes later, in the next paragraph "Tail Latency.": "…comparable tail latency for query type C. Prior to socket- and CCX-aware optimizations, the ghOSt policy led to nearly 2x worse latency for query type A and was on par with CFS for query type B and C (i.e., within 10%)." The "[…]" therefore joins the two in reverse order, and also hides "(i.e., within 10%)" |
| 1086 | "When developing a kernel scheduler, the write-test-write cycle includes (a) compiling…" | Paper p. 599, §4.4 | E |

### 3.3 — `schedext-docs` (`sched-ext.rst` at v6.12 and at mainline `7b63ef2d`)

| Line | First words | Locator | Verdict |
|---|---|---|---|
| 1110 | "sched_ext is a scheduler class whose behavior can be defined by a…" | v6.12 lines 5–6 and mainline lines 7–8, identical in both, which bears out line 1108 | E |
| 1118 (with 1119–1121) | "* sched_ext exports a full scheduling interface so that any scheduling algorithm…" | Mainline lines 10–21, verbatim. v6.12 lines 8–19 have the same words, but the last bullet ends ":kbd:`SysRq-S`" (reST markup). No version is attributed | E. Locator nuance: line 1116 calls these "문서가 내세우는 네 가지" (the four points the document puts forward), but the opening list has **five** bullets in both versions. The fifth: "* When the BPF scheduler triggers an error, debug information is dumped to aid debugging. The debug dump is passed to and printed out by the scheduler binary. …" |
| 1131 | "/* Need to initialize or the BPF verifier will reject the program */" | v6.12 line 145, mainline line 195. "verifier" occurs exactly once in each file, inside the example code, which bears out line 1129 | E |
| 1143 | "Terminating the sched_ext scheduler program, triggering `SysRq-S`, or detection of any…" | Mainline lines 63–65, which is the "최신 버전" (latest version) attributed at line 1141. Line 1145's v6.12 ending "reverts all tasks back to CFS" is right (v6.12 lines 62–64, with ":kbd:`SysRq-S`") | E |
| 1166 | "only tasks with the ``SCHED_EXT`` policy are scheduled by sched_ext, while tasks…" | Mainline lines 57–61. The v6.12 sentence ends "…policies are scheduled by CFS." with no precedence clause, which bears out lines 1164 and 1170 | E |
| 1176 | "The APIs provided by sched_ext to BPF schedulers programs have no stability…" | v6.12 lines 319–326, mainline lines 574–582. The "…" stands for ". This includes … While we will attempt to provide a relatively stable API surface when possible," | E |
| 1151–1156 (code block, extra row) | "# tools/sched_ext/build/bin/scx_simple / local=0 global=3 / … / ^CEXIT…" | v6.12 lines 69–75, mainline lines 70–76. The "…" stands for four counter lines | E |

Also in 3.3:
- Line 1135 ("감시 타이머라는 말이 나오지 않습니다", the word watchdog does not appear): right. Neither version contains "watchdog".
- Line 1096 ("Linux 6.12에 병합", merged in 6.12): neither version of the document states a merge version. The `scx` README states it instead (line 33: "`sched_ext` is supported by the upstream kernel starting from version 6.12."; line 257: "sched-ext has been fully upstreamed as of 6.12.").

### 3.4 — `scx` at v1.1.3

| Line | First words | Locator | Verdict |
|---|---|---|---|
| 1190 | "sched_ext is a Linux kernel feature which enables implementing kernel thread schedulers…" | README.md lines 5–8 (in the source, `sched_ext` is a Markdown link in backticks) | E |
| 1192 | "sched_ext enables safe and rapid iterations of scheduler implementations, thus radically…" | README.md lines 10–12 | E |
| 1200 | "In addition to terminating the program, there are two more ways to…" | README.md lines 81–84, which bears out lines 1196–1198 (the watchdog is in this repository) | E |
| 1230 | "sched_ext is supported by the upstream kernel starting from version 6.12. Both…" | README.md lines 33–35 | E |
| 1234 | "At Meta, we are actively experimenting with multiple production workloads and seeing…" | OVERVIEW.md lines 477–480, which bears out "개요 문서" (the overview document) at line 1232 | E |
| 1238 | "Distros are able to package and release these schedulers, allowing users to…" | OVERVIEW.md lines 283–286 | E |

### 3. Supplementary: inline (non-block) quotations in chapters 2–3, checked because they are cheap

- Line 1145, "reverts all tasks back to CFS" (v6.12): E.
- Lines 1210–1220, the scheduler descriptions of scx_rusty, scx_layered, scx_lavd, scx_bpfland and scx_flash: all E against each README's "## Overview" section at v1.1.3. Locator nuance: line 1208 says "첫 줄" (the first line), but each README's actual first line is the shared boilerplate "This is a single user-defined scheduler used within `sched_ext`, which is a Linux kernel feature…". The quoted text is the first line of the Overview section.
- Lines 752, 753, 754, 755 and 771 (OSTEP ch. 8, the textbook *Operating Systems: Three Easy Pieces*): "a three-queue scheduler" and "with a time slice of 10 ms (and with the allotment set equal to the time slice)" are on p. 4; "a priority boost every 100 ms (which is likely too small of a value, but used here for the example)" is on p. 6, body text describing Figure 8.4; "Lower Priority, Longer Quanta" is the caption of Figure 8.6. All E.
- Line 676, Miller's topic title "Response to control activation": E.

### 4. Counts (the 92 listed block-quote lines)

- **Exact: 84.**
- **Differs: 8.**
  - Two are substantive: L1080, whose fragments are joined in reverse source order, and L582, "dead line" for "deadline".
  - One is a silent correction of a source typo: L1048, "RocksDB" for the source's "RockDB".
  - Five drop only citation or cross-reference markers without an elision mark: L887 "(§3.1)" and "(§3.2)", L925 "[25] [23] [21]", L931 "[33]", L949 "[40]", L993 "(§2)".
- **Locator wrong: 0** among the quote rows themselves.
- **Not found: 0.**

Locator findings on the lines around the quotes:
- Line 558 is wrong: "lag" is not in the EEVDF introduction. It is defined in §2, and virtual time is formally defined in §3.
- Line 674 is wrong: Miller has seventeen topics, not eighteen.
- Nuances: line 865 (the abstract's first two sentences, not one), line 1116 (five bullets, not four), line 1208 (the Overview's first line, not the README's), line 696 (the chapter title "Usability Heuristics" cannot be checked from the copy).
- Editorial: line 875 duplicates line 873.

Extra rows checked: the 1119–1121 continuation lines (inside the L1118 row, E) and the 1151–1156 code block (E). Copies: the local and re-fetched Nielsen HTML both differ from the 9.11 record's hash, with the quoted text unchanged. The ghOSt README has no record.

---

### Scope-card item 60 (research slice 9.12): source quotations in vol-02 chapters 4–6

Checked on 2026-10-09 against the copies below. No repository file was edited. New copies went only into new subfolders of `_dev/research/jioh/task-9.12-related-work-prose/sources/V60/`: `scx-lavd-readme/`, `asa-arxiv25/`, `schedcp-mlsys25/`, `tuneagent-arxiv25/`, `jadhav-arxiv25/`. A sibling agent had already made an empty `V60/scx/`, so I left it alone and used `scx-lavd-readme/`.

**Method.** Text came from poppler `pdftotext` 26.10.0 in its default mode. Where a two-column page or a wrapped figure scrambled the reading order, I re-read the passage with `-layout`, with column-cropped `-x/-y/-W/-H` extraction, or with `-bbox-layout` (Decima p.4; Park pp.4–5; Kgent pp.6–7; ASA pp.3–4, 7). Before comparing, I normalised whitespace, line-break hyphenation (each case checked against `-layout`, because `pdftotext` drops real compound hyphens at line ends, as in "service-level"), ligatures, curly versus straight quotes, and markdown backticks. In the verbatim texts below, apostrophes and quote marks appear as straight characters. Page numbers are **PDF pages**. The FIRM and Kgent PDFs each start with a cover page, so their paper page is the PDF page minus 1.

### Copies

| Registry entry | URL / path | SHA-256 | Matches record |
|---|---|---|---|
| `scx` (scx_lavd README at release v1.1.3) | https://raw.githubusercontent.com/sched-ext/scx/c8728c6b6a3fde451f0f10b95f99aad7a32a750a/scheds/rust/scx_lavd/README.md → `V60/scx-lavd-readme/README.md` | `8e4f48c103d082585d4dfea98c436818bff6530632725f65108393451f3bb65f` | yes (search record S2-09) |
| `decima-sigcomm19` | `sources/S1-06/decima.pdf` | `b6b50a58ea743049f9bf7d92d2941afff1e4308b40ed208fc348fae8b57904d3` | yes (S1-06) |
| `firm-osdi20` | `sources/S1-07/firm.pdf` | `a0adcf9865358b5f10fc99b2fe4257ffb3eea3137d4c9ec72d6d91c2c9d46c68` | yes (S1-07) |
| `park-neurips19` | `sources/S1-08/park.pdf` | `c686bc445a7e97e36f342cf1234bc0ca1a9100056a16e6a9e362350ed7045f98` | yes (S1-08) |
| `asa-arxiv25` v1 PDF | https://arxiv.org/pdf/2511.11628v1 → `V60/asa-arxiv25/2511.11628v1.pdf` | `3a887853b4b21974373f912492963108f55f1526f1e951934a233c850fb07b8b` | yes (S1-11) |
| `asa-arxiv25` abstract page | https://export.arxiv.org/abs/2511.11628 → `V60/asa-arxiv25/abs.html` | `15e239f3d6bea2e215cf493042f2298de269234f6ae74ab4063dab5e76e98c8a` | yes (S1-11) |
| `schedcp-mlsys25` v1 | https://arxiv.org/pdf/2509.01245v1 → `V60/schedcp-mlsys25/2509.01245v1.pdf` (byte-identical to `sources/S1-34/schedcp-v1.pdf`) | `b0fc4ec042d9cb9b2c6ec7eaecf66a7f9dbaca209fbc5f3c6cb5f311328f3a8b` | yes (S1-12) |
| `schedcp-mlsys25` v2 | https://arxiv.org/pdf/2509.01245v2 → `…/2509.01245v2.pdf` | `7dbfe839cbfa3937db68b4654b8dec82c6b6d1d20e25736848729ef7fe25c378` | yes (S1-12) |
| `schedcp-mlsys25` v3 | https://arxiv.org/pdf/2509.01245v3 → `…/2509.01245v3.pdf` | `e22190017e1b88bfa4c9b68fcdd7cde77bf36907577aa8306dae21cc28b35fe4` | yes (S1-12) |
| `schedcp-mlsys25` v4 | https://arxiv.org/pdf/2509.01245v4 → `…/2509.01245v4.pdf` (byte-identical to `sources/S1-34/schedcp-v4.pdf`) | `cce49d3c0ff5466cafc3b921373f6d43df2adcb97e38b40c9d45e3b21206e97c` | yes (S1-12) |
| `schedcp-mlsys25` abstract page | https://export.arxiv.org/abs/2509.01245 → `…/abs.html` | `96a128b3ecd40eec9536bc5a1eb75a783c79034c62de7c416fba68601a3f51d6` | yes (S1-12) |
| `schedcp-mlsys25` TeX source v1 | https://arxiv.org/e-print/2509.01245v1 (redirects to /src/) → `…/eprint-v1.bin`, extracted to `eprint-v1-x/` | `df54a986a344fe7efe8411733f5a91e563a54a71d38a4e73419fc77956a7f791` | no record (new) |
| `schedcp-mlsys25` TeX source v2 | …/e-print/2509.01245v2 → `eprint-v2.bin`, extracted to `eprint-v2-x/` | `3421050c4c56d331508a387ac121c8115ad26207d207ace53acfa8ac862dd327` | no record (new) |
| `schedcp-mlsys25` TeX source v3 | …/e-print/2509.01245v3 → `eprint-v3.bin`, extracted to `eprint-v3-x/` | `3a1a1aaf532415b2fdc6162b4c88eef44ded7d1e39b94bc6dfdf5a8a1f1f5939` | no record (new) |
| `schedcp-mlsys25` TeX source v4 | …/e-print/2509.01245v4 → `eprint-v4.bin`, extracted to `eprint-v4-x/` | `289b0d4a68db1e85d1314faf78b422afa8291294e3af225d00ae8bbd485fca46` | no record (new) |
| `kgent-ebpf24` | `sources/S1-33/kgent-escholarship.pdf` | `1292f7508075a393ea431777dd3458d30fa6a2a3de2428ec813061693bebf754` | yes (S1-33) |
| `tuneagent-arxiv25` v1 | https://arxiv.org/pdf/2508.12551v1 → `V60/tuneagent-arxiv25/2508.12551v1.pdf` | `ee2cd50620be34e0bba2038d50c612d42c32752408eba0308106df84b17ec125` | yes (S1-14) |
| `tuneagent-arxiv25` v2 | https://arxiv.org/pdf/2508.12551v2 → `…/2508.12551v2.pdf` | `90ed2128c1832671fb19c3947191ac2baa1da0f97b431481280cbaa2ba75f413` | yes (S1-14) |
| `tuneagent-arxiv25` abstract page | https://export.arxiv.org/abs/2508.12551 → `…/abs.html` | `220f6ca1547dd1e565ef74f4eeff92dfcdecb1113b2c966ede18b46b066caa1e` | yes (S1-14) |
| `jadhav-arxiv25` v2 | https://arxiv.org/pdf/2506.02025v2 → `V60/jadhav-arxiv25/2506.02025v2.pdf` | `f6fd740b58046ea3b2bb742707d026f8dd7bc2eb3683a83186e545f7a9ca440f` | yes (S1-15) |
| `jadhav-arxiv25` abstract page | https://export.arxiv.org/abs/2506.02025 → `…/abs.html` | `5f7117a4a1c977bb92e80ccf8b7722cb11d54680e0704c4664a464f62b991ec6` | yes (S1-15) |

Not fetched: none of the 4.3–4.4 quotations comes from `lavd-ossna24` (Changwoo Min's OSS NA 2024 slides), `corbet-lwn24` or LWN 1051430. The guidebook takes all four of its 4.3 quotations from "저장소의 설명 문서" (the repository's README), and they match the scx_lavd README in registry entry `scx`. The table of slide numbers in 4.3 is prose, not a quotation, and I did not check it.

### Verdict key

- **exact**: matches after the normalisations above. The note column records any typographic difference that does not change meaning: × written as x, ∗ written as *, the source's inner double quotes turned into single quotes inside the guidebook's double-quoted quotation, LaTeX ``…'' quote marks, or markdown backticks.
- **differs-A**: the only omission (no elision mark) is a bracketed citation number or a figure, table or section cross-reference.
- **differs-B**: another small change: an inserted colon joining a heading, an omitted math interval, figure parentheticals together with a conjunction, a sentence cut off with a period, or a changed capital.
- **differs-C**: content words omitted without an elision mark.
- **locator wrong**: the text is right but the attribution is not.

### Per-quotation results (134 lines: 133 from vol02-quotes.json plus line 2609)

| Line | § | Opening (~12 words) | Source & locator | Verdict | Source verbatim (when not exact) / note |
|---|---|---|---|---|---|
| 1321 | 4.3 | scx_lavd is a BPF scheduler that implements an LAVD (Latency-criticality Aware Virtual | scx_lavd README §Overview | exact | README wraps scx_lavd and LAVD in backticks |
| 1327 | 4.3 | its core ideas are 1) measuring how much a task is latency | README §Overview | exact | fragment; the source continues "(e.g., task's deadline, time slice, etc.)." |
| 1335 | 4.3 | scx_lavd is initially motivated by gaming workloads. | README §Typical Use Case | exact | |
| 1339 | 4.3 | Production Ready?: Yes, scx_lavd should be performant across various CPU architectures. | README §Production Ready? | differs-B | The source has a heading and then a sentence: "## Production Ready?" / "Yes, `scx_lavd` should be performant across various CPU architectures." The guidebook joins them with an inserted colon. |
| 1483 | 5.2 | Efficiently scheduling data processing jobs on distributed compute clusters requires complex algorithms. | Decima p.1, abstract, first two sentences | exact | "초록의 첫 두 문장" (the abstract's first two sentences) is correct |
| 1491 | 5.2 | In this paper, we show that modern machine learning techniques can generate | Decima p.1 abstract | exact | |
| 1499 | 5.2 | However, off-the-shelf RL techniques cannot handle the complexity and scale of the | Decima p.1 abstract | exact | |
| 1507 | 5.2 | Our prototype integration with Spark on a 25-node cluster shows that Decima | Decima p.1 abstract | exact | typographic: the source has "2×" |
| 1517 | 5.2 | A Spark job consists of a DAG whose nodes are the execution | Decima p.3 §3 | exact | |
| 1525 | 5.2 | Spark must therefore handle three kinds of scheduling decisions: (i) deciding how | Decima p.3 §3 | exact | |
| 1529 | 5.2 | Decima focuses on DAG scheduling (i.e., which stage to run next) and | Decima p.3 §3 | exact | |
| 1539 | 5.2 | One option is to create a flat feature vector containing all the | Decima p.4 §5.1 | exact | runs from the foot of the left column to the right column, after Figure 4 and Table 1 |
| 1551 | 5.2 | As a naive approach, consider a solution, that given the embeddings, returns | Decima p.5 §5.2 | differs-A | "As a naive approach, consider a solution, that given the embeddings from §5.1, returns the assignment for all executors to job stages in one shot. … In RL, both large action spaces and long action sequences increase sample complexity and slow down training [7, 72]." ("from §5.1" and "[7, 72]" are omitted) |
| 1557 | 5.2 | Decima balances the size of the action space and the number of | Decima p.5 §5.2 | exact | |
| 1563 | 5.2 | Decima invokes the scheduling agent when the set of runnable stages — | Decima p.5 §5.2 | exact | |
| 1571 | 5.2 | Decima gives the agent a reward r_k after each action based on | Decima p.6 §5.3 | differs-B | "… Decima penalizes the agent r_k = −(t_k − t_{k−1})J_k after the k-th [superscript th] action, where J_k is the number of jobs in the system during the interval [t_{k−1}, t_k)." The guidebook ends "during the interval." and drops "[t_{k−1}, t_k)". Its subscript notation is a transcription. |
| 1577 | 5.2 | This objective minimizes the average number of jobs in the system, and | Decima p.6 §5.3 | differs-A | "…, and hence, by Little's law [21, §5], it effectively minimizing the average JCT." |
| 1587 | 5.2 | In our evaluation, we compare Decima's performance to that of seven baseline | Decima p.8 §7.1 | differs-A | item (7) in the source: "(7) Graphene∗, an adaptation of Graphene [36] for Decima's discrete executor classes." ("[36]" is omitted; ∗ written as *). Items (1)–(6) are exact. |
| 1593 | 5.2 | We sweep through α ∈ {−2,−1.9,…,2} for the optimal factor. | Decima p.8 §7.1, item (5) | exact | "다섯 번째 항목" (the fifth item) is correct. The source writes "..." as three dots. |
| 1601 | 5.2 | We randomly sample jobs from six different input sizes (2, 5, 10, | Decima p.9 §7.2 (batched arrivals) | differs-A | "… and all 22 TPC-H [73] queries, producing a heavy-tailed distribution: …" |
| 1605 | 5.2 | Decima outperforms all baseline algorithms and improves the average JCT by 21% | Decima p.9 §7.2 | exact | The source sentence opens "Finally, Decima outperforms…". The source writes ("opt. weighted fair") in double quotes; the guidebook uses single quotes inside its own double quotes. |
| 1611 | 5.2 | We sample 1,000 TPC-H jobs of six different sizes uniformly at random, | Decima p.9 §7.2 | exact | |
| 1615 | 5.2 | Decima's average JCT is 29% lower. In particular, Decima shines during busy, | Decima p.9 §7.2 | differs-A | "… where Decima completes jobs about 2× faster (Figure 10b)." (the guidebook's […] elision itself is correct) |
| 1621 | 5.2 | Decima's performance gain comes from finishing small jobs faster […] Decima achieves | Decima p.9 §7.2 | differs-A | "Decima achieves this by assigning more executors to the small jobs (Figure 10d)." |
| 1625 | 5.2 | The right number of executors for each job is workload-dependent: indiscriminately giving | Decima p.9 §7.2 | differs-A | "… would use cluster resources inefficiently (§2.2)." |
| 1633 | 5.2 | Finally, we train Decima for at least 50,000 iterations for all experiments. | Decima p.16, Appendix C | exact | |
| 1635 | 5.2 | We implemented Decima's training framework using TensorFlow, and we use 16 workers | Decima p.16, Appendix C | differs-A | "We implemented Decima's training framework using TensorFlow [1], and we use 16 workers …" (the rest is exact; Algorithm 1 interrupts it in the PDF) |
| 1641 | 5.2 | Each training iteration takes about 5 seconds. | Decima p.11 §7.4, "Training and inference performance" | exact | The locator "연속 도착 실험의 학습 곡선을 설명하는 문단" (the paragraph describing the continuous-arrival learning curve) is correct: "Figure 15a shows Decima's learning curve (in blue) on continuous TPC-H job arrivals" |
| 1647 | 5.2 | Our training infrastructure relies on a faithful simulator of Spark job execution | Decima p.16, Appendix D "Simulator fidelity" | exact | |
| 1655 | 5.2 | When training with a mixed set of workloads that cover the whole | Decima p.11 §7.4 | exact | the Figure 15 caption interrupts it in the PDF |
| 1659 | 5.2 | These results highlight that a diverse training workload set helps make Decima's | Decima p.11 §7.4 | exact | cut at the source's ";" |
| 1675 | 5.3 | multiplexing of compute resources across microservices is still challenging in production because | FIRM p.2 abstract | exact | "service-level" is hyphenated across a line break |
| 1683 | 5.3 | FIRM leverages online telemetry data and machine-learning methods to adaptively (a) detect/localize | FIRM p.2 abstract | exact | |
| 1691 | 5.3 | Experiments across four microservice benchmarks demonstrate that FIRM reduces SLO violations by | FIRM p.2 abstract | exact | typographic: the source has "16×" and "11×" |
| 1699 | 5.3 | We evaluated FIRM on a set of end-to-end interactive and responsive real-world | FIRM p.12 §4.1 | differs-A | "(i) DeathStarBench [34], consisting of … and (ii) Train-Ticket [128], consisting of the Train-Ticket Booking Service." |
| 1703 | 5.3 | Social Network implements a broadcast-style social network with unidirectional follow relationships whereby | FIRM p.12 §4.1 | exact | |
| 1709 | 5.3 | These benchmarks contain 36, 38, 15, and 41 unique microservices, respectively; cover | FIRM p.12 §4.1 | differs-A | "…; cover all workflow patterns (see §3.2); and use various programming languages …" |
| 1723 | 5.3 | Based on the insight that resource contention manifests as dynamically evolving CPs, | FIRM p.6 §3 | exact | |
| 1729 | 5.3 | FIRM estimates and controls a fine-grained set of resources, including CPU time, | FIRM p.8 | exact | |
| 1737 | 5.3 | CPU Actions: Actions on scaling CPU utilization are executed through modification of | FIRM p.11 | exact | |
| 1743 | 5.3 | FIRM includes a performance anomaly injection framework that triggers SLO violations by | FIRM p.6 §3 | exact | |
| 1749 | 5.3 | Model-free RL does not need the ergodic distribution of states or the | FIRM p.9 | exact | |
| 1757 | 5.3 | We observed that the AIMD-based method, albeit simple, outperforms the Kubernetes autoscaling | FIRM p.14 §4.4 | differs-B | "2. Lowered the overall requested CPU limit by 29–62%, as shown in Fig. 11(b), and increased the average cluster-level CPU utilization by up to 33%; and 3. Reduced the number of dropped or timed out user requests by up to 8× as shown in Fig. 11(c)." The guidebook omits "as shown in Fig. 11(b),", the "and" before "3." and "as shown in Fig. 11(c)". |
| 1773 | 5.4 | We present Park, a platform for researchers to experiment with Reinforcement Learning | Park p.1 abstract | exact | |
| 1777 | 5.4 | Thus, in this work we first discuss the unique challenges RL for | Park p.1 abstract | exact | |
| 1791 | 5.4 | Seven of the environments use real systems in the backend. For the | Park p.6 §4 | differs-A | "Seven of the environments use real systems in the backend (see Table 2)." |
| 1799 | 5.4 | In this section, we explain the unique characteristics and challenges that often | Park p.3 §3 | exact | The section title given at line 1797, "RL for Systems Characteristics and Challenges", is correct (§3) |
| 1807 | 5.4 | In some computer systems, the majority of the state-action space presents little | Park p.3 §3.1 | exact | |
| 1813 | 5.4 | To exit this bad state, the agent must set a low sending | Park p.3 §3.1 | exact | |
| 1821 | 5.4 | In these environments, using domain-knowledge to confine the search space helps to | Park p.4 §3.1 | exact | |
| 1827 | 5.4 | When designing RL methods for problems with complex structure, properly encoding the | Park p.4 §3.1 | exact | |
| 1831 | 5.4 | In other cases, the size of the action space is constantly changing | Park p.4 §3.1 | exact | |
| 1837 | 5.4 | However, finding the right representation for each problem is a central challenge, | Park p.4 §3.1 | exact | |
| 1845 | 5.4 | Queuing systems environments (e.g., job scheduling, load balancing, cache admission) have dynamics | Park p.4 §3.2 | exact | the wrapped Figure 1 interleaves with it in plain extraction |
| 1851 | 5.4 | If the arrival sequence after time t consists of a burst of | Park p.4 §3.2 | differs-B | "If the arrival sequence after time t consists of a burst of large jobs (e.g., job sequence 1), the job queue will grow and the agent will receive low rewards. In contrast, a stream of lightweight jobs (e.g., job sequence 2) will lead to short queues and large rewards. …" The guidebook omits both "(e.g., job sequence N)" parentheticals, which point at Figure 1. |
| 1857 | 5.4 | However, the proposed training implementations ('multi-value network' and 'meta baseline') are tailored | Park p.5 §3.2 | exact | the source writes ("multi-value network" and "meta baseline") in double quotes |
| 1863 | 5.4 | In practice, production computer systems (e.g., Spark schedulers, load balancers, cache controllers, | Park p.5 §3.2 | differs-A | "This creates an infinite horizon MDP [13] that prevents the RL agents from performing episodic training." |
| 1867 | 5.4 | Moreover, the discounted total reward formulation in the episodic case might not | Park p.5 §3.2 | **differs-C** | "For example, scheduling a large job on a slow server blocks future small jobs (affecting job runtime in the rewards), no matter whether the small jobs arrive immediately after the large job or much farther in the future over the course of the lifetime of the large job." The guidebook drops "(affecting job runtime in the rewards)". |
| 1875 | 5.4 | Unlike training RL in simulation, robustly deploying a trained RL agent or | Park p.5 §3.3 | exact | |
| 1881 | 5.4 | First, discrepancies between simulation and reality prevent direct generalization. For example, in | Park p.5 §3.3 | differs-A | "… due to both variance in the underlying data distribution and system-specific artifacts [53]." |
| 1885 | 5.4 | Second, interactions with some real systems can be slow. In adaptive video | Park p.5 §3.3 | differs-A | "Naively using the same training method from simulation (as in Figure 4a) would take a single-threaded agent more than 10 years to complete training in reality." |
| 1891 | 5.4 | Finally, live training or directly deploying an agent from simulation can degrade | Park p.5 §3.3 | exact | |
| 1895 | 5.4 | Therefore, to deploy training algorithms online, these problems require RL to train | Park p.5 §3.3 | differs-A | "… require RL to train robust policies that ensure safety [2, 33, 49]." |
| 1901 | 5.4 | As in other areas of ML, interpretability plays an important role in | Park p.5 §3.4 | exact | |
| 1909 | 5.4 | Here, a unique opportunity is to build hybrid solutions, which combine learning-based | Park pp.5–6 §3.4 | exact | Figure 3 interrupts it at the page break |
| 1967 | 5.6 | Modern operating system schedulers employ a single, static policy, which struggles to | ASA p.1 abstract | **locator wrong** (minor; text exact) | The guidebook calls this "초록의 첫 문장" (the abstract's first sentence), but the quotation is the first sentence plus the start of the second. The source: "Modern operating system schedulers employ a single, static policy, which struggles to deliver optimal performance across the diverse and dynamic workloads of contemporary systems. This "one-policy-fits-all" approach leads to significant compromises in fairness, throughput, and latency, particularly with the rise of heterogeneous hardware and varied application architectures." |
| 1973 | 5.6 | This paper proposes a new paradigm: dynamically selecting the optimal policy from | ASA p.1 abstract | exact | |
| 1981 | 5.6 | ASA's core is a novel, low-overhead offline/online approach. First, an offline process | ASA p.1 abstract | exact | |
| 1991 | 5.6 | The results show a clear U-shaped curve for response delay. A very | ASA p.9 | exact | the source spaces "W < 4s", "W > 10s", "W = 6s" |
| 2012 | 5.6 | The Perception module collects data from multiple sources, including kernel-level eBPF programs, | ASA pp.3–4 §3.2 | exact | "The" ends p.3 |
| 2026 | 5.6 | The expert scheduler set available to ASA includes: scx_p2dq, scx_bpfland, scx_nest, scx_lavd, | ASA p.8 | differs-A | "The expert scheduler set available to ASA includes: scx_p2dq [9], scx_bpfland [2], scx_nest [24], scx_lavd [3], scx_simple, scx_flash [4], scx_rusty [1], and the baseline EEVDF [29]." (the guidebook stops at scx_rusty) |
| 2034 | 5.6 | The primary limitation of ASA is that its performance ceiling is defined | ASA p.11 | exact | |
| 2040 | 5.6 | we constructed a benchmark suite of 28 scenarios. These are generated by | ASA p.7 §5.1.1 | exact | "resource-intensive" is hyphenated across a line break |
| 2052 | 5.6 | Our evaluation, based on a novel benchmark focused on user-experience metrics, demonstrates | ASA p.1 abstract | exact | |
| 2058 | 5.6 | The results show that ASA achieves an overall win rate of 86.4% | ASA p.8 | exact | |
| 2064 | 5.6 | Notably, in many scenarios where ASA does not significantly outperform EEVDF, it | ASA p.8 | exact | |
| 2072 | 5.6 | ASA's selected scheduler is the single best one in 45.4% of cases | ASA p.9 | exact | The abstract does say 78.6% (line 2052), so the discrepancy the guidebook reports is real |
| 2082 | 5.6 | Even without any environment-specific fine-tuning, the base model correctly identifies the running | ASA p.9 | exact | |
| 2084 | 5.6 | Without fine-tuning, the base workload classifier achieves a notable accuracy of 96.83%. | ASA p.9 | exact | |
| 2108 | 5.6 | This decoupled architecture allows ASA to adapt to new hardware platforms rapidly | ASA p.1 abstract | exact | |
| 2120 | 5.6 | This is complicated by two factors: the platform dependency of workload characteristics, | ASA p.5 | exact | |
| 2128 | 5.6 | With the system operational metrics, we train a preliminary workload classification model. | ASA p.6 §4.3.1 | exact | the source writes "scenario-optimal scheduler" in double quotes |
| 2138 | 5.6 | Deploying the generalized ASA agent onto a new hardware platform is a | ASA p.7 §4.4 | exact | the source writes "Generalization Model Training" in double quotes |
| 2239 | 6.2 | Operating system schedulers suffer from a fundamental semantic gap, where kernel policies | SchedCP v1–v4 p.1, abstract, first sentence | exact | |
| 2245 | 6.2 | Operating system schedulers face a fundamental challenge: kernel policies cannot understand what | SchedCP v4 p.1 §1 (also v3; absent from v1/v2) | differs-A | "… as Linux's EEVDF scheduler [9] applies one-size-fits-all policies to diverse workloads." "최신 판본의 서론" (the latest version's introduction) is correct |
| 2251 | 6.2 | a domain knowledge gap exists between developers and users: DevOps engineers lack | SchedCP v4 p.2 (also v3) | exact | v1/v2 read "application-specific performance targets"; the guidebook follows v4 |
| 2257 | 6.2 | In cloud platforms, system administrators who manage schedulers are not the developers | SchedCP v1/v2 p.1 | exact | marked long-version-only: correct, absent from v3/v4 |
| 2265 | 6.2 | Our core insight is that the challenge is not merely to apply | SchedCP v1–v4 p.1 abstract | exact | |
| 2275 | 6.2 | SchedCP is a secure control plane acting as an 'API for OS | SchedCP v4 p.2 (also v3) | exact | |
| 2281 | 6.2 | SchedCP provides a stable interface with three key services: a Workload Analysis | SchedCP v4 p.1 abstract | exact | Only v4 reads "code and configurations"; v1–v3 read "code and configure" (see the note on line 2283 below) |
| 2289 | 6.2 | Provides tiered access to system performance data: (1) cost-effective API endpoints with | SchedCP v4 p.3 (also v3) | exact | the guidebook adds markdown backticks around perf and top |
| 2297 | 6.2 | Database storing executable eBPF scheduler programs with metadata (natural language descriptions, target | SchedCP v4 p.3 | exact | |
| 2301 | 6.2 | includes a multi-stage validation pipeline: (1) kernel's eBPF verifier ensures memory safety | SchedCP v4 p.3 | exact | |
| 2311 | 6.2 | sched-agent is the first autonomous multi-agent system that decomposes scheduler optimization into | SchedCP v4 p.2 (also v3) | exact | |
| 2317 | 6.2 | For kernel compilation, it produces profiles like "CPU-intensive parallel compilation with short-lived | SchedCP v4 p.4 | exact | The guidebook keeps LaTeX ``…'' marks from the TeX source; the PDF shows curly quotes |
| 2323 | 6.2 | The Planning Agent transforms profiles into optimization strategies via the Scheduler Policy | SchedCP v4 p.4 | exact | |
| 2329 | 6.2 | For existing production-ready scheduler solutions with strong performance history, it configures parameters. | SchedCP v1/v2 p.5 | exact | long-version-only: correct |
| 2339 | 6.2 | For kernel compilation (tinyconfig, "make -j 172" on 6.14 source), SchedCP achieves | SchedCP v4 p.4 | differs-A | "… reaching 1.79× total improvement over EEVDF (Figure 2a)." |
| 2345 | 6.2 | The workload shows 1.63x speedup from 13.57s to 8.31s using scx_rusty as | SchedCP v2 p.6 | exact | long-version-only: correct (v1 has the typo "first attemp.") |
| 2351 | 6.2 | Pre-trained RL approaches show no improvement, likely because they require costly hardware/workload-specific | SchedCP v4 p.4 | differs-A | "Pre-trained RL approaches [7] show no improvement, …". The guidebook says the attached reference is a single article on ML for Linux load balancing; that is correct, since v4's [7] is "Jonathan Corbet. Improved load balancing with machine learning. LWN.net, July 2025." |
| 2359 | 6.2 | On schbench, initial AI configuration (scx_bpfland) underperformed, but three refinement iterations identified | SchedCP v4 p.4 | differs-A | "On schbench [12], initial AI configuration (scx_bpfland) underperformed, … versus EEVDF (Figure 2b), demonstrating effective learning from feedback." |
| 2365 | 6.2 | While AI configured scheduler initially underperformed with 13% worse P99 latency (46.1ms | SchedCP v1/v2 p.6 | exact | long-version-only: correct |
| 2371 | 6.2 | For 8 diverse batch workloads (file compression, video transcoding, software testing, data | SchedCP v4 p.5 | differs-A | "… implementing Longest Job First (LJF) scheduling to achieve 20% average latency reduction (Figure 2c)." |
| 2377 | 6.2 | generated custom eBPF code implementing a Longest Job First (LJF) scheduling policy—a | SchedCP v2 p.6 (not in v1) | exact | long-version-only: correct for v2 |
| 2387 | 6.2 | Claude Opus successfully classified all 8 workloads at $0.15 per analysis | SchedCP v4 p.5 (v3 p.4) | exact | |
| 2391 | 6.2 | The cost for this analysis averaged $0.15 per workload | SchedCP v2 p.6 (in v1, a figure splits it) | exact | long-version-only: correct |
| 2395 | 6.2 | Generation efficiency improved 13× (to 2.5 minutes) with $0.45 synthesis cost per | SchedCP v4 p.5 | differs-B | "Generation efficiency improved 13× (to 2.5 minutes) with $0.45 synthesis cost per workload, demonstrating economic viability alongside performance gains." The guidebook ends at "per workload." with a period. |
| 2399 | 6.2 | In addition to performance gains, our framework's optimizations reduced generation costs per | SchedCP v1/v2 p.6 | exact | long-version-only: correct |
| 2405 | 6.2 | The successful generation required 33 minutes, 221 LLM API calls, and 15+ | SchedCP v1–v4 (v4 p.2) | exact | |
| 2411 | 6.2 | We tested Claude Code, the state-of-the-art LLM agent, with "write a FIFO | SchedCP v4 p.2 | differs-A | "We tested Claude Code[4], the state-of-the-art LLM agent, …". The wording is v4's: v1–v3 read "state of the art" and "8 minutes development". |
| 2417 | 6.2 | The agent required root access, could crash the system during testing, and | SchedCP v1–v4 (v4 p.2) | exact | |
| 2429 | 6.2 | (4) operating in the control plane to generate optimized code that runs | SchedCP v4 p.2 (also v2 p.3) | exact | |
| 2433 | 6.2 | This control plane separation represents a key architectural insight: LLMs generate and | SchedCP v2 p.3 only | exact | long-version-only: correct for v2 (absent from v1) |
| 2435 | 6.2 | Deployed on the production-ready sched_ext infrastructure, our approach executes with zero LLM | SchedCP v1/v2 p.2 | exact | long-version-only: correct |
| 2445 | 6.2 | We validate SchedCP's effectiveness through four research questions: configuring existing schedulers (RQ1), | SchedCP v4 p.4 (also v3) | exact | |
| 2449 | 6.2 | • RQ1: Can SchedCP effectively configure existing schedulers? • RQ2: Can SchedCP | SchedCP v1/v2 p.5 | exact | |
| 2457 | 6.2 | How effectively can SchedCP understand workloads? | SchedCP **TeX source** of v1 and v2, `sections/evaluation.tex` line 13 | exact (macro expanded) | The source line is `% \item \textbf{RQ5}: How effectively can \sys understand workloads?`, with `\newcommand{\sys}{SchedCP\xspace}`. It is commented out, and absent from the v3/v4 source (`short.tex`). |
| 2463 | 6.2 | Claude Opus successfully classified all 8 workloads at $0.15 per analysis, while | SchedCP v4 p.5 | exact | it is inside the batch-workload ("New Scheduler Synthesis") paragraph, as the guidebook says |
| 2469 | 6.2 | All experiments successfully created working custom scheduler configurations or eBPF programs. Future | SchedCP v4 p.4 | exact | v3 reads "create" |
| 2519 | 6.3 | The extended Berkeley Packet Filters (eBPF) ecosystem allows for the extension of | Kgent PDF p.2 abstract | exact | |
| 2525 | 6.3 | This paper presents Kgent, an alternative framework that alleviates the difficulty of | Kgent PDF p.2 abstract | exact | |
| 2533 | 6.3 | To ensure that LLM's output is semantically equivalent to the user's prompt, | Kgent PDF p.2 abstract | exact | |
| 2539 | 6.3 | We show that Kgent produces correct eBPF programs on 80%—which is an | Kgent PDF p.2 abstract | exact | |
| 2543 | 6.3 | Moreover, we find that Kgent very rarely synthesizes "false positive" eBPF programs—i.e., | Kgent PDF p.2 abstract | exact | "초록에는 그 비율의 숫자가 없습니다" (the abstract gives no figure for that rate) is correct |
| 2551 | 6.3 | We split the prompts for which Kgent fails to correctly synthesize an | Kgent PDF p.6 §5 | differs-B | "To understand the consequence of Kgent's incorrect outputs, we split the prompts for which Kgent fails …" The guidebook capitalises "We" in the middle of the sentence. |
| 2557 | 6.3 | Conceptually, FPs represent a safety violation since a developer using Kgent may | Kgent PDF p.6 §5 | exact | |
| 2575 | 6.3 | The results indicate that model-guided feedback plays a large role in improving | Kgent PDF p.7 §5.2.1 | exact | the source prints "30%to 60%" |
| 2579 | 6.3 | Including the comprehension and symbolic execution component also improves Kgent's effectiveness substantially—accuracy | Kgent PDF p.7 §5.2.1 | **differs-C** | "Including the comprehension engine and symbolic execution component also improves Kgent's effectiveness substantially—accuracy improves to 77.5%, while the false positive rate moves to 5%." The guidebook drops "engine". The remainder, through "back down to the baseline of 2.5%", is exact. |
| 2599 | 6.4 | Linux kernel tuning is essential for optimizing operating system (OS) performance, yet | TuneAgent v2 p.1 abstract | exact | v1's abstract differs, as the guidebook says |
| 2603 | 6.4 | TuneAgent formulates the kernel space as a constrained RL environment, enabling large | TuneAgent v2 p.1 abstract | exact | |
| 2609 | 6.4 | OS-R1: Agentic Operating System Kernel Tuning with Reinforcement Learning | TuneAgent v1 p.1 title | exact | |
| 2631 | 6.4 | we propose a novel Large Language Model (LLM)-based scheduler using a ReAct-style | Jadhav v2 p.1 abstract | exact | "(LLM)-based" is hyphenated across a line break |
| 2637 | 6.4 | We evaluate our approach using OpenAI's O4-Mini and Anthropic's Claude 3.7 across | Jadhav v2 p.1 abstract | exact | |
| 2645 | 6.4 | The method excels in constraint satisfaction and adapts to diverse workloads without | Jadhav v2 p.1 abstract | exact | the ACM permission block interrupts it in the PDF |

### Counts (134 quotations)

- **exact: 103.** Nine carry typographic notes only: 1507 and 1691 (× written as x); 1605, 1857, 2128 and 2138 (inner quotes turned single); 2317 (LaTeX quote marks); 2289 (backticks added); 1593 ("…" for "..."). Line 2457 is exact with the `\sys` macro expanded.
- **differs: 30.**
  - **A, only citation or cross-reference markers omitted (22):** 1551, 1577, 1587, 1601, 1615, 1621, 1625, 1635, 1699, 1709, 1791, 1863, 1881, 1885, 1895, 2026, 2245, 2339, 2351, 2359, 2371, 2411.
  - **B, other small change (6):** 1339 (heading joined with an inserted colon), 1571 (interval "[t_{k−1}, t_k)" omitted), 1757 (figure references and an "and" omitted), 1851 (two "(e.g., job sequence N)" parentheticals omitted), 2395 (sentence cut and ended with a period), 2551 ("we" capitalised).
  - **C, content words omitted (2):** 1867 "(affecting job runtime in the rewards)"; 2579 "engine".
- **locator wrong: 1.** 1967: the guidebook calls it the abstract's first sentence, but it is the first sentence plus the start of the second.
- **not found: 0.**

SchedCP version marking is correct throughout. Every unmarked quotation is in v4. Every quotation marked as long-version-only is in v2 and not in v3/v4, and 2377 and 2433 are in v2 only (not v1).

### Other locators checked near the quotations (outside the 134 lines)

- **Inline quoted fragments.**
  - Exact: 1511/1585 "hand-tuned scheduling heuristics" and "Spark on a 25-node cluster" (Decima abstract); 1695 "four microservice benchmarks" and the three "up to" figures (FIRM abstract); 2038 "a novel benchmark", 2112 "a pre-configured, machine-specific mapping table" and 2148 "expensive retraining" (ASA abstract); 2627 "work under review" (the Jadhav comments field reads "10 pages, 6 figures, work under review").
  - 1617 "up to 2x improvement…": the source has "2×".
  - 2283: "code and configure" is in the v1, v2 and v3 PDFs and in their TeX sources (`sample-sigconf.tex:171`, `short.tex:67`), and v4 reads "code and configurations". Correct.
- **Versions and dates.**
  - Correct: 1955/1961 (ASA: v1 on 2025-11-07 is the only version; journal-ref and comments fields absent); 2207 (SchedCP: v1 2025-09-01, v2 09-03, v3 09-26, v4 09-30, no v5 as of 2026-10-09); 2597/2613 (TuneAgent: v1 2025-08-18, v2 2026-05-31; titles; the fourth author is Kaichun Yao in v1 and Zhenghong Lin in v2; "up to 5.6%" in both abstracts); 2625/2627 (Jadhav: v2 2025-09-03 is the latest).
  - The Korean renderings in quote marks at 2613 are faithful to v1's "efficiency, scalability, and generalization" and v2's "complex kernel space, sparse performance feedback, and strong workload sensitivity". They are translations shown in quote marks.
- **SchedCP journal-ref wording (2209, 2674; cite line 2201).** arXiv's "Journal reference" field reads **"MLforSystem 2025"**, not "ML for Systems 2025". I did not check the "@ NeurIPS 2025" part of 2201.
- **SchedCP length history (2211).** The guidebook says "길게 썼다가 다시 짧은 형태로 돌아온 것입니다" (it was written long, then went back to a short form). The copies don't support "went back": v1 is the same 8-page ACM sigconf manuscript as v2 (`sample-sigconf.tex`), and v3/v4 are 6 pages (`short.tex`). No earlier short version exists. v1 also lacks some v2-only sentences (those quoted at 2377 and 2433).
- **Kgent ablation table (line 2568), a transcription of the paper's table rather than a quotation.** The human-expertise row ("사람의 전문 지식으로 대체") swaps the "could not synthesise" (false negative) and accuracy columns. Source Table 1 (PDF p.7), with columns "A FP FN", reads "Human 72.5% 2.5% 25%": accuracy 72.5%, false positive 2.5%, false negative 25%. The guidebook gives false negative 72.5% and accuracy 25%. The source's prose agrees with the source table: "Kgent demonstrates higher accuracy without additional false positives compared to the human expertise baseline" (80% against 72.5%). The other four rows match.

---

### Scope-card item 60 (research slice 9.12): source quotations in vol-02 chapters 7 and 8

Guidebook: `docs/guidebook/vol-02-related-work.md`, chapter 7 (lines 2695–3183) and chapter 8 (lines 3187–3502).
I checked 52 quotations: the 51 entries in `vol02-quotes.json` whose `sec` starts with 7. or 8., minus line 3360 (Korean commentary), plus the nested quote at line 2715. I found no other block-quote line in these chapters that carries an English quotation after a label. The continuation lines 3236–3237 and 3250–3251 belong to the multi-line quotes that start at 3235 and 3249.

Method: I compared each quotation with the copy after normalising whitespace, curly and straight quotes, ligatures, line-break hyphenation, Markdown link markup (`[text](url)` → `text`) and list bullets. `...` counts as the guidebook's elision, and each fragment had to appear in order. A script did the match (`scratchpad/v60-scripts/check.py`), and I also read every passage by eye in the copy.

V60 is `_dev/research/jioh/task-9.12-related-work-prose/sources/V60/`, and VER is `_dev/research/jioh/2026-09-13-verification/sources/`. No repository file was edited.

### Copies

| Entry | URL / path of the copy used | SHA-256 | Equals the record's? |
|---|---|---|---|
| gamemode-docs: Game Mode portal | https://learn.microsoft.com/en-us/previous-versions/windows/desktop/gamemode/game-mode-portal → `V60/gamemode-docs/game-mode-portal.html` (fetched 2026-10-09, HTTP 200) | `d18e296974a8a5d1078b1a9c154e4c14a691a0496683f23b3874e8e748c63fbd` | **no** (S2-16: `20bb5394…17d0`). The live page bytes changed, but every quoted passage is present. |
| gamemode-docs: expandedresources.h header page | https://learn.microsoft.com/en-us/windows/win32/api/expandedresources/ → `V60/gamemode-docs/expandedresources.html` | `0614bd3ae3b0a531d96e5c33d1e0b2bae8e329ac07c6f5fd7ff06d40966231e7` | yes (S2-16) |
| gamemode-docs: HasExpandedResources | …/nf-expandedresources-hasexpandedresources → `V60/gamemode-docs/hasexpandedresources.html` | `aa3aab9ee8e7eac88a427dbff298546af3ad8f397a53efa6408de4f5ca960ade` | yes (S2-16) |
| gamemode-docs: GetExpandedResourceExclusiveCpuCount | …/nf-expandedresources-getexpandedresourceexclusivecpucount → `V60/gamemode-docs/getexpandedresourceexclusivecpucount.html` | `787e3c5cf070dc1f055fc766d7c34651197bafe5e6e6fc498980aafb45c7810e` | yes (S2-16) |
| gamemode-docs: ReleaseExclusiveCpuSets | https://learn.microsoft.com/en-us/windows/win32/api/expandedresources/nf-expandedresources-releaseexclusivecpusets → `V60/gamemode-docs/releaseexclusivecpusets.html` | `77de8a946e47b1796b16c2f8a722ac7167cff9c12fbbbb00b09826b16b6e5618` | **no record hash.** S2-16 has no copy of this page. The 2026-09-13 verification's copy (`VER/gamemode-docs/win32api-nf-releaseexclusivecpusets.html`, `ea82617d…038c`, listed in R07) also contains line 2777's sentence. |
| ananicy (upstream) | `VER/ananicy/README.md`, clone at `1e2cc9a62ba3b6793e59da66aa0039f89e1ad49f` | `7879441e10863035f42421925356910a9bbcc3040fc76346abb349e3bdc6b8d2` | yes (S2-30) |
| ananicy (ananicy-cpp) | `VER/ananicy-cpp/README.md`, clone at `3554447c1ca495478bd00e002078847dfd2205d6` | `603e16e86a3037f986669abd231c67b294a2cfd63e04dfe87839a012da7cbb39` | yes (S2-31) |
| ananicy-rules | `task-9.12…/sources/S3-19/ananicy-rules`, HEAD `03ef03fbf7e834385377432ccecaedd32e3414bb` (2026-09-08 19:11 −0300): `README.md` | `0886ec1f23a1ef772e676ba65bc13961ce7942bec6e0dc9d0936a4f60b16b7ed` | yes (S2-32) |
| ananicy-rules | same clone, `00-types.types` | `667d89cb61a949ac9b6595f2f318dc452b65c735d8cd6d4fcd5f934dc940591d` | yes (S2-32) |
| hackbench | `VER/rt-tests` at HEAD `fd45df830803dd7f26d2ca8bdcf05fd7e0d62ae8` (the commit the guidebook names): `src/hackbench/hackbench.8` | `84fe7408e1d820ee88a4114fbeb60cef600ebc70f07d27814030d728e091f3fc` | yes. It equals 9.11's S2-20 copy at the registry pin, tag `v2.11` (`62da2bef`). |
| hackbench | same clone, `src/hackbench/hackbench.c` | `36e5b4c86aee10fa7422e16c2a3cb218e7b040a364fe52f943ad8d68b167ac3e` | yes (S2-20, `v2.11`) |
| schbench | `VER/schbench-v1.0/README.md`, the registry pin, tag `v1.0` (`ab22f3f8`) | `b05bdfe9ca6f6e620dd31f476ff5fab9b4c2816b5d586b2febf845f6365bf5e4` | yes (9.11 S2-18, `README.md@v1.0`) |
| schbench | `VER/schbench/README.md`, GitHub HEAD `24e32b8e` | `520c9f3a6e0ff737bdf365969b1d5e48d738864e1b8b54ad3489e7807b00460b` | yes (9.11 S2-19) |
| interbench | `VER/interbench/readme`, clone at `e612a65ce941028ddea804e6b45ccde2750720d2` (the registry pin) | `a67f2b8b3d92896e63f2f03e25dc3f59077eb49192fa353d56cbe0da1f7c0b29` | yes (9.11 S2-15; 9.7 S1-01) |
| rt-app | `VER/rt-app/doc/tutorial.txt`, clone at `d6f8be41107642fd6ab41bc1ab3bb01a486fd00e` (the registry pin) | `a3e8823ebae6fda9893327637a48ab195f98206b00ad857a8cc736414d9ee3e7` | yes (9.11 S2-14) |
| rt-app | same clone, `README.in` | `a35dec3593020b2fcb0be7ac17ede7c16c06e2a289623db3e582635ff3d3ad93` | no record hash (`README.in` is not among the registry's or S2-14's files) |
| pcmark10 | `VER/pcmark10/pcmark10-technical-guide-2021-02-11.pdf` (cover "Updated February 11, 2021", 141 pp.) | `d7603a6cb96c78bd22b2721418361ecb92168d785846f241423bd943bb956067` | yes (registry and R05) |
| sysmark30 | https://web.archive.org/web/20250423024404id_/https://bapco.com/wp-content/uploads/2025/04/bapco-sysmark30-user-guide-v1.2.pdf → `V60/sysmark30/sysmark30-user-guide-v1.2-wayback-20250423024404.pdf` (40 pp.). bapco.com itself still answered 403 on 2026-10-09. | `03abdae1e7267ac9d97651e0303cb111a8fd20416d4ba84d30aaecde844766ed` | yes: R05's copy from the 2025-08-21 capture. The registry gives no hash. The copy's SHA-1 (base32 `C5HTWNBJPCNQN4MKXG5WCWPAY6J2IEKB`) equals the Wayback CDX digest of the 2025-04-23 capture. |
| procyon | https://benchmarks.ul.com/procyon → `V60/procyon/procyon.html` (fetched 2026-10-09, HTTP 200) | `b65d770ed436e449e230b925bc40a14bfd22497aa3a86c716959737fc35f4756` | yes: byte-identical to `VER/procyon/procyon.html`. R05's table abbreviates this hash as "b65d7708…4756", which looks like a typo for `b65d770e…`. |

Text extracted from the HTML pages sits beside them in V60 (`*.html.txt`). Text from the PDFs (pdftotext) is in `scratchpad/v60-text/`.

### Quotations

Locators given for the sources are mine. Wherever the guidebook attributes a page, file, commit, date or version, I checked it; that check is reported in the last column.

| vol-02 line | § | Quote begins | Source and locator found | Verdict | Notes |
|---|---|---|---|---|---|
| 2715 | 7.2 | The Game Mode APIs are deprecated in Windows 10, version 1809 and … | gamemode-docs portal, the "Important" note that opens the article body | exact | The guidebook's locator "개념 페이지의 첫머리" (the top of the concept page) is correct. |
| 2721 | 7.2 | Game Mode provides customers with the best possible gaming experience by fully … | portal, body paragraph 3 | exact | |
| 2729 | 7.2 | Game Mode works by default for most Windows games, requiring no action … | portal, body (first sentence of its paragraph) | exact | The guidebook's locator "개념 페이지" (the concept page) is correct. |
| 2735 | 7.2 | By using the expandedResources capability, you can explicitly declare that the game … | portal, body | exact | |
| 2739 | 7.2 | This capability is granted on a per-title basis; contact your account manager … | portal (after the manifest snippet); also the ReleaseExclusiveCpuSets page, Remarks | exact | |
| 2763 | 7.2 | Opts out of CPU exclusivity, giving the app access to all cores, … | ReleaseExclusiveCpuSets page, summary line; also the header page's function list and the portal's "In this section" table | exact | The guidebook's locator "독점 자원을 포기하는 함수의 설명" (the description of the function that gives up exclusive resources) is correct. |
| 2769 | 7.2 | they may opt-out of CPU exclusivity by calling ReleaseExclusiveCpuSets to get access … | portal, body | exact | A mid-sentence fragment: the source sentence begins "Based on the developer's judgment, they may opt-out …" and ends "… as the game." The guidebook's locator "개념 페이지" is correct. |
| 2777 | 7.2 | After this function is called, the app will still have access to … | **ReleaseExclusiveCpuSets page only**, Remarks | exact | It is on none of the four pages in the S2-16 record (portal, header page, HasExpandedResources, GetExpandedResourceExclusiveCpuCount). The portal has only a near paraphrase: "However, the game would still get access to other Game Mode resources, such as increased GPU prioritization." The quote is within the guidebook's own four-page set: line 2711 names one concept page plus three function pages, the same set as the registry's status line. See note A. |
| 2783 | 7.2 | While CPU resources may be revoked if the game exits Game Mode, … | portal, body | exact | |
| 2803 | 7.2 | The app must be in the foreground and have focus before exclusive … | HasExpandedResources, GetExpandedResourceExclusiveCpuCount and ReleaseExclusiveCpuSets pages (Remarks); also a Note on the portal | exact | Line 2805 says the sentence repeats on all three function pages, which is correct. |
| 2809 | 7.2 | Gets the current resource state (that is, whether the app is running … | HasExpandedResources page, summary line; also the header page and the portal table | exact | The guidebook's locator "현재 상태를 알려주는 함수" (the function that reports the current state) is correct. |
| 2811 | 7.2 | This function should be called during each iteration of the game loop … | HasExpandedResources page, Remarks | exact | |
| 2817 | 7.2 | When exclusive resources are revoked, such as when the game loses focus, … | portal, body | exact | The guidebook's locator "개념 페이지" is correct. |
| 2823 | 7.2 | Gets the expected number of exclusive CPU sets that are available to … | GetExpandedResourceExclusiveCpuCount page, summary line; also the header page and the portal table | exact | The guidebook's locator "core 수를 알려주는 함수" (the function that reports the number of cores) is correct. |
| 2825 | 7.2 | This function returns 0 if no exclusive CPU sets are available, or … | GetExpandedResourceExclusiveCpuCount page, Remarks | exact | |
| 2853 | 7.3 | Ananicy (ANother Auto NICe daemon) — is a shell daemon created to … | upstream Ananicy `README.md:22` | exact | Exact once the Markdown link markup around "IO", "CPU" and "pull request" is removed. The passage sits under the README's "# Old description" heading (`:19`). |
| 2869 | 7.3 | All fields except `name` are optional. | upstream `README.md:71` | exact | |
| 2871 | 7.3 | `name` used for match processes by exec bin name | upstream `README.md:73` | exact | |
| 2881 | 7.3 | This translates to: apply the rule to any process named `java`, that … | upstream `README.md:17` (under "## What's new?") | exact | |
| 2910 | 7.3 | Very useful for compilers or other CPU-hungry, non-interactive programs | ananicy-cpp `README.md:231`, the `batch` value of `sched` | exact | A fragment; the source continues ", like compilers for instance." The guidebook's locator (the C++ rewrite's documentation, the description of the batch value) is correct. |
| 2920 | 7.3 | To avoid repeating yourself, you can add types. It must be defined … | ananicy-cpp `README.md:283–284` ("### Types") | exact | |
| 3061 | 7.4 | This is a ananicy-cpp-rules collection for ananicy-cpp maintained by the CachyOS team … | ananicy-rules `README.md:3` @`03ef03fb` | exact | |
| 3063 | 7.4 | You can add your favorite games, apps, and more. Any help would … | ananicy-rules `README.md:22` | exact | |
| 3065 | 7.4 | Please also add the name of the game next to the url, … | ananicy-rules `README.md:37` | exact | |
| 3209 | 8.2 | Hackbench is both a benchmark and a stress test for the Linux … | `src/hackbench/hackbench.8:18–22` | exact | Guidebook locator (line 3203): "원본 저장소 … HEAD `fd45df83`", quotes from the man page and defaults from the source. Correct; see note B for the registry pin. |
| 3215 | 8.2 | Running in process mode with 10 groups using 40 file descriptors each … | `hackbench.8:68` (the EXAMPLES output); printed by `hackbench.c:504` | exact | |
| 3217 | 8.2 | Each sender will pass 100 messages of 100 bytes | `hackbench.8:70`; `hackbench.c:507` | exact | |
| 3223 | 8.2 | Defines how many file descriptors each child should use. Note that the … | `hackbench.8:31–34` (the `-f, --fds` option) | exact | |
| 3235–3237 | 8.2 | - Saturate all the CPUs on the system. Leaving idle CPUs behind … | schbench `README.md:6–8` @`v1.0`; HEAD `:8–11` | exact | The guidebook gives no locator. |
| 3243 | 8.2 | schbench uses messaging threads and worker threads. Workers perform an artificial request … | schbench `README.md:12–13` @`v1.0`; HEAD `:15–18` | exact | |
| 3249–3251 | 8.2 | - Wakeup latency: messaging threads record the time a worker is posted, … | schbench `README.md:17–19` @`v1.0`; HEAD `:22–26` | exact | |
| 3265 | 8.3 | This benchmark application is designed to benchmark interactivity in Linux. | interbench `readme:6` @`e612a65` | exact | The guidebook gives no locator. |
| 3267 | 8.3 | It is designed to emulate the cpu scheduling behaviour of interactive tasks … | interbench `readme:16–17` | exact | |
| 3271 | 8.3 | X: X is simulated as a thread that uses a variable amount … | interbench `readme:40–43` | exact | "X:" is the source's own heading line. |
| 3273 | 8.3 | Audio: Audio is simulated as a thread that tries to run at … | interbench `readme:45–47` | exact | The quote ends at a sentence boundary; the source continues "This behaviour ignores any caching …". |
| 3275 | 8.3 | Video: Video is simulated as a thread that tries to receive cpu … | interbench `readme:53–55` | exact | |
| 3277 | 8.3 | Gaming: The cpu usage behind gaming is not at all interactive, yet … | interbench `readme:59–63` | exact | The quote ends at a sentence boundary; the source continues "This does not accurately emulate a 3d game …". |
| 3287 | 8.3 | 1. The average scheduling latency... 2. The scheduling jitter is represented by … | interbench `readme:116–122` | exact | The "..." elides "(time to requesting cpu till actually getting it) of deadlines met during the test period." |
| 3299 | 8.3 | rt-app is a test application that starts multiple periodic threads in order … | rt-app `README.in:7–8` @`d6f8be4` | exact | Comes from `README.in`, a file the registry's rt-app entry does not list (it names `doc/tutorial.txt` and `src/rt-app.c`). The guidebook gives no locator. |
| 3303 | 8.3 | The json file that describes a workload is made on 3 main … | rt-app `doc/tutorial.txt:25–26` | exact | |
| 3305 | 8.3 | phases: Object. The phases object describes the behavior of the thread. This … | rt-app `doc/tutorial.txt:159–161` | exact | The source line begins with a "* " bullet. |
| 3335 | 8.4 | PCMark 10 uses a modular approach to build relevant tests around common … | PCMark 10 Technical Guide, p. 39 ("Benchmarks, test groups, and workloads") | exact | The guidebook's locator (line 3331: the February 2021 edition, 141 pages) is correct: the cover reads "Updated February 11, 2021" and the PDF has 141 pages. |
| 3352 | 8.4 | • Chromium web browser • Firefox web browser • LibreOffice Writer word … | PCMark 10 Technical Guide, p. 50, "App Start-up" workload | exact | Source context: these four items are the App Start-up workload's application list, not a list for the whole guide. |
| 3376 | 8.4 | The Office Applications scenario models office environment like usage including word processing … | SYSmark 30 User Guide (v1.2 file), p. 34, "Scenarios" | exact | Guidebook locator (line 3366): an Internet Archive copy of BAPCo's URL, captured 2025-04-23; file v1.2; cover 1.1; revision history to 1.2. All correct: the capture `20250423024404` exists, the cover reads "Revision: 1.1", and the history lists 1.0, 1.1 and 1.2. |
| 3380 | 8.4 | The General Productivity scenario models OCR of documents, web browsing, application installation, … | SYSmark 30 User Guide, p. 35 | exact | |
| 3384 | 8.4 | The Photo Editing scenario models editing digital photos (applying filters and creating … | SYSmark 30 User Guide, p. 35 | exact | |
| 3388 | 8.4 | The Advanced Content Creation scenario encodes video with a CPU render and … | SYSmark 30 User Guide, p. 35 | exact | |
| 3392 | 8.4 | The following applications (grouped by scenario) are installed and/or used by SYSmark … | SYSmark 30 User Guide, p. 34, "Applications" | exact | |
| 3425 | 8.4 | The AI Text Generation offers an easier and more compact way for … | benchmarks.ul.com/procyon, the "Procyon® AI Text Generation Benchmark" block | exact | The guidebook's locator (line 3419: the product overview page) is correct for all four Procyon quotes. |
| 3431 | 8.4 | This benchmark contains two tests built with different versions of the Stable … | same page, the "Procyon® AI Image Generation" block (its second paragraph) | exact | |
| 3437 | 8.4 | The workload has been designed around a range of machine vision tasks … | same page, the "Procyon® AI Computer Vision Benchmark 2.0" block (its second sentence) | exact | |
| 3449 | 8.4 | Procyon Essentials is a multitasking and browsing-focused benchmark, covering real-world workloads that … | same page, the "Procyon® Essentials Benchmark" block (from its second sentence) | exact | |

### Other verbatim source text in these chapters (code blocks, not block quotes)

| vol-02 lines | What | Source | Verdict |
|---|---|---|---|
| 2864 | the gcc rule | upstream Ananicy `README.md:68` | exact (byte-identical line) |
| 2878 | the java/freenet rule | upstream Ananicy `README.md:15` | exact |
| 2925 | the `JustCause2.exe` rule | ananicy-rules `README.md:45`; also `00-default/Games/wine_proton/wine_proton_j.rules:207` | exact |
| 2944–2990 | "분류 정의 파일 전체 … 주석까지 그대로" (the whole type-definition file, comments included) | ananicy-rules `00-types.types` @`03ef03fb` | exact: `diff` finds no difference against the whole file. The claim on line 2993 that it holds fifteen definitions is correct. |
| 3071–3074 | the Just Cause 2 example | ananicy-rules `README.md:44–45` | exact |
| 3082–3086 | the Mortal Shell example ("두 번째 예시", the second example) | ananicy-rules `README.md:51–53`, which is the README's example "2." | exact |
| 3229 (inline) | `Time: 0.890` | `hackbench.8:72` | exact |

### Locators stated in the prose, all checked and correct

- **Line 2934, ananicy-rules.** The commit `03ef03fb` is dated 2026-09-08, four days before 2026-09-12.
- **Line 3104, upstream Ananicy.** The current upstream types file (`ananicy.d/00-types.types` @`1e2cc9a6`, SHA-256 `e91e860d…0b37`) uses lowercase types. The capitalised `Heavy_CPU`, `BG_CPUIO` and `LowLatency_RT` are commented out under the heading "### Depricated types ###", which the guidebook translates as "폐기된 분류" (deprecated types).
- **Line 3205, hackbench.** The man page's `.TH` date is "September  19, 2020". The last change to `hackbench.c` in the `fd45df83` history is `cadd661`, 2024-05-22.
- **Line 3221, hackbench.** The source defaults (`hackbench.c:37–40`) are `datasize = 100`, `loops = 100`, `num_groups = 10`, `num_fds = 20`.
- **Line 2793, Game Mode.** It says none of the four pages mentions updates, driver installation or restart notifications. That is correct. Searching all five fetched pages for update, driver, restart and notification finds only a code comment on the portal ("let the game loop update it").

### Notes

- **A. Which four Game Mode pages.** Line 2711 says one concept page plus three function pages, and that every quote comes from those four. The registry's `gamemode-docs` status line says the same ("plus the three … function pages"). The 9.12 search record S2-16 instead lists the portal, the header page and only two function pages; it has no copy of the ReleaseExclusiveCpuSets page. Line 2777 is on that page only. The guidebook's locator is right; the gap is in what S2-16 kept.
- **B. Hackbench pin.** The guidebook cites repository HEAD `fd45df83`, while the registry pins tag `v2.11` (`62da2bef`). `hackbench.8` and `hackbench.c` are byte-identical at both (same SHA-256 as S2-20's `v2.11` copies), so every quote and default holds under either locator. The `fd45df83` clone in VER does not contain commit `62da2bef`.
- **C. rt-app.** Line 3299 comes from `README.in`, which the registry's rt-app entry does not list among its files.

### Seen in passing, outside item 60's scope (no verdict given)

- §7.2's "세 번째 질문" box (lines 2791–2797) and the chapter summary line 3174 still say that Game Mode deferring updates or notifications is unconfirmed. The 9.12 changelog's D45 (2026-10-09) settles this from S2-58, the Xbox Support article read rendered, and hands the doc edits on to 9.15.
- The Procyon overview page lists ten benchmarks, one of them "AI Inference Benchmark for Android". Line 3421 says nine.

### Counts

- exact: **52**
- differs: **0**
- locator wrong: **0**
- not found: **0**

Supplementary verbatim code blocks and inline text: 7 checked, 7 exact.

---

Audit note (9.12 audit, 2026-10-09): the counting rule, the re-graded rows `:1032` and `:1967`, the descriptions of `:949` and `:582`, and reader 3's 52 entries — changelog D97; the copies and their provenance — D98 (A3-01–A3-03).
