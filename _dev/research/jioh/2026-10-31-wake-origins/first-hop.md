
## chrome idle: 38 repeats, 22800 s, app CPU share 0.003
| component | wakes/s | CPU share of app | x wakes/CPU | tree wakes/CPU | tree_same_cpu wakes/CPU | idle wakes/CPU | kernel wakes/CPU | other wakes/CPU | none wakes/CPU |
|---|---|---|---|---|---|---|---|---|---|
| gpu/VizCompositorTh | 12.1 | 0.31 | 0.14/0.06 | 0.00/0.00 | 0.47/0.64 | 0.39/0.29 | 0.00/0.00 | 0.00/0.00 |  |
| renderer/Compositor | 12.7 | 0.30 |  | 0.00/0.00 | 0.74/0.82 | 0.26/0.18 | 0.00/0.00 | 0.00/0.00 |  |
| renderer/chrome | 7.4 | 0.19 |  | 0.00/0.00 | 0.69/0.60 | 0.31/0.40 | 0.00/0.00 | 0.00/0.00 | 0.00/0.00 |
| gpu/Chrome_ChildIOT | 7.6 | 0.08 |  | 0.00/0.00 | 1.00/1.00 |  |  |  |  |
| chrome | 0.8 | 0.04 | 0.09/0.03 | 0.00/0.00 | 0.20/0.08 | 0.71/0.89 | 0.00/0.00 | 0.00/0.00 |  |
| MemoryInfra | 0.1 | 0.03 |  |  | 0.51/0.97 | 0.49/0.03 |  | 0.00/0.00 |  |
| utility/chrome | 0.8 | 0.02 |  | 0.00/0.00 | 0.01/0.01 | 0.99/0.99 | 0.00/0.00 | 0.00/0.00 |  |
| gpu/chrome | 0.3 | 0.01 |  |  | 0.00/0.01 | 0.99/0.99 |  | 0.00/0.00 |  |

## chrome op: 38 repeats, 22990 s, app CPU share 0.039
| component | wakes/s | CPU share of app | x wakes/CPU | tree wakes/CPU | tree_same_cpu wakes/CPU | idle wakes/CPU | kernel wakes/CPU | other wakes/CPU | none wakes/CPU |
|---|---|---|---|---|---|---|---|---|---|
| renderer/chrome | 5.2 | 0.52 | 0.00/0.00 | 0.00/0.00 | 0.73/0.93 | 0.27/0.07 | 0.00/0.00 | 0.00/0.00 |  |
| renderer/ThreadPoolForeg | 18.0 | 0.19 | 0.00/0.00 | 0.00/0.00 | 0.96/0.99 | 0.04/0.01 | 0.00/0.00 | 0.00/0.00 |  |
| chrome | 19.0 | 0.11 | 0.02/0.02 |  | 0.67/0.81 | 0.31/0.17 | 0.00/0.00 | 0.00/0.00 |  |
| gpu/VizCompositorTh | 8.2 | 0.09 | 0.17/0.03 | 0.00/0.00 | 0.63/0.83 | 0.20/0.15 | 0.00/0.00 | 0.00/0.00 |  |
| Chrome_IOThread | 28.2 | 0.02 |  | 0.00/0.00 | 1.00/1.00 | 0.00/0.00 |  | 0.00/0.00 |  |
| utility/Chrome_ChildIOT | 3.8 | 0.02 | 0.00/0.00 | 0.00/0.00 | 0.92/0.61 | 0.05/0.04 | 0.00/0.00 | 0.03/0.34 |  |
| renderer/Compositor | 6.7 | 0.01 |  | 0.00/0.00 | 0.90/0.94 | 0.10/0.06 | 0.00/0.00 | 0.00/0.00 |  |
| ThreadPoolForeg | 9.6 | 0.01 | 0.00/0.00 | 0.00/0.00 | 0.85/0.80 | 0.10/0.14 | 0.05/0.05 | 0.00/0.00 |  |

