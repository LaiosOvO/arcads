"""自动生成：路由来自抓包实证的端点清单（docs/api-spec.json）。

家族：admin　端点数：60
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


@router.api_route('/admin/actors', methods=['GET'], include_in_schema=True)
async def get_admin_actors(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/actors）',
    })

@router.api_route('/admin/actors/checkVoices', methods=['GET'], include_in_schema=True)
async def get_admin_actors_checkvoices(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/actors/checkVoices）',
    })

@router.api_route('/admin/actors/new', methods=['GET'], include_in_schema=True)
async def get_admin_actors_new(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/actors/new）',
    })

@router.api_route('/admin/actors/stats', methods=['GET'], include_in_schema=True)
async def get_admin_actors_stats(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/actors/stats）',
    })

@router.api_route('/admin/actors/validationProcess', methods=['GET'], include_in_schema=True)
async def get_admin_actors_validationprocess(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/actors/validationProcess）',
    })

@router.api_route('/admin/agent/animation-studio', methods=['GET'], include_in_schema=True)
async def get_admin_agent_animation_studio(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/agent/animation-studio）',
    })

@router.api_route('/admin/agent/motion-templates', methods=['GET'], include_in_schema=True)
async def get_admin_agent_motion_templates(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/agent/motion-templates）',
    })

@router.api_route('/admin/agent/skills', methods=['GET'], include_in_schema=True)
async def get_admin_agent_skills(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/agent/skills）',
    })

@router.api_route('/admin/agent/skills/import', methods=['GET'], include_in_schema=True)
async def get_admin_agent_skills_import(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/agent/skills/import）',
    })

@router.api_route('/admin/asset-swipe', methods=['GET'], include_in_schema=True)
async def get_admin_asset_swipe(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/asset-swipe）',
    })

@router.api_route('/admin/asset-swipe/next', methods=['GET'], include_in_schema=True)
async def get_admin_asset_swipe_next(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/asset-swipe/next）',
    })

@router.api_route('/admin/asset-swipe/votes', methods=['GET'], include_in_schema=True)
async def get_admin_asset_swipe_votes(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/asset-swipe/votes）',
    })

@router.api_route('/admin/camera-movement', methods=['GET'], include_in_schema=True)
async def get_admin_camera_movement(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/camera-movement）',
    })

@router.api_route('/admin/camera-movement/situations', methods=['GET'], include_in_schema=True)
async def get_admin_camera_movement_situations(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/camera-movement/situations）',
    })

@router.api_route('/admin/contents', methods=['GET'], include_in_schema=True)
async def get_admin_contents(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/contents）',
    })

@router.api_route('/admin/creator-codes', methods=['GET'], include_in_schema=True)
async def get_admin_creator_codes(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/creator-codes）',
    })

@router.api_route('/admin/credit-codes', methods=['GET'], include_in_schema=True)
async def get_admin_credit_codes(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/credit-codes）',
    })

@router.api_route('/admin/credit-codes/batches', methods=['GET'], include_in_schema=True)
async def get_admin_credit_codes_batches(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/credit-codes/batches）',
    })

@router.api_route('/admin/credit-codes/cost-rate', methods=['GET'], include_in_schema=True)
async def get_admin_credit_codes_cost_rate(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/credit-codes/cost-rate）',
    })

@router.api_route('/admin/editingRequests', methods=['GET'], include_in_schema=True)
async def get_admin_editingrequests(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/editingRequests）',
    })

@router.api_route('/admin/events', methods=['GET'], include_in_schema=True)
async def get_admin_events(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/events）',
    })

@router.api_route('/admin/featured-models', methods=['GET'], include_in_schema=True)
async def get_admin_featured_models(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/featured-models）',
    })

@router.api_route('/admin/featured-models/reorder', methods=['GET'], include_in_schema=True)
async def get_admin_featured_models_reorder(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/featured-models/reorder）',
    })

@router.api_route('/admin/first-generations', methods=['GET'], include_in_schema=True)
async def get_admin_first_generations(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/first-generations）',
    })

@router.api_route('/admin/global', methods=['GET'], include_in_schema=True)
async def get_admin_global(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/global）',
    })

@router.api_route('/admin/global/featured-models', methods=['GET'], include_in_schema=True)
async def get_admin_global_featured_models(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/global/featured-models）',
    })

@router.api_route('/admin/landing-tests', methods=['GET'], include_in_schema=True)
async def get_admin_landing_tests(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/landing-tests）',
    })

@router.api_route('/admin/landing-tests/new', methods=['GET'], include_in_schema=True)
async def get_admin_landing_tests_new(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/landing-tests/new）',
    })

@router.api_route('/admin/lipsync/actors', methods=['GET'], include_in_schema=True)
async def get_admin_lipsync_actors(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/lipsync/actors）',
    })

@router.api_route('/admin/moderation', methods=['GET'], include_in_schema=True)
async def get_admin_moderation(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/moderation）',
    })

@router.api_route('/admin/personalActors', methods=['GET'], include_in_schema=True)
async def get_admin_personalactors(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/personalActors）',
    })

@router.api_route('/admin/personalActors/stats', methods=['GET'], include_in_schema=True)
async def get_admin_personalactors_stats(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/personalActors/stats）',
    })

@router.api_route('/admin/pricing/ab-tests', methods=['GET'], include_in_schema=True)
async def get_admin_pricing_ab_tests(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/pricing/ab-tests）',
    })

@router.api_route('/admin/pricing/ab-tests/new', methods=['GET'], include_in_schema=True)
async def get_admin_pricing_ab_tests_new(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/pricing/ab-tests/new）',
    })

@router.api_route('/admin/pricing/catalogs', methods=['GET'], include_in_schema=True)
async def get_admin_pricing_catalogs(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/pricing/catalogs）',
    })

@router.api_route('/admin/pricing/catalogs/active', methods=['GET'], include_in_schema=True)
async def get_admin_pricing_catalogs_active(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/pricing/catalogs/active）',
    })

@router.api_route('/admin/pricing/margin-simulator', methods=['GET'], include_in_schema=True)
async def get_admin_pricing_margin_simulator(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/pricing/margin-simulator）',
    })

@router.api_route('/admin/pricing/plans', methods=['GET'], include_in_schema=True)
async def get_admin_pricing_plans(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/pricing/plans）',
    })

@router.api_route('/admin/pricing/stripe-products', methods=['GET'], include_in_schema=True)
async def get_admin_pricing_stripe_products(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/pricing/stripe-products）',
    })

@router.api_route('/admin/products', methods=['GET'], include_in_schema=True)
async def get_admin_products(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/products）',
    })

@router.api_route('/admin/products/create', methods=['GET'], include_in_schema=True)
async def get_admin_products_create(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/products/create）',
    })

@router.api_route('/admin/releases/whats-new', methods=['GET'], include_in_schema=True)
async def get_admin_releases_whats_new(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/releases/whats-new）',
    })

@router.api_route('/admin/scripts', methods=['GET'], include_in_schema=True)
async def get_admin_scripts(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/scripts）',
    })

@router.api_route('/admin/scripts/all', methods=['GET'], include_in_schema=True)
async def get_admin_scripts_all(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/scripts/all）',
    })

@router.api_route('/admin/scripts/moderated', methods=['GET'], include_in_schema=True)
async def get_admin_scripts_moderated(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/scripts/moderated）',
    })

@router.api_route('/admin/situations', methods=['GET'], include_in_schema=True)
async def get_admin_situations(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/situations）',
    })

@router.api_route('/admin/situations/data', methods=['GET'], include_in_schema=True)
async def get_admin_situations_data(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/situations/data）',
    })

@router.api_route('/admin/situations/gestures/create', methods=['GET'], include_in_schema=True)
async def get_admin_situations_gestures_create(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/situations/gestures/create）',
    })

@router.api_route('/admin/video-templates', methods=['GET'], include_in_schema=True)
async def get_admin_video_templates(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/video-templates）',
    })

@router.api_route('/admin/video-templates/categories', methods=['GET'], include_in_schema=True)
async def get_admin_video_templates_categories(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/video-templates/categories）',
    })

@router.api_route('/admin/video-templates/new', methods=['GET'], include_in_schema=True)
async def get_admin_video_templates_new(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/video-templates/new）',
    })

@router.api_route('/admin/voices', methods=['GET'], include_in_schema=True)
async def get_admin_voices(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/voices）',
    })

@router.api_route('/admin/voices/new', methods=['GET'], include_in_schema=True)
async def get_admin_voices_new(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/voices/new）',
    })

@router.api_route('/admin/voices/stats', methods=['GET'], include_in_schema=True)
async def get_admin_voices_stats(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/voices/stats）',
    })

@router.api_route('/admin/workflows', methods=['GET'], include_in_schema=True)
async def get_admin_workflows(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/workflows）',
    })

@router.api_route('/admin/workflows/library', methods=['GET'], include_in_schema=True)
async def get_admin_workflows_library(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/workflows/library）',
    })

@router.api_route('/admin/workflows/library/order', methods=['GET'], include_in_schema=True)
async def get_admin_workflows_library_order(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/workflows/library/order）',
    })

@router.api_route('/admin/workflows/library/settings', methods=['GET'], include_in_schema=True)
async def get_admin_workflows_library_settings(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/workflows/library/settings）',
    })

@router.api_route('/admin/workflows/top', methods=['GET'], include_in_schema=True)
async def get_admin_workflows_top(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/workflows/top）',
    })

@router.api_route('/admin/workspaces/arcads10-offer/links', methods=['GET'], include_in_schema=True)
async def get_admin_workspaces_arcads10_offer_links(request: Request):
    return JSONResponse({
        'ret': '0', 'errmsg': 'success',
        'data': None,
        '_note': '未抓到该端点响应体，字段未实证（method=GET path=/admin/workspaces/arcads10-offer/links）',
    })
