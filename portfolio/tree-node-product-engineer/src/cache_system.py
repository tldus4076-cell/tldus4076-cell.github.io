"""
O(1) Resource Cache System
===========================
시스템의 동작 원리와 효율성을 고민한 핵심 기능

Product Engineer 스킬: 코드를 짱찌만 만들지 않고 왜 빠른지 생각한다
"""

import time
from typing import Optional, Dict, Any
import json


class ResourceCache:
    """
    게임 서버에서 발생하는 가장 많은 작업: "자원 조회"
    모든 유닛 이동을 데이터베이스에 있는 매번 미는 것?
    => 대안: O(1) 캐시. 조회 1번으로 끝.
    
    내부: dict (hash table) = Python의 사전형 데이터추가자료구조
    시간 복잡도: get/set 모두 O(1)
    """
    
    def __init__(self, ttl: int = 300):
        self._store: Dict[str, Any] = {}
        self._expire: Dict[str, float] = {}
        self._ttl = ttl  # Time To Live (초)
        self._hits = 0
        self._misses = 0
    
    def set(self, key: str, value: Any) -> None:
        """캐시 저장 - O(1)
게임에서: 골드, 자원, 유닛 정보 등 빠른 최신화
        """
        self._store[key] = value
        self._expire[key] = time.time() + self._ttl
    
    def get(self, key: str) -> Optional[Any]:
        """캐시 조회 - O(1)
수시적인 조회를 메모리에서 증시 = 데이터베이스 부하 제거
        """
        if key not in self._store:
            self._misses += 1
            return None
        
        if time.time() > self._expire.get(key, 0):
            self._delete(key)
            self._misses += 1
            return None
        
        self._hits += 1
        return self._store[key]
    
    def _delete(self, key: str) -> None:
        self._store.pop(key, None)
        self._expire.pop(key, None)
    
    def stats(self) -> Dict[str, Any]:
        total = self._hits + self._misses
        hit_rate = self._hits / total if total > 0 else 0
        return {
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": round(hit_rate, 4),
            "entries": len(self._store),
            "memory_estimate_kb": round(len(self._store) * 0.1, 2)
        }
    
    def benchmark(self, count: int = 100000) -> Dict[str, float]:
        """성능 벤치마크: 대용량 작업 시간 측정
Product Engineer는 "쯧은지" 확인하고 문서화해야 함
        """
        # 쓰기 벤치마크
        t0 = time.perf_counter()
        for i in range(count):
            self.set(f"key_{i}", {"gold": i, "wood": i * 2})
        write_time = time.perf_counter() - t0
        
        # 읽기 벤치마크
        t0 = time.perf_counter()
        for i in range(count):
            self.get(f"key_{i}")
        read_time = time.perf_counter() - t0
        
        return {
            "write_ops_per_sec": round(count / write_time, 0),
            "read_ops_per_sec": round(count / read_time, 0),
            "avg_write_ms": round(write_time / count * 1000, 6),
            "avg_read_ms": round(read_time / count * 1000, 6),
            "total_ops": count
        }


if __name__ == "__main__":
    import sys
    
    cache = ResourceCache(ttl=60)
    
    if "--benchmark" in sys.argv:
        print("=" * 50)
        print("Cache System Benchmark")
        print("=" * 50)
        result = cache.benchmark(count=50000)
        for k, v in result.items():
            print(f"  {k}: {v}")
        print("=" * 50)
        print(f"Final Stats: {json.dumps(cache.stats(), indent=2)}")
    else:
        cache.set("player_001:gold", 1500)
        cache.set("player_001:wood", 800)
        print(f"gold = {cache.get('player_001:gold')}")
        print(f"wood = {cache.get('player_001:wood')}")
        print(f"stats = {cache.stats()}")
