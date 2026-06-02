# 🎮 게임 클라이언트/모바일 개발자 포트폴리오

> **지원 공고**: 개발자(프로그래머) 신입 사원 모집 (게임개발 클라이언트/모바일)
> **핵심 언어**: Lua, JavaScript, C# 중 1개 이상
> **우대사항**: 게임엔진 사용 경험

---

## 📂 포트폴리오 구성

| 프로젝트 | 기술 | 설명 | 상태 |
|---------|------|------|------|
| **Mini RPG (Unity 2D)** | C# | Unity 엔진으로 제작한 2D 탑다운 RPG | ✅ 완료 |
| **Web Arcade Game** | JavaScript | HTML5 Canvas로 만든 웹 게임 | ✅ 완료 |
| **Lua Game Scripts** | Lua | 게임 내 메커닉스/이벤트 스크립팅 | ✅ 완료 |
| **Game Live Service API** | Python | 게임 데이터 저장/리더보드 REST API | ✅ 완료 |

---

## 🎯 이 포트폴리오가 공고 요건을 충족하는 이유

### 1. 게임 콘텐츠 및 시스템 개발
- **Unity 2D RPG**: 플레이어 이동, 전투, 적 AI, 아이템 시스템 구현
- **웹 게임**: Canvas 기반 렌더링, 게임 루프, 충돌 검사

### 2. 게임 콘텐츠 유지보수 및 라이브서비스 운영
- **Python Flask API**: 유저 점수 저장, 리더보드 조회, 게임 데이터 백업
- **Lua 스크립트**: 게임 내 이벤트/퀘스트를 외부 파일로 분리 → 수정/배포 용이

### 3. 게임 개발에 필요한 각종 서비스 시스템 설계 및 구축
- REST API 서버 설계 (게임 클라이언트 ↔ 서버 통신)
- JSON 데이터 포맷 표준화
- 에러 핸들링 및 로깅 시스템

---

## 🛠️ 기술 스택

| 분야 | 기술 |
|------|------|
| 클라이언트 | Unity (C#), HTML5 Canvas (JavaScript) |
| 스크립팅 | Lua 5.4 |
| 서버 | Python 3, Flask |
| 데이터 | JSON, SQLite |
| 도구 | Git, VS Code |

---

## 🚀 실행 방법

### Unity 2D 게임
1. Unity Hub 설치 (2022.3 LTS 권장)
2. `unity-2d-game/` 폴더를 Unity 프로젝트로 오픈
3. `Scenes/MainScene` 실행

### 웹 게임
```bash
cd web-game
python -m http.server 8080
# 브라우저에서 http://localhost:8080 접속
```

### 게임 서버 API
```bash
cd game-service
pip install -r requirements.txt
python app.py
# http://localhost:5000 에서 API 동작
```

### Lua 스크립트
```bash
lua lua-scripts/game_mechanics.lua
```

---

## 📞 Contact
- GitHub: https://github.com/tldus4076-cell
- Email: Tldus4076@gmail.com
