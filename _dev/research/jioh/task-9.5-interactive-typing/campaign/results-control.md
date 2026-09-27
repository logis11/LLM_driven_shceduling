# Untraced control — campaign

## web-browser (`chrome`)

6 jobs (3 traced untraced, 3 untraced traced); builds: Google Chrome 153.0.8010.52 (1, 2, 3, 4, 5, 6).
32 intervals read; at 95 % chance alone gives about 1.6 differences; differences found: 9 (idle gpu/Chrome_ChildIOT run mean (ms), idle gpu/VizCompositorTh run mean (ms), idle gpu/VizCompositorTh wakes/s, idle utility/HangWatcher run mean (ms), idle utility/HangWatcher wakes/s, op Chrome_IOThread run mean (ms), op Chrome_IOThread wakes/s, op chrome run mean (ms), op gpu/Chrome_ChildIOT run mean (ms)).

| value | traced median | untraced median | medians' ratio | per-job mean | 95 % interval | reading | by order | n | exited (CPU, wakes) | left out (CPU, wakes) | in the operation windows (CPU, wakes) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| driven per-input run (ms) | 1.2752 | 1.8792 | 1.4737 | 1.2281 | 0.5657–1.8905 | not resolved | traced first 1.1748; untraced first 1.2814 | 6 | — | — | — |
| idle chrome run mean (ms) | 0.1711 | 0.1589 | 0.9288 | 0.9633 | 0.9008–1.0259 | not resolved | traced first 0.9533; untraced first 0.9733 | 6 | 0, 0 | 0, 0 | — |
| idle chrome wakes/s | 0.7913 | 0.7891 | 0.9972 | 0.9974 | 0.9361–1.0588 | not resolved | traced first 0.9498; untraced first 1.0451 | 6 | 0, 0 | 0, 0 | — |
| idle gpu/Chrome_ChildIOT run mean (ms) | 0.0316 | 0.0273 | 0.8634 | 0.8634 | 0.8497–0.8772 | difference | traced first 0.8567; untraced first 0.8701 | 6 | 0, 0 | 0, 0 | — |
| idle gpu/Chrome_ChildIOT wakes/s | 7.5429 | 7.4418 | 0.9866 | 0.9911 | 0.9752–1.007 | not resolved | traced first 1.0029; untraced first 0.9793 | 6 | 0, 0 | 0, 0 | — |
| idle gpu/VizCompositorTh run mean (ms) | 0.0779 | 0.075 | 0.9622 | 0.9537 | 0.9291–0.9783 | difference | traced first 0.9399; untraced first 0.9675 | 6 | 0, 0 | 0, 0 | — |
| idle gpu/VizCompositorTh wakes/s | 11.7826 | 11.5974 | 0.9843 | 0.9767 | 0.96–0.9933 | difference | traced first 0.9827; untraced first 0.9707 | 6 | 0, 0 | 0, 0 | — |
| idle residual run mean (ms) | 0.2038 | 0.1223 | 0.6002 | 0.8506 | 0.4122–1.2889 | not resolved | traced first 0.7718; untraced first 0.9293 | 6 | 0.003, 0.002 | 0.312, 0.001 | — |
| idle residual wakes/s | 1.0448 | 1.0341 | 0.9897 | 0.9855 | 0.8375–1.1336 | not resolved | traced first 0.8664; untraced first 1.1047 | 6 | 0.003, 0.002 | 0.312, 0.001 | — |
| idle utility/HangWatcher run mean (ms) | 0.0429 | 0.0405 | 0.9429 | 0.9364 | 0.9109–0.9618 | difference | traced first 0.9271; untraced first 0.9457 | 6 | 0, 0 | 0, 0 | — |
| idle utility/HangWatcher wakes/s | 0.2993 | 0.3 | 1.0025 | 1.0026 | 1.0022–1.0029 | difference | traced first 1.0025; untraced first 1.0026 | 6 | 0, 0 | 0, 0 | — |
| idle utility/chrome run mean (ms) | 0.0937 | 0.0896 | 0.9563 | 0.9736 | 0.938–1.0092 | not resolved | traced first 0.949; untraced first 0.9982 | 6 | 0.002, 0 | 0, 0 | — |
| idle utility/chrome wakes/s | 0.8129 | 0.7999 | 0.9839 | 0.9937 | 0.9773–1.0101 | not resolved | traced first 0.9937; untraced first 0.9937 | 6 | 0.002, 0 | 0, 0 | — |
| op Chrome_IOThread run mean (ms) | 0.0252 | 0.0221 | 0.8759 | 0.8607 | 0.8184–0.9029 | difference | traced first 0.8269; untraced first 0.8944 | 6 | 0, 0 | — | 0.886, 0.903 |
| op Chrome_IOThread wakes/s | 27.8892 | 28.9893 | 1.0394 | 1.0368 | 1.014–1.0597 | difference | traced first 1.0518; untraced first 1.0219 | 6 | 0, 0 | — | 0.886, 0.903 |
| op CompositorTileW run mean (ms) | 0.0943 | 0.0935 | 0.9922 | 0.9731 | 0.9403–1.006 | not resolved | traced first 0.9659; untraced first 0.9804 | 6 | 0, 0 | — | 0.93, 0.901 |
| op CompositorTileW wakes/s | 3.2161 | 3.2642 | 1.015 | 1.0058 | 0.9823–1.0292 | not resolved | traced first 1.0004; untraced first 1.0111 | 6 | 0, 0 | — | 0.93, 0.901 |
| op ThreadPoolForeg run mean (ms) | 0.0391 | 0.0352 | 0.8985 | 0.9349 | 0.8525–1.0173 | not resolved | traced first 1.0; untraced first 0.8698 | 6 | 0, 0 | — | 0.543, 0.664 |
| op ThreadPoolForeg wakes/s | 9.8894 | 9.8265 | 0.9936 | 1.0105 | 0.9763–1.0446 | not resolved | traced first 1.0076; untraced first 1.0133 | 6 | 0, 0 | — | 0.543, 0.664 |
| op chrome run mean (ms) | 0.2338 | 0.2251 | 0.9626 | 0.9634 | 0.9333–0.9934 | difference | traced first 0.9585; untraced first 0.9683 | 6 | 0, 0 | — | 0.776, 0.596 |
| op chrome wakes/s | 18.946 | 18.9299 | 0.9991 | 1.006 | 0.974–1.038 | not resolved | traced first 1.0264; untraced first 0.9856 | 6 | 0, 0 | — | 0.776, 0.596 |
| op gpu/Chrome_ChildIOT run mean (ms) | 0.0313 | 0.0285 | 0.9113 | 0.8895 | 0.8589–0.9201 | difference | traced first 0.8835; untraced first 0.8954 | 6 | 0, 0 | — | 0.822, 0.848 |
| op gpu/Chrome_ChildIOT wakes/s | 7.5562 | 7.6506 | 1.0125 | 1.0098 | 0.9938–1.0258 | not resolved | traced first 1.0026; untraced first 1.017 | 6 | 0, 0 | — | 0.822, 0.848 |
| op gpu/VizCompositorTh run mean (ms) | 0.3586 | 0.3514 | 0.98 | 0.9807 | 0.9386–1.0228 | not resolved | traced first 0.9964; untraced first 0.965 | 6 | 0, 0 | — | 0.875, 0.818 |
| op gpu/VizCompositorTh wakes/s | 8.0823 | 8.1382 | 1.0069 | 0.9979 | 0.9746–1.0213 | not resolved | traced first 0.9854; untraced first 1.0105 | 6 | 0, 0 | — | 0.875, 0.818 |
| op operation duration mean (ms) | 481.867 | 480.028 | 0.9962 | 0.9884 | 0.9591–1.0178 | not resolved | traced first 0.9789; untraced first 0.9979 | 6 | — | — | — |
| op residual run mean (ms) | 0.1007 | 0.0982 | 0.9755 | 1.019 | 0.8359–1.2022 | not resolved | traced first 1.1089; untraced first 0.9292 | 6 | 0.001, 0.001 | — | 0.377, 0.517 |
| op residual wakes/s | 5.1988 | 5.1202 | 0.9849 | 0.9914 | 0.9762–1.0065 | not resolved | traced first 1.0009; untraced first 0.9819 | 6 | 0.001, 0.001 | — | 0.377, 0.517 |
| op utility/Chrome_ChildIOT run mean (ms) | 0.1375 | 0.1322 | 0.9611 | 0.9505 | 0.8785–1.0224 | not resolved | traced first 0.9001; untraced first 1.0009 | 6 | 0, 0 | — | 0.963, 0.946 |
| op utility/Chrome_ChildIOT wakes/s | 3.8205 | 3.8749 | 1.0142 | 1.0112 | 0.9444–1.0779 | not resolved | traced first 1.0561; untraced first 0.9662 | 6 | 0, 0 | — | 0.963, 0.946 |
| op utility/ThreadPoolForeg run mean (ms) | 0.0322 | 0.0317 | 0.9849 | 0.9618 | 0.8069–1.1167 | not resolved | traced first 0.8339; untraced first 1.0897 | 6 | 0, 0 | — | 0.869, 0.9 |
| op utility/ThreadPoolForeg wakes/s | 1.4236 | 1.4495 | 1.0182 | 1.0834 | 0.5448–1.622 | not resolved | traced first 0.6181; untraced first 1.5487 | 6 | 0, 0 | — | 0.869, 0.9 |

