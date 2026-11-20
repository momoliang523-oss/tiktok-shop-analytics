"""
Marketing analytics API endpoints
"""
from fastapi import APIRouter, Query
from typing import Optional
from app.services.analytics.marketing_analyzer import MarketingAnalyzer

router = APIRouter(prefix="/analytics/marketing", tags=["Marketing"])
analyzer = MarketingAnalyzer()


@router.get("/campaigns")
async def get_campaigns(
    campaign_id: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
):
    """Get campaign performance"""
    return analyzer.get_campaign_performance(campaign_id, start_date, end_date)


@router.get("/roi")
async def get_roi(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
):
    """Get ROI analysis across all channels"""
    return analyzer.get_roi_analysis(start_date, end_date)
