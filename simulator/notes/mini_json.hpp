// 최소 JSON 파서. 기계가 생성한 파일만 먹으므로 관대할 필요가 없다.
// 정수와 실수를 구분해 보관한다 — 시간은 정수 µs 여야 하고(비협상 규칙 3),
// 실수는 batch_bandwidth_cap 하나뿐이다.
#pragma once
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <map>
#include <sstream>
#include <string>
#include <vector>

[[noreturn]] inline void die(const std::string& m) {
  std::fprintf(stderr, "거부: %s\n", m.c_str());
  std::exit(2);   // 부분 수리 금지 — 파일 전체를 거부한다 (guide §3)
}

struct Json {
  enum class K { Null, Bool, Int, Real, Str, Arr, Obj } k = K::Null;
  bool b = false; std::int64_t i = 0; double d = 0; std::string s;
  std::vector<Json> arr; std::map<std::string, Json> obj;

  bool has(const char* key) const { return k == K::Obj && obj.count(key) != 0; }
  const Json& at(const char* key) const {
    auto it = obj.find(key);
    if (k != K::Obj || it == obj.end()) die(std::string("키 없음: ") + key);
    return it->second;
  }
  std::int64_t as_int(const char* w) const {
    if (k != K::Int) die(std::string(w) + ": 정수여야");
    return i;
  }
  double as_num(const char* w) const {
    if (k == K::Int) return (double)i;
    if (k != K::Real) die(std::string(w) + ": 숫자여야");
    return d;
  }
  const std::string& as_str(const char* w) const {
    if (k != K::Str) die(std::string(w) + ": 문자열이어야");
    return s;
  }
};

class JsonParser {
 public:
  explicit JsonParser(const std::string& t) : t_(t) {}
  Json parse() { skip(); return value(); }
 private:
  const std::string& t_; std::size_t p_ = 0;
  void skip() { while (p_ < t_.size() && (t_[p_]==' '||t_[p_]=='\n'||t_[p_]=='\r'||t_[p_]=='\t')) ++p_; }
  char peek() { return p_ < t_.size() ? t_[p_] : '\0'; }
  void want(char c) { if (peek() != c) die(std::string("JSON: '") + c + "' 기대"); ++p_; }
  Json value() {
    switch (peek()) {
      case '{': return object();
      case '[': return array();
      case '"': { Json v; v.k = Json::K::Str; v.s = str(); return v; }
      case 't': p_ += 4; { Json v; v.k = Json::K::Bool; v.b = true;  return v; }
      case 'f': p_ += 5; { Json v; v.k = Json::K::Bool; v.b = false; return v; }
      case 'n': p_ += 4; return Json{};
      default:  return number();
    }
  }
  Json object() {
    Json v; v.k = Json::K::Obj; want('{'); skip();
    if (peek() == '}') { ++p_; return v; }
    for (;;) { skip(); std::string key = str(); skip(); want(':'); skip();
               v.obj.emplace(std::move(key), value()); skip();
               if (peek() == ',') { ++p_; continue; } want('}'); return v; }
  }
  Json array() {
    Json v; v.k = Json::K::Arr; want('['); skip();
    if (peek() == ']') { ++p_; return v; }
    for (;;) { skip(); v.arr.push_back(value()); skip();
               if (peek() == ',') { ++p_; continue; } want(']'); return v; }
  }
  std::string str() {
    want('"'); std::string o;
    while (p_ < t_.size() && t_[p_] != '"') {
      if (t_[p_] == '\\') { ++p_;
        switch (t_[p_]) { case 'n': o += '\n'; break; case 't': o += '\t'; break;
                          case 'u': p_ += 4; o += '?'; break; default: o += t_[p_]; }
        ++p_;
      } else o += t_[p_++];
    }
    want('"'); return o;
  }
  Json number() {
    const std::size_t a = p_; bool real = false;
    if (peek() == '-') ++p_;
    while (p_ < t_.size()) { const char c = t_[p_];
      if (c >= '0' && c <= '9') { ++p_; continue; }
      if (c=='.'||c=='e'||c=='E'||c=='+'||c=='-') { real = true; ++p_; continue; } break; }
    const std::string tok = t_.substr(a, p_ - a);
    Json v;
    if (real) { v.k = Json::K::Real; v.d = std::strtod(tok.c_str(), nullptr); }
    else      { v.k = Json::K::Int;  v.i = std::strtoll(tok.c_str(), nullptr, 10); }
    return v;
  }
};

inline Json load_json(const std::string& path) {
  std::ifstream in(path, std::ios::binary);
  if (!in) die("파일을 열 수 없다: " + path);
  std::ostringstream ss; ss << in.rdbuf();
  const std::string text = ss.str();
  return JsonParser(text).parse();
}
