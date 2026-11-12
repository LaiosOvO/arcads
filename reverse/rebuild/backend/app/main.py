"""小云雀复刻后端（骨架）：路由与实测端点一一对应。

启动：uvicorn app.main:app --reload --port 8000
"""
from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(title='xiaoyunque-rebuild', version='0.1.0',
              description='基于 ego-browser 抓包 + REA 静态逆向生成的复刻骨架')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

from .r_root import router as root_router
app.include_router(root_router)
from .r_ab_tests import router as ab_tests_router
app.include_router(ab_tests_router)
from .r_admin import router as admin_router
app.include_router(admin_router)
from .r_api_4506948625170432 import router as api_4506948625170432_router
app.include_router(api_4506948625170432_router)
from .r_api_auth import router as api_auth_router
app.include_router(api_auth_router)
from .r_api_v1 import router as api_v1_router
app.include_router(api_v1_router)
from .r_api_v2 import router as api_v2_router
app.include_router(api_v2_router)
from .r_auth import router as auth_router
app.include_router(auth_router)
from .r_ccm import router as ccm_router
app.include_router(ccm_router)
from .r_cdn_cgi import router as cdn_cgi_router
app.include_router(cdn_cgi_router)
from .r_config import router as config_router
app.include_router(config_router)
from .r_consents import router as consents_router
app.include_router(consents_router)
from .r_credit_codes import router as credit_codes_router
app.include_router(credit_codes_router)
from .r_cu6vrvqykjig import router as cu6vrvqykjig_router
app.include_router(cu6vrvqykjig_router)
from .r_dashboard import router as dashboard_router
app.include_router(dashboard_router)
from .r_dropbox import router as dropbox_router
app.include_router(dropbox_router)
from .r_e import router as e_router
app.include_router(e_router)
from .r_features import router as features_router
app.include_router(features_router)
from .r_flow import router as flow_router
app.include_router(flow_router)
from .r_g import router as g_router
app.include_router(g_router)
from .r_google_drive import router as google_drive_router
app.include_router(google_drive_router)
from .r_industries import router as industries_router
app.include_router(industries_router)
from .r_integrations import router as integrations_router
app.include_router(integrations_router)
from .r_libs import router as libs_router
app.include_router(libs_router)
from .r_media import router as media_router
app.include_router(media_router)
from .r_messenger import router as messenger_router
app.include_router(messenger_router)
from .r_meta_ads import router as meta_ads_router
app.include_router(meta_ads_router)
from .r_notion import router as notion_router
app.include_router(notion_router)
from .r_offers import router as offers_router
app.include_router(offers_router)
from .r_onboarding import router as onboarding_router
app.include_router(onboarding_router)
from .r_package import router as package_router
app.include_router(package_router)
from .r_pagead import router as pagead_router
app.include_router(pagead_router)
from .r_payment import router as payment_router
app.include_router(payment_router)
from .r_pixel_config import router as pixel_config_router
app.include_router(pixel_config_router)
from .r_pricing import router as pricing_router
app.include_router(pricing_router)
from .r_rmkt import router as rmkt_router
app.include_router(rmkt_router)
from .r_sdk import router as sdk_router
app.include_router(sdk_router)
from .r_slack import router as slack_router
app.include_router(slack_router)
from .r_tiktok import router as tiktok_router
app.include_router(tiktok_router)
from .r_tiktok_ads import router as tiktok_ads_router
app.include_router(tiktok_ads_router)
from .r_tr import router as tr_router
app.include_router(tr_router)
from .r_tracking import router as tracking_router
app.include_router(tracking_router)
from .r_use_cases import router as use_cases_router
app.include_router(use_cases_router)
from .r_users import router as users_router
app.include_router(users_router)
from .r_v1 import router as v1_router
app.include_router(v1_router)
from .r_video import router as video_router
app.include_router(video_router)
from .r_wa import router as wa_router
app.include_router(wa_router)
from .r_widget import router as widget_router
app.include_router(widget_router)
from .r_workflows import router as workflows_router
app.include_router(workflows_router)
from .r_workspaces import router as workspaces_router
app.include_router(workspaces_router)
from .r_x_twitter import router as x_twitter_router
app.include_router(x_twitter_router)

@app.get('/_meta/spec')
async def meta_spec():
    p = Path(__file__).resolve().parent.parent.parent / 'docs' / 'api-spec.json'
    return JSONResponse(json.loads(p.read_text('utf8')) if p.exists() else {'endpoints': []})
