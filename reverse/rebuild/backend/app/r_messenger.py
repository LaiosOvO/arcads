"""自动生成：路由来自抓包实证的端点清单（docs/api-spec.json）。

家族：messenger　端点数：3
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


@router.api_route('/messenger/web/metrics', methods=['POST'], include_in_schema=True)
async def post_messenger_web_metrics(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=POST path=/messenger/web/metrics）',
    })

@router.api_route('/messenger/web/page_view_events', methods=['POST'], include_in_schema=True)
async def post_messenger_web_page_view_events(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=POST path=/messenger/web/page_view_events）',
    })

@router.api_route('/messenger/web/ping', methods=['POST'], include_in_schema=True)
async def post_messenger_web_ping(request: Request):
    data = _fixture('post_messenger_web_ping.json')
    return JSONResponse(data)
