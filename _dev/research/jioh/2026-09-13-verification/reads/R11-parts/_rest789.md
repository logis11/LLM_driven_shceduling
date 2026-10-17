# R11 part: C-plain-7, C-plain-8, C-plain-9

Local root: `_dev/research/jioh/2026-09-13-verification/sources/` (abbreviated `S/`). All retrievals 2026-09-13.

---

## C-plain-7 — public traces of desktop process activity with process names; process-identity fields in Azure and Google cluster traces

The topic covers three things: (A) Google cluster traces, (B) Azure traces, (C) desktop process-activity traces. Each gets its own answer below.

### C-plain-7A — Google cluster traces (2009 v1, 2011 v2.1, 2019 v3)

**(a) Verbatim**

`cluster-data/TraceVersion1.md` (commit 48b1244):
> The data have been anonymized in several ways: there are no task or job names, just numeric identifiers; timestamps are relative to the start of data collection; the consumption of CPU and memory is obscured using a linear transformation.

`cluster-data/ClusterData2019.md`:
> The 2019 traces focus on resource requests and usage, and contain no information about end users, their data, or access patterns to storage systems and other services.

`cluster-data/clusterdata_trace_format_v3.proto`, lines 199–204 (CollectionEvent):
```
  // The user who runs the collection
  optional string user = 9;
  // Obfuscated name of the collection.
  optional string collection_name = 10;
  // Obfuscated logical name of the collection.
  optional string collection_logical_name = 11;
```

Google cluster-usage traces v3 doc (PDF p. 3–4, "User and collection names"):
> User and collection names are hashed and provided as opaque base64-encoded strings that can be tested for equality.

> Usernames in this trace represent Google engineers and services. Production jobs run by the same username are likely to be part of the same external or internal service.

Same doc, PDF p. 9 (collection events field list):
> user – the obfuscated name of the “user” (person or system) that submitted the collection

> collection_name – a hash of the original complete collection name

> collection_logical_name – a hash of the parts of the collection name that reflect its purpose, and excluding things like sequence numbers or UIDs

2011 v2.1 schema doc, PDF p. 3 ("User and job names"):
> User and job names are hashed and provided as opaque base64-encoded strings that can be tested for equality.

2011 v2.1 schema doc, PDF p. 5:
> Usually all tasks within a job execute exactly the same binary with the same options and resource request.

`clusterdata-2011-2/schema.csv`, rows 6, 8, 9, 16:
```
job_events/part-?????-of-?????.csv.gz,5,user,STRING_HASH,NO
job_events/part-?????-of-?????.csv.gz,7,job name,STRING_HASH,NO
job_events/part-?????-of-?????.csv.gz,8,logical job name,STRING_HASH,NO
task_events/part-?????-of-?????.csv.gz,7,user,STRING_HASH,NO
```

**(b) Locators:** files and lines as given above, at google/cluster-data commit 48b12446; the v3 doc PDF (Drive id 10r6cnJ5…) pp. 3–4 and 9; the v2.1 doc PDF (Drive id 0B5g07T…) pp. 3 and 5; the GCS schema.csv.

**(c) Reading:** In Google's traces, workload identity is recorded per job (2011) or per collection (2019): a hashed user, a hashed job or collection name, and a hashed "logical" name. Tasks and instances are identified by numeric IDs. No trace has a process-name or binary-name field. The 2009 v1 trace has only numeric job and task IDs. The 2011 doc says tasks in a job usually run the same binary, but it does not name that binary. The 2019 v3 schema was checked in the proto and the v3 doc. The 2019 power traces and ETA exploration traces in the repo were not checked.

**(d) Verdict: FOUND.** The identity fields are hashed user, hashed job or collection name and hashed logical name, plus numeric IDs. There is no process-name field.

### C-plain-7B — Azure public traces

**(a) Verbatim**

`AzurePublicDatasetV2.md`, "### Schema" (lines 22–42). V1 has the same fields 1–12 at lines 21–35:
```
1.	Encrypted subscription id
2.	Encrypted deployment id 
...
6.	Encrypted VM id
...
12.	VM category
```

