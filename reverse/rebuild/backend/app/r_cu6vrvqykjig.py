"""自动生成：路由来自抓包实证的端点清单（docs/api-spec.json）。

家族：cu6vrvqykjig　端点数：1
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


@router.api_route('/cu6vrvqykjig/dkjmj', methods=['GET'], include_in_schema=True)
async def get_cu6vrvqykjig_dkjmj(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/cu6vrvqykjig/dkjmj）',
    })
