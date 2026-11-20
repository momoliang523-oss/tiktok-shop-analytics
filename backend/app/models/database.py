"""
Database models for TikTok Shop Analytics
"""
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Column, String, Integer, Numeric, DateTime, Boolean, JSONB, Text, ForeignKey, Index, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Order(Base):
    """Order table"""
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_number = Column(String(50), unique=True, nullable=False, index=True)
    customer_id = Column(String(100), nullable=False, index=True)
    order_date = Column(DateTime, nullable=False, index=True)
    status = Column(String(50), nullable=False, index=True)

    # 订单金额
    subtotal = Column(Numeric(12, 2), nullable=False)
    discount_amount = Column(Numeric(12, 2), default=0)
    shipping_fee = Column(Numeric(12, 2), default=0)
    total_amount = Column(Numeric(12, 2), nullable=False)

    # 订单信息
    currency = Column(String(10), default="USD")
    payment_method = Column(String(50))

    # 营销信息
    coupon_code = Column(String(50))
    campaign_id = Column(String(100))

    # 直播相关
    live_session_id = Column(String(100))
    live_host_id = Column(String(100))

    # 流量来源
    traffic_source = Column(String(100))
    traffic_medium = Column(String(100))

    # 元数据
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    raw_data = Column(JSONB)

    # Relationships
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_orders_date", "order_date"),
        Index("idx_orders_customer", "customer_id"),
        Index("idx_orders_status", "status"),
        Index("idx_orders_live", "live_session_id"),
        Index("idx_orders_traffic", "traffic_source"),
    )


class OrderItem(Base):
    """Order items table"""
    __tablename__ = "order_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(String(100), nullable=False, index=True)
    product_name = Column(String(500), nullable=False)
    product_sku = Column(String(100))
    sku_id = Column(String(100), nullable=False, index=True)

    # 商品信息
    category_id = Column(String(100))
    category_name = Column(String(200))

    # 图案样式（美国市场）
    pattern_name = Column(String(200))
    pattern_category = Column(String(100))
    pattern_style = Column(String(100))
    cultural_theme = Column(String(100))
    pop_culture_reference = Column(Boolean, default=False)

    # 规格属性
    color = Column(String(50))
    color_hex = Column(String(20))
    size = Column(String(50))

    # 数量和价格
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(12, 2), nullable=False)
    total_price = Column(Numeric(12, 2), nullable=False)

    # 优惠信息
    discount_amount = Column(Numeric(12, 2), default=0)

    # 直播相关
    is_live_product = Column(Boolean, default=False)
    live_show_time = Column(DateTime)

    # 元数据
    created_at = Column(DateTime, default=datetime.utcnow)
    raw_data = Column(JSONB)

    # Relationships
    order = relationship("Order", back_populates="order_items")

    __table_args__ = (
        Index("idx_order_items_order", "order_id"),
        Index("idx_order_items_product", "product_id"),
        Index("idx_order_items_sku", "sku_id"),
        Index("idx_order_items_category", "category_id"),
    )


class Product(Base):
    """Product table"""
    __tablename__ = "products"

    id = Column(String(100), primary_key=True)
    name = Column(String(500), nullable=False)
    sku = Column(String(100))

    # 分类信息
    category_id = Column(String(100))
    category_name = Column(String(200))
    subcategory_id = Column(String(100))
    subcategory_name = Column(String(200))

    # 价格信息
    price = Column(Numeric(12, 2), nullable=False)
    original_price = Column(Numeric(12, 2))
    cost_price = Column(Numeric(12, 2))

    # 库存信息
    stock_quantity = Column(Integer, default=0)
    sold_quantity = Column(Integer, default=0)

    # 商品属性
    brand = Column(String(200))
    weight = Column(Numeric(10, 2))
    attributes = Column(JSONB)

    # 状态
    status = Column(String(50), default="active", index=True)

    # 时间信息
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    first_published_at = Column(DateTime)

    # 元数据
    raw_data = Column(JSONB)

    __table_args__ = (
        Index("idx_products_category", "category_id"),
        Index("idx_products_status", "status"),
        Index("idx_products_brand", "brand"),
    )


