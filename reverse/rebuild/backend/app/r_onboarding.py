"""自动生成：路由来自抓包实证的端点清单（docs/api-spec.json）。

家族：onboarding　端点数：10
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


@router.api_route('/onboarding/ad-spend', methods=['GET'], include_in_schema=True)
async def get_onboarding_ad_spend(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/onboarding/ad-spend）',
    })

@router.api_route('/onboarding/attribution', methods=['GET'], include_in_schema=True)
async def get_onboarding_attribution(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/onboarding/attribution）',
    })

@router.api_route('/onboarding/business-type', methods=['GET'], include_in_schema=True)
async def get_onboarding_business_type(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/onboarding/business-type）',
    })

@router.api_route('/onboarding/contact', methods=['GET'], include_in_schema=True)
async def get_onboarding_contact(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/onboarding/contact）',
    })

@router.api_route('/onboarding/intent', methods=['GET'], include_in_schema=True)
async def get_onboarding_intent(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/onboarding/intent）',
    })

@router.api_route('/onboarding/payment', methods=['GET'], include_in_schema=True)
async def get_onboarding_payment(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/onboarding/payment）',
    })

@router.api_route('/onboarding/paywall', methods=['GET'], include_in_schema=True)
async def get_onboarding_paywall(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/onboarding/paywall）',
    })

@router.api_route('/onboarding/success', methods=['GET'], include_in_schema=True)
async def get_onboarding_success(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/onboarding/success）',
    })

@router.api_route('/onboarding/team-size', methods=['GET'], include_in_schema=True)
async def get_onboarding_team_size(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/onboarding/team-size）',
    })

@router.api_route('/onboarding/website', methods=['GET'], include_in_schema=True)
async def get_onboarding_website(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/onboarding/website）',
    })
