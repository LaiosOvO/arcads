"""自动生成：路由来自抓包实证的端点清单（docs/api-spec.json）。

家族：pixel-config　端点数：1
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


@router.api_route('/pixel-config/v1/63KWrdSGxuziTXF3Coczky.json', methods=['GET'], include_in_schema=True)
async def get_pixel_config_v1_63kwrdsgxuzitxf3coczky_j(request: Request):
    data = _fixture('get_pixel_config_v1_63kwrdsgxuzitxf3coczky_json.json')
    return JSONResponse(data)
