import { Card, Row, Col, Spin, Table, Descriptions, Tag } from 'antd'
import ReactEChartsCore from 'echarts-for-react/lib/core'
import * as echarts from 'echarts/core'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { useLiveOverview, useLiveProducts } from '../../hooks/useData'
import { useFilterStore } from '../../store'
import { formatCurrency, formatNumber } from '../../utils/formatters'

echarts.use([LineChart, GridComponent, TooltipComponent, LegendComponent, CanvasRenderer])

export default function LiveAnalytics() {
  const { dateRange } = useFilterStore()
  const params = { start_date: dateRange.start_date, end_date: dateRange.end_date }

  const { data: overview, isLoading } = useLiveOverview(params)
  const { data: products } = useLiveProducts(params)

  const stats = overview?.data
  const liveProducts = products?.data?.products || []

  const trendOption = {
    tooltip: { trigger: 'axis' },
    legend: { data: ['Views', 'Orders'] },
    xAxis: { type: 'category', data: stats?.trend?.dates?.map((d: string) => d.slice(5)) || [] },
    yAxis: [
      { type: 'value', name: 'Views' },
      { type: 'value', name: 'Orders' },
    ],
    series: [
      { name: 'Views', type: 'line', smooth: true, data: stats?.trend?.views || [], areaStyle: { opacity: 0.15 } },
      { name: 'Orders', type: 'line', smooth: true, yAxisIndex: 1, data: stats?.trend?.orders || [], lineStyle: { color: '#e74c3c' } },
    ],
  }

  const productColumns = [
    { title: 'Product', dataIndex: 'name', key: 'name' },
    { title: 'Orders', dataIndex: 'orders', key: 'orders' },
    { title: 'Revenue', dataIndex: 'revenue', key: 'revenue', render: (v: number) => formatCurrency(v) },
    { title: 'Conversion', dataIndex: 'conversion_rate', key: 'conv', render: (v: number) => `${(v * 100).toFixed(2)}%` },
  ]

  return (
    <div>
      <Row gutter={[16, 16]} style={{ marginBottom: 16 }}>
        <Col xs={12} sm={6}><Card><Descriptions title="Sessions" column={1}>{stats?.summary?.total_live_sessions}</Descriptions></Card></Col>
        <Col xs={12} sm={6}><Card><Descriptions title="Total Views" column={1}>{formatNumber(stats?.summary?.total_views || 0)}</Descriptions></Card></Col>
        <Col xs={12} sm={6}><Card><Descriptions title="Orders" column={1}>{formatNumber(stats?.summary?.total_orders || 0)}</Descriptions></Card></Col>
        <Col xs={12} sm={6}><Card><Descriptions title="Revenue" column={1}>{formatCurrency(stats?.summary?.total_revenue || 0)}</Descriptions></Card></Col>
      </Row>

      <Row gutter={[16, 16]}>
        <Col xs={24} lg={14}>
          <Card title="Live Stream Trend"><Spin spinning={isLoading}>
            <ReactEChartsCore echarts={echarts} option={trendOption} style={{ height: 350 }} />
          </Spin></Card>
        </Col>
        <Col xs={24} lg={10}>
          <Card title="Top Live Products">
            <Table columns={productColumns} dataSource={liveProducts} rowKey="product_id" size="small" pagination={false} />
          </Card>
        </Col>
      </Row>

      <Card title="Top Sessions" style={{ marginTop: 16 }}>
        <Table columns={[
          { title: 'Session', dataIndex: 'title', key: 'title' },
          { title: 'Views', dataIndex: 'views', key: 'views', render: (v: number) => formatNumber(v) },
          { title: 'Orders', dataIndex: 'orders', key: 'orders' },
          { title: 'Revenue', dataIndex: 'revenue', key: 'revenue', render: (v: number) => formatCurrency(v) },
        ]} dataSource={stats?.top_sessions || []} rowKey="live_id" size="small" />
      </Card>
    </div>
  )
}
