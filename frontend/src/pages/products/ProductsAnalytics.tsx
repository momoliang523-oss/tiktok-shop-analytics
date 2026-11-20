import { useState } from 'react'
import { Card, Row, Col, Select, Spin, Table, Tag, Descriptions } from 'antd'
import ReactEChartsCore from 'echarts-for-react/lib/core'
import * as echarts from 'echarts/core'
import { BarChart, PieChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { usePatternAnalysis, useSkuInventory } from '../../hooks/useData'
import { useFilterStore } from '../../store'
import { formatCurrency } from '../../utils/formatters'

echarts.use([BarChart, PieChart, GridComponent, TooltipComponent, LegendComponent, CanvasRenderer])

export default function ProductsAnalytics() {
  const { dateRange } = useFilterStore()
  const [region, setRegion] = useState<string | undefined>()
  const [generation, setGeneration] = useState<string | undefined>()

  const { data: patternData, isLoading } = usePatternAnalysis({
    start_date: dateRange.start_date,
    end_date: dateRange.end_date,
    region,
    generation,
  })

  const { data: inventoryData } = useSkuInventory({})

  const patterns = patternData?.data
  const inventory = inventoryData?.data

  const popularityOption = {
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: patterns?.patterns?.map((p: any) => p.pattern_name) || [] },
    yAxis: { type: 'value', name: 'Popularity Score' },
    series: [{
      name: 'Popularity', type: 'bar',
      data: patterns?.patterns?.map((p: any) => p.popularity_score) || [],
      itemStyle: { color: '#1a1a2e' },
    }],
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
  }

  const regionalOption = {
    tooltip: { trigger: 'axis' },
    legend: { data: ['West Coast', 'East Coast', 'Midwest', 'South'] },
    xAxis: { type: 'category', data: patterns?.patterns?.map((p: any) => p.pattern_name) || [] },
    yAxis: { type: 'value', name: 'Regional Score' },
    series: [
      { name: 'West Coast', type: 'bar', data: patterns?.patterns?.map((p: any) => p.regional_popularity?.west || 0) },
      { name: 'East Coast', type: 'bar', data: patterns?.patterns?.map((p: any) => p.regional_popularity?.east || 0) },
      { name: 'Midwest', type: 'bar', data: patterns?.patterns?.map((p: any) => p.regional_popularity?.midwest || 0) },
      { name: 'South', type: 'bar', data: patterns?.patterns?.map((p: any) => p.regional_popularity?.south || 0) },
    ],
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
  }

  const columns = [
    { title: 'Pattern', dataIndex: 'pattern_name', key: 'pattern' },
    { title: 'Category', dataIndex: 'category', key: 'category', render: (v: string) => <Tag>{v}</Tag> },
    { title: 'Sales', dataIndex: 'total_sales', key: 'sales', render: (v: number) => v.toLocaleString() },
    { title: 'Revenue', dataIndex: 'total_revenue', key: 'revenue', render: (v: number) => formatCurrency(v) },
    { title: 'Score', dataIndex: 'popularity_score', key: 'score' },
    { title: 'Life Cycle', dataIndex: 'life_cycle', key: 'cycle',
      render: (v: string) => <Tag color={v === 'growth' ? 'green' : v === 'mature' ? 'blue' : v === 'decline' ? 'red' : 'orange'}>{v}</Tag> },
    { title: 'Seasonal', dataIndex: 'seasonal', key: 'seasonal', render: (v: boolean) => v ? <Tag color="orange">Yes</Tag> : <Tag>No</Tag> },
  ]

  return (
    <div>
      <Card style={{ marginBottom: 16 }}>
        <Row gutter={16}>
          <Col>
            <Select placeholder="US Region" allowClear style={{ width: 160 }} value={region} onChange={setRegion}
              options={[
                { value: 'west', label: 'West Coast' }, { value: 'east', label: 'East Coast' },
                { value: 'midwest', label: 'Midwest' }, { value: 'south', label: 'South' },
              ]} />
          </Col>
          <Col>
            <Select placeholder="Generation" allowClear style={{ width: 160 }} value={generation} onChange={setGeneration}
              options={[
                { value: 'gen_z', label: 'Gen Z (1997-2012)' }, { value: 'millennial', label: 'Millennials' },
                { value: 'gen_x', label: 'Gen X' }, { value: 'boomer', label: 'Boomers' },
              ]} />
          </Col>
        </Row>
      </Card>

      <Row gutter={[16, 16]}>
        <Col xs={24} lg={12}>
          <Card title="Pattern Popularity"><Spin spinning={isLoading}>
            <ReactEChartsCore echarts={echarts} option={popularityOption} style={{ height: 350 }} />
          </Spin></Card>
        </Col>
        <Col xs={24} lg={12}>
          <Card title="Regional Preference Comparison"><Spin spinning={isLoading}>
            <ReactEChartsCore echarts={echarts} option={regionalOption} style={{ height: 350 }} />
          </Spin></Card>
        </Col>
      </Row>

      <Card title="Pattern Analysis Table" style={{ marginTop: 16 }}>
        <Table columns={columns} dataSource={patterns?.patterns || []} rowKey="pattern_name" size="small" />
      </Card>

      {patterns?.insights?.recommendations && (
        <Card title="US Market Recommendations" style={{ marginTop: 16 }}>
          <Descriptions column={2}>
            <Descriptions.Item label="Design Trends">
              {patterns?.insights?.recommendations?.design_trends?.join(', ')}
            </Descriptions.Item>
            <Descriptions.Item label="Marketing Strategies">
              {patterns?.insights?.recommendations?.marketing_strategies?.join(', ')}
            </Descriptions.Item>
          </Descriptions>
        </Card>
      )}
    </div>
  )
}
