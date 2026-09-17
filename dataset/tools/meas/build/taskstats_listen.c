/* taskstats_listen.c — exit-time accounting for every task that exits on a
 * set of CPUs (9.6 changelog D3; Linux Documentation/accounting/taskstats.rst).
 *
 *   taskstats_listen -m <cpumask> [-o <file>] [-r <rcvbuf-bytes>]
 *
 * Registers a taskstats listener for the cpumask (ascii ranges, e.g. "3" or
 * "1-3"), then writes one tab-separated row per record the kernel sends —
 * a per-pid row for every exiting thread and a per-tgid row when the last
 * thread of a thread group exits (the sum over its threads) — until SIGINT
 * or SIGTERM. Fields are the kernel's struct taskstats as the installed
 * <linux/taskstats.h> declares it; the kernel may send a newer, larger
 * struct, of which the declared prefix is read (fields are only appended
 * across versions). Times: CPU in microseconds (ac_utime, ac_stime), delays
 * in nanoseconds, elapsed in microseconds; the receive time is stamped on
 * CLOCK_MONOTONIC (perf sched's clock in the campaign) and CLOCK_REALTIME.
 * Delay fields are populated only when kernel.task_delayacct=1 was set
 * before the task started. Needs CAP_NET_ADMIN (run under sudo). Loss:
 * ENOBUFS on the socket is counted and reported on stderr and in the
 * trailer row; the receive buffer is raised with SO_RCVBUFFORCE.
 */
#define _GNU_SOURCE
#include <errno.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <sys/socket.h>
#include <linux/genetlink.h>
#include <linux/netlink.h>
#include <linux/taskstats.h>

#define GENLMSG_DATA(glh) ((void *)((char *)NLMSG_DATA(glh) + GENL_HDRLEN))
#define GENLMSG_PAYLOAD(glh) (NLMSG_PAYLOAD(glh, 0) - GENL_HDRLEN)
#define NLA_DATA(na) ((void *)((char *)(na) + NLA_HDRLEN))
#define NLA_PAYLOAD(len) ((len) - NLA_HDRLEN)

struct msgtemplate {
    struct nlmsghdr n;
    struct genlmsghdr g;
    char buf[4096];
};

static volatile sig_atomic_t stop_now = 0;
static void on_signal(int sig) { (void)sig; stop_now = 1; }

static int send_cmd(int sd, uint16_t nlmsg_type, uint32_t nlmsg_pid, uint8_t genl_cmd,
                    uint16_t nla_type, const void *nla_data, int nla_len)
{
    struct msgtemplate msg;
    struct nlattr *na;
    char *buf;
    int r, buflen;

    memset(&msg, 0, sizeof(msg));
    msg.n.nlmsg_len = NLMSG_LENGTH(GENL_HDRLEN);
    msg.n.nlmsg_type = nlmsg_type;
    msg.n.nlmsg_flags = NLM_F_REQUEST;
    msg.n.nlmsg_seq = 0;
    msg.n.nlmsg_pid = nlmsg_pid;
    msg.g.cmd = genl_cmd;
    msg.g.version = 0x1;
    na = (struct nlattr *)GENLMSG_DATA(&msg);
    na->nla_type = nla_type;
    na->nla_len = nla_len + NLA_HDRLEN;
    memcpy(NLA_DATA(na), nla_data, nla_len);
    msg.n.nlmsg_len += NLMSG_ALIGN(na->nla_len);

    buf = (char *)&msg;
    buflen = msg.n.nlmsg_len;
    while ((r = send(sd, buf, buflen, 0)) < buflen) {
        if (r > 0) { buf += r; buflen -= r; }
        else if (errno != EAGAIN) return -1;
    }
    return 0;
}

static int get_family_id(int sd)
{
    struct msgtemplate ans;
    struct nlattr *na;
    int rep_len;
    const char name[] = TASKSTATS_GENL_NAME;

    if (send_cmd(sd, GENL_ID_CTRL, getpid(), CTRL_CMD_GETFAMILY, CTRL_ATTR_FAMILY_NAME, name, sizeof(name)) < 0)
        return -1;
    rep_len = recv(sd, &ans, sizeof(ans), 0);
    if (rep_len < 0 || ans.n.nlmsg_type == NLMSG_ERROR || !NLMSG_OK(&ans.n, (unsigned)rep_len))
        return -1;
    na = (struct nlattr *)GENLMSG_DATA(&ans);
    na = (struct nlattr *)((char *)na + NLA_ALIGN(na->nla_len));   /* skip CTRL_ATTR_FAMILY_NAME */
    if (na->nla_type == CTRL_ATTR_FAMILY_ID)
        return *(uint16_t *)NLA_DATA(na);
    return -1;
}

static uint64_t now_ns(clockid_t c)
{
    struct timespec ts;
    clock_gettime(c, &ts);
    return (uint64_t)ts.tv_sec * 1000000000ull + (uint64_t)ts.tv_nsec;
}

