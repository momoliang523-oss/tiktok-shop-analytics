/**
 * TypeScript type definitions for API responses and data models
 */

// ==================== Sales Types ====================
export interface SalesTrendData {
  dates: string[];
  metrics: {
    revenue: number[];
    orders: number[];
    avg_order_value: number[];
  };
  summary: {
    total_revenue: number;
    total_orders: number;
    avg_order_value: number;
    daily_avg_revenue: number;
  };
}

export interface SalesRanking {
  ranking: {
    name: string;
    value: number;
    orders: number;
    conversion_rate?: number;
  }[];
}

// ==================== Product/SKU Types ====================
export interface SkuPerformance {
  skus: {
    sku_id: string;
    product_name: string;
    pattern_name: string;
    pattern_category: string;
    color: string;
    size: string;
    sales: number;
    revenue: number;
    conversion_rate: number;
    pattern_score: number;
    pattern_life_cycle: string;
  }[];
  summary: {
    total_skus: number;
    total_sales: number;
    top_pattern: string;
    pattern_diversity: number;
  };
}

export interface PatternAnalysis {
  patterns: {
    pattern_name: string;
    category: string;
    total_sales: number;
    total_revenue: number;
    sku_count: number;
    avg_price: number;
    popularity_score: number;
    growth_rate: number;
    life_cycle: string;
    seasonal: boolean;
    generational_preference?: string[];
    regional_popularity?: Record<string, number>;
  }[];
  insights: {
    trending_patterns: string[];
    declining_patterns: string[];
    cross_selling_opportunities: string[];
    seasonal_patterns: {
      upcoming: string[];
      year_round: string[];
    };
    american_market_specific?: {
      regional_preferences: Record<string, string>;
      generational_preferences: Record<string, string>;
      cultural_themes: Record<string, string[]>;
    };
    recommendations: {
      design_trends: string[];
      marketing_strategies: string[];
    };
  };
}

// ==================== Customer Types ====================
export interface CustomerSegment {
  segment_id: string;
  segment_name: string;
  segment_type: string;
  channel: string;
  size: number;
  percentage: number;
  characteristics: {
    avg_ltv: number;
    avg_cac: number;
    ltv_cac_ratio: number;
    avg_order_value: number;
    purchase_frequency: number;
    avg_time_to_first_purchase: number;
    preferred_patterns: string[];
    price_sensitivity: string;
    discount_sensitivity: string;
  };
  demographics: {
    age_range: string;
    gender: string;
    location: string;
    income_level: string;
    education: string;
    ethnicity: string;
  };
  marketing_insights: {
    best_messaging: string;
    best_channel: string;
    optimal_send_time: string;
    preferred_content: string;
    churn_risk: string;
    upsell_potential: string;
    payment_preference: string;
  };
}

export interface RfmAnalysis {
  recency: number;
  frequency: number;
  monetary: number;
  segment: string;
}

// ==================== LTV/CAC Types ====================
export interface LtvCacData {
  overview: {
    total_ltv: number;
    total_cac: number;
    ltv_cac_ratio: number;
    payback_period_days: number;
  };
  by_channel: {
    channel: string;
    ltv: number;
    cac: number;
    ltv_cac_ratio: number;
    payback_period: number;
    customer_count: number;
    total_acquisition_cost: number;
  }[];
  recommendations: {
    high_value_channels: string[];
    low_efficiency_channels: string[];
    budget_optimization: {
      increase_budget_for: string[];
      reduce_budget_for: string[];
    };
  };
}

export interface ChannelValue {
  channel_ranking: {
    channel: string;
    rank: number;
    score: number;
    ltv: number;
    cac: number;
    conversion_rate: number;
    avg_order_value: number;
    profit_margin: number;
    customer_retention_rate: number;
    value_score: number;
  }[];
}

// ==================== Live Types ====================
export interface LiveOverview {
  summary: {
    total_live_sessions: number;
    total_views: number;
    total_orders: number;
    conversion_rate: number;
    avg_watch_time: number;
  };
  trend?: {
    dates: string[];
    views: number[];
    orders: number[];
  };
}

// ==================== Traffic Types ====================
export interface TrafficFunnel {
  funnel: {
    stage: string;
    value: number;
  }[];
}

// ==================== Advanced Analytics Types ====================
export interface CorrelationMatrix {
  correlation_matrix: (string | number)[][];
  significance?: Record<string, number>;
}

export interface ClusteringResult {
  clusters: {
    cluster_id: number;
    count: number;
    centroid: number[];
    characteristics: string;
  }[];
}

// ==================== Report Types ====================
export interface ReportTask {
  task_id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  progress?: number;
  download_url?: string;
}

// ==================== Import Types ====================
export interface ImportStatus {
  upload_id: string;
  status: 'processing' | 'completed' | 'failed';
  total_rows: number;
  processed_rows: number;
  errors: string[];
}

// ==================== Dashboard Types ====================
export interface DashboardData {
  sales_overview: SalesTrendData;
  top_products: SalesRanking;
  top_patterns: PatternAnalysis;
  traffic_summary: TrafficFunnel;
  ltv_cac_overview: LtvCacData;
}
