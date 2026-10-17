# Idealised (uncontended) trace of interbench emulate_x + periodic_schedule, units = ms
def run(cycles=3, verbose=False):
    t = 0; d = 0
    for c in range(cycles):
        cyc_start = t; run_total = 0; sleep_total = 0; met = 0; missed = 0; skipped = 0
        steps = []
        for i in range(0, 101):
            j = 100 - i
            ts = t
            if j and t > d + j:            # missed before burning
                d += j; k = (t - d)//j + 1; missed += k; d += k*j
                sl = d - t; t = d; sleep_total += sl; skipped += 1
                steps.append((i, 0, sl)); d += i; continue
            t += i; run_total += i
            d += j
            if d >= t:
                met += 1
            elif j:
                k = (t - d)//j + 1; missed += k; d += k*j
            else:
                d = t; steps.append((i, i, 0)); d += i; continue
            sl = d - t; t = d; sleep_total += sl
            steps.append((i, i, sl))
            d += i
        el = t - cyc_start
        print(f"cycle {c}: elapsed={el}ms run={run_total}ms sleep={sleep_total}ms cpu={run_total/el:.4f} met={met} missed={missed} skipped={skipped}")
        if verbose and c == 0:
            print([s for s in steps if s[0] in (0,1,2,3,10,25,49,50,51,75,90,98,99,100)])
run(4, True)
