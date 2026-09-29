// A — 가상 시계 + 이벤트 큐. 태스크도 스케줄러도 없다.
// 근거: DES 의 전부는 "가장 이른 미래 사건을 꺼내고 시계를 거기로 점프"다 (guide §1).
// D1(§9.3) 동시각 tie-break = 삽입 순번. 비교자에서 seq 를 빼면 순서가 *미정의*가 되고
//         비협상 규칙 4(바이트 동일한 trace)가 죽는다 — README 의 양성 대조 참조.
#include <cassert>
#include <cstdint>
#include <cstdio>
#include <queue>
#include <vector>

using i64 = std::int64_t;

struct Event { i64 t; std::uint64_t seq; int what; };

struct Later {  // priority_queue 는 max-heap → 부호 반전
  bool operator()(const Event& a, const Event& b) const {
    return a.t != b.t ? a.t > b.t : a.seq > b.seq;
  }
};

class Sim {
 public:
  void push(i64 t, int what) { q_.push({t, seq_++, what}); }

  void run() {
    while (!q_.empty()) {
      const Event e = q_.top();
      q_.pop();
      assert(e.t >= now_);  // 시계는 뒤로 가지 않는다
      now_ = e.t;
      std::printf("t=%8lld  ev=%d\n", (long long)now_, e.what);
    }
  }

 protected:
  std::priority_queue<Event, std::vector<Event>, Later> q_;
  std::uint64_t seq_ = 0;
  i64 now_ = 0;
};

int main() {
  Sim s;
  for (int i = 0; i < 3; ++i) s.push(500, 10 + i);   // 동시각 3개
  s.push(100, 20);
  s.push(0, 30);
  s.push(100, 21);
  s.run();
}