- job 1: the screenshots after its two preludes differ in (21, 164, 22, 179)
- job 2: the screenshots after its two preludes differ in (21, 164, 22, 179)
- job 3: the screenshots after its two preludes differ in (21, 164, 22, 179)
- job 4: the screenshots after its two preludes differ in (21, 164, 22, 179)
- job 5: the screenshots after its two preludes differ in (21, 164, 22, 179)
- job 6: the screenshots after its two preludes differ in (21, 164, 22, 179)

The operation phase's second page-load pass wakes the network service's foreground pool (`utility/ThreadPoolForeg`) about 40 % less than the first, which keeps that component's ratio from resolving.

The traced runs against the carried pool (decision 17): largest |z| 6.31 over 45 values; only in the carried pool: input_run mean, 136M (ms).

## code-editor (`code`)

6 jobs (3 traced untraced, 3 untraced traced); builds: 1.138.0 (1, 2, 3, 4, 5, 6).
19 intervals read; at 95 % chance alone gives about 1.0 differences; differences found: 3 (idle gpu/Chrome_ChildIOT run mean (ms), idle renderer/Compositor run mean (ms), idle utility/libuv-worker run mean (ms)).

| value | traced median | untraced median | medians' ratio | per-job mean | 95 % interval | reading | by order | n | exited (CPU, wakes) | left out (CPU, wakes) |
|---|---|---|---|---|---|---|---|---|---|---|
| driven per-input run (ms) | 110.2846 | 108.1361 | 0.9805 | 1.0022 | 0.947–1.0574 | not resolved | traced first 0.995; untraced first 1.0094 | 6 | — | — |
| idle code run mean (ms) | 0.0909 | 0.0904 | 0.9949 | 1.0938 | 0.4759–1.7117 | not resolved | traced first 0.5567; untraced first 1.6309 | 6 | 0, 0 | — |
| idle code wakes/s | 3.4704 | 3.4681 | 0.9993 | 0.9993 | 0.9066–1.092 | not resolved | traced first 0.919; untraced first 1.0796 | 6 | 0, 0 | — |
| idle gpu/Chrome_ChildIOT run mean (ms) | 0.0258 | 0.0229 | 0.8895 | 0.884 | 0.8356–0.9323 | difference | traced first 0.9061; untraced first 0.8618 | 6 | 0, 0 | — |
| idle gpu/Chrome_ChildIOT wakes/s | 20.244 | 19.952 | 0.9856 | 1.001 | 0.9873–1.0148 | not resolved | traced first 0.99; untraced first 1.0121 | 6 | 0, 0 | — |
| idle gpu/VizCompositorTh run mean (ms) | 0.243 | 0.2391 | 0.9838 | 0.9879 | 0.9552–1.0206 | not resolved | traced first 1.007; untraced first 0.9688 | 6 | 0, 0 | — |
| idle gpu/VizCompositorTh wakes/s | 23.4436 | 23.4195 | 0.999 | 1.0005 | 0.9881–1.0129 | not resolved | traced first 0.9926; untraced first 1.0084 | 6 | 0, 0 | — |
| idle renderer/Compositor run mean (ms) | 0.0832 | 0.0794 | 0.9542 | 0.9478 | 0.9254–0.9702 | difference | traced first 0.9565; untraced first 0.939 | 6 | 0, 0 | — |
| idle renderer/Compositor wakes/s | 23.19 | 23.0301 | 0.9931 | 0.9828 | 0.9587–1.0068 | not resolved | traced first 0.9834; untraced first 0.9821 | 6 | 0, 0 | — |
| idle renderer/ThreadPoolForeg run mean (ms) | 0.1484 | 0.1453 | 0.9792 | 1.0152 | 0.6755–1.355 | not resolved | traced first 1.3083; untraced first 0.7221 | 6 | 0, 0 | — |
| idle renderer/ThreadPoolForeg wakes/s | 2.952 | 2.9998 | 1.0162 | 1.0176 | 0.9561–1.0792 | not resolved | traced first 0.9852; untraced first 1.0501 | 6 | 0, 0 | — |
| idle renderer/code run mean (ms) | 0.2709 | 0.2632 | 0.9717 | 0.9906 | 0.9283–1.0529 | not resolved | traced first 0.9459; untraced first 1.0353 | 6 | 0, 0 | — |
| idle renderer/code wakes/s | 19.472 | 19.6258 | 1.0079 | 1.0079 | 0.9588–1.0569 | not resolved | traced first 1.0451; untraced first 0.9707 | 6 | 0, 0 | — |
| idle residual run mean (ms) | 0.1346 | 0.129 | 0.9582 | 1.8147 | 0.052–3.5773 | not resolved | traced first 0.2832; untraced first 3.3461 | 6 | 0.001, 0.001 | — |
| idle residual wakes/s | 3.3436 | 3.3387 | 0.9985 | 1.0213 | 0.8166–1.2261 | not resolved | traced first 0.8434; untraced first 1.1993 | 6 | 0.001, 0.001 | — |
| idle utility/code run mean (ms) | 0.0577 | 0.0528 | 0.9143 | 0.9383 | 0.845–1.0315 | not resolved | traced first 1.011; untraced first 0.8656 | 6 | 0, 0 | — |
| idle utility/code wakes/s | 10.7072 | 11.1625 | 1.0425 | 1.0212 | 0.8058–1.2367 | not resolved | traced first 0.8386; untraced first 1.2039 | 6 | 0, 0 | — |
| idle utility/libuv-worker run mean (ms) | 0.0107 | 0.0074 | 0.6915 | 0.7156 | 0.6387–0.7925 | difference | traced first 0.7261; untraced first 0.7051 | 6 | 0, 0 | — |
| idle utility/libuv-worker wakes/s | 5.3681 | 6.7429 | 1.2561 | 1.2066 | 0.9499–1.4633 | not resolved | traced first 1.1025; untraced first 1.3107 | 6 | 0, 0 | — |

