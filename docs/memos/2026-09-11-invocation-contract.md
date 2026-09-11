# Invocation contract 안내 — harness가 daemon과 simulator를 실행하는 명령의 모양 (contract 10)

> Status: memo · Created 2026-09-11 · Updated 2026-09-11
> From 인지오 to 인경민, 박이안. data contract 하나가 새로 생겼어요: **harness가 daemon과 simulator를 어떤 명령으로 실행하는가.** 이 memo는 그 명령의 모양과 규칙만 적어요. 두 프로그램의 입출력 파일 형식(config schedule, recognition log, trace)은 하나도 안 바뀌었어요. 규범 문서는 `docs/data-contracts.md` §11이고, 이 memo는 그걸 풀어 쓴 거예요. 급하면 §2와 §3만 읽어도 돼요.

## 1. 한 문단 요약

실험은 harness가 워크로드 파일 하나 × 조건 하나(× 난수를 쓰는 조건이면 seed 하나)마다 **daemon을 한 번, 그다음 simulator를 한 번** 프로세스로 실행하는 식으로 돌아가요. 그래서 두 프로그램이 명령줄에서 무엇을 받고 무엇을 쓰는지가 정해져 있어야 해요. 정한 건 이거예요: **입력은 전부 이름 있는 flag로, 출력도 flag로 받은 경로에, 성공 여부는 exit code로, 그 외의 채널은 없음.** 두 분이 만드는 daemon과 simulator가 아래 모양 그대로 실행되면, harness는 아무 수정 없이 두 프로그램을 돌릴 수 있어요. 지금은 harness 안의 mock 두 개가 이 모양으로 돌아가고 있고, 두 분 프로그램이 오면 그 자리에 그대로 들어가요.

## 2. 명령의 모양

daemon — 워크로드 하나, 조건 하나, (난수 조건이면) seed 하나:

```sh
<daemon 실행 명령> --workload      /abs/dataset/build/coreset-single/c2-p1a.workload.json \
                   --condition     random  --seed 5 \
                   --driver-table  /abs/daemon/driver-table/prior.yaml \
                   --boot-default  /abs/harness/boot-defaults/ostep.json \
                   --out-schedule  /abs/runs/c2-p1a/random-5/schedule.json \
                   --out-log       /abs/runs/c2-p1a/random-5/log.json
```

simulator — 같은 run:

```sh
<simulator 실행 명령> --workload   /abs/dataset/build/coreset-single/c2-p1a.workload.json \
                      --schedule   /abs/runs/c2-p1a/random-5/schedule.json \
                      --out-trace  /abs/runs/c2-p1a/random-5/trace.jsonl.gz
```

`<daemon 실행 명령>`, `<simulator 실행 명령>` 자리는 각자 프로그램의 실행 방법이에요(`python3 daemon.py`든 빌드된 바이너리든). harness는 설정에 적힌 그 명령 뒤에 위 flag들을 붙여서 실행해요. 명령 앞부분에 각자 필요한 옵션을 넣는 건 자유예요 — 예를 들어 simulator의 스레드 수 같은 것. 그건 contract 밖이에요.

## 3. 규칙

