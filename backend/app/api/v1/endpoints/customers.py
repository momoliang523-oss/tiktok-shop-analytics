"""
Customer analytics API endpoints
"""
from fastapi import APIRouter, Query
from typing import Optional
from app.services.analytics.customer_analyzer import CustomerAnalyzer

router = APIRouter(prefix="/analytics/customers", tags=["Customers"])
analyzer = CustomerAnalyzer()


@router.get("/segments")
async def get_customer_segments(
    segmentation_type: str = Query("behavioral", description="behavioral, demographic, psychographic, value_based"),
):
    """Get customer segmentation results"""
    return analyzer.get_customer_segments(segmentation_type)


@router.get("/rfm")
async def get_customer_rfm(
    customer_id: Optional[str] = Query(None),
):
    """Get customer RFM analysis"""
    return analyzer.get_rfm_analysis(customer_id)
