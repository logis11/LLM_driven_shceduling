
## chrome idle: 38 repeats, app CPU share 0.003; whole tree timer 1.00/1.00, input 0.00/0.00, ext 0.00/0.00, irq 0.00/0.00, unknown 0.00/0.00, none 0.00/0.00
| component | wakes/s | CPU share of app | timer | input | x | ext | irq | unknown | none |
|---|---|---|---|---|---|---|---|---|---|
| gpu/VizCompositorTh | 12.1 | 0.31 | 1.00/1.00 | 0.00/0.00 |  | 0.00/0.00 | 0.00/0.00 | 0.00/0.00 |  |
| renderer/Compositor | 12.7 | 0.30 | 1.00/1.00 | 0.00/0.00 |  | 0.00/0.00 | 0.00/0.00 | 0.00/0.00 |  |
| renderer/chrome | 7.4 | 0.19 | 1.00/1.00 | 0.00/0.00 |  | 0.00/0.00 | 0.00/0.00 | 0.00/0.00 | 0.00/0.00 |
| gpu/Chrome_ChildIOT | 7.6 | 0.08 | 1.00/1.00 | 0.00/0.00 |  | 0.00/0.00 | 0.00/0.00 | 0.00/0.00 |  |
| chrome | 0.8 | 0.04 | 1.00/1.00 | 0.00/0.00 |  | 0.00/0.00 | 0.00/0.00 |  |  |
| MemoryInfra | 0.1 | 0.03 | 1.00/1.00 |  |  | 0.00/0.00 |  |  |  |
| utility/chrome | 0.8 | 0.02 | 1.00/1.00 | 0.00/0.00 |  | 0.00/0.00 | 0.00/0.00 |  |  |
| gpu/chrome | 0.3 | 0.01 | 1.00/1.00 | 0.00/0.00 |  | 0.00/0.00 |  |  |  |

## chrome op: 38 repeats, app CPU share 0.039; whole tree timer 0.36/0.27, input 0.64/0.73, ext 0.00/0.00, irq 0.00/0.00
| component | wakes/s | CPU share of app | timer | input | x | ext | irq | unknown | none |
|---|---|---|---|---|---|---|---|---|---|
| renderer/chrome | 5.2 | 0.52 | 0.49/0.19 | 0.51/0.81 |  | 0.00/0.00 | 0.00/0.00 |  |  |
| renderer/ThreadPoolForeg | 18.0 | 0.19 | 0.37/0.38 | 0.63/0.62 |  | 0.00/0.00 | 0.00/0.00 |  |  |
| chrome | 19.0 | 0.11 | 0.59/0.38 | 0.41/0.62 |  | 0.00/0.00 | 0.00/0.00 |  |  |
| gpu/VizCompositorTh | 8.2 | 0.09 | 0.42/0.29 | 0.58/0.71 |  | 0.00/0.00 | 0.00/0.00 |  |  |
| Chrome_IOThread | 28.2 | 0.02 | 0.24/0.27 | 0.75/0.73 |  | 0.00/0.00 | 0.00/0.00 |  |  |
| utility/Chrome_ChildIOT | 3.8 | 0.02 | 0.12/0.12 | 0.87/0.88 |  | 0.00/0.01 | 0.00/0.00 |  |  |
| renderer/Compositor | 6.7 | 0.01 | 0.22/0.18 | 0.78/0.82 |  | 0.00/0.00 | 0.00/0.00 |  |  |
| ThreadPoolForeg | 9.6 | 0.01 | 0.38/0.50 | 0.57/0.45 |  | 0.00/0.00 | 0.05/0.05 |  |  |
| renderer/Chrome_ChildIOT | 15.4 | 0.01 | 0.18/0.19 | 0.82/0.81 |  | 0.00/0.00 | 0.00/0.00 |  |  |

