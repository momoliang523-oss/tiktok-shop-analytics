"""
Product/SKU analytics API endpoints
"""
from fastapi import APIRouter, Query
from typing import Optional
from app.services.analytics.product_analyzer import ProductAnalyzer

router = APIRouter(prefix="/analytics/products", tags=["Products"])
analyzer = ProductAnalyzer()


@router.get("/performance")
async def get_sku_performance(
    pattern_name: Optional[str] = Query(None),
    color: Optional[str] = Query(None),
    size: Optional[str] = Query(None),
    sort_by: str = Query("sales", description="sales, revenue, conversion_rate, pattern_score"),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
):
    """Get SKU performance data"""
    return analyzer.get_sku_performance(pattern_name, color, size, sort_by, start_date, end_date)


@router.get("/sku-ranking")
async def get_sku_ranking(
    sort_by: str = Query("sales"),
    top_n: int = Query(10, ge=1, le=100),
):
    """Get SKU ranking"""
    result = analyzer.get_sku_performance(sort_by=sort_by)
    result["skus"] = result["skus"][:top_n]
    return result


@router.get("/association")
async def get_sku_association(
    sku_id: Optional[str] = Query(None),
    pattern_name: Optional[str] = Query(None),
    top_n: int = Query(5, ge=1, le=20),
):
    """Get SKU association rules"""
    return analyzer.get_sku_association(sku_id, pattern_name, top_n)


@router.get("/pattern-analysis")
async def get_pattern_analysis(
    category: Optional[str] = Query(None),
    sort_by: str = Query("sales"),
    region: Optional[str] = Query(None, description="US region: west, east, midwest, south"),
    generation: Optional[str] = Query(None, description="gen_z, millennial, gen_x, boomer"),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
):
    """Get pattern analysis with US market insights"""
    return analyzer.get_pattern_analysis(category, sort_by, region, generation, start_date, end_date)


@router.get("/inventory")
async def get_sku_inventory(
    low_stock_only: bool = Query(False),
    pattern_name: Optional[str] = Query(None),
):
    """Get SKU inventory status"""
    return analyzer.get_sku_inventory(low_stock_only, pattern_name)
