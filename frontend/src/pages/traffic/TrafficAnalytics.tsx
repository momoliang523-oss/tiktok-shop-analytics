import { Card, Row, Col, Spin, Table, Descriptions, Tag, Progress } from 'antd'
import ReactEChartsCore from 'echarts-for-react/lib/core'
import * as echarts from 'echarts/core'
import { BarChart, LineChart, PieChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { useLtvCac, useChannelValue, useTrafficFunnel } from '../../hooks/useData'
import { useFilterStore } from '../../store'
import { formatCurrency } from '../../utils/formatters'

echarts.use([BarChart, LineChart, PieChart, GridComponent, TooltipComponent, LegendComponent, CanvasRenderer])

export default function TrafficAnalytics() {
  const { dateRange } = useFilterStore()
  const params = { start_date: dateRange.start_date, end_date: dateRange.end_date }

  const { data: ltvData, isLoading: ltvLoading } = useLtvCac(params)
  const { data: valueData } = useChannelValue(params)
  const { data: funnelData } = useTrafficFunnel(params)

  const ltvStats = ltvData?.data
  const valueStats = valueData?.data
  const funnelStats = funnelData?.data

  const ltvBarOption = {
    tooltip: { trigger: 'axis' },
    legend: { data: ['LTV', 'CAC'] },
    xAxis: { type: 'category', data: ltvStats?.by_channel?.map((c: any) => c.channel) || [] },
    yAxis: { type: 'value', name: 'Amount ($)' },
    series: [
      { name: 'LTV', type: 'bar', data: ltvStats?.by_channel?.map((c: any) => c.ltv) || [], itemStyle: { color: '#27ae60' } },
      { name: 'CAC', type: 'bar', data: ltvStats?.by_channel?.map((c: any) => c.cac) || [], itemStyle: { color: '#e74c3c' } },
    ],
  }

  const ratioOption = {
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: ltvStats?.by_channel?.map((c: any) => c.channel) || [] },
    yAxis: { type: 'value', name: 'LTV/CAC Ratio' },
    series: [{
      name: 'LTV/CAC', type: 'line',
      data: ltvStats?.by_channel?.map((c: any) => c.ltv_cac_ratio) || [],
      markLine: { data: [{ yAxis: 3, label: { formatter: 'Min Healthy (3x)' }, lineStyle: { color: '#f39c12' } }] },
      lineStyle: { color: '#1a1a2e', width: 2 },
    }],
  }

  const funnelOption = {
    tooltip: { trigger: 'item' },
    series: [{
      type: 'funnel', left: '10%', width: '80%',
      data: funnelStats?.funnel?.map((f: any) => ({ name: f.stage, value: f.value })) || [],
      label: { show: true, position: 'inside' },
    }],
  }

  const columns = [
    { title: 'Channel', dataIndex: 'channel', key: 'channel' },
    { title: 'LTV', dataIndex: 'ltv', key: 'ltv', render: (v: number) => formatCurrency(v) },
    { title: 'CAC', dataIndex: 'cac', key: 'cac', render: (v: number) => formatCurrency(v) },
    { title: 'LTV/CAC', dataIndex: 'ltv_cac_ratio', key: 'ratio', render: (v: number) => {
      const color = v > 5 ? 'green' : v > 3 ? 'orange' : 'red'
      return <Tag color={color}>{v.toFixed(1)}x</Tag>
    }},
    { title: 'Payback (days)', dataIndex: 'payback_period', key: 'payback' },
    { title: 'Customers', dataIndex: 'customer_count', key: 'count' },
  ]

  return (
    <div>
      <Row gutter={[16, 16]} style={{ marginBottom: 16 }}>
        <Col xs={24} sm={8}>
          <Card><Descriptions title="LTV/CAC Overview" column={1} size="small">
            <Descriptions.Item label="Total LTV">{formatCurrency(ltvStats?.overview?.total_ltv || 0)}</Descriptions.Item>
            <Descriptions.Item label="Total CAC">{formatCurrency(ltvStats?.overview?.total_cac || 0)}</Descriptions.Item>
            <Descriptions.Item label="Overall Ratio">
              <Tag color={ltvStats?.overview?.ltv_cac_ratio > 5 ? 'green' : 'orange'}>
                {ltvStats?.overview?.ltv_cac_ratio?.toFixed(1)}x
              </Tag>
            </Descriptions.Item>
            <Descriptions.Item label="Payback Period">{ltvStats?.overview?.payback_period_days} days</Descriptions.Item>
          </Descriptions></Card>
        </Col>
        <Col xs={24} sm={8}>
          <Card title="LTV vs CAC by Channel"><Spin spinning={ltvLoading}>
            <ReactEChartsCore echarts={echarts} option={ltvBarOption} style={{ height: 250 }} />
          </Spin></Card>
        </Col>
        <Col xs={24} sm={8}>
          <Card title="LTV/CAC Ratio Trend"><Spin spinning={ltvLoading}>
            <ReactEChartsCore echarts={echarts} option={ratioOption} style={{ height: 250 }} />
          </Spin></Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]}>
        <Col xs={24} lg={12}>
          <Card title="Conversion Funnel">
            <ReactEChartsCore echarts={echarts} option={funnelOption} style={{ height: 400 }} />
          </Card>
        </Col>
        <Col xs={24} lg={12}>
          <Card title="Channel Performance Detail">
            <Table columns={columns} dataSource={ltvStats?.by_channel || []} rowKey="channel"
              size="small" pagination={false} />
          </Card>
        </Col>
      </Row>

      {ltvStats?.recommendations && (
        <Card title="Budget Optimization" style={{ marginTop: 16 }}>
          <Row gutter={16}>
            <Col span={12}>
              <Descriptions title="Increase Budget" column={1}>
                {ltvStats.recommendations.budget_optimization?.increase_budget_for?.map((c: string) => (
                  <Descriptions.Item key={c}><Tag color="green">{c}</Tag></Descriptions.Item>
                ))}
              </Descriptions>
            </Col>
            <Col span={12}>
              <Descriptions title="Reduce Budget" column={1}>
                {ltvStats.recommendations.budget_optimization?.reduce_budget_for?.map((c: string) => (
                  <Descriptions.Item key={c}><Tag color="red">{c}</Tag></Descriptions.Item>
                ))}
              </Descriptions>
            </Col>
          </Row>
        </Card>
      )}
    </div>
  )
}
