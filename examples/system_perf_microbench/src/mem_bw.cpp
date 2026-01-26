#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstring>
#include <iomanip>
#include <iostream>
#include <string>
#include <thread>
#include <vector>

#if defined(_WIN32)
#  include <malloc.h>
#endif

static void* aligned_alloc_64(size_t bytes) {
#if defined(_WIN32)
  return _aligned_malloc(bytes, 64);
#else
  void* p = nullptr;
  if (posix_memalign(&p, 64, bytes) != 0) return nullptr;
  return p;
#endif
}

static void aligned_free_64(void* p) {
#if defined(_WIN32)
  _aligned_free(p);
#else
  free(p);
#endif
}

static uint64_t now_ns() {
  return static_cast<uint64_t>(
      std::chrono::duration_cast<std::chrono::nanoseconds>(
          std::chrono::steady_clock::now().time_since_epoch())
          .count());
}

static uint64_t parse_u64(const char* s, uint64_t def) {
  if (!s) return def;
  try {
    return static_cast<uint64_t>(std::stoull(std::string(s)));
  } catch (...) {
    return def;
  }
}

int main(int argc, char** argv) {
  // Args: --size_mb N --iters N --threads N
  uint64_t size_mb = 256;
  uint64_t iters = 20;
  uint64_t threads = std::max<uint64_t>(1, std::thread::hardware_concurrency());

  for (int i = 1; i < argc; i++) {
    std::string a = argv[i];
    if (a == "--size_mb" && i + 1 < argc) size_mb = parse_u64(argv[++i], size_mb);
    else if (a == "--iters" && i + 1 < argc) iters = parse_u64(argv[++i], iters);
    else if (a == "--threads" && i + 1 < argc) threads = parse_u64(argv[++i], threads);
  }

  if (threads == 0) threads = 1;

  const uint64_t size_bytes = size_mb * 1024ull * 1024ull;
  if (size_bytes < 64) {
    std::cerr << "size_mb too small\n";
    return 2;
  }

  void* src_raw = aligned_alloc_64(static_cast<size_t>(size_bytes));
  void* dst_raw = aligned_alloc_64(static_cast<size_t>(size_bytes));
  if (!src_raw || !dst_raw) {
    std::cerr << "alloc failed\n";
    return 3;
  }

  auto* src = static_cast<uint8_t*>(src_raw);
  auto* dst = static_cast<uint8_t*>(dst_raw);
  for (uint64_t i = 0; i < size_bytes; i++) src[i] = static_cast<uint8_t>(i * 131u + 7u);

  // Warm-up
  std::memcpy(dst, src, static_cast<size_t>(size_bytes));

  const uint64_t chunk = (size_bytes + threads - 1) / threads;

  const uint64_t t0 = now_ns();
  for (uint64_t it = 0; it < iters; it++) {
    std::vector<std::thread> pool;
    pool.reserve(static_cast<size_t>(threads));
    for (uint64_t t = 0; t < threads; t++) {
      const uint64_t begin = t * chunk;
      const uint64_t end = std::min<uint64_t>(size_bytes, begin + chunk);
      pool.emplace_back([=]() {
        if (begin >= end) return;
        std::memcpy(dst + begin, src + begin, static_cast<size_t>(end - begin));
      });
    }
    for (auto& th : pool) th.join();
  }
  const uint64_t t1 = now_ns();

  const double elapsed_s = static_cast<double>(t1 - t0) / 1e9;
  const double total_bytes = static_cast<double>(size_bytes) * static_cast<double>(iters);
  const double gb_s = (total_bytes / (1024.0 * 1024.0 * 1024.0)) / elapsed_s;

  // Minimal JSON to stdout
  std::cout << "{\n";
  std::cout << "  \"size_mb\": " << size_mb << ",\n";
  std::cout << "  \"iters\": " << iters << ",\n";
  std::cout << "  \"threads\": " << threads << ",\n";
  std::cout << "  \"elapsed_ms\": " << std::fixed << std::setprecision(3) << (elapsed_s * 1000.0) << ",\n";
  std::cout << "  \"throughput_gb_s\": " << std::fixed << std::setprecision(3) << gb_s << "\n";
  std::cout << "}\n";

  aligned_free_64(src_raw);
  aligned_free_64(dst_raw);
  return 0;
}


