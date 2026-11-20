"""
Traffic analytics API endpoints
"""
from fastapi import APIRouter, Query
from typing import Optional
from app.services.analytics.traffic_analyzer import TrafficAnalyzer
from app.services.analytics.ltv_cac_analyzer import LtvCacAnalyzer
from app.services.analytics.advanced_analytics import AdvancedAnalytics

router = APIRouter(prefix="/analytics/traffic", tags=["Traffic"])
traffic_analyzer = TrafficAnalyzer()
ltv_analyzer = LtvCacAnalyzer()
advanced = AdvancedAnalytics()


@router.get("/channels")
async def get_traffic_channels(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
):
    """Get traffic channel analysis"""
    return traffic_analyzer.get_channel_analysis(start_date, end_date)


@router.get("/funnel")
async def get_conversion_funnel(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
):
    """Get conversion funnel data"""
    return traffic_analyzer.get_conversion_funnel(start_date, end_date)


@router.get("/ltv-cac")
async def get_ltv_cac(
    channel: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    ltv_period: str = Query("90d", description="30d, 90d, 180d, 365d"),
):
    """Get LTV/CAC analysis by channel"""
    return ltv_analyzer.get_ltv_cac(channel, start_date, end_date, ltv_period)


@router.get("/channel-value")
async def get_channel_value(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    value_dimension: str = Query("ltv"),
):
    """Get channel value evaluation"""
    return ltv_analyzer.get_channel_value(start_date, end_date, value_dimension)


@router.get("/segmentation")
async def get_traffic_segmentation(
    channel: Optional[str] = Query(None),
    segmentation_type: str = Query("behavioral"),
):
    """Get traffic source customer segmentation"""
    return traffic_analyzer.get_traffic_segmentation(channel, segmentation_type)


@router.get("/correlation")
async def get_correlation(
    metrics: Optional[str] = Query(None, description="Comma-separated metrics"),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
):
    """Get correlation analysis"""
    metrics_list = metrics.split(",") if metrics else None
    return advanced.get_correlation_matrix(metrics_list, start_date, end_date)


@router.post("/clustering")
async def create_clustering(data: dict):
    """Perform clustering analysis"""
    return advanced.create_clustering(
        cluster_type=data.get("type", "customer"),
        n_clusters=data.get("n_clusters", 3),
        features=data.get("features"),
    )


@router.get("/prediction")
async def get_prediction(
    metric: str = Query("revenue"),
    periods: int = Query(30, ge=1, le=365),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
):
    """Get trend prediction"""
    return advanced.get_prediction(metric, periods, start_date, end_date)