1. **한 번의 실행 = run 하나.** 워크로드 파일 하나 × 조건 하나 × (난수를 쓰는 조건이면) seed 하나. 여러 run을 한 프로세스에서 묶어 처리하는 건 없어요. harness가 loop를 돌면서 run마다 한 번씩 실행해요.
2. **flag는 전부 필수, 기본값 없음, 위치 인자 없음.** 빠진 입력은 기본값으로 채우지 말고 실패로 처리해 주세요.
3. **`--workload`는 canonical 워크로드 파일**(`dataset/build/…/*.workload.json`)이에요. 각자 loader가 자기 view만 꺼내 쓰는 건 지금 guide대로예요 — simulator는 `events`만, daemon은 visible projection만(oracle만 `ground_truth`).
4. **`--seed`는 난수를 쓰는 조건에만.** 지금은 `random`뿐이고, 나중에 sampling하는 LLM 조건이 생기면 그것도요. 다른 조건에서는 `--seed`가 오지 않고, 오면 daemon이 거부해 주세요. recognition log의 top-level `seed`는 받은 값 그대로, 없으면 `null`이에요(log contract 그대로).
5. **`--driver-table`은 daemon 실행마다 항상.** `fixed`는 table을 안 쓰지만 flag는 그래도 와요 — 조건마다 명령 모양이 달라지지 않게 하려고요.
6. **`--boot-default`는 작은 JSON 파일이에요.** 모양은 config schema 그대로 `{algorithm, params, batch_bandwidth_cap}`. daemon은 이 내용을 **그대로** schedule의 첫 entry(t = 0, provenance `fallback`)에 복사하고, 이후 `fallback`으로 물러날 때도 이 값을 써요. daemon 안에 boot default를 따로 갖고 있지 않아도 돼요 — 파일이 곧 값이에요. 파일은 `harness/boot-defaults/`에 있고, 지금은 `ostep.json`(OSTEP 예시 MLFQ) 하나예요.
7. **simulator는 조건을 받지 않아요.** trace 헤더의 `condition`은 schedule 파일의 `condition`을 복사하면 돼요.
8. **경로는 전부 절대경로**로 오고, 출력 디렉터리는 harness가 미리 만들어 둬요. 프로그램은 **flag로 받은 출력 파일만** 쓰고 그 외에는 아무것도 남기지 말아 주세요(작업 디렉터리에 의존하지 말고, 임시 파일이 필요하면 시스템 temp에). trace는 출력 경로가 `.gz`로 끝날 때만 gzip으로.
9. **exit code.** 0 = 받은 출력 파일을 전부 썼다. 0이 아니면 실패이고, harness는 디스크에 뭐가 있든 그 run의 출력을 없는 것으로 봐요. 잘못된 입력(t = 0 entry가 없는 schedule, 구현 안 된 조건 등)도 그냥 0이 아닌 code로 끝내 주세요. 출력 파일이 맞는지는 harness가 자기 reader로 직접 확인하니까, 프로그램이 성공을 주장하는 방법은 exit code 하나뿐이에요.
10. **stdout은 무시, stderr는 사람용.** stdout에 뭘 써도 harness는 안 읽어요. stderr는 출력 옆에 로그 파일로 저장만 하고 parsing하지 않아요. 진단 메시지는 마음껏 stderr로.
11. **같은 명령줄 → byte 단위로 같은 출력.** seed까지 같으면 결과가 완전히 같아야 하고, 난수의 출처는 seed뿐이에요. harness의 determinism guard와 cache가 이 하나에 기대요. (두 분 guide의 "deterministic rerun"과 같은 말이에요.)
12. **버전은 프로그램이 알려주지 않아요.** `--version` 같은 건 없어요. harness가 자기 설정에 "이 명령 = 이 버전(예: git commit)"을 적어 두고 cache key에 넣어요. trace 헤더의 `sim` 문자열은 그것과 대조만 해요.

## 4. 각자에게

- **인경민 (simulator):** flag 세 개 — `--workload`, `--schedule`, `--out-trace`. 조건 flag는 없고, `condition`은 schedule에서 복사. 헤더의 `sim`에는 지금처럼 버전이나 commit을 넣어 주세요. 그 외 simulator 자체 옵션은 실행 명령 앞부분에 두면 돼요.
- **박이안 (daemon):** flag 다섯 개 + 조건부 하나 — `--workload`, `--condition`, `--driver-table`, `--boot-default`, `--out-schedule`, `--out-log`, 그리고 난수 조건에만 `--seed`. 조건 이름은 daemon guide §4의 표 그대로(`fixed`, `random`, `whitelist`, `llm_vocab`, `llm_algo`, `llm_full`, `oracle`). boot default는 파일에서 읽어 첫 entry에 복사.

## 5. 참고

- 규범 문서: `docs/data-contracts.md` §11 (contract 10). 이 memo와 다른 점이 있으면 그쪽이 맞아요.
- 실제로 이 모양으로 돌아가는 예시: `harness/tools/tests/mocks/mock_daemon.py`, `harness/tools/tests/mocks/mock_simulator.py`. 두 분 프로그램이 오면 버릴 test double이지만, "이 flag로 실행되면 이 파일이 나온다"를 눈으로 확인하기엔 충분해요. 실행 방법은 각 파일 맨 위 docstring에 있어요.
- boot default 파일과 schema: `harness/boot-defaults/ostep.json`, `harness/boot-defaults/schema/boot-default.schema.json`.