- job 1: the screenshots after its two preludes differ in (54, 761, 56, 764)
- job 2: the screenshots after its two preludes differ in (4, 40, 56, 764)
- job 3: the screenshots after its two preludes differ in (4, 40, 125, 764)
- job 4: the screenshots after its two preludes differ in (4, 40, 56, 764)
- job 5: the screenshots after its two preludes differ in (54, 761, 56, 764)
- job 6: the screenshots after its two preludes differ in (54, 761, 56, 764)

The second idle run, 915–1815 s after the first began, differs from the first whichever is traced — the main thread wakes about 7 % less and its runs are about 40 % shorter, the residual's about 70 % shorter — which keeps those ratios from resolving; the carried idle values match the first run.

The traced runs against the carried pool (decision 17): largest |z| 10.83 over 28 values; only in the carried pool: input_run mean, 136M (ms).

## image-editor (`gimp`)

6 jobs (3 traced untraced, 3 untraced traced); builds: GNU Image Manipulation Program version 2.10.36 (1, 2, 3, 4, 5, 6).
7 intervals read; at 95 % chance alone gives about 0.4 differences; differences found: 3 (op gimp run mean (ms), op gimp wakes/s, op script-fu wakes/s).

| value | traced median | untraced median | medians' ratio | per-job mean | 95 % interval | reading | by order | n | exited (CPU, wakes) | left out (CPU, wakes) | in the operation windows (CPU, wakes) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| driven gimp run mean (ms) | 0.401 | 0.3949 | 0.9848 | 0.9856 | 0.9698–1.0014 | not resolved | traced first 0.9922; untraced first 0.979 | 6 | 0, 0 | — | — |
| driven gimp wakes/s | 7.0457 | 7.0336 | 0.9983 | 1.0008 | 0.9971–1.0044 | not resolved | traced first 0.9993; untraced first 1.0022 | 6 | 0, 0 | — | — |
| op gimp run mean (ms) | 97.7927 | 96.5942 | 0.9877 | 0.981 | 0.9704–0.9915 | difference | traced first 0.9788; untraced first 0.9832 | 6 | 0, 0 | — | 0.924, 0.181 |
| op gimp wakes/s | 2.176 | 2.2065 | 1.014 | 1.0206 | 1.0074–1.0337 | difference | traced first 1.0268; untraced first 1.0144 | 6 | 0, 0 | — | 0.924, 0.181 |
| op operation duration mean (ms) | 2350.0605 | 2346.658 | 0.9986 | 0.9989 | 0.9952–1.0025 | not resolved | traced first 0.9966; untraced first 1.0011 | 6 | — | — | — |
| op script-fu run mean (ms) | 0.0376 | 0.0375 | 0.9966 | 0.9812 | 0.9407–1.0217 | not resolved | traced first 0.9475; untraced first 1.0149 | 6 | 0, 0 | — | 0.988, 0.991 |
| op script-fu wakes/s | 2.2466 | 2.18 | 0.9704 | 0.9716 | 0.9644–0.9787 | difference | traced first 0.9656; untraced first 0.9775 | 6 | 0, 0 | — | 0.988, 0.991 |