class ProductSku(Base):
    """Product SKU table - 核心表，美国市场图案分析"""
    __tablename__ = "product_skus"

    id = Column(String(100), primary_key=True)
    product_id = Column(String(100), nullable=False)
    product_name = Column(String(500), nullable=False)

    # SKU基本属性
    sku_code = Column(String(100), unique=True, nullable=False)
    sku_name = Column(String(500))

    # 图案样式（核心维度 - 美国市场）
    pattern_id = Column(String(100))
    pattern_name = Column(String(200), nullable=False)
    pattern_category = Column(String(100))
    pattern_style = Column(String(100))
    cultural_theme = Column(String(100))
    pop_culture_reference = Column(Boolean, default=False)
    season_pattern = Column(Boolean, default=False)

    # 规格属性
    color = Column(String(50))
    color_hex = Column(String(20))
    size = Column(String(50))
    size_category = Column(String(50))

    # 价格信息
    price = Column(Numeric(12, 2), nullable=False)
    original_price = Column(Numeric(12, 2))
    cost_price = Column(Numeric(12, 2))
    discount_rate = Column(Numeric(5, 4))

    # 库存信息
    stock_quantity = Column(Integer, default=0)
    sold_quantity = Column(Integer, default=0)
    reserved_quantity = Column(Integer, default=0)
    low_stock_threshold = Column(Integer, default=10)

    # 销售统计
    total_sales = Column(Integer, default=0)
    total_revenue = Column(Numeric(12, 2), default=0)
    avg_daily_sales = Column(Numeric(10, 2), default=0)

    # 图案表现指标
    pattern_rank = Column(Integer)
    pattern_score = Column(Numeric(5, 2))
    pattern_life_cycle = Column(String(50))

    # 时间信息
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    first_sale_date = Column(DateTime)
    last_sale_date = Column(DateTime)

    # 元数据
    raw_data = Column(JSONB)

    __table_args__ = (
        Index("idx_skus_product", "product_id"),
        Index("idx_skus_pattern", "pattern_name"),
        Index("idx_skus_color", "color"),
        Index("idx_skus_pattern_category", "pattern_category"),
        Index("idx_skus_lifecycle", "pattern_life_cycle"),
    )


class Customer(Base):
    """Customer table"""
    __tablename__ = "customers"

    id = Column(String(100), primary_key=True)

    # 基本信息
    name = Column(String(200))
    email = Column(String(200))
    phone = Column(String(50))

    # 地理信息
    country = Column(String(100))
    province = Column(String(100))
    city = Column(String(100))

    # 统计信息
    total_orders = Column(Integer, default=0)
    total_spent = Column(Numeric(12, 2), default=0)
    avg_order_value = Column(Numeric(12, 2), default=0)

    # RFM分析
    recency_days = Column(Integer)
    frequency = Column(Integer)
    monetary = Column(Numeric(12, 2))
    rfm_segment = Column(String(50))

    # 会员信息
    membership_level = Column(String(50))
    points = Column(Integer, default=0)

    # 时间信息
    first_order_date = Column(DateTime)
    last_order_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 元数据
    raw_data = Column(JSONB)

    __table_args__ = (
        Index("idx_customers_rfm", "rfm_segment"),
        Index("idx_customers_membership", "membership_level"),
        Index("idx_customers_location", "country", "province"),
    )


class CustomerLtvCac(Base):
    """Customer LTV/CAC table"""
    __tablename__ = "customer_ltv_cac"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(String(100), unique=True, nullable=False, index=True)

    # LTV相关
    lifetime_value = Column(Numeric(12, 2), nullable=False)
    ltv_30d = Column(Numeric(12, 2))
    ltv_90d = Column(Numeric(12, 2))
    ltv_180d = Column(Numeric(12, 2))
    ltv_365d = Column(Numeric(12, 2))

    # CAC相关
    acquisition_cost = Column(Numeric(12, 2), nullable=False)
    acquisition_channel = Column(String(100))
    acquisition_source = Column(String(100))
    acquisition_medium = Column(String(100))
    acquisition_campaign = Column(String(200))

    # LTV/CAC指标
    ltv_cac_ratio = Column(Numeric(10, 2))
    payback_period_days = Column(Integer)
    ltv_cac_ratio_30d = Column(Numeric(10, 2))
    ltv_cac_ratio_90d = Column(Numeric(10, 2))
    ltv_cac_ratio_180d = Column(Numeric(10, 2))

    # 流量入口价值指标
    channel_value_score = Column(Numeric(5, 2))
    conversion_rate_from_channel = Column(Numeric(5, 4))
    retention_rate_from_channel = Column(Numeric(5, 4))

    # 时间信息
    first_acquisition_date = Column(DateTime, nullable=False)
    calculated_at = Column(DateTime, default=datetime.utcnow)

    # 元数据
    raw_data = Column(JSONB)

    __table_args__ = (
        Index("idx_ltv_cac_customer", "customer_id"),
        Index("idx_ltv_cac_channel", "acquisition_channel"),
        Index("idx_ltv_cac_ratio", "ltv_cac_ratio"),
    )


