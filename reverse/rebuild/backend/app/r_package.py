"""自动生成：路由来自抓包实证的端点清单（docs/api-spec.json）。

家族：package　端点数：1
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


@router.api_route('/package/latest/a2378073-dfcc-4ce0-b9cf-cc4866dac6e2/', methods=['GET'], include_in_schema=True)
async def get_package_latest_a2378073_dfcc_4ce0_b9cf_c(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/package/latest/a2378073-dfcc-4ce0-b9cf-cc4866dac6e2/）',
    })
