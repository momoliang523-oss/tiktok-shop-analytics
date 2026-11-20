import { Row, Col, Card, Statistic, Spin, Tabs } from 'antd'
import {
  DollarOutlined, ShoppingCartOutlined, UserOutlined, RiseOutlined,
} from '@ant-design/icons'
import ReactEChartsCore from 'echarts-for-react/lib/core'
import * as echarts from 'echarts/core'
import { LineChart, BarChart, PieChart, ScatterChart } from 'echarts/charts'
import {
  GridComponent, TooltipComponent, TitleComponent, LegendComponent, DataZoomComponent,
} from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { useSalesTrend, usePatternAnalysis, useLtvCac } from '../../hooks/useData'
import { useFilterStore } from '../../store'
import { formatCurrency, formatNumber } from '../../utils/formatters'

echarts.use([
  LineChart, BarChart, PieChart, ScatterChart, GridComponent, TooltipComponent,
  TitleComponent, LegendComponent, DataZoomComponent, CanvasRenderer,
])

export default function Dashboard() {
  const { dateRange } = useFilterStore()

  const { data: salesData, isLoading: salesLoading } = useSalesTrend({
    start_date: dateRange.start_date,
    end_date: dateRange.end_date,
    granularity: 'day',
  })

  const { data: patternData, isLoading: patternLoading } = usePatternAnalysis({
    start_date: dateRange.start_date,
    end_date: dateRange.end_date,
  })

  const { data: ltvData, isLoading: ltvLoading } = useLtvCac({
    start_date: dateRange.start_date,
    end_date: dateRange.end_date,
  })

  const saleStats = salesData?.data
  const patterns = patternData?.data
  const ltvStats = ltvData?.data

  const revenueTrendOption = {
    tooltip: { trigger: 'axis' },
    legend: { data: ['Revenue', 'Orders'] },
    xAxis: { type: 'category', data: saleStats?.dates || [], boundaryGap: false },
    yAxis: [
      { type: 'value', name: 'Revenue ($)' },
      { type: 'value', name: 'Orders' },
    ],
    series: [
      {
        name: 'Revenue', type: 'line', smooth: true,
        data: saleStats?.metrics?.revenue || [],
        areaStyle: { opacity: 0.15 },
        lineStyle: { color: '#1a1a2e' },
      },
      {
        name: 'Orders', type: 'line', yAxisIndex: 1,
        data: saleStats?.metrics?.orders || [],
        lineStyle: { color: '#e74c3c' },
      },
    ],
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
  }

  const patternPieOption = {
    tooltip: { trigger: 'item' },
    legend: { orient: 'vertical', left: 'left' },
    series: [{
      name: 'Pattern Distribution', type: 'pie', radius: ['40%', '70%'],
      data: patterns?.patterns?.slice(0, 5).map((p: any) => ({
        name: p.pattern_name, value: p.total_revenue,
      })) || [],
      emphasis: { itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0, 0, 0, 0.5)' } },
    }],
  }

  const ltvBarOption = {
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: ltvStats?.by_channel?.map((c: any) => c.channel) || [] },
    yAxis: { type: 'value', name: 'LTV/CAC Ratio' },
    series: [{
      name: 'LTV/CAC', type: 'bar',
      data: ltvStats?.by_channel?.map((c: any) => c.ltv_cac_ratio) || [],
      itemStyle: { color: '#1a1a2e' },
    }],
  }

  return (
    <div>
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={12} md={6}>
          <Card><Statistic title="Total Revenue" value={saleStats?.summary?.total_revenue || 0}
            prefix={<DollarOutlined />} precision={0} formatter={(v) => `$${formatNumber(Number(v))}`} /></Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card><Statistic title="Total Orders" value={saleStats?.summary?.total_orders || 0}
            prefix={<ShoppingCartOutlined />} formatter={(v) => formatNumber(Number(v))} /></Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card><Statistic title="Avg Order Value" value={saleStats?.summary?.avg_order_value || 0}
            prefix={<DollarOutlined />} precision={2} formatter={(v) => `$${Number(v).toFixed(2)}`} /></Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card><Statistic title="LTV/CAC Ratio" value={ltvStats?.overview?.ltv_cac_ratio || 0}
            prefix={<RiseOutlined />} precision={1} suffix="x" /></Card>
        </Col>
      </Row>

      <Tabs defaultActiveKey="revenue" items={[
        {
          key: 'revenue', label: 'Revenue Trend',
          children: <Card><Spin spinning={salesLoading}>
            <ReactEChartsCore echarts={echarts} option={revenueTrendOption} style={{ height: 400 }} />
          </Spin></Card>,
        },
        {
          key: 'patterns', label: 'Pattern Distribution',
          children: <Card><Spin spinning={patternLoading}>
            <ReactEChartsCore echarts={echarts} option={patternPieOption} style={{ height: 400 }} />
          </Spin></Card>,
        },
        {
          key: 'ltv', label: 'LTV/CAC by Channel',
          children: <Card><Spin spinning={ltvLoading}>
            <ReactEChartsCore echarts={echarts} option={ltvBarOption} style={{ height: 400 }} />
          </Spin></Card>,
        },
      ]} />
    </div>
  )
}