## code idle: 44 repeats, 39600 s, app CPU share 0.015
| component | wakes/s | CPU share of app | x wakes/CPU | tree wakes/CPU | tree_same_cpu wakes/CPU | idle wakes/CPU | kernel wakes/CPU | other wakes/CPU | none wakes/CPU |
|---|---|---|---|---|---|---|---|---|---|
| gpu/VizCompositorTh | 23.1 | 0.37 | 0.05/0.01 | 0.00/0.00 | 0.55/0.91 | 0.40/0.08 | 0.00/0.00 | 0.00/0.00 |  |
| renderer/code | 19.5 | 0.33 |  |  | 0.68/0.85 | 0.32/0.15 | 0.00/0.00 | 0.00/0.00 | 0.00/0.00 |
| renderer/Compositor | 22.8 | 0.12 |  | 0.00/0.00 | 0.72/0.82 | 0.28/0.18 | 0.00/0.00 | 0.00/0.00 |  |
| utility/code | 12.6 | 0.04 |  | 0.00/0.00 | 0.61/0.54 | 0.39/0.46 | 0.00/0.00 | 0.00/0.00 |  |
| gpu/Chrome_ChildIOT | 20.2 | 0.03 |  | 0.00/0.00 | 1.00/1.00 |  |  |  |  |
| V8Worker | 0.2 | 0.03 |  | 0.07/0.14 | 0.93/0.86 |  |  |  |  |
| code | 3.6 | 0.03 |  | 0.00/0.00 | 0.62/0.52 | 0.38/0.48 | 0.00/0.00 | 0.00/0.00 |  |
| renderer/ThreadPoolForeg | 3.4 | 0.03 |  | 0.00/0.00 | 0.99/1.00 | 0.01/0.00 |  | 0.00/0.00 | 0.00/0.00 |

## gimp driven: 5 repeats, 3025 s, app CPU share 0.003
| component | wakes/s | CPU share of app | x wakes/CPU | tree wakes/CPU | tree_same_cpu wakes/CPU | idle wakes/CPU | kernel wakes/CPU | other wakes/CPU | none wakes/CPU |
|---|---|---|---|---|---|---|---|---|---|
| gimp | 8.6 | 1.00 | 0.91/0.98 |  |  | 0.09/0.02 | 0.00/0.00 | 0.00/0.00 |  |

## gimp op: 5 repeats, 3025 s, app CPU share 0.233
| component | wakes/s | CPU share of app | x wakes/CPU | tree wakes/CPU | tree_same_cpu wakes/CPU | idle wakes/CPU | kernel wakes/CPU | other wakes/CPU | none wakes/CPU |
|---|---|---|---|---|---|---|---|---|---|
| gimp | 2.2 | 0.92 | 0.63/0.08 | 0.00/0.00 | 0.29/0.91 | 0.07/0.00 | 0.00/0.01 |  |  |
| async | 0.1 | 0.08 |  | 0.01/0.01 | 0.99/0.99 |  |  |  |  |

## kdenlive driven: 20 repeats, 12100 s, app CPU share 0.372
| component | wakes/s | CPU share of app | x wakes/CPU | tree wakes/CPU | tree_same_cpu wakes/CPU | idle wakes/CPU | kernel wakes/CPU | other wakes/CPU | none wakes/CPU |
|---|---|---|---|---|---|---|---|---|---|
| kdenlive | 136.6 | 1.00 | 0.00/0.00 | 0.00/0.00 | 0.55/0.78 | 0.45/0.22 | 0.00/0.00 | 0.00/0.00 |  |
| QXcbEventQueue | 72.8 | 0.00 | 1.00/1.00 |  | 0.00/0.00 |  |  |  |  |

