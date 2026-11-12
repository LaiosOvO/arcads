"""自动生成：路由来自抓包实证的端点清单（docs/api-spec.json）。

家族：use-cases　端点数：4
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


@router.api_route('/use-cases/ad-creative-testing', methods=['GET'], include_in_schema=True)
async def get_use_cases_ad_creative_testing(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/use-cases/ad-creative-testing）',
    })

@router.api_route('/use-cases/ai-facebook-video-ad-generator', methods=['GET'], include_in_schema=True)
async def get_use_cases_ai_facebook_video_ad_generator(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/use-cases/ai-facebook-video-ad-generator）',
    })

@router.api_route('/use-cases/ai-tik-tok-video-generator', methods=['GET'], include_in_schema=True)
async def get_use_cases_ai_tik_tok_video_generator(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/use-cases/ai-tik-tok-video-generator）',
    })

@router.api_route('/use-cases/ai-youtube-video-generator', methods=['GET'], include_in_schema=True)
async def get_use_cases_ai_youtube_video_generator(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/use-cases/ai-youtube-video-generator）',
    })
