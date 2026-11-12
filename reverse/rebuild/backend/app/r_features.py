"""自动生成：路由来自抓包实证的端点清单（docs/api-spec.json）。

家族：features　端点数：15
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


@router.api_route('/features/ai-actors', methods=['GET'], include_in_schema=True)
async def get_features_ai_actors(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/features/ai-actors）',
    })

@router.api_route('/features/ai-ads', methods=['GET'], include_in_schema=True)
async def get_features_ai_ads(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/features/ai-ads）',
    })

@router.api_route('/features/ai-avatars', methods=['GET'], include_in_schema=True)
async def get_features_ai_avatars(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/features/ai-avatars）',
    })

@router.api_route('/features/ai-content-generator', methods=['GET'], include_in_schema=True)
async def get_features_ai_content_generator(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/features/ai-content-generator）',
    })

@router.api_route('/features/ai-for-affiliate', methods=['GET'], include_in_schema=True)
async def get_features_ai_for_affiliate(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/features/ai-for-affiliate）',
    })

@router.api_route('/features/ai-lipsync', methods=['GET'], include_in_schema=True)
async def get_features_ai_lipsync(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/features/ai-lipsync）',
    })

@router.api_route('/features/ai-product-video-generator', methods=['GET'], include_in_schema=True)
async def get_features_ai_product_video_generator(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/features/ai-product-video-generator）',
    })

@router.api_route('/features/ai-shorts-generator', methods=['GET'], include_in_schema=True)
async def get_features_ai_shorts_generator(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/features/ai-shorts-generator）',
    })

@router.api_route('/features/ai-tik-tok-ads-generator', methods=['GET'], include_in_schema=True)
async def get_features_ai_tik_tok_ads_generator(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/features/ai-tik-tok-ads-generator）',
    })

@router.api_route('/features/ai-ugc-video', methods=['GET'], include_in_schema=True)
async def get_features_ai_ugc_video(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/features/ai-ugc-video）',
    })

@router.api_route('/features/ai-video-api', methods=['GET'], include_in_schema=True)
async def get_features_ai_video_api(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/features/ai-video-api）',
    })

@router.api_route('/features/ai-video-generator', methods=['GET'], include_in_schema=True)
async def get_features_ai_video_generator(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/features/ai-video-generator）',
    })

@router.api_route('/features/facebook-ai-ads-generator', methods=['GET'], include_in_schema=True)
async def get_features_facebook_ai_ads_generator(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/features/facebook-ai-ads-generator）',
    })

@router.api_route('/features/talking-avatar-ai', methods=['GET'], include_in_schema=True)
async def get_features_talking_avatar_ai(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/features/talking-avatar-ai）',
    })

@router.api_route('/features/text-to-speech', methods=['GET'], include_in_schema=True)
async def get_features_text_to_speech(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/features/text-to-speech）',
    })