- job 1: the screenshots after its two preludes differ in (223, 445, 335, 454)
- job 2: the screenshots after its two preludes differ in (223, 445, 335, 454)
- job 3: the screenshots after its two preludes differ in (223, 445, 335, 454)
- job 4: the screenshots after its two preludes differ in (223, 445, 335, 454)
- job 5: the screenshots after its two preludes differ in (223, 445, 335, 454)
- job 6: the screenshots after its two preludes differ in (223, 445, 335, 454)

The driven runs start from the control's prelude (the image reverted, the pointer over the canvas), in which the main thread wakes about 18 % less often with about 19 % longer runs than in the carried pool at the same CPU share; the driven ratios are perf's effect in that state.

The traced runs against the carried pool (decision 17): largest |z| 51.72 over 10 values.

## video-editor (`kdenlive`)

6 jobs (3 traced untraced, 3 untraced traced); builds: Could not detect package type, probably default? App dir is "/usr/bin" (1, 2, 3, 4, 5, 6).
13 intervals read; at 95 % chance alone gives about 0.7 differences; differences found: 2 (driven QXcbEventQueue run mean (ms), op operation duration mean (ms)).

| value | traced median | untraced median | medians' ratio | per-job mean | 95 % interval | reading | by order | n | exited (CPU, wakes) | left out (CPU, wakes) | in the operation windows (CPU, wakes) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| driven QXcbEventQueue run mean (ms) | 0.0218 | 0.0188 | 0.8616 | 0.8612 | 0.8152–0.9073 | difference | traced first 0.8292; untraced first 0.8933 | 6 | 0, 0 | — | — |
| driven QXcbEventQueue wakes/s | 74.2364 | 73.845 | 0.9947 | 0.9973 | 0.9702–1.0244 | not resolved | traced first 1.0149; untraced first 0.9798 | 6 | 0, 0 | — | — |
| driven kdenlive run mean (ms) | 2.6837 | 2.7428 | 1.022 | 1.037 | 0.9017–1.1723 | not resolved | traced first 0.9517; untraced first 1.1222 | 6 | 0.033, 0.023 | — | — |
| driven kdenlive wakes/s | 133.7114 | 132.0272 | 0.9874 | 0.9869 | 0.8913–1.0826 | not resolved | traced first 1.0455; untraced first 0.9284 | 6 | 0.033, 0.023 | — | — |
| driven residual run mean (ms) | 0.4831 | 0.4887 | 1.0116 | 0.9984 | 0.957–1.0398 | not resolved | traced first 0.9745; untraced first 1.0223 | 6 | 0.044, 0.578 | — | — |
| driven residual wakes/s | 0.7444 | 0.7467 | 1.003 | 1.006 | 0.9298–1.0822 | not resolved | traced first 0.9561; untraced first 1.0559 | 6 | 0.044, 0.578 | — | — |
| idle Qt bearer threa run mean (ms) | 0.4289 | 0.4273 | 0.9963 | 1.0002 | 0.9612–1.0391 | not resolved | traced first 1.0228; untraced first 0.9775 | 6 | 0, 0 | — | — |
| idle Qt bearer threa wakes/s | 0.1066 | 0.1 | 0.9381 | 0.9781 | 0.907–1.0492 | not resolved | traced first 0.9381; untraced first 1.018 | 6 | 0, 0 | — | — |
| idle kdenlive run mean (ms) | 0.0424 | 0.0394 | 0.9298 | 0.9708 | 0.911–1.0305 | not resolved | traced first 0.9563; untraced first 0.9852 | 6 | 0, 0 | — | — |
| idle kdenlive wakes/s | 1.2466 | 1.2287 | 0.9856 | 0.9985 | 0.9041–1.0928 | not resolved | traced first 0.9256; untraced first 1.0713 | 6 | 0, 0 | — | — |
| op kdenlive_render run mean (ms) | — | — | — | — | — | — | — | 0 | 1, 1 | — | 1, 1 |
| op kdenlive_render wakes/s | — | — | — | — | — | — | — | 0 | 1, 1 | — | 1, 1 |
| op operation duration mean (ms) | 11360.5875 | 11279.4 | 0.9929 | 0.9875 | 0.9778–0.9972 | difference | traced first 0.9847; untraced first 0.9904 | 6 | — | — | — |
| op residual run mean (ms) | 2.8379 | 2.8124 | 0.991 | 0.9932 | 0.9744–1.012 | not resolved | traced first 0.9801; untraced first 1.0062 | 6 | 0.021, 0.005 | — | 0.952, 0.839 |
| op residual wakes/s | 9.1085 | 9.2161 | 1.0118 | 1.0065 | 0.947–1.0661 | not resolved | traced first 0.9556; untraced first 1.0574 | 6 | 0.021, 0.005 | — | 0.952, 0.839 |