## code idle: 44 repeats, app CPU share 0.015; whole tree timer 0.99/1.00, input 0.00/0.00, ext 0.00/0.00, irq 0.00/0.00, none 0.00/0.00
| component | wakes/s | CPU share of app | timer | input | x | ext | irq | unknown | none |
|---|---|---|---|---|---|---|---|---|---|
| gpu/VizCompositorTh | 23.1 | 0.37 | 1.00/1.00 | 0.00/0.00 |  | 0.00/0.00 | 0.00/0.00 |  |  |
| renderer/code | 19.5 | 0.33 | 1.00/1.00 | 0.00/0.00 |  | 0.00/0.00 | 0.00/0.00 |  | 0.00/0.00 |
| renderer/Compositor | 22.8 | 0.12 | 1.00/1.00 | 0.00/0.00 |  | 0.00/0.00 | 0.00/0.00 |  |  |
| utility/code | 12.6 | 0.04 | 1.00/1.00 | 0.00/0.00 |  | 0.00/0.00 | 0.00/0.00 |  |  |
| gpu/Chrome_ChildIOT | 20.2 | 0.03 | 1.00/1.00 | 0.00/0.00 |  | 0.00/0.00 | 0.00/0.00 |  |  |
| V8Worker | 0.2 | 0.03 | 0.96/0.99 |  |  | 0.00/0.01 | 0.03/0.00 |  |  |
| code | 3.6 | 0.03 | 0.95/0.98 | 0.00/0.00 |  | 0.00/0.00 | 0.05/0.02 |  |  |
| renderer/ThreadPoolForeg | 3.4 | 0.03 | 0.99/1.00 | 0.00/0.00 |  | 0.00/0.00 | 0.00/0.00 |  | 0.00/0.00 |
| utility/libuv-worker | 5.8 | 0.00 | 1.00/1.00 | 0.00/0.00 |  | 0.00/0.00 | 0.00/0.00 |  |  |

## gimp driven: 5 repeats, app CPU share 0.003; whole tree timer 0.27/0.05, input 0.73/0.95, ext 0.00/0.00, irq 0.00/0.00
| component | wakes/s | CPU share of app | timer | input | x | ext | irq | unknown | none |
|---|---|---|---|---|---|---|---|---|---|
| gimp | 8.6 | 1.00 | 0.27/0.05 | 0.73/0.95 |  | 0.00/0.00 | 0.00/0.00 |  |  |

## gimp op: 5 repeats, app CPU share 0.233; whole tree timer 0.15/0.00, input 0.85/0.99, ext 0.00/0.00, irq 0.00/0.01
| component | wakes/s | CPU share of app | timer | input | x | ext | irq | unknown | none |
|---|---|---|---|---|---|---|---|---|---|
| gimp | 2.2 | 0.92 | 0.24/0.00 | 0.76/0.99 |  |  | 0.00/0.01 |  |  |
| async | 0.1 | 0.08 |  | 0.99/0.99 |  |  | 0.01/0.01 |  |  |

## kdenlive driven: 20 repeats, app CPU share 0.372; whole tree timer 0.89/0.88, input 0.11/0.12, ext 0.00/0.00, irq 0.00/0.00
| component | wakes/s | CPU share of app | timer | input | x | ext | irq | unknown | none |
|---|---|---|---|---|---|---|---|---|---|
| kdenlive | 136.6 | 1.00 | 0.92/0.88 | 0.08/0.12 |  | 0.00/0.00 | 0.00/0.00 |  |  |
| QXcbEventQueue | 72.8 | 0.00 | 0.87/0.85 | 0.13/0.15 |  | 0.00/0.00 | 0.00/0.00 |  |  |

## kdenlive op: 20 repeats, app CPU share 0.496; whole tree timer 0.00/0.00, input 0.99/1.00, ext 0.00/0.00, irq 0.00/0.00
| component | wakes/s | CPU share of app | timer | input | x | ext | irq | unknown | none |
|---|---|---|---|---|---|---|---|---|---|
| kdenlive_render | 317.7 | 0.94 |  | 1.00/1.00 |  |  | 0.00/0.00 |  |  |
| kdenlive | 6.2 | 0.05 | 0.14/0.04 | 0.86/0.95 |  | 0.00/0.00 | 0.00/0.00 |  |  |

## soffice idle: 14 repeats, app CPU share 0.001; whole tree timer 1.00/1.00, input 0.00/0.00, ext 0.00/0.00, irq 0.00/0.00
| component | wakes/s | CPU share of app | timer | input | x | ext | irq | unknown | none |
|---|---|---|---|---|---|---|---|---|---|
| soffice.bin | 3.5 | 1.00 | 1.00/1.00 | 0.00/0.00 |  | 0.00/0.00 | 0.00/0.00 |  |  |

