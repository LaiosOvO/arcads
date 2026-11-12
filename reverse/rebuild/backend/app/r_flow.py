"""自动生成：路由来自抓包实证的端点清单（docs/api-spec.json）。

家族：flow　端点数：3
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


@router.api_route('/flow/library', methods=['GET'], include_in_schema=True)
async def get_flow_library(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/flow/library）',
    })

@router.api_route('/flow/try', methods=['GET'], include_in_schema=True)
async def get_flow_try(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/flow/try）',
    })

@router.api_route('/flow/use', methods=['GET'], include_in_schema=True)
async def get_flow_use(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/flow/use）',
    })
