"""自动生成：路由来自抓包实证的端点清单（docs/api-spec.json）。

家族：cdn-cgi　端点数：2
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


@router.api_route('/cdn-cgi/challenge-platform/h/g/turnstile/f/av0/rch/fc3ic/0x4AAAAAAAQTptj2So4dx43e/auto/fbE/new/normal', methods=['GET'], include_in_schema=True)
async def get_cdn_cgi_challenge_platform_h_g_turnstile(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/cdn-cgi/challenge-platform/h/g/turnstile/f/av0/rch/fc3ic/0x4AAAAAAAQTptj2So4dx43e/auto/fbE/new/normal）',
    })

@router.api_route('/cdn-cgi/challenge-platform/h/g/turnstile/f/av0/rch/fc3ic/0x4AAAAAAAQTptj2So4dx43e/auto/fbE/new/normal', methods=['POST'], include_in_schema=True)
async def post_cdn_cgi_challenge_platform_h_g_turnstile(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=POST path=/cdn-cgi/challenge-platform/h/g/turnstile/f/av0/rch/fc3ic/0x4AAAAAAAQTptj2So4dx43e/auto/fbE/new/normal）',
    })
