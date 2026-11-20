"""
Sales trend analysis service
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional
from statsmodels.tsa.seasonal import STL


class SalesAnalyzer:
    """Sales trend and ranking analysis"""

    def __init__(self, db=None):
        self.db = db

    def get_sales_trend(
        self,
        start_date: str,
        end_date: str,
        granularity: str = 'day',
        metrics: Optional[list] = None
    ) -> dict:
        """
        Calculate sales trend data

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            granularity: 'day', 'week', or 'month'
            metrics: List of metrics to include
        """
        if metrics is None:
            metrics = ['revenue', 'orders', 'avg_order_value']

        # Generate date range
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        dates = date_range.strftime('%Y-%m-%d').tolist()

        # TODO: Replace with actual database query
        # For now, generate sample data
        np.random.seed(42)
        n_days = len(dates)
        base_revenue = 1000
        trend = np.linspace(0, 500, n_days)
        noise = np.random.normal(0, 100, n_days)
        revenue = (base_revenue + trend + noise).tolist()

        orders = [max(0, int(r / 100 + np.random.randint(-2, 3))) for r in revenue]
        avg_order_value = [revenue[i] / max(1, orders[i]) for i in range(n_days)]

        result = {
            "dates": dates,
            "metrics": {
                "revenue": [round(r, 2) for r in revenue],
                "orders": orders,
                "avg_order_value": [round(v, 2) for v in avg_order_value],
            },
            "summary": {
                "total_revenue": round(sum(revenue), 2),
                "total_orders": sum(orders),
                "avg_order_value": round(sum(revenue) / max(1, sum(orders)), 2),
                "daily_avg_revenue": round(sum(revenue) / n_days, 2),
            }
        }

        # Add seasonal decomposition if enough data
        if n_days >= 14:
            try:
                series = pd.Series(revenue, index=date_range)
                stl = STL(series, period=min(7, n_days // 2))
                result_decomp = stl.fit()
                result["seasonal"] = {
                    "trend": [round(v, 2) if not np.isnan(v) else None for v in result_decomp.trend.values],
                    "seasonal": [round(v, 2) if not np.isnan(v) else None for v in result_decomp.seasonal.values],
                    "residual": [round(v, 2) if not np.isnan(v) else None for v in result_decomp.resid.values],
                }
            except Exception:
                pass  # Skip decomposition if fails

        return result

    def get_sales_ranking(
        self,
        dimension: str = 'product',
        top_n: int = 10,
        start_date: str = None,
        end_date: str = None
    ) -> dict:
        """
        Get sales ranking by dimension

        Args:
            dimension: 'product', 'category', or 'customer'
            top_n: Number of top items to return
            start_date: Start date filter
            end_date: End date filter
        """
        # TODO: Replace with actual database query
        sample_data = {
            'product': [
                {"name": "Graphic T-Shirt - Space Theme", "value": 15000, "orders": 300},
                {"name": "Graphic T-Shirt - Retro 80s", "value": 12000, "orders": 240},
                {"name": "Hoodie - Minimalist Typography", "value": 18000, "orders": 200},
                {"name": "Graphic T-Shirt - Galaxy Pattern", "value": 10000, "orders": 200},
                {"name": "Sweatshirt - Abstract Geometric", "value": 9000, "orders": 150},
                {"name": "Tank Top - Surf Culture", "value": 8000, "orders": 200},
                {"name": "Long Sleeve - Nature Inspired", "value": 7500, "orders": 150},
                {"name": "Graphic T-Shirt - Meme Culture", "value": 7000, "orders": 175},
                {"name": "Hoodie - Halloween Special", "value": 6500, "orders": 130},
                {"name": "T-Shirt - Patriotic Theme", "value": 6000, "orders": 120},
            ],
            'category': [
                {"name": "Pop Culture", "value": 35000, "orders": 700},
                {"name": "Abstract/Sci-Fi", "value": 30000, "orders": 600},
                {"name": "Typography", "value": 25000, "orders": 500},
                {"name": "Nature", "value": 20000, "orders": 400},
                {"name": "Seasonal/Holiday", "value": 15000, "orders": 300},
            ],
        }

        return {
            "ranking": sample_data.get(dimension, sample_data['product'])[:top_n]
        }

    def get_yoy_comparison(
        self,
        metric: str = 'revenue',
        current_start: str = None,
        current_end: str = None
    ) -> dict:
        """
        Year-over-year comparison

        Args:
            metric: Metric to compare
            current_start: Current period start
            current_end: Current period end
        """
        # Calculate YoY automatically
        if current_end is None:
            current_end = datetime.now().strftime('%Y-%m-%d')
        if current_start is None:
            current_start = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

        # Previous year same period
        prev_start = (datetime.strptime(current_start, '%Y-%m-%d') - timedelta(days=365)).strftime('%Y-%m-%d')
        prev_end = (datetime.strptime(current_end, '%Y-%m-%d') - timedelta(days=365)).strftime('%Y-%m-%d')

        # Get current period data
        current_data = self.get_sales_trend(current_start, current_end)
        current_total = current_data['summary']['total_revenue']

        # Get previous period data
        prev_data = self.get_sales_trend(prev_start, prev_end)
        prev_total = prev_data['summary']['total_revenue']

        yoy_change = ((current_total - prev_total) / max(1, prev_total)) * 100

        return {
            "current_period": {
                "start": current_start,
                "end": current_end,
                "total": current_total,
            },
            "previous_period": {
                "start": prev_start,
                "end": prev_end,
                "total": prev_total,
            },
            "yoy_change_pct": round(yoy_change, 2),
        }
