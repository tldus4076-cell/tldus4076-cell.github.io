#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
게임 라이브 서비스 API
공고 요건: 게임 개발에 필요한 각종 서비스 시스템 설계 및 구축
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime
from uuid import uuid4

app = Flask(__name__)
CORS(app)  # CORS 허용 (게임 클라이언트와 통신)

DATA_FILE = os.path.join(os.path.dirname(__file__), "game_data.json")

# -------------------------------
# 데이터 저장/로드 유틸리티
# -------------------------------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"scores": [], "users": {}, "logs": []}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = load_data()

# -------------------------------
# 1. 점수 등록 API
# POST /api/score
# -------------------------------
@app.route("/api/score", methods=["POST"])
def submit_score():
    try:
        req = request.get_json()
        if not req or "score" not in req:
            return jsonify({"error": "score 필드 누락"}), 400
        
        entry = {
            "id": str(uuid4())[:8],
            "nickname": req.get("nickname", "Anonymous"),
            "score": int(req["score"]),
            "stage": req.get("stage", 1),
            "timestamp": datetime.now().isoformat()
        }
        
        data["scores"].append(entry)
        # 점수 높은 순으로 정렬, 최대 100개 유지
        data["scores"].sort(key=lambda x: x["score"], reverse=True)
        data["scores"] = data["scores"][:100]
        
        save_data(data)
        
        # 로그 남기기
        data["logs"].append({
            "action": "score_submit",
            "id": entry["id"],
            "timestamp": entry["timestamp"]
        })
        
        return jsonify({"success": True, "id": entry["id"], "rank": get_rank(entry["id"])}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------------------
# 2. 리더보드 조회 API
# GET /api/leaderboard?limit=10
# -------------------------------
@app.route("/api/leaderboard", methods=["GET"])
def get_leaderboard():
    limit = request.args.get("limit", 10, type=int)
    top_scores = data["scores"][:limit]
    
    return jsonify({
        "success": True,
        "count": len(top_scores),
        "leaderboard": [
            {
                "rank": i + 1,
                "nickname": s["nickname"],
                "score": s["score"],
                "stage": s["stage"],
                "date": s["timestamp"][:10]
            }
            for i, s in enumerate(top_scores)
        ]
    })

# -------------------------------
# 3. 유저 데이터 저장 API
# POST /api/user/<user_id>
# -------------------------------
@app.route("/api/user/<user_id>", methods=["POST"])
def save_user_data(user_id):
    try:
        req = request.get_json()
        data["users"][user_id] = {
            "data": req,
            "updated_at": datetime.now().isoformat()
        }
        save_data(data)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------------------
# 4. 유저 데이터 로드 API
# GET /api/user/<user_id>
# -------------------------------
@app.route("/api/user/<user_id>", methods=["GET"])
def load_user_data(user_id):
    user = data["users"].get(user_id)
    if not user:
        return jsonify({"error": "유저를 찾을 수 없습니다"}), 404
    return jsonify({"success": True, "data": user["data"]})

# -------------------------------
# 5. 서버 상태 체크 (Health Check)
# GET /api/health
# -------------------------------
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "ok",
        "service": "game-live-service",
        "version": "1.0.0",
        "total_scores": len(data["scores"]),
        "total_users": len(data["users"]),
        "timestamp": datetime.now().isoformat()
    })

# -------------------------------
# 허도 유틸리티
# -------------------------------
def get_rank(score_id):
    for i, s in enumerate(data["scores"]):
        if s["id"] == score_id:
            return i + 1
    return None

# -------------------------------
# 스탠들런 데모 데이터 생성
# -------------------------------
def seed_demo_data():
    if not data["scores"]:
        demo_scores = [
            {"id": "demo1", "nickname": "루키에드",   "score": 2500, "stage": 5, "timestamp": "2026-06-01T10:00:00"},
            {"id": "demo2", "nickname": "용사당",       "score": 1800, "stage": 4, "timestamp": "2026-06-01T11:00:00"},
            {"id": "demo3", "nickname": "마법사",       "score": 1200, "stage": 3, "timestamp": "2026-06-01T12:00:00"},
        ]
        data["scores"] = demo_scores
        save_data(data)
        print("✅ 데몤 데이터 생성 완료!")

if __name__ == "__main__":
    seed_demo_data()
    print("🎮 게임 라이브 서비스 시작!")
    print("엔드포인트: http://localhost:5000")
    print("  GET  /api/health      - 상태 체크")
    print("  GET  /api/leaderboard - 리더보드")
    print("  POST /api/score       - 점수 등록")
    print("  GET  /api/user/<id>   - 유저 데이터")
    print("")
    app.run(host="0.0.0.0", port=5000, debug=True)
