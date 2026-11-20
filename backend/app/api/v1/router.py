"""
API v1 Router - aggregates all endpoint routers
"""
from fastapi import APIRouter
from app.api.v1.endpoints import sales, products, customers, marketing, live, traffic, reports, data_import

api_router = APIRouter(prefix="/api/v1")

# Analytics endpoints
api_router.include_router(sales.router)
api_router.include_router(products.router)
api_router.include_router(customers.router)
api_router.include_router(marketing.router)
api_router.include_router(live.router)
api_router.include_router(traffic.router)

# Report and data endpoints
api_router.include_router(reports.router)
api_router.include_router(data_import.router)


@api_router.get("/")
async def api_v1_root():
    """API v1 root endpoint"""
    return {
        "message": "TikTok Shop Analytics API v1",
        "version": "1.0.0",
        "endpoints": {
            "sales": "/api/v1/analytics/sales",
            "products": "/api/v1/analytics/products",
            "customers": "/api/v1/analytics/customers",
            "marketing": "/api/v1/analytics/marketing",
            "live": "/api/v1/analytics/live",
            "traffic": "/api/v1/analytics/traffic",
            "reports": "/api/v1/reports",
            "data": "/api/v1/data",
        }
    }
