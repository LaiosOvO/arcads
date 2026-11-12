"""自动生成：路由来自抓包实证的端点清单（docs/api-spec.json）。

家族：industries　端点数：8
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


@router.api_route('/industries/e-commerce', methods=['GET'], include_in_schema=True)
async def get_industries_e_commerce(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/industries/e-commerce）',
    })

@router.api_route('/industries/insurance', methods=['GET'], include_in_schema=True)
async def get_industries_insurance(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/industries/insurance）',
    })

@router.api_route('/industries/law-firms', methods=['GET'], include_in_schema=True)
async def get_industries_law_firms(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/industries/law-firms）',
    })

@router.api_route('/industries/lead-gen', methods=['GET'], include_in_schema=True)
async def get_industries_lead_gen(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/industries/lead-gen）',
    })

@router.api_route('/industries/marketing-agencies', methods=['GET'], include_in_schema=True)
async def get_industries_marketing_agencies(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/industries/marketing-agencies）',
    })

@router.api_route('/industries/mobile-apps', methods=['GET'], include_in_schema=True)
async def get_industries_mobile_apps(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/industries/mobile-apps）',
    })

@router.api_route('/industries/real-estate-agencies', methods=['GET'], include_in_schema=True)
async def get_industries_real_estate_agencies(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/industries/real-estate-agencies）',
    })

@router.api_route('/industries/saas', methods=['GET'], include_in_schema=True)
async def get_industries_saas(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/industries/saas）',
    })
