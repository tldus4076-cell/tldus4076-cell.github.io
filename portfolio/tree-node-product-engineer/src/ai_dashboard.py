"""
AI Collaboration Dashboard - 실시간 운영 대시보드
=============================================
Product Engineer가 AI와 협업하는 방식을 보여주는 도구

비즈니스 가치: 운영 데이터 를 보고 AI 배우도록 배우기
"""

import asyncio
import json
import time
from typing import Dict, Any
from aiohttp import web


class OpsDashboard:
    """
    게임 서버의 실시간 상태를 시각화
    
    Product Engineer 스킬: 데이터를 보고 의사결정 내리기
    """
    
    def __init__(self, game_server_stats_fn=None):
        self.start_time = time.time()
        self.stats_fn = game_server_stats_fn
        self.decisions: list = []  # AI 협업 의사결정 기록
    
    def get_metrics(self) -> Dict[str, Any]:
        uptime = int(time.time() - self.start_time)
        return {
            "status": "running",
            "uptime_seconds": uptime,
            "uptime_formatted": f"{uptime // 3600}h {(uptime % 3600) // 60}m",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "ai_decisions": len(self.decisions)
        }
    
    def log_decision(self, context: str, ai_suggestion: str, human_choice: str):
        """
        AI 협업 기록: 어떤 상황에서 AI가 뭐라고 했고, 내가 무엇을 결정했다
        이게 Product Engineer의 핵심: AI를 도구로 쓰지만 최종 결정은 사람이 함
        """
        self.decisions.append({
            "time": time.strftime("%H:%M:%S"),
            "context": context,
            "ai_suggestion": ai_suggestion,
            "human_choice": human_choice,
            "match": ai_suggestion == human_choice
        })
    
    async def handle_http(self, request):
        """HTTP 서비스 - 운영자가 봤었으면 좋을 대시보드"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>운영 대시보드</title>
            <style>
                body {{ font-family: 'Segoe UI', sans-serif; background: #0f172a; color: #e2e8f0; padding: 40px; }}
                h1 {{ color: #38bdf8; }}
                .metric {{ background: #1e293b; border-radius: 12px; padding: 20px; margin: 10px 0; }}
                .label {{ color: #94a3b8; font-size: 14px; }}
                .value {{ font-size: 28px; font-weight: bold; color: #22c55e; }}
                .ai-box {{ background: #312e81; border-left: 4px solid #818cf8; padding: 15px; margin: 10px 0; border-radius: 4px; }}
            </style>
        </head>
        <body>
            <h1>트리노드 RTS 운영 대시보드</h1>
            <div class="metric">
                <div class="label">서버 상태</div>
                <div class="value">✅ {self.get_metrics()['status']}</div>
            </div>
            <div class="metric">
                <div class="label">가동 시간</div>
                <div class="value">{self.get_metrics()['uptime_formatted']}</div>
            </div>
            <div class="metric">
                <div class="label">AI 협업 의사결정 수</div>
                <div class="value">{self.get_metrics()['ai_decisions']}</div>
            </div>
            <h2>🧠 AI 협업 기록</h2>
            <p>이 대시보드는 AI(Claude)와 협업하며 내린 결정을 모든 기록합니다.</p>
            {"".join(f'<div class="ai-box"><strong>{d["time"]}</strong><br>상황: {d["context"]}<br>AI 제안: {d["ai_suggestion"]}<br>결정: {d["human_choice"]} {"✅" if d["match"] else "⚠️"}</div>' for d in self.decisions[-5:])}
        </body>
        </html>
        """
        return web.Response(text=html, content_type='text/html')


if __name__ == "__main__":
    dash = OpsDashboard()
    dash.log_decision("자원 캐시 설계", "dict + TTL", "dict + TTL + hit stats")
    dash.log_decision("이벤트 버스 도입", "버전 1: 동기 직접호출", "버전 2: 비동기 이벤트 버스")
    
    app = web.Application()
    app.router.add_get('/', dash.handle_http)
    web.run_app(app, host="0.0.0.0", port=8080)