## kdenlive op: 20 repeats, 12100 s, app CPU share 0.496
| component | wakes/s | CPU share of app | x wakes/CPU | tree wakes/CPU | tree_same_cpu wakes/CPU | idle wakes/CPU | kernel wakes/CPU | other wakes/CPU | none wakes/CPU |
|---|---|---|---|---|---|---|---|---|---|
| kdenlive_render | 317.7 | 0.94 | 0.00/0.00 | 0.01/0.04 | 0.99/0.96 |  | 0.00/0.00 | 0.00/0.00 |  |
| kdenlive | 6.2 | 0.05 | 0.00/0.00 | 0.01/0.02 | 0.89/0.96 | 0.10/0.02 | 0.00/0.00 | 0.00/0.00 |  |

## soffice idle: 14 repeats, 1680 s, app CPU share 0.001
| component | wakes/s | CPU share of app | x wakes/CPU | tree wakes/CPU | tree_same_cpu wakes/CPU | idle wakes/CPU | kernel wakes/CPU | other wakes/CPU | none wakes/CPU |
|---|---|---|---|---|---|---|---|---|---|
| soffice.bin | 3.5 | 1.00 | 0.49/0.09 |  |  | 0.51/0.91 | 0.00/0.00 | 0.00/0.00 |  |

## thunderbird-send driven: 8 repeats, 4840 s, app CPU share 0.009
| component | wakes/s | CPU share of app | x wakes/CPU | tree wakes/CPU | tree_same_cpu wakes/CPU | idle wakes/CPU | kernel wakes/CPU | other wakes/CPU | none wakes/CPU |
|---|---|---|---|---|---|---|---|---|---|
| thunderbird-bin | 12.6 | 0.48 | 0.36/0.64 | 0.00/0.00 | 0.64/0.36 | 0.00/0.00 | 0.00/0.00 |  |  |
| Compositor | 89.7 | 0.10 |  | 0.00/0.00 | 1.00/1.00 |  |  |  |  |
| Renderer | 4.4 | 0.09 | 0.00/0.00 | 0.00/0.00 | 1.00/1.00 |  |  |  |  |
| Softwar~cThread | 17.2 | 0.09 |  | 0.00/0.00 | 0.19/0.06 | 0.80/0.94 | 0.00/0.00 | 0.00/0.00 |  |
| WRRende~ckend#1 | 2.4 | 0.06 |  | 0.00/0.00 | 1.00/1.00 |  |  |  |  |
| WRScene~ilder#1 | 1.7 | 0.04 |  | 0.00/0.00 | 1.00/1.00 |  |  |  |  |
| glean.dispatche | 4.3 | 0.02 |  | 0.00/0.00 | 0.99/0.99 | 0.01/0.01 |  | 0.00/0.00 |  |
| Timer | 5.0 | 0.02 |  | 0.00/0.00 | 0.28/0.08 | 0.72/0.92 |  | 0.00/0.00 |  |

## thunderbird-send idle: 43 repeats, 25800 s, app CPU share 0.001
| component | wakes/s | CPU share of app | x wakes/CPU | tree wakes/CPU | tree_same_cpu wakes/CPU | idle wakes/CPU | kernel wakes/CPU | other wakes/CPU | none wakes/CPU |
|---|---|---|---|---|---|---|---|---|---|
| thunderbird-bin | 0.4 | 0.15 |  | 0.00/0.01 | 1.00/0.99 |  | 0.00/0.00 |  |  |
| WebExtensions/WebExtensions | 0.2 | 0.03 |  | 0.01/0.01 | 0.99/0.99 |  |  |  |  |
| StreamTrans #47 | 0.0 | 0.03 |  | 0.35/0.76 | 0.30/0.23 | 0.35/0.00 |  |  |  |
| StreamTrans #49 | 0.0 | 0.02 |  | 0.31/0.80 | 0.39/0.20 | 0.30/0.00 |  |  |  |
| StreamTrans #45 | 0.0 | 0.02 |  | 0.32/0.87 | 0.36/0.12 | 0.32/0.00 |  |  |  |
| StreamTrans #52 | 0.0 | 0.02 |  | 0.32/0.73 | 0.37/0.27 | 0.32/0.00 |  |  |  |
| StreamTrans #51 | 0.0 | 0.02 |  | 0.35/0.80 | 0.30/0.19 | 0.35/0.01 |  |  |  |
| StreamTrans #50 | 0.0 | 0.02 |  | 0.28/0.70 | 0.45/0.29 | 0.28/0.00 |  |  |  |

