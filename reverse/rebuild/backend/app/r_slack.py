"""自动生成：路由来自抓包实证的端点清单（docs/api-spec.json）。

家族：slack　端点数：1
有响应样本的直接回放真实抓包体；没有的返回 untyped 占位并显式标注。
"""
from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()
FIX = Path(__file__).resolve().parent.parent / 'fixtures'


def _fixture(name: str):
    p = FIX / name
    if p.exists():
        return json.loads(p.read_text('utf8'))
    return None


@router.api_route('/slack/connection-status', methods=['GET'], include_in_schema=True)
async def get_slack_connection_status(request: Request):
    data = _fixture('get_slack_connection_status.json')
    return JSONResponse(data)