- job 1: op-untraced: 1 of 26 operations failed
- job 1: the screenshots after its two preludes differ in (0, 5, 1230, 792)
- job 2: op: 1 of 26 operations failed
- job 2: the screenshots after its two preludes differ in (0, 5, 1230, 792)
- job 3: op-untraced: 1 of 26 operations failed
- job 3: the screenshots after its two preludes differ in (0, 5, 1230, 792)
- job 4: op: 1 of 26 operations failed
- job 4: the screenshots after its two preludes differ in (0, 5, 1230, 792)
- job 5: op-untraced: 1 of 26 operations failed
- job 5: the screenshots after its two preludes differ in (0, 5, 1230, 792)
- job 6: op: 1 of 26 operations failed
- job 6: the screenshots after its two preludes differ in (0, 5, 1230, 792)

The first preview render of each job's second operation run did not start (`kdenlive_render` never appeared within 30 s), so that run's operation values rest on 25 renders against the first run's 26–27.

The traced runs against the carried pool (decision 17): largest |z| 0.98 over 20 values.

## audio-player (`mpv-audio`)

6 jobs (3 traced untraced, 3 untraced traced); builds: mpv 0.37.0 Copyright © 2000-2023 mpv/MPlayer/mplayer2 projects (1, 2, 3, 4, 5, 6).
1 intervals read; at 95 % chance alone gives about 0.1 differences; differences found: 1 (play CPU share).

| value | traced median | untraced median | medians' ratio | per-job mean | 95 % interval | reading | by order | n | exited (CPU, wakes) | left out (CPU, wakes) |
|---|---|---|---|---|---|---|---|---|---|---|
| play CPU share | 0.0076 | 0.0067 | 0.877 | 0.8598 | 0.8339–0.8857 | difference | traced first 0.8745; untraced first 0.8451 | 6 | — | — |

The traced runs against the carried pool (decision 17): largest |z| 0.11 over 3 values.

## video-player (`mpv-video`)

6 jobs (3 traced untraced, 3 untraced traced); builds: mpv 0.37.0 Copyright © 2000-2023 mpv/MPlayer/mplayer2 projects (1, 2, 3, 4, 5, 6).
1 intervals read; at 95 % chance alone gives about 0.1 differences; differences found: 1 (play CPU share).

| value | traced median | untraced median | medians' ratio | per-job mean | 95 % interval | reading | by order | n | exited (CPU, wakes) | left out (CPU, wakes) |
|---|---|---|---|---|---|---|---|---|---|---|
| play CPU share | 0.1213 | 0.1182 | 0.9741 | 0.9759 | 0.9636–0.9883 | difference | traced first 0.9663; untraced first 0.9856 | 6 | — | — |

