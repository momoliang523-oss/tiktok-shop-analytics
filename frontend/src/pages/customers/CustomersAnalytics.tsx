import { useState } from 'react'
import { Card, Row, Col, Select, Spin, Table, Tag, Descriptions } from 'antd'
import ReactEChartsCore from 'echarts-for-react/lib/core'
import * as echarts from 'echarts/core'
import { BarChart, PieChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { useCustomerSegments } from '../../hooks/useData'
import { formatCurrency } from '../../utils/formatters'

echarts.use([BarChart, PieChart, GridComponent, TooltipComponent, LegendComponent, CanvasRenderer])

export default function CustomersAnalytics() {
  const [segType, setSegType] = useState('behavioral')
  const { data, isLoading } = useCustomerSegments({ segmentation_type: segType })
  const segments = data?.data?.segments || []

  const pieOption = {
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie', radius: ['40%', '70%'],
      data: segments.map((s: any) => ({ name: s.segment_name, value: s.size })),
      emphasis: { itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0,0,0,0.5)' } },
    }],
  }

  const barOption = {
    tooltip: { trigger: 'axis' },
    legend: { data: ['LTV', 'CAC'] },
    xAxis: { type: 'category', data: segments.map((s: any) => s.segment_name) },
    yAxis: { type: 'value' },
    series: [
      { name: 'LTV', type: 'bar', data: segments.map((s: any) => s.characteristics?.avg_ltv), itemStyle: { color: '#27ae60' } },
      { name: 'CAC', type: 'bar', data: segments.map((s: any) => s.characteristics?.avg_cac), itemStyle: { color: '#e74c3c' } },
    ],
  }

  const columns = [
    { title: 'Segment', dataIndex: 'segment_name', key: 'name' },
    { title: 'Type', dataIndex: 'segment_type', key: 'type', render: (v: string) => <Tag>{v}</Tag> },
    { title: 'Size', dataIndex: 'size', key: 'size' },
    { title: '%', dataIndex: 'percentage', key: 'pct', render: (v: number) => `${v}%` },
    { title: 'Avg LTV', key: 'ltv', render: (_: any, r: any) => formatCurrency(r.characteristics?.avg_ltv) },
    { title: 'Avg CAC', key: 'cac', render: (_: any, r: any) => formatCurrency(r.characteristics?.avg_cac) },
    { title: 'LTV/CAC', key: 'ratio', render: (_: any, r: any) => <Tag color={r.characteristics?.ltv_cac_ratio > 5 ? 'green' : 'orange'}>{r.characteristics?.ltv_cac_ratio?.toFixed(1)}x</Tag> },
    { title: 'Churn Risk', key: 'churn', render: (_: any, r: any) => <Tag color={r.marketing_insights?.churn_risk === 'low' ? 'green' : 'red'}>{r.marketing_insights?.churn_risk}</Tag> },
  ]

  return (
    <div>
      <Card style={{ marginBottom: 16 }}>
        <Select value={segType} onChange={setSegType} style={{ width: 200 }}
          options={[
            { value: 'behavioral', label: 'Behavioral' }, { value: 'demographic', label: 'Demographic' },
            { value: 'psychographic', label: 'Psychographic' }, { value: 'value_based', label: 'Value Based' },
          ]} />
      </Card>

      <Row gutter={[16, 16]}>
        <Col xs={24} lg={12}>
          <Card title="Segment Distribution"><Spin spinning={isLoading}>
            <ReactEChartsCore echarts={echarts} option={pieOption} style={{ height: 350 }} />
          </Spin></Card>
        </Col>
        <Col xs={24} lg={12}>
          <Card title="LTV vs CAC by Segment"><Spin spinning={isLoading}>
            <ReactEChartsCore echarts={echarts} option={barOption} style={{ height: 350 }} />
          </Spin></Card>
        </Col>
      </Row>

      <Card title="Segment Details" style={{ marginTop: 16 }}>
        <Table columns={columns} dataSource={segments} rowKey="segment_id" size="small" expandable={{
          expandedRowRender: (record: any) => (
            <Descriptions column={2} size="small" bordered>
              <Descriptions.Item label="Best Channel">{record.marketing_insights?.best_channel}</Descriptions.Item>
              <Descriptions.Item label="Best Time">{record.marketing_insights?.optimal_send_time}</Descriptions.Item>
              <Descriptions.Item label="Message">{record.marketing_insights?.best_messaging}</Descriptions.Item>
              <Descriptions.Item label="Content">{record.marketing_insights?.preferred_content}</Descriptions.Item>
              <Descriptions.Item label="Location">{record.demographics?.location}</Descriptions.Item>
              <Descriptions.Item label="Payment">{record.marketing_insights?.payment_preference}</Descriptions.Item>
            </Descriptions>
          ),
        }} />
      </Card>
    </div>
  )
}