## thunderbird-send op: 8 repeats, 4840 s, app CPU share 0.188
| component | wakes/s | CPU share of app | x wakes/CPU | tree wakes/CPU | tree_same_cpu wakes/CPU | idle wakes/CPU | kernel wakes/CPU | other wakes/CPU | none wakes/CPU |
|---|---|---|---|---|---|---|---|---|---|
| thunderbird-bin | 143.8 | 0.80 | 0.35/0.24 | 0.00/0.00 | 0.60/0.74 | 0.05/0.02 | 0.00/0.00 | 0.00/0.00 |  |
| Renderer | 27.7 | 0.04 | 0.01/0.10 | 0.00/0.00 | 0.99/0.90 |  | 0.00/0.00 |  |  |
| TaskCon~ller #0 | 15.4 | 0.02 |  | 0.00/0.00 | 1.00/1.00 |  |  |  |  |
| WRRende~ckend#0 | 10.4 | 0.02 |  | 0.00/0.00 | 1.00/1.00 |  |  |  |  |
| Compositor | 219.2 | 0.01 |  | 0.00/0.00 | 1.00/1.00 |  |  |  |  |
| WRScene~ilder#0 | 9.2 | 0.01 |  | 0.00/0.00 | 1.00/1.00 |  |  |  |  |
| Socket Thread | 90.1 | 0.01 |  | 0.02/0.15 | 0.98/0.85 |  |  |  |  |
| Softwar~cThread | 26.2 | 0.01 |  | 0.00/0.00 | 0.37/0.19 | 0.63/0.81 | 0.00/0.00 | 0.00/0.00 |  |

# Wakers

## chrome idle
- gpu/VizCompositorTh (12.1/s, 0.31 of CPU): gpu/Chrome_ChildIOT 0.47/0.64; swapper 0.39/0.29; Xvfb 0.14/0.06; renderer/Compositor 0.00/0.00; .NET TP Worker 0.00/0.00
- renderer/Compositor (12.7/s, 0.30 of CPU): gpu/VizCompositorTh 0.48/0.31; renderer/chrome 0.26/0.51; swapper 0.26/0.18; .NET TP Worker 0.00/0.00; hv_kvp_daemon 0.00/0.00
- renderer/chrome (7.4/s, 0.19 of CPU): renderer/Compositor 0.69/0.60; swapper 0.31/0.40; renderer/Chrome_ChildIOT 0.00/0.00; renderer/MemoryInfra 0.00/0.00; .NET TP Worker 0.00/0.00
- gpu/Chrome_ChildIOT (7.6/s, 0.08 of CPU): renderer/Compositor 1.00/1.00; chrome 0.00/0.00; MemoryInfra 0.00/0.00; gpu/VizCompositorTh 0.00/0.00
- chrome (0.8/s, 0.04 of CPU): swapper 0.71/0.89; MemoryInfra 0.10/0.05; Xvfb 0.09/0.03; ThreadPoolForeg 0.08/0.02; Chrome_IOThread 0.01/0.01
- MemoryInfra (0.1/s, 0.03 of CPU): chrome 0.51/0.97; swapper 0.49/0.03; .NET TP Worker 0.00/0.00; gpu/Chrome_ChildIOT 0.00/0.00; renderer/chrome 0.00/0.00
- utility/chrome (0.8/s, 0.02 of CPU): swapper 0.99/0.99; utility/Chrome_ChildIOT 0.00/0.00; renderer/Compositor 0.00/0.00; utility/chrome 0.00/0.00; utility/MemoryInfra 0.00/0.00
- gpu/chrome (0.3/s, 0.01 of CPU): swapper 0.99/0.99; gpu/Chrome_ChildIOT 0.00/0.00; gpu/MemoryInfra 0.00/0.00; .NET TP Worker 0.00/0.00; renderer/chrome 0.00/0.00

