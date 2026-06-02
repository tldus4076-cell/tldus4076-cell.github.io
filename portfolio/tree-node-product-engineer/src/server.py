"""
Mini RTS Game Server - 실시간 매칭 & 전투 서버
=====================================================
AI 시대 Product Engineer 포트폴리오 핵심 코드
목표: 실시간 통신 + 이벤트 기반 아키텍처 + 효율적인 자원 관리
"""

import asyncio
import json
import time
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
import websockets
from websockets.server import WebSocketServerProtocol

from cache_system import ResourceCache
from event_bus import EventBus


# =========================================================
# 주요 설계 결정: 이벤트 기반 아키텍처
# 왜? 방 수 게임은 상태 변경이 많아서 이벤트 기반이 더 유연함
# =========================================================

@dataclass
class Player:
    """게임 플레이어 모델 - 동기 적용을 위해 dataclass 사용"""
    player_id: str
    name: str
    level: int = 1
    resources: Dict[str, int] = None
    
    def __post_init__(self):
        if self.resources is None:
            self.resources = {"gold": 1000, "wood": 500, "stone": 300}


class MatchRoom:
    """매칭 룸 - 2명의 플레이어를 매칭시켜 실시간 전투를 진행"""
    def __init__(self, room_id: str):
        self.room_id = room_id
        self.players: List[WebSocketServerProtocol] = []
        self.started = False
        self.created_at = time.time()
    
    def add_player(self, ws: WebSocketServerProtocol) -> bool:
        if len(self.players) >= 2:
            return False
        self.players.append(ws)
        if len(self.players) == 2:
            self.started = True
        return True


class GameServer:
    """게임 서버 핵심 클래스
    각 기능은 도메인 분리: 매칭, 캐시, 이벤트 = 당연한 별도 모듈
    Product Engineer는 이런 경계 분리를 "어떻게 지으나?"를 고민해야 함
    """
    
    def __init__(self):
        # 오늘날의 게임 서버에서 자주 사용하는 자료구조 선택:
        # dict + list? NO. 이벤트 버스 + O(1) 캐시. WHY? 상태 관리가 쾌음
        self.event_bus = EventBus()
        self.cache = ResourceCache()  # O(1) 캐시
        
        self.players: Dict[str, Player] = {}
        self.rooms: Dict[str, MatchRoom] = {}
        self.connected: Dict[str, WebSocketServerProtocol] = {}
        
        self._setup_event_handlers()
    
    def _setup_event_handlers(self):
        """이벤트 버스에 핸들러 등록
- 게임 서버에서 발생하는 모든 주요 일을 이벤트로 처리
- 동기 로직을 지옥 + 모듈 도르 경계 선명히
"""
        @self.event_bus.on("player_join")
        async def on_player_join(data):
            player_id = data["player_id"]
            name = data["name"]
            self.players[player_id] = Player(player_id=player_id, name=name)
            print(f"[이벤트] 플레이어 입장: {name} ({player_id})")
        
        @self.event_bus.on("match_request")
        async def on_match_request(data):
            player_id = data["player_id"]
            room = self._find_or_create_room()
            # 비즈니스: 매칭 요청 자체를 이벤트로 취급하여 비동기 처리
            await self.event_bus.emit("match_found", {
                "room_id": room.room_id,
                "player_id": player_id
            })
        
        @self.event_bus.on("resource_update")
        async def on_resource_update(data):
            # 성능 핵심: 캐시를 통해 자원 변경 사항 즉시 반영
            player_id = data["player_id"]
            resource = data["resource"]
            amount = data["amount"]
            self.cache.set(f"res:{player_id}:{resource}", amount)
    
    def _find_or_create_room(self) -> MatchRoom:
        for room in self.rooms.values():
            if not room.started and len(room.players) < 2:
                return room
        new_room = MatchRoom(f"room_{int(time.time()*1000)}")
        self.rooms[new_room.room_id] = new_room
        return new_room
    
    async def handle_client(self, ws: WebSocketServerProtocol, path: str):
        """개발 계기록의 프로토타입이자 출시를 알려주는 부분
- 연결 → 인증 → 이벤트 발행 → 단련변 큐 처리
"""
        player_id = None
        try:
            async for message in ws:
                data = json.loads(message)
                action = data.get("action")
                
                if action == "auth":
                    player_id = data["player_id"]
                    self.connected[player_id] = ws
                    await self.event_bus.emit("player_join", data)
                    await ws.send(json.dumps({"type": "auth_ok", "player_id": player_id}))
                
                elif action == "match":
                    await self.event_bus.emit("match_request", data)
                    await ws.send(json.dumps({"type": "match_queued"}))
                
                elif action == "get_resource":
                    # O(1) 캐시 조회 - 데이터베이스 질의보다 1000배 빠름
                    val = self.cache.get(f"res:{player_id}:{data['resource']}")
                    await ws.send(json.dumps({
                        "type": "resource_data",
                        "resource": data["resource"],
                        "amount": val
                    }))
                
                elif action == "update_resource":
                    await self.event_bus.emit("resource_update", {
                        "player_id": player_id,
                        "resource": data["resource"],
                        "amount": data["amount"]
                    })
                    await ws.send(json.dumps({"type": "resource_updated"}))
                
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            if player_id:
                self.connected.pop(player_id, None)
                self.players.pop(player_id, None)
                print(f"[이벤트] 플레이어 종료: {player_id}")
    
    async def start(self, host="0.0.0.0", port=8765):
        print(f"[확장] 게임 서버 시작 - ws://{host}:{port}")
        async with websockets.serve(self.handle_client, host, port):
            await asyncio.Future()  # 영구 실행


# =========================================================
# 실행 진입점
# =========================================================
if __name__ == "__main__":
    server = GameServer()
    asyncio.run(server.start())
