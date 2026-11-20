"""
LTV/CAC analysis service for customer lifetime value and acquisition cost
"""
from typing import Optional


class LtvCacAnalyzer:
    """Customer Lifetime Value and Acquisition Cost analysis"""

    def __init__(self, db=None):
        self.db = db

    def get_ltv_cac(
        self,
        channel: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        ltv_period: str = '90d'
    ) -> dict:
        """Calculate LTV/CAC metrics by channel"""
        channels = [
            {
                "channel": "TikTok Ads",
                "ltv": 450, "cac": 80, "ltv_cac_ratio": 5.6,
                "payback_period": 40, "customer_count": 1000,
                "total_acquisition_cost": 80000
            },
            {
                "channel": "TikTok Live",
                "ltv": 600, "cac": 120, "ltv_cac_ratio": 5.0,
                "payback_period": 50, "customer_count": 500,
                "total_acquisition_cost": 60000
            },
            {
                "channel": "Organic Traffic",
                "ltv": 400, "cac": 30, "ltv_cac_ratio": 13.3,
                "payback_period": 20, "customer_count": 2000,
                "total_acquisition_cost": 60000
            },
            {
                "channel": "Instagram Ads",
                "ltv": 350, "cac": 70, "ltv_cac_ratio": 5.0,
                "payback_period": 55, "customer_count": 300,
                "total_acquisition_cost": 21000
            },
            {
                "channel": "Pinterest",
                "ltv": 300, "cac": 50, "ltv_cac_ratio": 6.0,
                "payback_period": 45, "customer_count": 200,
                "total_acquisition_cost": 10000
            },
        ]

        filtered = [c for c in channels if not channel or c['channel'] == channel]

        total_customers = sum(c['customer_count'] for c in filtered)
        total_ltv = sum(c['ltv'] * c['customer_count'] for c in filtered) / max(1, total_customers)
        total_cac = sum(c['total_acquisition_cost'] for c in filtered) / max(1, total_customers)

        return {
            "overview": {
                "total_ltv": round(total_ltv, 2),
                "total_cac": round(total_cac, 2),
                "ltv_cac_ratio": round(total_ltv / max(1, total_cac), 2),
                "payback_period_days": round(total_cac / max(1, total_ltv / 365), 0),
            },
            "by_channel": filtered,
            "cohort_analysis": {
                "channel": "TikTok Ads",
                "ltv_by_cohort": {"2024-01": 300, "2024-02": 350, "2024-03": 400, "2024-04": 450},
                "cac_by_cohort": {"2024-01": 90, "2024-02": 85, "2024-03": 80, "2024-04": 80},
            },
            "recommendations": {
                "high_value_channels": ["TikTok Ads", "TikTok Live"],
                "low_efficiency_channels": ["Instagram Ads"],
                "budget_optimization": {
                    "increase_budget_for": ["TikTok Ads"],
                    "reduce_budget_for": ["Instagram Ads"],
                }
            }
        }

    def get_channel_value(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        value_dimension: str = 'ltv'
    ) -> dict:
        """Evaluate traffic channel value"""
        ranking = [
            {
                "channel": "TikTok Ads - Interest Recommendation", "rank": 1, "score": 9.5,
                "ltv": 500, "cac": 80, "conversion_rate": 0.05,
                "avg_order_value": 100, "profit_margin": 0.3,
                "customer_retention_rate": 0.7, "value_score": 9.5
            },
            {
                "channel": "TikTok Live", "rank": 2, "score": 8.8,
                "ltv": 600, "cac": 120, "conversion_rate": 0.08,
                "avg_order_value": 120, "profit_margin": 0.25,
                "customer_retention_rate": 0.65, "value_score": 8.8
            },
            {
                "channel": "Organic Search", "rank": 3, "score": 8.2,
                "ltv": 400, "cac": 30, "conversion_rate": 0.03,
                "avg_order_value": 90, "profit_margin": 0.35,
                "customer_retention_rate": 0.60, "value_score": 8.2
            },
        ]

        return {
            "channel_ranking": ranking,
            "channel_comparison": {
                "ltv_distribution": {"TikTok Ads": 0.4, "TikTok Live": 0.3, "Organic Traffic": 0.3},
                "cac_distribution": {"TikTok Ads": 0.35, "TikTok Live": 0.4, "Organic Traffic": 0.25},
            }
        }
