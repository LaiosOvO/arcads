"""自动生成：路由来自抓包实证的端点清单（docs/api-spec.json）。

家族：dashboard　端点数：14
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


@router.api_route('/dashboard/addProduct', methods=['GET'], include_in_schema=True)
async def get_dashboard_addproduct(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/dashboard/addProduct）',
    })

@router.api_route('/dashboard/folder', methods=['GET'], include_in_schema=True)
async def get_dashboard_folder(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/dashboard/folder）',
    })

@router.api_route('/dashboard/paywall', methods=['GET'], include_in_schema=True)
async def get_dashboard_paywall(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/dashboard/paywall）',
    })

@router.api_route('/dashboard/product', methods=['GET'], include_in_schema=True)
async def get_dashboard_product(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/dashboard/product）',
    })

@router.api_route('/dashboard/project', methods=['GET'], include_in_schema=True)
async def get_dashboard_project(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/dashboard/project）',
    })

@router.api_route('/dashboard/script', methods=['GET'], include_in_schema=True)
async def get_dashboard_script(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/dashboard/script）',
    })

@router.api_route('/dashboard/settings', methods=['GET'], include_in_schema=True)
async def get_dashboard_settings(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/dashboard/settings）',
    })

@router.api_route('/dashboard/settings/account', methods=['GET'], include_in_schema=True)
async def get_dashboard_settings_account(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/dashboard/settings/account）',
    })

@router.api_route('/dashboard/settings/billing', methods=['GET'], include_in_schema=True)
async def get_dashboard_settings_billing(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/dashboard/settings/billing）',
    })

@router.api_route('/dashboard/settings/general', methods=['GET'], include_in_schema=True)
async def get_dashboard_settings_general(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/dashboard/settings/general）',
    })

@router.api_route('/dashboard/settings/integrations', methods=['GET'], include_in_schema=True)
async def get_dashboard_settings_integrations(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/dashboard/settings/integrations）',
    })

@router.api_route('/dashboard/settings/mcp', methods=['GET'], include_in_schema=True)
async def get_dashboard_settings_mcp(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/dashboard/settings/mcp）',
    })

@router.api_route('/dashboard/settings/members', methods=['GET'], include_in_schema=True)
async def get_dashboard_settings_members(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/dashboard/settings/members）',
    })

@router.api_route('/dashboard/settings/public-api', methods=['GET'], include_in_schema=True)
async def get_dashboard_settings_public_api(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/dashboard/settings/public-api）',
    })
