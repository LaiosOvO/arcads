"""自动生成：路由来自抓包实证的端点清单（docs/api-spec.json）。

家族：workspaces　端点数：7
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


@router.api_route('/workspaces/77a46767-0e96-4b87-b393-267643c7adc2', methods=['OPTIONS'], include_in_schema=True)
async def options_workspaces_77a46767_0e96_4b87_b393_26764(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=OPTIONS path=/workspaces/77a46767-0e96-4b87-b393-267643c7adc2）',
    })

@router.api_route('/workspaces/77a46767-0e96-4b87-b393-267643c7adc2', methods=['PUT'], include_in_schema=True)
async def put_workspaces_77a46767_0e96_4b87_b393_26764(request: Request):
    data = _fixture('put_workspaces_77a46767_0e96_4b87_b393_267643c7adc2.json')
    return JSONResponse(data)

@router.api_route('/workspaces/api-credentials', methods=['GET'], include_in_schema=True)
async def get_workspaces_api_credentials(request: Request):
    data = _fixture('get_workspaces_api_credentials.json')
    return JSONResponse(data)

@router.api_route('/workspaces/credit-consumption-history', methods=['GET'], include_in_schema=True)
async def get_workspaces_credit_consumption_history(request: Request):
    data = _fixture('get_workspaces_credit_consumption_history.json')
    return JSONResponse(data)

@router.api_route('/workspaces/credit-consumption-history', methods=['OPTIONS'], include_in_schema=True)
async def options_workspaces_credit_consumption_history(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=OPTIONS path=/workspaces/credit-consumption-history）',
    })

@router.api_route('/workspaces/members', methods=['GET'], include_in_schema=True)
async def get_workspaces_members(request: Request):
    data = _fixture('get_workspaces_members.json')
    return JSONResponse(data)

@router.api_route('/workspaces/members', methods=['OPTIONS'], include_in_schema=True)
async def options_workspaces_members(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=OPTIONS path=/workspaces/members）',
    })
