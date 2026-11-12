"""自动生成：路由来自抓包实证的端点清单（docs/api-spec.json）。

家族：config　端点数：4
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


@router.api_route('/config/44e5a6f3152249aae19ed3e4cad65ea', methods=['GET'], include_in_schema=True)
async def get_config_44e5a6f3152249aae19ed3e4cad65ea(request: Request):
    data = _fixture('get_config_44e5a6f3152249aae19ed3e4cad65ea.json')
    return JSONResponse(data)

@router.api_route('/config/b2e63b5453c36ec48b28059c3ab6a699', methods=['GET'], include_in_schema=True)
async def get_config_b2e63b5453c36ec48b28059c3ab6a699(request: Request):
    data = _fixture('get_config_b2e63b5453c36ec48b28059c3ab6a699.json')
    return JSONResponse(data)

@router.api_route('/config/private', methods=['GET'], include_in_schema=True)
async def get_config_private(request: Request):
    data = _fixture('get_config_private.json')
    return JSONResponse(data)

@router.api_route('/config/private', methods=['OPTIONS'], include_in_schema=True)
async def options_config_private(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=OPTIONS path=/config/private）',
    })
