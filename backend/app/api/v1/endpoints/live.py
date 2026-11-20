"""
Live stream analytics API endpoints
"""
from fastapi import APIRouter, Query
from typing import Optional
from app.services.analytics.live_analyzer import LiveAnalyzer

router = APIRouter(prefix="/analytics/live", tags=["Live"])
analyzer = LiveAnalyzer()


@router.get("/overview")
async def get_live_overview(
    live_id: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
):
    """Get live stream overview"""
    return analyzer.get_live_overview(live_id, start_date, end_date)


@router.get("/products")
async def get_live_products(
    live_id: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
):
    """Get product performance in live streams"""
    return analyzer.get_live_products(live_id, start_date, end_date)


@router.get("/hosts")
async def get_live_hosts(
    host_id: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
):
    """Get host performance"""
    return analyzer.get_live_hosts(host_id, start_date, end_date)