## chrome op
- renderer/chrome (5.2/s, 0.52 of CPU): renderer/Chrome_ChildIOT 0.38/0.14; swapper 0.27/0.07; renderer/Compositor 0.20/0.05; renderer/ThreadPoolForeg 0.15/0.74; chrome 0.01/0.00
- renderer/ThreadPoolForeg (18.0/s, 0.19 of CPU): renderer/chrome 0.74/0.68; renderer/ThreadPoolForeg 0.15/0.16; swapper 0.04/0.01; renderer/Chrome_ChildIOT 0.02/0.04; renderer/Compositor 0.02/0.11
- chrome (19.0/s, 0.11 of CPU): Chrome_IOThread 0.51/0.69; swapper 0.31/0.17; CompositorTileW 0.09/0.07; renderer/chrome 0.04/0.02; ThreadPoolForeg 0.02/0.02
- gpu/VizCompositorTh (8.2/s, 0.09 of CPU): gpu/Chrome_ChildIOT 0.44/0.28; swapper 0.20/0.15; Xvfb 0.17/0.03; renderer/chrome 0.13/0.43; renderer/ThreadPoolForeg 0.03/0.08
- Chrome_IOThread (28.2/s, 0.02 of CPU): chrome 0.37/0.26; gpu/VizCompositorTh 0.23/0.24; renderer/Chrome_ChildIOT 0.19/0.28; renderer/chrome 0.12/0.15; utility/Chrome_ChildIOT 0.06/0.04
- utility/Chrome_ChildIOT (3.8/s, 0.02 of CPU): chrome 0.71/0.34; renderer/chrome 0.10/0.03; renderer/Chrome_ChildIOT 0.06/0.02; swapper 0.05/0.04; utility/ThreadPoolForeg 0.03/0.19
- renderer/Compositor (6.7/s, 0.01 of CPU): renderer/chrome 0.41/0.59; gpu/VizCompositorTh 0.18/0.15; swapper 0.10/0.06; renderer/Chrome_ChildIOT 0.09/0.03; chrome 0.08/0.06
- ThreadPoolForeg (9.6/s, 0.01 of CPU): chrome 0.80/0.72; swapper 0.10/0.14; jbd2/sda1-8 0.03/0.05; ThreadPoolServi 0.03/0.05; Chrome_IOThread 0.01/0.03

## code idle
- gpu/VizCompositorTh (23.1/s, 0.37 of CPU): gpu/Chrome_ChildIOT 0.54/0.91; swapper 0.40/0.08; Xvfb 0.05/0.01; renderer/code 0.00/0.00; renderer/Compositor 0.00/0.00
- renderer/code (19.5/s, 0.33 of CPU): renderer/Compositor 0.66/0.83; swapper 0.32/0.15; renderer/Chrome_ChildIOT 0.02/0.01; renderer/ThreadPoolForeg 0.00/0.00; gpu/VizCompositorTh 0.00/0.00
- renderer/Compositor (22.8/s, 0.12 of CPU): renderer/code 0.40/0.50; swapper 0.28/0.18; gpu/VizCompositorTh 0.24/0.14; renderer/ThreadPoolForeg 0.08/0.18; V8Worker 0.00/0.00
- utility/code (12.6/s, 0.04 of CPU): utility/code 0.56/0.35; swapper 0.39/0.46; utility/libuv-worker 0.02/0.02; utility/Chrome_ChildIOT 0.02/0.13; gpu/VizCompositorTh 0.00/0.00
- gpu/Chrome_ChildIOT (20.2/s, 0.03 of CPU): renderer/Compositor 1.00/1.00; code 0.00/0.00; gpu/code 0.00/0.00; gpu/VizCompositorTh 0.00/0.00
- V8Worker (0.2/s, 0.03 of CPU): code 0.89/0.85; V8Worker 0.07/0.15; DelayedTaskSche 0.04/0.00
- code (3.6/s, 0.03 of CPU): code 0.52/0.18; swapper 0.38/0.48; libuv-worker 0.06/0.02; Chrome_IOThread 0.04/0.05; V8Worker 0.01/0.25
- renderer/ThreadPoolForeg (3.4/s, 0.03 of CPU): renderer/Compositor 0.87/0.28; renderer/code 0.11/0.58; renderer/Chrome_ChildIOT 0.01/0.00; swapper 0.01/0.00; renderer/ThreadPoolForeg 0.00/0.14