static void print_header(FILE *out)
{
    fputs("recv_mono_ns\trecv_real_ns\ttype\tid\tversion\tpid\tppid\ttgid\tcomm\texitcode\tflag\tnice\tsched"
          "\tbtime_s\tetime_us\tutime_us\tstime_us\trun_real_ns\trun_virtual_ns"
          "\tcpu_count\tcpu_delay_ns\tblkio_count\tblkio_delay_ns\tswapin_count\tswapin_delay_ns"
          "\tfreepages_count\tfreepages_delay_ns\tthrashing_count\tthrashing_delay_ns"
          "\tnvcsw\tnivcsw\tminflt\tmajflt\tread_bytes\twrite_bytes\tcancelled_write_bytes\tread_char\twrite_char"
          "\thiwater_rss_kb\thiwater_vm_kb\n", out);
}

static void print_row(FILE *out, const char *type, uint32_t id, const struct taskstats *t, int len,
                      uint64_t mono, uint64_t real)
{
    /* fields past the declared struct or past what the kernel sent read as 0 */
    struct taskstats s;
    memset(&s, 0, sizeof(s));
    memcpy(&s, t, (size_t)len < sizeof(s) ? (size_t)len : sizeof(s));
    char comm[TS_COMM_LEN + 1];
    memcpy(comm, s.ac_comm, TS_COMM_LEN); comm[TS_COMM_LEN] = 0;
    for (char *p = comm; *p; p++) if (*p == '\t' || *p == '\n') *p = ' ';
    uint32_t tgid = 0;
    uint64_t thr_count = 0, thr_delay = 0;
#if TASKSTATS_VERSION >= 9
    thr_count = s.thrashing_count; thr_delay = s.thrashing_delay_total;
#endif
#if TASKSTATS_VERSION >= 12
    tgid = s.ac_tgid;
#endif
    fprintf(out,
            "%llu\t%llu\t%s\t%u\t%u\t%u\t%u\t%u\t%s\t%u\t%u\t%u\t%u"
            "\t%u\t%llu\t%llu\t%llu\t%llu\t%llu"
            "\t%llu\t%llu\t%llu\t%llu\t%llu\t%llu"
            "\t%llu\t%llu\t%llu\t%llu"
            "\t%llu\t%llu\t%llu\t%llu\t%llu\t%llu\t%llu\t%llu\t%llu"
            "\t%llu\t%llu\n",
            (unsigned long long)mono, (unsigned long long)real, type, id, s.version,
            s.ac_pid, s.ac_ppid, tgid, comm, s.ac_exitcode, s.ac_flag, s.ac_nice, s.ac_sched,
            s.ac_btime, (unsigned long long)s.ac_etime, (unsigned long long)s.ac_utime, (unsigned long long)s.ac_stime,
            (unsigned long long)s.cpu_run_real_total, (unsigned long long)s.cpu_run_virtual_total,
            (unsigned long long)s.cpu_count, (unsigned long long)s.cpu_delay_total,
            (unsigned long long)s.blkio_count, (unsigned long long)s.blkio_delay_total,
            (unsigned long long)s.swapin_count, (unsigned long long)s.swapin_delay_total,
            (unsigned long long)s.freepages_count, (unsigned long long)s.freepages_delay_total,
            (unsigned long long)thr_count, (unsigned long long)thr_delay,
            (unsigned long long)s.nvcsw, (unsigned long long)s.nivcsw,
            (unsigned long long)s.ac_minflt, (unsigned long long)s.ac_majflt,
            (unsigned long long)s.read_bytes, (unsigned long long)s.write_bytes, (unsigned long long)s.cancelled_write_bytes,
            (unsigned long long)s.read_char, (unsigned long long)s.write_char,
            (unsigned long long)s.hiwater_rss, (unsigned long long)s.hiwater_vm);
}

