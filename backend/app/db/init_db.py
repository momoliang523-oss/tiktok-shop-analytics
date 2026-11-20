"""
Database initialization script
"""
from sqlalchemy import text
from app.db.base import engine, Base
from app.models.database import (
    Order, OrderItem, Product, ProductSku, Customer, CustomerLtvCac,
    LiveSession, LiveProduct, Traffic, Campaign, DataImport, Report, CustomerSegment
)
from app.core.config import get_settings

settings = get_settings()


def init_database():
    """
    Initialize database by creating all tables
    """
    print(f"🗄️  Initializing database: {settings.DATABASE_URL}")

    # Create all tables
    Base.metadata.create_all(bind=engine)

    print("✅ Database tables created successfully")


def drop_database():
    """
    Drop all tables (use with caution!)
    """
    print("⚠️  Dropping all database tables...")

    # Drop all tables
    Base.metadata.drop_all(bind=engine)

    print("✅ Database tables dropped successfully")


def reset_database():
    """
    Reset database by dropping and recreating all tables
    """
    print("🔄 Resetting database...")
    drop_database()
    init_database()


def create_materialized_views():
    """
    Create materialized views for performance optimization
    """
    print("📊 Creating materialized views...")

    with engine.connect() as conn:
        # Daily sales summary
        conn.execute(text("""
            CREATE MATERIALIZED VIEW IF NOT EXISTS daily_sales_summary AS
            SELECT
                order_date::date as date,
                COUNT(*) as order_count,
                SUM(total_amount) as total_revenue,
                SUM(subtotal) as subtotal_revenue,
                SUM(discount_amount) as total_discount,
                AVG(total_amount) as avg_order_value,
                COUNT(DISTINCT customer_id) as unique_customers,
                SUM(CASE WHEN live_session_id IS NOT NULL THEN 1 ELSE 0 END) as live_orders
            FROM orders
            WHERE status IN ('completed', 'paid')
            GROUP BY order_date::date
            WITH DATA;
        """))

        # Daily SKU sales
        conn.execute(text("""
            CREATE MATERIALIZED VIEW IF NOT EXISTS daily_sku_sales AS
            SELECT
                o.order_date::date as date,
                oi.sku_id,
                ps.pattern_name,
                ps.pattern_category,
                SUM(oi.quantity) as quantity,
                SUM(oi.total_price) as revenue,
                COUNT(DISTINCT o.customer_id) as unique_customers,
                AVG(oi.unit_price) as avg_price
            FROM orders o
            JOIN order_items oi ON o.id = oi.order_id
            LEFT JOIN product_skus ps ON oi.sku_id = ps.id
            WHERE o.status IN ('completed', 'paid')
            GROUP BY
                o.order_date::date,
                oi.sku_id,
                ps.pattern_name,
                ps.pattern_category
            WITH DATA;
        """))

        # Pattern performance
        conn.execute(text("""
            CREATE MATERIALIZED VIEW IF NOT EXISTS pattern_performance AS
            SELECT
                pattern_name,
                pattern_category,
                COUNT(DISTINCT sku_id) as sku_count,
                SUM(total_sales) as total_sales,
                SUM(total_revenue) as total_revenue,
                AVG(price) as avg_price,
                AVG(pattern_score) as avg_pattern_score,
                MAX(last_sale_date) as latest_sale_date
            FROM product_skus
            WHERE pattern_name IS NOT NULL
            GROUP BY pattern_name, pattern_category
            WITH DATA;
        """))

        # Channel LTV/CAC summary
        conn.execute(text("""
            CREATE MATERIALIZED VIEW IF NOT EXISTS channel_ltv_cac_summary AS
            SELECT
                acquisition_channel,
                COUNT(*) as customer_count,
                AVG(lifetime_value) as avg_ltv,
                AVG(acquisition_cost) as avg_cac,
                AVG(ltv_cac_ratio) as avg_ltv_cac_ratio,
                AVG(payback_period_days) as avg_payback_period,
                SUM(acquisition_cost) as total_acquisition_cost
            FROM customer_ltv_cac
            GROUP BY acquisition_channel
            WITH DATA;
        """))

        # Segment performance
        conn.execute(text("""
            CREATE MATERIALIZED VIEW IF NOT EXISTS segment_performance AS
            SELECT
                segment_name,
                segment_type,
                size,
                percentage,
                avg_ltv,
                avg_cac,
                avg_ltv_cac_ratio,
                avg_order_value,
                primary_channel
            FROM customer_segments
            WITH DATA;
        """))

        conn.commit()

    print("✅ Materialized views created successfully")


def refresh_materialized_views():
    """
    Refresh all materialized views
    """
    print("🔄 Refreshing materialized views...")

    views = [
        "daily_sales_summary",
        "daily_sku_sales",
        "pattern_performance",
        "channel_ltv_cac_summary",
        "segment_performance"
    ]

    with engine.connect() as conn:
        for view in views:
            conn.execute(text(f"REFRESH MATERIALIZED VIEW CONCURRENTLY {view};"))
        conn.commit()

    print("✅ Materialized views refreshed successfully")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "init":
            init_database()
        elif command == "drop":
            drop_database()
        elif command == "reset":
            reset_database()
        elif command == "views":
            create_materialized_views()
        elif command == "refresh":
            refresh_materialized_views()
        else:
            print(f"Unknown command: {command}")
            print("Available commands: init, drop, reset, views, refresh")
    else:
        init_database()
        create_materialized_views()
