"""自动生成：路由来自抓包实证的端点清单（docs/api-spec.json）。

家族：api_4506948625170432　端点数：1
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


@router.api_route('/api/4506948625170432/envelope/', methods=['POST'], include_in_schema=True)
async def post_api_4506948625170432_envelope(request: Request):
    data = _fixture('post_api_4506948625170432_envelope.json')
    return JSONResponse(data)