## thunderbird-send driven: 8 repeats, app CPU share 0.009; whole tree timer 0.82/0.55, input 0.18/0.45, ext 0.00/0.00, irq 0.00/0.00
| component | wakes/s | CPU share of app | timer | input | x | ext | irq | unknown | none |
|---|---|---|---|---|---|---|---|---|---|
| thunderbird-bin | 12.6 | 0.48 | 0.58/0.36 | 0.42/0.64 |  | 0.00/0.00 | 0.00/0.00 |  |  |
| Compositor | 89.7 | 0.10 | 0.89/0.83 | 0.10/0.17 |  | 0.00/0.00 | 0.00/0.00 |  |  |
| Renderer | 4.4 | 0.09 | 0.68/0.58 | 0.32/0.42 |  | 0.00/0.00 | 0.00/0.00 |  |  |
| Softwar~cThread | 17.2 | 0.09 | 0.87/0.96 | 0.13/0.04 |  | 0.00/0.00 | 0.00/0.00 |  |  |
| WRRende~ckend#1 | 2.4 | 0.06 | 0.43/0.53 | 0.57/0.47 |  | 0.00/0.00 | 0.00/0.00 |  |  |
| WRScene~ilder#1 | 1.7 | 0.04 | 0.19/0.20 | 0.81/0.80 |  | 0.00/0.00 |  |  |  |
| glean.dispatche | 4.3 | 0.02 | 0.38/0.42 | 0.62/0.58 |  | 0.00/0.00 | 0.00/0.00 |  |  |
| Timer | 5.0 | 0.02 | 0.80/0.94 | 0.20/0.06 |  | 0.00/0.00 | 0.00/0.00 |  |  |

## thunderbird-send idle: 43 repeats, app CPU share 0.001; whole tree timer 0.99/1.00, input 0.00/0.00, ext 0.00/0.00, irq 0.00/0.00
| component | wakes/s | CPU share of app | timer | input | x | ext | irq | unknown | none |
|---|---|---|---|---|---|---|---|---|---|
| thunderbird-bin | 0.4 | 0.15 | 0.99/1.00 |  |  | 0.00/0.00 | 0.00/0.00 |  |  |
| WebExtensions/WebExtensions | 0.2 | 0.03 | 1.00/1.00 | 0.00/0.00 |  | 0.00/0.00 |  |  |  |
| StreamTrans #47 | 0.0 | 0.03 | 1.00/1.00 |  |  |  |  |  |  |
| StreamTrans #49 | 0.0 | 0.02 | 1.00/1.00 |  |  |  |  |  |  |
| StreamTrans #45 | 0.0 | 0.02 | 0.99/0.95 |  |  |  | 0.01/0.05 |  |  |
| StreamTrans #52 | 0.0 | 0.02 | 1.00/1.00 |  |  |  |  |  |  |
| StreamTrans #51 | 0.0 | 0.02 | 1.00/1.00 |  |  |  |  |  |  |
| StreamTrans #50 | 0.0 | 0.02 | 1.00/1.00 |  |  |  |  |  |  |
| WebExtensions/StreamTrans #12 | 0.0 | 0.02 | 1.00/1.00 |  |  |  |  |  |  |
| WebExtensions/StreamTrans #15 | 0.0 | 0.02 | 1.00/1.00 |  |  |  |  |  |  |

## thunderbird-send op: 8 repeats, app CPU share 0.188; whole tree timer 0.59/0.42, input 0.40/0.58, ext 0.00/0.00, irq 0.01/0.01
| component | wakes/s | CPU share of app | timer | input | x | ext | irq | unknown | none |
|---|---|---|---|---|---|---|---|---|---|
| thunderbird-bin | 143.8 | 0.80 | 0.38/0.36 | 0.61/0.64 |  | 0.00/0.00 | 0.00/0.01 |  |  |
| Renderer | 27.7 | 0.04 | 0.68/0.63 | 0.31/0.36 |  | 0.00/0.00 | 0.01/0.01 |  |  |
| TaskCon~ller #0 | 15.4 | 0.02 | 0.66/0.80 | 0.33/0.20 |  | 0.00/0.00 | 0.01/0.00 |  |  |
| WRRende~ckend#0 | 10.4 | 0.02 | 0.72/0.73 | 0.28/0.26 |  | 0.00/0.00 | 0.00/0.01 |  |  |
| Compositor | 219.2 | 0.01 | 0.73/0.71 | 0.26/0.28 |  | 0.00/0.00 | 0.00/0.01 |  |  |
| WRScene~ilder#0 | 9.2 | 0.01 | 0.63/0.57 | 0.36/0.42 |  | 0.00/0.00 | 0.01/0.01 |  |  |
| Socket Thread | 90.1 | 0.01 | 0.06/0.05 | 0.94/0.95 |  | 0.00/0.00 | 0.00/0.00 |  |  |
| Softwar~cThread | 26.2 | 0.01 | 0.75/0.86 | 0.24/0.14 |  | 0.00/0.00 | 0.00/0.00 |  |  |