`AzureFunctionsDataset2019.md`, lines 38–47:
> | HashOwner | unique id of the application owner <sup>1</sup> |
> | HashApp | unique id for application name <sup>1</sup> |
> | HashFunction | unique id for the function name within the app <sup>1</sup>|

> 1. All ids are hashed using HMAC-SHA256 with secret salts. Each column uses a different salt.

`AzureFunctionsInvocationTrace2021.md`, lines 27–34:
> - app: application id (encrypted)
> - func: function id (encrypted), and unique only within an application

> In Azure Functions, the unit of deployment is called an application, and an application has one or more functions. For example, an application could be a binary file with one or more entry points.

`AzureTracesForPacking2020.md`, lines 36–43:
> | vmId | unique id of the vm request<sup>1</sup> |
> | tenantId | unique id for the owner of a group of requests<sup>1</sup> |
> | vmTypeId | requested VM type<sup>1</sup>|

> 1. All ids are anonymized. These are consistent only within a single sqlite file.

`AzureFunctionsBlobDataset2020.md`, lines 38–48:
> | AnonAppName | Unique id for the application<sup>1</sup> |

> 1. Ids are hashed using HMAC-SHA512 with secret salts and cropped.

`AzureLLMInferenceDataset2023.md`, lines 25–30:
> | TIMESTAMP | Invocation time |
> | ContextTokens | Number of context tokens |
> | GeneratedTokens | Number of generated  tokens |

**(b) Locators:** Azure/AzurePublicDataset commit 207bed67. Files and line ranges are given above.

**(c) Reading:** The Azure VM traces (2017 V1, 2019 V2) identify workloads by encrypted subscription, deployment and VM IDs, plus a "VM category". The Functions traces use hashed or encrypted owner, application and function IDs. The packing trace uses anonymized VM, tenant and VM-type IDs. The LLM inference trace has no identity field. None of these has a process name or executable name. The Functions doc says only that an app "could be a binary file"; the binary's name is hashed. The VM category values are not defined in the V1 or V2 md files; the docs point to the SOSP'17 paper, which was not checked. The Azure LMM 2025, LLM 2024, GreenSKU and VM-noise docs were grepped for "process" and "name" and have no process-identity field.

**(d) Verdict: FOUND.** The identity fields are encrypted or hashed IDs only. There is no process-name field.

### C-plain-7C — public traces of desktop process activity with process names

**(a) Verbatim**

