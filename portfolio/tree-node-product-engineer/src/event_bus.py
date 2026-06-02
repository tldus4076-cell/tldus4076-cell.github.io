"""
Event Bus - 이벤트 기반 아키텍처
============================
시스템 동작 원리와 효율성을 고민한 설계

Product Engineer 필요 스킬: 도메인 간 물리 흘림을 이벤트로 제어
"""

import asyncio
from typing import Dict, List, Callable, Any
from collections import defaultdict


class EventBus:
    """
    룰 닷 게임의 검증: 방수 게임은 상태 변경이 많음
    대안: 도메인 간 직접 호출이 아닌 이벤트 발행/구독
    
    이점: 추가/삭제가 쉽고, 이벤트 대길이증가 가능, 단위테스트 쉽겟
    """
    
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = defaultdict(list)
        self._event_count = 0
    
    def on(self, event_type: str):
        """디코레이터: 이벤트 구독 등록

사용법:
    @event_bus.on("player_join")
    async def handler(data):
        ...
        """
        def decorator(func: Callable):
            self._handlers[event_type].append(func)
            return func
        return decorator
    
    async def emit(self, event_type: str, data: Any = None) -> None:
        """이벤트 발행 - 모든 구독자에게 비동기 전달
        
        비즈니스: 동기 로직을 비동기로 바꾼 이유
        - 플레이어 매칭: 2명이 동시에 요청 가능
        - 이벤트 대길: 발행되기만 하면 소비되지 않음
        """
        self._event_count += 1
        handlers = self._handlers.get(event_type, [])
        if not handlers:
            return
        
        # 비동기: 모든 핸들러를 동시에 실행
        await asyncio.gather(
            *[h(data) for h in handlers],
            return_exceptions=True
        )
    
    def stats(self) -> Dict[str, Any]:
        return {
            "registered_events": list(self._handlers.keys()),
            "total_handlers": sum(len(h) for h in self._handlers.values()),
            "emitted_count": self._event_count
        }


if __name__ == "__main__":
    bus = EventBus()
    
    @bus.on("test")
    async def handler_a(data):
        print(f"A 받음: {data}")
    
    @bus.on("test")
    async def handler_b(data):
        print(f"B 받음: {data}")
    
    async def demo():
        await bus.emit("test", {"msg": "hello"})
        print(f"stats: {bus.stats()}")
    
    asyncio.run(demo())