class LiveSession(Base):
    """Live session table"""
    __tablename__ = "live_sessions"

    id = Column(String(100), primary_key=True)

    # 基本信息
    title = Column(String(500))
    description = Column(Text)
    host_id = Column(String(100))
    host_name = Column(String(200))

    # 时间信息
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    duration_seconds = Column(Integer)

    # 流量数据
    total_views = Column(Integer, default=0)
    peak_concurrent_users = Column(Integer, default=0)
    avg_concurrent_users = Column(Integer, default=0)
    total_watch_time_seconds = Column(Integer, default=0)

    # 互动数据
    total_likes = Column(Integer, default=0)
    total_comments = Column(Integer, default=0)
    total_shares = Column(Integer, default=0)

    # 转化数据
    total_orders = Column(Integer, default=0)
    total_revenue = Column(Numeric(12, 2), default=0)
    conversion_rate = Column(Numeric(5, 4), default=0)

    # 商品信息
    products_count = Column(Integer, default=0)

    # 时间信息
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 元数据
    raw_data = Column(JSONB)

    __table_args__ = (
        Index("idx_live_sessions_time", "start_time", "end_time"),
        Index("idx_live_sessions_host", "host_id"),
        Index("idx_live_sessions_revenue", "total_revenue"),
    )


class LiveProduct(Base):
    """Live product performance table"""
    __tablename__ = "live_products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    live_session_id = Column(String(100), ForeignKey("live_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(String(100), nullable=False)
    product_name = Column(String(500), nullable=False)
    sku_id = Column(String(100), nullable=False)

    # 展示信息
    show_time = Column(DateTime)
    show_duration_seconds = Column(Integer)
    show_order = Column(Integer)

    # 表现数据
    views = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    orders = Column(Integer, default=0)
    revenue = Column(Numeric(12, 2), default=0)
    conversion_rate = Column(Numeric(5, 4), default=0)

    # 价格信息
    price = Column(Numeric(12, 2))
    discount_price = Column(Numeric(12, 2))

    # 元数据
    created_at = Column(DateTime, default=datetime.utcnow)
    raw_data = Column(JSONB)

    __table_args__ = (
        Index("idx_live_products_session", "live_session_id"),
        Index("idx_live_products_product", "product_id"),
    )


class Traffic(Base):
    """Traffic table"""
    __tablename__ = "traffic"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(Date, nullable=False)

    # 渠道信息
    source = Column(String(100), nullable=False)
    medium = Column(String(100))
    campaign = Column(String(200))

    # 流量数据
    impressions = Column(Integer, default=0)
    visits = Column(Integer, default=0)
    unique_visitors = Column(Integer, default=0)
    page_views = Column(Integer, default=0)

    # 转化数据
    product_views = Column(Integer, default=0)
    add_to_carts = Column(Integer, default=0)
    checkouts = Column(Integer, default=0)
    orders = Column(Integer, default=0)
    revenue = Column(Numeric(12, 2), default=0)

    # 计算指标
    click_through_rate = Column(Numeric(5, 4), default=0)
    conversion_rate = Column(Numeric(5, 4), default=0)
    avg_order_value = Column(Numeric(12, 2), default=0)

    # 时间信息
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 元数据
    raw_data = Column(JSONB)

    __table_args__ = (
        Index("idx_traffic_unique", "date", "source", "medium", "campaign", unique=True),
        Index("idx_traffic_date", "date"),
        Index("idx_traffic_source", "source"),
    )


