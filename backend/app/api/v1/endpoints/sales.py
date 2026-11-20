"""
Sales analytics API endpoints
"""
from fastapi import APIRouter, Query
from typing import Optional
from app.services.analytics.sales_analyzer import SalesAnalyzer

router = APIRouter(prefix="/analytics/sales", tags=["Sales"])
analyzer = SalesAnalyzer()


@router.get("/trend")
async def get_sales_trend(
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(..., description="End date (YYYY-MM-DD)"),
    granularity: str = Query("day", description="day, week, or month"),
    metrics: Optional[str] = Query(None, description="Comma-separated metrics"),
):
    """Get sales trend data with seasonal decomposition"""
    metrics_list = metrics.split(",") if metrics else None
    return analyzer.get_sales_trend(start_date, end_date, granularity, metrics_list)


@router.get("/ranking")
async def get_sales_ranking(
    dimension: str = Query("product", description="product, category, or customer"),
    top_n: int = Query(10, ge=1, le=100),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
):
    """Get sales ranking by dimension"""
    return analyzer.get_sales_ranking(dimension, top_n, start_date, end_date)


@router.get("/yoy")
async def get_yoy_comparison(
    metric: str = Query("revenue"),
    current_start: Optional[str] = Query(None),
    current_end: Optional[str] = Query(None),
):
    """Year-over-year comparison"""
    return analyzer.get_yoy_comparison(metric, current_start, current_end)
