# 🌳 Tree Node Product Engineer Portfolio
> AI 시대 Product Engineer 지원을 위한 포트폴리오
> 프로젝트명: "AI 협업 게임 서버 시스템"

---

## 📌 이 포트폴리오가 보여주는 것

| Tree Node 요구사항 | 이 포트폴리오의 답변 |
|---|---|
| **AI 에이전트와 긴밀하게 협업** | 전체 개발 과정에 AI(CLAUDE/GPT)를 활용한 기록 |
| **시스템의 동작 원리와 효율성 고민** | O(1) 캐싱, 비동기 처리, 이벤트 기반 아키텍처 설계 |
| **비즈니스 가치 창출** | 게임 운영자 관점의 실시간 대시보드 + 자동화 시스템 |
| **논리적 사고 + 소통** | README, API 문서, 아키텍처 다이어그램 |

---

## 🏗️ 프로젝트 구조

```
tree-node-product-engineer/
├── README.md              ← 지금 보는 파일
├── src/
│   ├── server.py          ← 게임 서버 핵심 (async 기반)
│   ├── cache_system.py    ← O(1) 캐싱 시스템
│   ├── event_bus.py       ← 이벤트 기반 아키텍처
│   └── ai_dashboard.py    ← 실시간 운영 대시보드
├── docs/
│   ├── architecture.md    ← 시스템 설계 문서
│   ├── ai-collaboration-log.md  ← AI 협업 기록
│   └── efficiency-report.md     ← 성능 분석 보고서
├── output/
│   └── benchmark.json     ← 성능 측정 결과
└── assets/
    └── architecture.png   ← 시스템 다이어그램
```

---

## 🎮 프로젝트 개요: "미니 RTS 운영 시스템"

간단한 RTS 게임의 **서버 + 운영 대시보드**를 구현했습니다.

### 핵심 기능
1. **실시간 플레이어 매칭** - WebSocket 기반
2. **O(1) 자원 캐싱** - 게임 내 자원(골드, 자원) 빠른 조회
3. **이벤트 기반 전투 로그** - 모든 행동을 이벤트로 기록
4. **운영자 대시보드** - 실시간 DAU, 동접, 전투 통계 확인

### 왜 이 프로젝트인가?
> "돌아가는 코드"가 아닌 **"돌아가면서도 효율적인 시스템"**을 고민했습니다.

---

## 📊 성능 목표 vs 결과

| 지표 | 목표 | 결과 | 상태 |
|------|------|------|------|
| 자원 조회 | O(1) | O(1) | ✅ |
| 이벤트 처리 | 10,000/sec | 15,000/sec | ✅ |
| 동시 접속 | 100명 | 500명 | ✅ |
| 메모리 사용 | < 100MB | 78MB | ✅ |

---

## 🛠️ 기술 스택

- **Python 3.10+** (asyncio, dataclasses)
- **WebSocket** (실시간 통신)
- **Redis-style In-Memory Cache** (O(1) 룩업)
- **Event Bus Pattern** (느슨한 결합)

---

## 🚀 실행 방법

```bash
# 1. 의존성 설치
pip install websockets aiohttp

# 2. 서버 실행
python src/server.py

# 3. 대시보드 실행 (별도 터미널)
python src/ai_dashboard.py

# 4. 성능 벤치마크
python src/cache_system.py --benchmark
```

---

## 📝 AI 협업 기록

이 프로젝트는 AI(Claude)와 함께 기획·설계·구현했습니다.

| 단계 | AI 역할 | 내 역할 |
|------|---------|---------|
| 시스템 설계 | 아키텍처 패턴 제안 | 비즈니스 요구사항 정의 |
| 코드 구현 | 초안 작성 | 리뷰 + 최적화 + 통합 |
| 성능 분석 | 병목 지점 분석 | 측정 + 검증 |
| 문서화 | 구조화 제안 | 내용 작성 + 검토 |

> 💡 **Product Engineer의 AI 활용 능력**을 직접 보여줍니다.

---

## 📞 Contact

- GitHub: https://github.com/tldus4076-cell
- Email: tldus4076@gmail.com
- Phone: 010-9536-8426
