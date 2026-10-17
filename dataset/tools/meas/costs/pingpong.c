/* pingpong.c — loads for the 9.12 kernel-cost campaign (research-slice changelog D31). Run each under
 * `taskset -c <cpu>` so every process it makes shares one CPU.
 *
 *   pingpong pair N     two processes pass one byte back and forth over two pipes, N round trips: each round
 *                       trip is two context switches and, per process, one write and one blocking read
 *                       (Li, Ding & Shen, ExpCS 2007, Ousterhout's method). Prints ns per round trip and the
 *                       system's context switches over the timed loop (/proc/stat ctxt).
 *   pingpong self N     one process writes one byte to its own pipe and reads it back, N times: the same two
 *                       calls with no switch. Prints ns per write+read pair.
 *   pingpong sleep N U  N sleeps of U µs: each sleep leaves the CPU with nothing runnable, so the fair class's
 *                       pick runs its idle path.
 *   pingpong getpid N   N getpid system calls: the tracer's calibration load.
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <sys/wait.h>

static unsigned long long ctxt(void) {
    FILE *f = fopen("/proc/stat", "r");
    char line[256];
    unsigned long long v = 0;
    if (!f) return 0;
    while (fgets(line, sizeof line, f))
        if (strncmp(line, "ctxt ", 5) == 0) { v = strtoull(line + 5, NULL, 10); break; }
    fclose(f);
    return v;
}

static double ns_since(const struct timespec *t0) {
    struct timespec t1;
    clock_gettime(CLOCK_MONOTONIC, &t1);
    return (t1.tv_sec - t0->tv_sec) * 1e9 + (t1.tv_nsec - t0->tv_nsec);
}

static int pair(long n) {
    int p2c[2], c2p[2];
    char b = 'x';
    if (pipe(p2c) || pipe(c2p)) { perror("pipe"); return 1; }
    pid_t pid = fork();
    if (pid < 0) { perror("fork"); return 1; }
    if (pid == 0) {
        for (long i = 0; i < n + 1; i++) {
            if (read(p2c[0], &b, 1) != 1) _exit(1);
            if (write(c2p[1], &b, 1) != 1) _exit(1);
        }
        _exit(0);
    }
    /* one untimed round trip: the child is running and both pipes are warm before the clock starts */
    if (write(p2c[1], &b, 1) != 1 || read(c2p[0], &b, 1) != 1) return 1;
    unsigned long long c0 = ctxt();
    struct timespec t0;
    clock_gettime(CLOCK_MONOTONIC, &t0);
    for (long i = 0; i < n; i++) {
        if (write(p2c[1], &b, 1) != 1) return 1;
        if (read(c2p[0], &b, 1) != 1) return 1;
    }
    double ns = ns_since(&t0);
    unsigned long long c1 = ctxt();
    int status = 0;
    waitpid(pid, &status, 0);
    printf("mode=pair n=%ld total_ns=%.0f ns_per_round_trip=%.3f ctxt_delta=%llu child_status=%d\n",
           n, ns, ns / n, c1 - c0, status);
    return 0;
}

static int self(long n) {
    int p[2];
    char b = 'x';
    if (pipe(p)) { perror("pipe"); return 1; }
    if (write(p[1], &b, 1) != 1 || read(p[0], &b, 1) != 1) return 1;
    struct timespec t0;
    clock_gettime(CLOCK_MONOTONIC, &t0);
    for (long i = 0; i < n; i++) {
        if (write(p[1], &b, 1) != 1) return 1;
        if (read(p[0], &b, 1) != 1) return 1;
    }
    double ns = ns_since(&t0);
    printf("mode=self n=%ld total_ns=%.0f ns_per_pair=%.3f\n", n, ns, ns / n);
    return 0;
}

static int sleeper(long n, long us) {
    struct timespec d = { us / 1000000, (us % 1000000) * 1000 }, t0;
    clock_gettime(CLOCK_MONOTONIC, &t0);
    for (long i = 0; i < n; i++) nanosleep(&d, NULL);
    printf("mode=sleep n=%ld us=%ld total_ns=%.0f\n", n, us, ns_since(&t0));
    return 0;
}

static int getpids(long n) {
    struct timespec t0;
    clock_gettime(CLOCK_MONOTONIC, &t0);
    for (long i = 0; i < n; i++) syscall(SYS_getpid);
    double ns = ns_since(&t0);
    printf("mode=getpid n=%ld total_ns=%.0f ns_per_call=%.3f\n", n, ns, ns / n);
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: %s pair|self|getpid N | sleep N US\n", argv[0]); return 2; }
    long n = atol(argv[2]);
    if (!strcmp(argv[1], "pair")) return pair(n);
    if (!strcmp(argv[1], "self")) return self(n);
    if (!strcmp(argv[1], "getpid")) return getpids(n);
    if (!strcmp(argv[1], "sleep") && argc > 3) return sleeper(n, atol(argv[3]));
    fprintf(stderr, "unknown mode %s\n", argv[1]);
    return 2;
}