## gimp driven
- gimp (8.6/s, 1.00 of CPU): Xvfb 0.91/0.98; swapper 0.09/0.02; .NET TP Worker 0.00/0.00; .NET Tiered Com 0.00/0.00; kworker/3:0-eve 0.00/0.00

## gimp op
- gimp (2.2/s, 0.92 of CPU): Xvfb 0.63/0.08; script-fu 0.18/0.91; async 0.11/0.00; swapper 0.07/0.00; khugepaged 0.00/0.01
- async (0.1/s, 0.08 of CPU): gimp 1.00/1.00

## kdenlive driven
- kdenlive (136.6/s, 1.00 of CPU): QXcbEventQueue 0.52/0.75; swapper 0.45/0.22; kdenlive 0.03/0.03; Qt bearer threa 0.00/0.00; khugepaged 0.00/0.00
- QXcbEventQueue (72.8/s, 0.00 of CPU): Xvfb 1.00/1.00; kdenlive 0.00/0.00

## kdenlive op
- kdenlive_render (317.7/s, 0.94 of CPU): kdenlive_render 0.98/0.99; QXcbEventQueue 0.01/0.01; Xvfb 0.00/0.00; pgrep 0.00/0.00; :10443 0.00/0.00
- kdenlive (6.2/s, 0.05 of CPU): kdenlive_render 0.43/0.51; QXcbEventQueue 0.43/0.45; swapper 0.10/0.02; Qt bearer threa 0.02/0.00; kdenlive 0.01/0.02

## soffice idle
- soffice.bin (3.5/s, 1.00 of CPU): swapper 0.51/0.91; Xvfb 0.49/0.09; .NET Tiered Com 0.00/0.00; khugepaged 0.00/0.00; python3 0.00/0.00

## thunderbird-send driven
- thunderbird-bin (12.6/s, 0.48 of CPU): Xvfb 0.36/0.64; Timer 0.26/0.27; Compositor 0.23/0.05; Softwar~cThread 0.12/0.03; IPC I/O Parent 0.00/0.00
- Compositor (89.7/s, 0.10 of CPU): Softwar~cThread 0.82/0.68; thunderbird-bin 0.07/0.14; Timer 0.05/0.09; Renderer 0.04/0.06; WRScene~ilder#1 0.02/0.03
- Renderer (4.4/s, 0.09 of CPU): WRRende~ckend#1 0.44/0.88; SwComposite 0.35/0.08; Compositor 0.20/0.01; WRRende~ckend#0 0.01/0.03; Xvfb 0.00/0.00
- Softwar~cThread (17.2/s, 0.09 of CPU): swapper 0.80/0.94; thunderbird-bin 0.19/0.05; Compositor 0.00/0.00; WRScene~ilder#1 0.00/0.00; .NET TP Worker 0.00/0.00
- WRRende~ckend#1 (2.4/s, 0.06 of CPU): WRScene~ilder#1 0.69/0.62; Compositor 0.31/0.38
- WRScene~ilder#1 (1.7/s, 0.04 of CPU): Compositor 1.00/1.00; WRRende~ckend#0 0.00/0.00; thunderbird-bin 0.00/0.00
- glean.dispatche (4.3/s, 0.02 of CPU): thunderbird-bin 0.82/0.83; Compositor 0.16/0.16; Timer 0.01/0.01; swapper 0.01/0.01; StreamTrans #70 0.00/0.00
- Timer (5.0/s, 0.02 of CPU): swapper 0.72/0.92; thunderbird-bin 0.16/0.05; Compositor 0.11/0.03; IPDL Background 0.00/0.00; Renderer 0.00/0.00