LANL "Comprehensive, Multi-Source Cyber-Security Events" page (https://csr.lanl.gov/data/cyber1/), "proc.txt.gz":
> This data represents process start and stop events collected from individual Windows-based desktop computers and servers. Each event is on a separate line in the form of “time,user@domain,computer,process name,start/end” and represents a process event at the given time.

Same page:
> All other users, computers, process, ports, times, and other details were de-identified as a unified set across all the data elements (e.g. U1 is the same U1 in all of the data).

Example rows on the page:
```
1,C553$@DOM1,C553,P16,Start
1,C553$@DOM1,C553,P25,End
```

LANL "Unified Host and Network Data Set" page (https://csr.lanl.gov/data/2017/), field table:
> ProcessName
> The process executable name, for authentication events this is the process that processed the authentication event. ProcessNames may include the file type extensions (i.e exe).

Turcotte, Kent & Hash, arXiv:1708.07518v1, PDF p. 10:
> When de-identifying the process events, only the base process name was de-identified and the extension was left as is.

Same, PDF p. 11:
> For the process names, dates, version numbers, operating systems and hexadecimal strings were removed where possible so that processes run on different operating systems or with different versions would map to the same process name.

DARPA OpTC `README.md` (FiveDirections/OpTC-data commit 5b10860):
> Each Windows 10 endpoint is equipped with an endpoint sensor that monitors host events, packs them into JSON records, and sends them to Kafka.

> The evaluation started with a period of benign record generation, followed by the injection of malware by a red team. Benign traffic ran continuously during red team activity.

OpTC `ecar.md`:
> * When process details are present, an "image_path" entry in Event.properties will also typically be present

Example eCAR object in `ecar.md`:
```
  "object": "PROCESS",
  "action": "CREATE",
...
    "image_path": "\\Device\\HarddiskVolume1\\cygwin64\\bin\\bash.exe",
```

BEHACOM, Data in Brief 31 (2020) 105767, PMC7270191, Table 5 "Application usage statistics features description":
> current_app
> Application executable name in foreground when the vector was generated.

> penultimate_app
> Penultimate application executable name in foreground during the time window.

> active_apps_average
> Average number of applications active during the time window.

Same article, §2 (scenario):
> The proposed scenario comprises twelve different individuals interacting for fifty-five consecutive days with their personal computers in their own way and without restrictions.

**(b) Locators:** as given above. The LANL pages are HTML with no version. The Turcotte paper is arXiv 1708.07518v1, PDF pp. 10–11. OpTC is at commit 5b10860, files README.md and ecar.md. BEHACOM is PMC7270191, Table 5 and §2.

**(c) Reading:**
- **LANL 2015 (cyber1):** public per-computer process start and stop events from Windows desktops and servers. The "process name" field is de-identified to tokens such as `P16`, so no real names are published.
- **LANL 2017 (Unified Host and Network):** public Windows host events (4688/4689) with `ProcessName` and `ParentProcessName`. The base name is de-identified and only the file extension is kept, so again no real names. The raw data sits behind an email form: the HEAD request for `wls_day-01.bz2` returned 401, and I did not submit the form, so the data rows were not inspected.
- **DARPA OpTC:** publishes real executable paths (`image_path`) for PROCESS CREATE events on about 500 Windows 10 hosts. These are hosts in an instrumented enterprise exercise with red-team activity. The README does not say that the benign activity came from real human users. The data itself is on Google Drive and was not downloaded.
- **BEHACOM:** from real personal use by 12 users on Windows and Linux. It publishes the foreground application's executable name (current and penultimate) per one-minute window, plus only a *count* of active applications. Background process names are not released. The CSV files on Mendeley Data were not downloaded.

Search method: WebSearch queries "public dataset desktop computer process names application usage logs Windows users trace released researchers", "OpTC dataset FiveDirections process create image_path schema github", and "dataset "process names" "window titles" desktop users logged released open data computer usage study". I then read primary docs for LANL (2015, 2017), OpTC and BEHACOM. This is not an exhaustive survey. Loghub, GroundCUA and a UIC HCI log set appeared in search results but were not checked.

**(d) Verdict: PARTIAL.** Public traces with a process-name *field* exist. In LANL the names are de-identified. OpTC has real executable paths, but from an instrumented exercise that is not described as natural desktop use. BEHACOM from natural use gives only the foreground executable name per minute. No dataset checked publishes the real names of all processes from natural desktop use.

---

## C-plain-8 — what Phoronix Test Suite and UnixBench measure; whether mobile app-usage datasets record concurrent foreground apps

### C-plain-8A — Phoronix Test Suite

**(a) Verbatim** (`documentation/phoronix-test-suite.md` at tag v10.8.4, "Overview"):
> The Phoronix Test Suite client itself is an automated test framework for providing seamless execution of test profiles and test suites. There are more than 650 tests available by default, which are transparently available via OpenBenchmarking.org integration. Of these default test profiles there is a range of sub-systems that can be tested and a range of hardware from mobile devices to desktops and workstations/servers.

> Test profiles can produce a quantitative result or other qualitative/abstract results like image quality comparisons and pass/fail. Using Phoronix Test Suite modules, other data can also be automatically collected at run-time such as the system power consumption, disk usage, and other software/hardware sensors.

Same file, line 100 (`stress-run`):
> This option will run the passed tests/suites in the multi-process stress-testing mode. The stress-run mode will not produce a result file but is rather intended for running multiple test profiles concurrently to stress / burn-in the system. The number of tests to run concurrently can be toggled via the PTS_CONCURRENT_TEST_RUNS environment variable and by default is set to a value of 2.

`README.md` at v10.8.4:
> This framework is designed to be an extensible architecture so that new test profiles and suites can be easily added to represent performance benchmarks, unit tests, and other quantitative and qualitative (e.g. image quality comparison and pass/fail) measurements.

**(b) Locator:** phoronix-test-suite tag v10.8.4 (commit f0365737): `documentation/phoronix-test-suite.md` "Getting Started > Overview" and line 100; `README.md` paragraph 3.

**(c) Reading:** PTS is a framework, not a single benchmark. What it measures depends on the test profile chosen from more than 650 profiles, covering many subsystems. Profiles report a quantitative result, or an image-quality or pass/fail result, and modules can also collect sensor data. By default the `run` and `benchmark` commands run tests one after another. `stress-run` runs several profiles at the same time (default 2) but writes no result file. Caveat: the doc is v10.8.4 from 2022, the latest version tag in `git ls-remote`.

**(d) Verdict: FOUND.**

### C-plain-8B — UnixBench (byte-unixbench)

**(a) Verbatim** (`README.md`, commit e949d44):
> The purpose of UnixBench is to provide a basic indicator of the performance of a Unix-like system; hence, multiple tests are used to test various aspects of the system's performance. These test results are then compared to the scores from a baseline system to produce an index value, which is generally easier to handle than the raw scores. The entire set of index values is then combined to make an overall index for the system.

> Multi-CPU systems are handled. If your system has multiple CPUs, the default behaviour is to run the selected tests twice -- once with one copy of each test program running at a time, and once with N copies, where N is the number of CPUs.

> Do be aware that this is a system benchmark, not a CPU, RAM or disk benchmark.

`UnixBench/USAGE`, "Tests" (system category, excerpt):
```
    dhry2reg         Dhrystone 2 using register variables
    whetstone-double Double-Precision Whetstone
    syscall          System Call Overhead
    pipe             Pipe Throughput
    context1         Pipe-based Context Switching
    spawn            Process Creation
    execl            Execl Throughput
    fstime-w         File Write 1024 bufsize 2000 maxblocks
...
    shell1           Shell Scripts (1 concurrent) (runs "looper 60 multi.sh 1")
    shell8           Shell Scripts (8 concurrent) (runs "looper 60 multi.sh 8")
```

`UnixBench/USAGE`, "Running the Tests":
> However, if using a windowing system, you may want to switch to a minimal window setup (for example, log in to a "twm" session), so that randomly-churning background processes don't randomise the results too much.

**(b) Locator:** kdlucas/byte-unixbench commit e949d44: `README.md` (intro and "Included Tests"); `UnixBench/USAGE` ("Running the Tests", "Tests").

**(c) Reading:** UnixBench measures raw throughput of synthetic tests: integer and floating-point compute (Dhrystone, Whetstone), syscall overhead, pipe throughput, context switching, process creation, execl, file I/O, shell-script loops, and 2D/3D graphics. It normalises the scores against a baseline machine (SPARCstation 20-61 per the README) into index values. It runs 1 copy and N copies of each test. It is not an interactive-latency benchmark, and the USAGE file advises reducing background processes.

**(d) Verdict: FOUND.**

### C-plain-8C — do mobile app-usage datasets record concurrent foreground apps? (per dataset)

**LSApp** — `README.md` (commit c001713), "Format":
> * app_name: name of the app.
> * event_type: type of the event recorded. Possible values: Opened, Closed, User Interaction, Broken

Reading: the data is an event log (Opened, Closed, User Interaction, Broken) per user and session. The README does not say whether two apps can be open at once, and there is no foreground or background field. **NOT FOUND** (searched the README for foreground, concurrent, background and multi-window; none present).

**Tsinghua App Usage** — dataset page, "Dataset information":
> In this App usage dataset, each entry contains an anonymized User identification, timestamps of HTTP request or response, the length of the packet, the domain visited and the user-agent field. We identify Apps from the networking metadata by adopting SAMPLES

File description:
> App_Usage_Trace.txt
> User ID||Timestamp(Second) ||Location (base station ID)||Used App

Reading: apps are inferred from network traffic, so there is no notion of a foreground app. **PREMISE NOT IN SOURCE**: the dataset records network-derived "Used App" per timestamp, not foreground state.

**LiveLab** (Rice, iPhone 3GS, 2010–2011) — traces page, `appusage.sql`:
> appusage.sql: applications run by users (event / built-in logfile driven)

> duration: duration for which the application was running in seconds. Note that turning the screen off effectively exits the application

Reading: each row is an app run with a start time and duration. The page does not say whether runs can overlap or whether a row means foreground. **NOT FOUND**.

**Carat Top 1000 Users Long-Term App Usage Dataset** — data-sharing page:
> apps (app usage data, see below)
> Where app usage is a list of JSON objects with the following attributes:
> processName (App Android package name)
> priority (background, foreground, etc, see Android documentation)

> The app collected application usage and battery level information every time the battery level changed by 1%, as allowed by the mobile operating system.

Reading: each sample (taken at each 1% battery change) lists several running apps, each with an Android importance label that includes "foreground". The page does not say whether more than one app can carry "foreground" in the same sample, or what "foreground" means beyond the Android documentation. **PARTIAL**: a per-sample list of apps with foreground/background priority exists, but concurrent foreground apps are not documented. The zip (password given on the page) was not downloaded.

**Device Analyzer** (Cambridge) — **COPY UNREACHABLE**. https://deviceanalyzer.cl.cam.ac.uk/ and http://deviceanalyzer.cl.cam.ac.uk/ timed out (curl error 28, 30 s and 60 s). https://www.cl.cam.ac.uk/research/dtg/deviceanalyzer/ returned 404.

Not checked: Nokia Mobile Data Challenge (MDC), which is access-controlled.

**Overall C-plain-8C verdict: NOT FOUND.** None of the four reachable datasets documents concurrent foreground apps. Carat is the closest (PARTIAL).

---

## C-plain-9 — peer-reviewed papers citing Phoronix Test Suite / UnixBench by repository URL

### UnixBench (github.com/kdlucas/byte-unixbench)

**Example 1 — Lock-in-Pop, USENIX ATC '17** (Yiwen Li, Brendan Dolan-Gavitt, Sam Weber, Justin Cappos; *Proceedings of the 2017 USENIX Annual Technical Conference*, ISBN 978-1-931971-38-6). The USENIX PDF is byte-identical to the NYU-hosted copy (checked with `cmp`).

PDF p. 12 (body):
> Graphene [43] also shows an overhead ranging from 1.4x to 2x when running applications such as the Apache web server and the Unixbench suite [44].

PDF p. 13 (references):
> [44] Unixbench. https://github.com/kdlucas/byte-unixbench. Accessed September 2016.

**Example 2 — The Koala Benchmarks for the Shell, USENIX ATC '25** (Lamprou et al.; *Proceedings of the 2025 USENIX Annual Technical Conference*, ISBN 978-1-939133-48-9).

PDF p. 13 (body):
> Similarly, zsh-bench [68], the Oils benchmarks [8], and UnixBench [47] focus on isolated performance characteristics—e.g., interactive shell behavior or command invocation times.

PDF p. 15 (references):
> [47] Kirk D. Lucas and Contributors. UnixBench: The BYTE UNIX Benchmark Suite. https://github.com/kdlucas/byte-unixbench, 2012. Accessed: 2025-04-28.

Verdict (UnixBench): **FOUND**, two peer-reviewed USENIX ATC papers.

### Phoronix Test Suite (github.com/phoronix-test-suite/phoronix-test-suite)

**Example 3 — Popescu & Lopes, "Exploiting Undefined Behavior in C/C++ Programs for Optimization: A Study on the Performance Impact"**, *Proc. ACM Program. Lang.* 9 (PLDI), Article 161, 2025. Copy: author-hosted PDF with the PACMPL running heads "161:n" and a CC-BY 4.0 notice. The ACM DL PDF returned HTTP 403, so I could not compare it with the publisher copy.

PDF p. 6 (printed 161:6), body and footnote 4:
> All the benchmarks we used were from the Phoronix Test Suite,4 with the exception of Z3 for which we created new performance tests using files from the SMT library.5

> 4https://github.com/phoronix-test-suite/phoronix-test-suite/

**Example 4 — Gamess & Hernandez, "Performance Evaluation of Different Raspberry Pi Models for a Broad Spectrum of Interests"**, *IJACSA* 13(2), 2022. The repository URL appears in the body (Fig. 21 listing), but the reference list cites the website instead.

PDF p. 8 (printed p. 826):
> In Line 02, PTS was cloned from GitHub.

> 02: git clone https://github.com/phoronix-test-suite/\
> phoronix-test-suite.git

PDF p. 11 (printed p. 829, references):
> [38] “Phoronix Test Suite: Open-Source, Automated Benchmarking.” https://www.phoronix-test-suite.com.

Not counted as peer-reviewed (arXiv copies carry no venue statement):
- arXiv 2305.04641, "The Cure is in the Cause: A Filesystem for Container Debloating", PDF p. 14 ref: "[38] Phoronix. Phoronix test suite 10.8.4. https://github.com/phoronix-test-suite/ phoronix-test-suite, 2023. [Online; accessed 2023-04-30]."
- arXiv 2401.10582, "Exploiting Kubernetes' Image Pull Implementation to Deny Node Availability", PDF p. 14 ref: "[18] Phoronix Media, “Phoronix Test Suite,” Sep. 2023, original-date: 2014-01-12T04:56:38Z. [Online]. Available: https://github.com/ phoronix-test-suite/phoronix-test-suite".

Search method: WebSearch for the quoted repo URLs (with usenix and proceedings terms), and an OpenAlex full-text search for `"github.com/phoronix-test-suite"` (13 hits, used only for discovery). The OpenAlex search for `"github.com/kdlucas/byte-unixbench"` was rate-limited (HTTP 429, twice). Each paper listed was verified in its downloaded PDF. The PACMPL OOPSLA 2023 paper "Building Dynamic System Call Sandbox with Partial Order Analysis" (doi 10.1145/3622842) was also an OpenAlex hit, but the ACM PDF returned 403 and it was not verified. The TUNA EuroSys'25 paper (NSF PAR and arXiv copies) was checked and contains no "Phoronix" string.

Verdict (Phoronix Test Suite): **FOUND** for the PACMPL 2025 paper (footnote URL; caveat: author-hosted copy). **PARTIAL** for IJACSA 2022 (URL in body text only).

**Overall C-plain-9 verdict: FOUND.**

---

## Verdict summary (this part)

- C-plain-7A Google traces: FOUND (hashed user, job/collection name and logical name; numeric IDs; no process names)
- C-plain-7B Azure traces: FOUND (encrypted or hashed subscription, deployment, VM, owner, app and function IDs; no process names)
- C-plain-7C desktop process traces with names: PARTIAL (LANL de-identified; OpTC real image paths but from an exercise; BEHACOM foreground executable only)
- C-plain-8A PTS: FOUND
- C-plain-8B UnixBench: FOUND
- C-plain-8C mobile concurrent foreground: NOT FOUND overall. LSApp NOT FOUND; Tsinghua PREMISE NOT IN SOURCE; LiveLab NOT FOUND; Carat PARTIAL; Device Analyzer COPY UNREACHABLE.
- C-plain-9 papers citing by repo URL: FOUND (UnixBench: ATC'17, ATC'25; PTS: PACMPL/PLDI'25; IJACSA'22 partial)

Unreachable or blocked URLs:
- https://deviceanalyzer.cl.cam.ac.uk/ (timeout), http://deviceanalyzer.cl.cam.ac.uk/ (timeout), https://www.cl.cam.ac.uk/research/dtg/deviceanalyzer/ (404)
- https://csr.lanl.gov/data-fence//unified-host-network-dataset-2017/wls/wls_day-01.bz2 (401; form not submitted)
- https://dl.acm.org/doi/pdf/10.1145/3729260 and https://dl.acm.org/doi/pdf/10.1145/3622842 (403)
- https://www.mdpi.com/2079-9292/13/23/4838/pdf (403)
- https://dl.acm.org/doi/pdf/10.1145/3689031.3717480 and the MSR TUNA PDF (403)
- OpenAlex full-text search for byte-unixbench (429)