class Campaign(Base):
    """Campaign table"""
    __tablename__ = "campaigns"

    id = Column(String(100), primary_key=True)
    name = Column(String(500), nullable=False)
    type = Column(String(50), nullable=False)

    # 时间信息
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)

    # 预算和成本
    budget = Column(Numeric(12, 2))
    cost = Column(Numeric(12, 2), default=0)

    # 效果数据
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    orders = Column(Integer, default=0)
    revenue = Column(Numeric(12, 2), default=0)

    # 计算指标
    click_through_rate = Column(Numeric(5, 4), default=0)
    conversion_rate = Column(Numeric(5, 4), default=0)
    cost_per_click = Column(Numeric(12, 2), default=0)
    cost_per_order = Column(Numeric(12, 2), default=0)
    return_on_investment = Column(Numeric(5, 2), default=0)

    # 优惠信息
    discount_type = Column(String(50))
    discount_value = Column(Numeric(12, 2))

    # 状态
    status = Column(String(50), default="active", index=True)

    # 时间信息
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 元数据
    raw_data = Column(JSONB)

    __table_args__ = (
        Index("idx_campaigns_date", "start_date", "end_date"),
        Index("idx_campaigns_type", "type"),
        Index("idx_campaigns_status", "status"),
    )


class DataImport(Base):
    """Data import record table"""
    __tablename__ = "data_imports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # 文件信息
    file_name = Column(String(500), nullable=False)
    file_size = Column(Integer)
    file_type = Column(String(50), nullable=False)

    # 数据类型
    data_type = Column(String(50), nullable=False)

    # 处理状态
    status = Column(String(50), nullable=False, index=True)

    # 处理结果
    total_rows = Column(Integer)
    processed_rows = Column(Integer, default=0)
    success_rows = Column(Integer, default=0)
    error_rows = Column(Integer, default=0)

    # 错误信息
    error_details = Column(JSONB)

    # 时间信息
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

    # 用户信息
    uploaded_by = Column(String(100))

    __table_args__ = (
        Index("idx_data_imports_status", "status"),
        Index("idx_data_imports_type", "data_type"),
    )


class Report(Base):
    """Report generation record table"""
    __tablename__ = "reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # 报告信息
    report_type = Column(String(50), nullable=False)
    title = Column(String(500), nullable=False)

    # 参数
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    parameters = Column(JSONB)

    # 处理状态
    status = Column(String(50), nullable=False, index=True)
    progress = Column(Integer, default=0)

    # 文件信息
    file_path = Column(String(1000))
    file_size = Column(Integer)
    download_url = Column(String(1000))

    # 时间信息
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

    # 用户信息
    created_by = Column(String(100))

    __table_args__ = (
        Index("idx_reports_status", "status"),
        Index("idx_reports_type", "report_type"),
        Index("idx_reports_date", "created_at"),
    )


class CustomerSegment(Base):
    """Customer segmentation table"""
    __tablename__ = "customer_segments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    segment_id = Column(String(100), unique=True, nullable=False)
    segment_name = Column(String(200), nullable=False)
    segment_type = Column(String(50), nullable=False)  # behavioral, demographic, psychographic, value_based

    # 分群特征
    size = Column(Integer, nullable=False)
    percentage = Column(Numeric(5, 2), nullable=False)

    # 统计指标
    avg_ltv = Column(Numeric(12, 2))
    avg_cac = Column(Numeric(12, 2))
    avg_ltv_cac_ratio = Column(Numeric(10, 2))
    avg_order_value = Column(Numeric(12, 2))
    purchase_frequency = Column(Numeric(5, 2))
    avg_time_to_first_purchase = Column(Numeric(10, 2))

    # 人群属性（美国市场）
    demographics = Column(JSONB)
    behavior_patterns = Column(JSONB)
    preferences = Column(JSONB)
    american_market_insights = Column(JSONB)

    # 营销洞察
    marketing_insights = Column(JSONB)
    churn_risk = Column(String(50))
    upsell_potential = Column(String(50))

    # 分群维度
    primary_channel = Column(String(100))
    primary_pattern_preference = Column(String(200))
    price_sensitivity = Column(String(50))

    # 时间信息
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 元数据
    raw_data = Column(JSONB)

    __table_args__ = (
        Index("idx_segments_type", "segment_type"),
        Index("idx_segments_channel", "primary_channel"),
        Index("idx_segments_size", "size"),
    )
