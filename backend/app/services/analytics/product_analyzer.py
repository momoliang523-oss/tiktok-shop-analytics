"""
Product and SKU analysis service with US market pattern analysis
"""
import numpy as np
from typing import Optional
from collections import Counter


class ProductAnalyzer:
    """SKU-level product analysis with pattern intelligence"""

    US_REGIONS = ['west', 'east', 'midwest', 'south']
    US_GENERATIONS = ['gen_z', 'millennial', 'gen_x', 'boomer']
    PATTERN_CATEGORIES = ['animal', 'plant', 'geometric', 'typography', 'abstract', 'pop_culture', 'seasonal']
    PATTERN_STYLES = ['cartoon', 'realistic', 'minimalist', 'graffiti', 'retro', 'futuristic']
    CULTURAL_THEMES = ['halloween', 'thanksgiving', 'christmas', 'independence_day', 'super_bowl', 'generic']
    LIFE_CYCLE_STAGES = ['new', 'growth', 'mature', 'decline']

    def __init__(self, db=None):
        self.db = db

    def get_sku_performance(
        self,
        pattern_name: Optional[str] = None,
        color: Optional[str] = None,
        size: Optional[str] = None,
        sort_by: str = 'sales',
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> dict:
        """Get SKU performance data with pattern details"""
        # TODO: Replace with actual database query
        sample_skus = [
            {
                "sku_id": "SKU001", "product_name": "Graphic T-Shirt",
                "pattern_name": "Space/Galaxy", "pattern_category": "Abstract/Sci-Fi",
                "color": "Black", "size": "L", "sales": 500, "revenue": 12500,
                "conversion_rate": 0.05, "pattern_score": 9.2, "pattern_life_cycle": "growth"
            },
            {
                "sku_id": "SKU002", "product_name": "Graphic T-Shirt",
                "pattern_name": "Retro 80s Neon", "pattern_category": "Pop Culture",
                "color": "White", "size": "M", "sales": 450, "revenue": 11250,
                "conversion_rate": 0.045, "pattern_score": 8.9, "pattern_life_cycle": "mature"
            },
            {
                "sku_id": "SKU003", "product_name": "Hoodie",
                "pattern_name": "Minimalist Typography", "pattern_category": "Typography",
                "color": "Gray", "size": "XL", "sales": 400, "revenue": 20000,
                "conversion_rate": 0.04, "pattern_score": 8.5, "pattern_life_cycle": "mature"
            },
            {
                "sku_id": "SKU004", "product_name": "Graphic T-Shirt",
                "pattern_name": "Halloween Spooky", "pattern_category": "Seasonal/Holiday",
                "color": "Orange", "size": "M", "sales": 300, "revenue": 7500,
                "conversion_rate": 0.035, "pattern_score": 7.5, "pattern_life_cycle": "decline"
            },
            {
                "sku_id": "SKU005", "product_name": "Sweatshirt",
                "pattern_name": "Abstract Geometric", "pattern_category": "Abstract",
                "color": "Navy", "size": "L", "sales": 350, "revenue": 14000,
                "conversion_rate": 0.042, "pattern_score": 8.3, "pattern_life_cycle": "growth"
            },
            {
                "sku_id": "SKU006", "product_name": "Tank Top",
                "pattern_name": "Surf Culture", "pattern_category": "Pop Culture",
                "color": "Blue", "size": "M", "sales": 250, "revenue": 5000,
                "conversion_rate": 0.038, "pattern_score": 7.8, "pattern_life_cycle": "growth"
            },
            {
                "sku_id": "SKU007", "product_name": "Long Sleeve",
                "pattern_name": "Nature PNW", "pattern_category": "Nature",
                "color": "Green", "size": "L", "sales": 200, "revenue": 7000,
                "conversion_rate": 0.033, "pattern_score": 7.2, "pattern_life_cycle": "new"
            },
            {
                "sku_id": "SKU008", "product_name": "Graphic T-Shirt",
                "pattern_name": "Meme Culture", "pattern_category": "Pop Culture",
                "color": "White", "size": "S", "sales": 380, "revenue": 9500,
                "conversion_rate": 0.048, "pattern_score": 8.7, "pattern_life_cycle": "growth"
            },
        ]

        # Filter by params
        result = sample_skus
        if pattern_name:
            result = [s for s in result if pattern_name.lower() in s['pattern_name'].lower()]
        if color:
            result = [s for s in result if s['color'] == color]
        if size:
            result = [s for s in result if s['size'] == size]

        # Sort
        result = sorted(result, key=lambda x: x.get(sort_by, 0), reverse=True)

        return {
            "skus": result,
            "summary": {
                "total_skus": len(result),
                "total_sales": sum(s['sales'] for s in result),
                "top_pattern": max(result, key=lambda x: x['pattern_score'])['pattern_name'],
                "pattern_diversity": round(len(set(s['pattern_name'] for s in result)) / max(1, len(result)), 2),
            }
        }

    def get_pattern_analysis(
        self,
        category: Optional[str] = None,
        sort_by: str = 'sales',
        region: Optional[str] = None,
        generation: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> dict:
        """Analyze pattern performance with US market insights"""
        patterns = [
            {
                "pattern_name": "Space/Galaxy", "category": "Abstract/Sci-Fi",
                "total_sales": 500, "total_revenue": 25000, "sku_count": 10,
                "avg_price": 50, "popularity_score": 9.2, "growth_rate": 0.30,
                "life_cycle": "growth", "seasonal": False,
                "generational_preference": ["gen_z", "millennial"],
                "regional_popularity": {"west": 9.5, "east": 8.8, "midwest": 7.5, "south": 7.2}
            },
            {
                "pattern_name": "Retro 80s Neon", "category": "Pop Culture",
                "total_sales": 450, "total_revenue": 22500, "sku_count": 8,
                "avg_price": 55, "popularity_score": 8.9, "growth_rate": 0.25,
                "life_cycle": "mature", "seasonal": False,
                "generational_preference": ["gen_z", "millennial"],
                "regional_popularity": {"west": 9.2, "east": 8.5, "midwest": 8.0, "south": 7.8}
            },
            {
                "pattern_name": "Minimalist Typography", "category": "Typography",
                "total_sales": 400, "total_revenue": 20000, "sku_count": 15,
                "avg_price": 45, "popularity_score": 8.5, "growth_rate": 0.20,
                "life_cycle": "mature", "seasonal": False,
                "generational_preference": ["millennial", "gen_x", "boomer"],
                "regional_popularity": {"west": 8.8, "east": 9.0, "midwest": 8.5, "south": 8.0}
            },
            {
                "pattern_name": "Halloween Spooky", "category": "Seasonal/Holiday",
                "total_sales": 300, "total_revenue": 15000, "sku_count": 5,
                "avg_price": 50, "popularity_score": 7.5, "growth_rate": -0.40,
                "life_cycle": "decline", "seasonal": True,
                "generational_preference": ["all_generations"],
                "regional_popularity": {"west": 7.5, "east": 7.2, "midwest": 7.8, "south": 7.0}
            },
        ]

        return {
            "patterns": patterns,
            "insights": {
                "trending_patterns": ["Space/Galaxy", "Retro 80s Neon", "Abstract Geometric"],
                "declining_patterns": ["Halloween (outside season)", "Summer specific"],
                "cross_selling_opportunities": [
                    "Space theme + Galaxy patterns",
                    "Retro 80s + Neon colors",
                    "Typography + Quote combinations"
                ],
                "seasonal_patterns": {
                    "upcoming": ["Halloween", "Thanksgiving", "Christmas", "Independence Day"],
                    "year_round": ["Abstract", "Geometric", "Minimalist"]
                },
                "american_market_specific": {
                    "regional_preferences": {
                        "West Coast": "Minimalist, Surf culture, Tech-inspired, California vibes",
                        "East Coast": "Classic, Typography, Abstract, Urban themes",
                        "Midwest": "Rustic, Nature-inspired, Americana, Outdoor themes",
                        "South": "Traditional, Nature, Religious themes, Southern charm"
                    },
                    "generational_preferences": {
                        "Gen Z (1997-2012)": "Retro 80s/90s, Abstract, Pop Culture, Social Media trends, Memes",
                        "Millennials (1981-1996)": "Minimalist, Typography, Sustainable themes, Nostalgia, Wellness",
                        "Gen X (1965-1980)": "Classic, Nostalgia, Americana, Music/Pop Culture",
                        "Boomers (1946-1964)": "Traditional, Nature, Americana, Patriotic, Religious"
                    },
                    "cultural_themes": {
                        "current_events": ["Election year themes", "Climate awareness"],
                        "pop_culture": ["TV show references", "Music artist collaborations"],
                        "social_causes": ["Diversity", "Sustainability", "Mental health awareness"]
                    }
                },
                "recommendations": {
                    "design_trends": [
                        "Incorporate social media quote trends",
                        "Design seasonal collections 2-3 months in advance",
                        "Create region-specific collections"
                    ],
                    "marketing_strategies": [
                        "Target Gen Z with TikTok challenges and influencer partnerships",
                        "Use nostalgia marketing for Gen X and Boomers",
                        "Highlight sustainability and ethical sourcing for Millennials"
                    ]
                }
            }
        }

    def get_sku_association(
        self,
        sku_id: Optional[str] = None,
        pattern_name: Optional[str] = None,
        top_n: int = 5
    ) -> dict:
        """Get SKU association rules based on pattern co-purchase"""
        # TODO: Implement Apriori algorithm with actual data
        associations = [
            {"sku_id": "SKU002", "name": "Retro 80s Neon T-Shirt", "score": 0.85},
            {"sku_id": "SKU005", "name": "Abstract Geometric Sweatshirt", "score": 0.72},
            {"sku_id": "SKU008", "name": "Meme Culture T-Shirt", "score": 0.68},
            {"sku_id": "SKU004", "name": "Halloween Spooky T-Shirt", "score": 0.55},
            {"sku_id": "SKU007", "name": "Nature PNW Long Sleeve", "score": 0.42},
        ]

        return {
            "associations": associations[:top_n],
            "insight": "Customers who buy Space/Galaxy patterns often also purchase Retro 80s designs, suggesting a shared interest in nostalgic/futuristic themes."
        }

    def get_sku_inventory(
        self,
        low_stock_only: bool = False,
        pattern_name: Optional[str] = None
    ) -> dict:
        """Get SKU inventory status"""
        inventory = [
            {"sku_id": "SKU001", "sku_name": "Space/Galaxy T-Shirt L Black",
             "stock": 25, "sold": 500, "turnover_rate": 20.0, "status": "healthy"},
            {"sku_id": "SKU002", "sku_name": "Retro 80s T-Shirt M White",
             "stock": 8, "sold": 450, "turnover_rate": 56.25, "status": "low_stock"},
            {"sku_id": "SKU004", "sku_name": "Halloween T-Shirt M Orange",
             "stock": 50, "sold": 300, "turnover_rate": 6.0, "status": "overstock"},
            {"sku_id": "SKU007", "sku_name": "Nature PNW Long Sleeve L Green",
             "stock": 5, "sold": 200, "turnover_rate": 40.0, "status": "low_stock"},
        ]

        if low_stock_only:
            inventory = [i for i in inventory if i['status'] == 'low_stock']

        return {
            "inventory": inventory,
            "summary": {
                "total_items": len(inventory),
                "low_stock_count": sum(1 for i in inventory if i['status'] == 'low_stock'),
                "overstock_count": sum(1 for i in inventory if i['status'] == 'overstock'),
                "healthy_count": sum(1 for i in inventory if i['status'] == 'healthy'),
            }
        }