int main(int argc, char **argv)
{
    const char *cpumask = NULL, *outpath = NULL;
    int rcvbuf = 64 << 20;
    int opt;
    while ((opt = getopt(argc, argv, "m:o:r:")) != -1) {
        switch (opt) {
        case 'm': cpumask = optarg; break;
        case 'o': outpath = optarg; break;
        case 'r': rcvbuf = atoi(optarg); break;
        default: fprintf(stderr, "usage: %s -m <cpumask> [-o file] [-r rcvbuf]\n", argv[0]); return 2;
        }
    }
    if (!cpumask) { fprintf(stderr, "usage: %s -m <cpumask> [-o file] [-r rcvbuf]\n", argv[0]); return 2; }

    FILE *out = stdout;
    if (outpath) { out = fopen(outpath, "w"); if (!out) { perror("fopen"); return 1; } }

    int sd = socket(AF_NETLINK, SOCK_RAW, NETLINK_GENERIC);
    if (sd < 0) { perror("socket"); return 1; }
    if (setsockopt(sd, SOL_SOCKET, SO_RCVBUFFORCE, &rcvbuf, sizeof(rcvbuf)) < 0)
        if (setsockopt(sd, SOL_SOCKET, SO_RCVBUF, &rcvbuf, sizeof(rcvbuf)) < 0) perror("setsockopt SO_RCVBUF");
    struct sockaddr_nl local;
    memset(&local, 0, sizeof(local));
    local.nl_family = AF_NETLINK;
    if (bind(sd, (struct sockaddr *)&local, sizeof(local)) < 0) { perror("bind"); return 1; }

    int family = get_family_id(sd);
    if (family < 0) { fprintf(stderr, "taskstats family not found (CONFIG_TASKSTATS?)\n"); return 1; }
    uint32_t mypid = getpid();
    if (send_cmd(sd, family, mypid, TASKSTATS_CMD_GET, TASKSTATS_CMD_ATTR_REGISTER_CPUMASK, cpumask, strlen(cpumask) + 1) < 0) {
        perror("register cpumask"); return 1;
    }
    int actual = 0; socklen_t al = sizeof(actual);
    getsockopt(sd, SOL_SOCKET, SO_RCVBUF, &actual, &al);
    fprintf(stderr, "taskstats_listen: family %d, cpumask %s, rcvbuf %d, header version %d, pid %u\n",
            family, cpumask, actual, TASKSTATS_VERSION, mypid);

    signal(SIGINT, on_signal);
    signal(SIGTERM, on_signal);
    print_header(out);
    fprintf(out, "# started_mono_ns=%llu started_real_ns=%llu cpumask=%s rcvbuf=%d header_version=%d\n",
            (unsigned long long)now_ns(CLOCK_MONOTONIC), (unsigned long long)now_ns(CLOCK_REALTIME), cpumask, actual, TASKSTATS_VERSION);
    fflush(out);

    unsigned long rows = 0, enobufs = 0, errs = 0;
    static char rbuf[1 << 16];
    while (!stop_now) {
        int rep_len = recv(sd, rbuf, sizeof(rbuf), 0);
        uint64_t mono = now_ns(CLOCK_MONOTONIC), real = now_ns(CLOCK_REALTIME);
        if (rep_len < 0) {
            if (errno == EINTR) continue;
            if (errno == ENOBUFS) { enobufs++; fprintf(stderr, "taskstats_listen: ENOBUFS (%lu)\n", enobufs); continue; }
            perror("recv"); errs++; if (errs > 100) break; continue;
        }
        struct nlmsghdr *nh = (struct nlmsghdr *)rbuf;
        for (; NLMSG_OK(nh, (unsigned)rep_len); nh = NLMSG_NEXT(nh, rep_len)) {
            if (nh->nlmsg_type == NLMSG_ERROR) {   /* an ack (error 0) answers the register command; anything else is an error */
                struct nlmsgerr *e = (struct nlmsgerr *)NLMSG_DATA(nh);
                if (e->error != 0) { errs++; fprintf(stderr, "taskstats_listen: netlink error %d\n", e->error); }
                continue;
            }
            if (nh->nlmsg_type != family) continue;
            struct nlattr *na = (struct nlattr *)GENLMSG_DATA(nh);
            int len = 0, total = GENLMSG_PAYLOAD(nh);
            while (len < total) {
                int nla_len = NLA_ALIGN(na->nla_len);
                if (na->nla_type == TASKSTATS_TYPE_AGGR_PID || na->nla_type == TASKSTATS_TYPE_AGGR_TGID) {
                    const char *type = na->nla_type == TASKSTATS_TYPE_AGGR_PID ? "pid" : "tgid";
                    int inner_len = NLA_PAYLOAD(na->nla_len), off = 0;
                    struct nlattr *in = (struct nlattr *)NLA_DATA(na);
                    uint32_t id = 0;
                    while (off < inner_len) {
                        int l = NLA_ALIGN(in->nla_len);
                        if (in->nla_type == TASKSTATS_TYPE_PID || in->nla_type == TASKSTATS_TYPE_TGID)
                            id = *(uint32_t *)NLA_DATA(in);
                        else if (in->nla_type == TASKSTATS_TYPE_STATS) {
                            print_row(out, type, id, (struct taskstats *)NLA_DATA(in), NLA_PAYLOAD(in->nla_len), mono, real);
                            rows++;
                        }
                        off += l; in = (struct nlattr *)((char *)in + l);
                    }
                }
                len += nla_len; na = (struct nlattr *)((char *)na + nla_len);
            }
        }
    }
    send_cmd(sd, family, mypid, TASKSTATS_CMD_GET, TASKSTATS_CMD_ATTR_DEREGISTER_CPUMASK, cpumask, strlen(cpumask) + 1);
    fprintf(out, "# stopped_mono_ns=%llu rows=%lu enobufs=%lu errors=%lu\n",
            (unsigned long long)now_ns(CLOCK_MONOTONIC), rows, enobufs, errs);
    fflush(out);
    fprintf(stderr, "taskstats_listen: rows=%lu enobufs=%lu errors=%lu\n", rows, enobufs, errs);
    if (out != stdout) fclose(out);
    close(sd);
    return 0;
}