## thunderbird-send idle
- thunderbird-bin (0.4/s, 0.15 of CPU): Timer 0.54/0.94; IndexedDB IO #9 0.01/0.00; StreamTrans #46 0.01/0.00; StreamTrans #51 0.01/0.00; BgIOThr~Pool #3 0.01/0.00
- WebExtensions/WebExtensions (0.2/s, 0.03 of CPU): WebExtensions/Timer 0.58/0.76; WebExtensions/IPC I/O Child 0.17/0.17; WebExtensions/StreamTrans #8 0.04/0.01; WebExtensions/StreamTrans #9 0.04/0.01; WebExtensions/StreamTrans #11 0.02/0.01
- StreamTrans #47 (0.0/s, 0.03 of CPU): thunderbird-bin 0.64/0.99; swapper 0.35/0.00; StreamTrans #48 0.01/0.00
- StreamTrans #49 (0.0/s, 0.02 of CPU): thunderbird-bin 0.70/1.00; swapper 0.30/0.00
- StreamTrans #45 (0.0/s, 0.02 of CPU): thunderbird-bin 0.67/1.00; swapper 0.32/0.00; StreamTrans #46 0.01/0.00
- StreamTrans #52 (0.0/s, 0.02 of CPU): thunderbird-bin 0.68/1.00; swapper 0.32/0.00
- StreamTrans #51 (0.0/s, 0.02 of CPU): thunderbird-bin 0.65/0.99; swapper 0.35/0.01
- StreamTrans #50 (0.0/s, 0.02 of CPU): thunderbird-bin 0.64/0.98; swapper 0.28/0.00; StreamTrans #51 0.08/0.01

## thunderbird-send op
- thunderbird-bin (143.8/s, 0.80 of CPU): Xvfb 0.35/0.24; Socket Thread 0.31/0.13; Softwar~cThread 0.09/0.06; Timer 0.08/0.10; Compositor 0.06/0.02
- Renderer (27.7/s, 0.04 of CPU): SwComposite 0.38/0.09; WRRende~ckend#0 0.36/0.62; WRRende~ckend#1 0.15/0.13; Compositor 0.10/0.05; Xvfb 0.01/0.10
- TaskCon~ller #0 (15.4/s, 0.02 of CPU): thunderbird-bin 0.90/0.98; DOM Worker 0.05/0.00; TaskCon~ller #1 0.04/0.01; TaskCon~ller #2 0.01/0.01; TaskCon~ller #3 0.00/0.00
- WRRende~ckend#0 (10.4/s, 0.02 of CPU): Compositor 0.74/0.76; WRScene~ilder#0 0.26/0.24; Renderer 0.01/0.01; thunderbird-bin 0.00/0.00; glean.dispatche 0.00/0.00
- Compositor (219.2/s, 0.01 of CPU): Softwar~cThread 0.47/0.35; thunderbird-bin 0.25/0.32; Renderer 0.17/0.18; WRScene~ilder#0 0.06/0.04; Timer 0.02/0.10
- WRScene~ilder#0 (9.2/s, 0.01 of CPU): Compositor 0.99/0.99; Renderer 0.01/0.00; WRScene~derLP#0 0.00/0.00; Softwar~cThread 0.00/0.00; thunderbird-bin 0.00/0.00
- Socket Thread (90.1/s, 0.01 of CPU): thunderbird-bin 0.98/0.85; python3 0.02/0.15; TaskCon~ller #0 0.00/0.00; Timer 0.00/0.00; Softwar~cThread 0.00/0.00
- Softwar~cThread (26.2/s, 0.01 of CPU): swapper 0.63/0.81; thunderbird-bin 0.33/0.17; Compositor 0.01/0.00; TaskCon~ller #0 0.01/0.00; Socket Thread 0.01/0.00