- left out of the control's pool: 2@36300802358 — D66: window 2 measured twice — the restarted gate loop relaunched it (#627) before the previous loop's relaunch (#625) had started; the original launch's copy (#625, 36300400332) is kept

The traced runs against the carried pool (decision 17): largest |z| 1.41 over 3 values.

## office-writer (`soffice`)

6 jobs (3 traced untraced, 3 untraced traced); builds: LibreOffice 24.2.7.2 420(Build:2) (1, 2, 3, 4, 5, 6).
3 intervals read; at 95 % chance alone gives about 0.2 differences; differences found: 2 (driven per-input run (ms), idle soffice.bin wakes/s).

| value | traced median | untraced median | medians' ratio | per-job mean | 95 % interval | reading | by order | n | exited (CPU, wakes) | left out (CPU, wakes) |
|---|---|---|---|---|---|---|---|---|---|---|
| driven per-input run (ms) | 5.1596 | 5.0678 | 0.9822 | 0.9836 | 0.9694–0.9979 | difference | traced first 0.9785; untraced first 0.9888 | 6 | — | — |
| idle soffice.bin run mean (ms) | 0.1783 | 0.1741 | 0.9766 | 0.9861 | 0.9573–1.0149 | not resolved | traced first 0.9735; untraced first 0.9987 | 6 | 0, 0 | — |
| idle soffice.bin wakes/s | 3.4468 | 3.4572 | 1.003 | 1.0031 | 1.0012–1.0051 | difference | traced first 1.0026; untraced first 1.0037 | 6 | 0, 0 | — |

The traced runs against the carried pool (decision 17): largest |z| 0.8 over 4 values; only in the carried pool: input_run mean, 136M (ms).

## mail-client (`thunderbird-send`)

6 jobs (3 traced untraced, 3 untraced traced); builds: Mozilla Thunderbird 156.0.1 (1, 2, 3, 4, 5, 6).
44 intervals read; at 95 % chance alone gives about 2.2 differences; differences found: 14 (driven per-input run (ms), idle IPC I/O Child run mean (ms), idle IPC I/O Child wakes/s, idle IPDL Background run mean (ms), idle Timer run mean (ms), idle glean.dispatche run mean (ms), idle residual run mean (ms), op Compositor run mean (ms), op Renderer run mean (ms), op Socket Thread run mean (ms), op Softwar~cThread run mean (ms), op Timer run mean (ms), op WRRende~ckend#0 run mean (ms), op glean.dispatche run mean (ms)).

| value | traced median | untraced median | medians' ratio | per-job mean | 95 % interval | reading | by order | n | exited (CPU, wakes) | left out (CPU, wakes) | in the operation windows (CPU, wakes) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| driven per-input run (ms) | 6.2906 | 5.4763 | 0.8705 | 0.8951 | 0.8529–0.9373 | difference | traced first 0.8815; untraced first 0.9087 | 6 | — | — | — |
| idle IPC I/O Child run mean (ms) | 0.0279 | 0.0243 | 0.8702 | 0.8629 | 0.8032–0.9226 | difference | traced first 0.8247; untraced first 0.9011 | 6 | 0, 0 | — | — |
| idle IPC I/O Child wakes/s | 0.0399 | 0.04 | 1.0025 | 1.0025 | 1.0025–1.0025 | difference | traced first 1.0025; untraced first 1.0025 | 6 | 0, 0 | — | — |
| idle IPC I/O Parent run mean (ms) | 0.0362 | 0.033 | 0.9109 | 0.9256 | 0.7733–1.078 | not resolved | traced first 1.0069; untraced first 0.8444 | 6 | 0, 0 | — | — |
| idle IPC I/O Parent wakes/s | 0.0449 | 0.0416 | 0.9276 | 0.9412 | 0.7776–1.1047 | not resolved | traced first 0.9161; untraced first 0.9663 | 6 | 0, 0 | — | — |
| idle IPDL Background run mean (ms) | 0.0212 | 0.018 | 0.8509 | 0.8826 | 0.8238–0.9414 | difference | traced first 0.8587; untraced first 0.9066 | 6 | 0, 0 | — | — |
| idle IPDL Background wakes/s | 0.2444 | 0.2466 | 1.0092 | 0.9829 | 0.9179–1.0479 | not resolved | traced first 0.9819; untraced first 0.9839 | 6 | 0, 0 | — | — |
| idle Indexed~ IO run mean (ms) | — | — | — | — | — | — | — | 0 | 1, 1 | — | — |
| idle Indexed~ IO wakes/s | — | — | — | — | — | — | — | 0 | 1, 1 | — | — |
| idle JS Watchdog run mean (ms) | 0.0344 | 0.0323 | 0.9405 | 0.9611 | 0.8672–1.0551 | not resolved | traced first 0.9502; untraced first 0.972 | 6 | 0, 0 | — | — |
| idle JS Watchdog wakes/s | 0.1737 | 0.18 | 1.0363 | 1.0231 | 0.9894–1.0568 | not resolved | traced first 1.0248; untraced first 1.0214 | 6 | 0, 0 | — | — |
| idle StreamTrans run mean (ms) | — | — | — | — | — | — | — | 0 | 1, 1 | — | — |
| idle StreamTrans wakes/s | — | — | — | — | — | — | — | 0 | 1, 1 | — | — |
| idle Timer run mean (ms) | 0.0486 | 0.0417 | 0.8583 | 0.8428 | 0.7654–0.9203 | difference | traced first 0.8735; untraced first 0.8122 | 6 | 0, 0 | — | — |
| idle Timer wakes/s | 0.276 | 0.2883 | 1.0448 | 1.0415 | 0.9339–1.1492 | not resolved | traced first 0.9762; untraced first 1.1069 | 6 | 0, 0 | — | — |
| idle WebExtensions run mean (ms) | 0.0892 | 0.0916 | 1.0272 | 1.0223 | 0.8506–1.194 | not resolved | traced first 0.8784; untraced first 1.1661 | 6 | 0, 0 | — | — |
| idle WebExtensions wakes/s | 0.2435 | 0.2249 | 0.9236 | 0.957 | 0.8501–1.0638 | not resolved | traced first 1.0449; untraced first 0.869 | 6 | 0, 0 | — | — |
| idle glean.dispatche run mean (ms) | 0.0395 | 0.0314 | 0.7948 | 0.7912 | 0.7209–0.8614 | difference | traced first 0.8403; untraced first 0.742 | 6 | 0, 0 | — | — |
| idle glean.dispatche wakes/s | 0.0582 | 0.0575 | 0.988 | 0.995 | 0.8897–1.1004 | not resolved | traced first 1.0629; untraced first 0.9272 | 6 | 0, 0 | — | — |
| idle gmain run mean (ms) | 0.068 | 0.0649 | 0.9545 | 1.0001 | 0.8986–1.1016 | not resolved | traced first 1.0307; untraced first 0.9695 | 6 | 0, 0 | — | — |
| idle gmain wakes/s | 0.2502 | 0.25 | 0.9992 | 0.9992 | 0.9955–1.0029 | not resolved | traced first 1.0024; untraced first 0.996 | 6 | 0, 0 | — | — |
| idle residual run mean (ms) | 0.0365 | 0.0343 | 0.9401 | 0.9425 | 0.8919–0.9931 | difference | traced first 0.9266; untraced first 0.9584 | 6 | 0.548, 0.323 | — | — |
| idle residual wakes/s | 0.0565 | 0.0542 | 0.9593 | 0.9948 | 0.8178–1.1717 | not resolved | traced first 1.1409; untraced first 0.8486 | 6 | 0.548, 0.323 | — | — |
| idle thunderbird-bin run mean (ms) | 0.2755 | 0.2613 | 0.9485 | 0.9788 | 0.6822–1.2755 | not resolved | traced first 0.7604; untraced first 1.1973 | 6 | 0, 0 | — | — |
| idle thunderbird-bin wakes/s | 0.4672 | 0.4625 | 0.99 | 1.0691 | 0.7725–1.3657 | not resolved | traced first 1.3086; untraced first 0.8296 | 6 | 0, 0 | — | — |
| op Compositor run mean (ms) | 0.0135 | 0.0112 | 0.8269 | 0.8171 | 0.782–0.8522 | difference | traced first 0.7988; untraced first 0.8354 | 6 | 0, 0 | — | 0.374, 0.341 |
| op Compositor wakes/s | 220.6841 | 223.3445 | 1.0121 | 1.0079 | 0.9542–1.0617 | not resolved | traced first 1.0494; untraced first 0.9665 | 6 | 0, 0 | — | 0.374, 0.341 |
| op Renderer run mean (ms) | 0.2805 | 0.2685 | 0.9573 | 0.9696 | 0.9442–0.995 | difference | traced first 0.9546; untraced first 0.9846 | 6 | 0, 0 | — | 0.307, 0.541 |
| op Renderer wakes/s | 27.4722 | 27.2961 | 0.9936 | 0.9821 | 0.9295–1.0347 | not resolved | traced first 0.9885; untraced first 0.9758 | 6 | 0, 0 | — | 0.307, 0.541 |
| op Socket Thread run mean (ms) | 0.022 | 0.0178 | 0.8097 | 0.8246 | 0.6681–0.9811 | difference | traced first 0.7041; untraced first 0.9452 | 6 | 0, 0 | — | 0.995, 0.997 |
| op Socket Thread wakes/s | 101.8195 | 105.7403 | 1.0385 | 1.0458 | 0.784–1.3076 | not resolved | traced first 1.2709; untraced first 0.8207 | 6 | 0, 0 | — | 0.995, 0.997 |
| op Softwar~cThread run mean (ms) | 0.0552 | 0.0415 | 0.7513 | 0.7453 | 0.7249–0.7657 | difference | traced first 0.7353; untraced first 0.7552 | 6 | 0, 0 | — | 0.25, 0.283 |
| op Softwar~cThread wakes/s | 26.1107 | 26.0334 | 0.997 | 0.9925 | 0.978–1.007 | not resolved | traced first 0.9926; untraced first 0.9924 | 6 | 0, 0 | — | 0.25, 0.283 |
| op StreamT~ns run mean (ms) | — | — | — | — | — | — | — | 0 | 1, 1 | — | 0.177, 0.07 |
| op StreamT~ns wakes/s | — | — | — | — | — | — | — | 0 | 1, 1 | — | 0.177, 0.07 |
| op SwComposite run mean (ms) | 0.0239 | 0.022 | 0.9197 | 0.9266 | 0.8102–1.0429 | not resolved | traced first 0.8598; untraced first 0.9933 | 6 | 0.797, 0.744 | — | 0.196, 0.432 |
| op SwComposite wakes/s | 5.7466 | 5.8309 | 1.0147 | 0.9912 | 0.9531–1.0292 | not resolved | traced first 0.9937; untraced first 0.9886 | 6 | 0.797, 0.744 | — | 0.196, 0.432 |
| op TaskCon~ller run mean (ms) | 0.2755 | 0.273 | 0.991 | 1.0187 | 0.7398–1.2976 | not resolved | traced first 1.26; untraced first 0.7773 | 6 | 0, 0 | — | 0.164, 0.211 |
| op TaskCon~ller wakes/s | 20.9863 | 21.2901 | 1.0145 | 1.0105 | 0.898–1.1229 | not resolved | traced first 0.9161; untraced first 1.1048 | 6 | 0, 0 | — | 0.164, 0.211 |
| op Timer run mean (ms) | 0.0275 | 0.022 | 0.8 | 0.8145 | 0.759–0.8699 | difference | traced first 0.7695; untraced first 0.8594 | 6 | 0, 0 | — | 0.179, 0.25 |
| op Timer wakes/s | 14.8445 | 14.6162 | 0.9846 | 0.9827 | 0.8959–1.0694 | not resolved | traced first 1.0564; untraced first 0.909 | 6 | 0, 0 | — | 0.179, 0.25 |
| op WRRende~ckend#0 run mean (ms) | 0.3182 | 0.2965 | 0.9316 | 0.9112 | 0.8281–0.9943 | difference | traced first 0.9328; untraced first 0.8895 | 6 | 0, 0 | — | 0.367, 0.322 |
| op WRRende~ckend#0 wakes/s | 10.4032 | 10.5561 | 1.0147 | 1.0136 | 0.9877–1.0396 | not resolved | traced first 0.9927; untraced first 1.0346 | 6 | 0, 0 | — | 0.367, 0.322 |
| op glean.dispatche run mean (ms) | 0.0505 | 0.0374 | 0.7403 | 0.7375 | 0.6888–0.7863 | difference | traced first 0.7592; untraced first 0.7158 | 6 | 0, 0 | — | 0.317, 0.188 |
| op glean.dispatche wakes/s | 17.7028 | 17.9597 | 1.0145 | 1.0208 | 0.9718–1.0697 | not resolved | traced first 0.9785; untraced first 1.063 | 6 | 0, 0 | — | 0.317, 0.188 |
| op operation duration mean (ms) | 2973.304 | 2942.335 | 0.9896 | 0.9768 | 0.9126–1.0409 | not resolved | traced first 0.9868; untraced first 0.9667 | 6 | — | — | — |
| op residual run mean (ms) | 0.1404 | 0.1351 | 0.9621 | 0.9832 | 0.8322–1.1343 | not resolved | traced first 0.991; untraced first 0.9754 | 6 | 0.169, 0.165 | — | 0.488, 0.268 |
| op residual wakes/s | 38.9798 | 39.4108 | 1.0111 | 1.0129 | 0.9867–1.039 | not resolved | traced first 1.0223; untraced first 1.0034 | 6 | 0.169, 0.165 | — | 0.488, 0.268 |
| op thunderbird-bin run mean (ms) | 1.1553 | 1.1216 | 0.9708 | 0.985 | 0.765–1.2051 | not resolved | traced first 1.1715; untraced first 0.7986 | 6 | 0, 0 | — | 0.552, 0.375 |
| op thunderbird-bin wakes/s | 133.7811 | 135.9434 | 1.0162 | 1.0216 | 0.877–1.1662 | not resolved | traced first 0.8962; untraced first 1.147 | 6 | 0, 0 | — | 0.552, 0.375 |

The operation phase's second send pass wakes `Socket Thread` about 22 % more and `TaskCon~ller` about 35 % less inside the sends than the first, which keeps `Socket Thread`'s wake rate and both of `TaskCon~ller`'s ratios from resolving.

The traced runs against the carried pool (decision 17): largest |z| 8.96 over 70 values; only in the carried pool: input_run mean, 136M (ms).

## video-call (`webrtc`)

6 jobs (3 traced untraced, 3 untraced traced); builds: Google Chrome 153.0.8010.52 (1, 2, 3, 4, 5, 6).
1 intervals read; at 95 % chance alone gives about 0.1 differences; differences found: 1 (play CPU share).

| value | traced median | untraced median | medians' ratio | per-job mean | 95 % interval | reading | by order | n | exited (CPU, wakes) | left out (CPU, wakes) |
|---|---|---|---|---|---|---|---|---|---|---|
| play CPU share | 0.1873 | 0.1808 | 0.965 | 0.9524 | 0.9342–0.9707 | difference | traced first 0.9543; untraced first 0.9506 | 6 | — | — |

The traced runs against the carried pool (decision 17): largest |z| 0.37 over 3 values.
