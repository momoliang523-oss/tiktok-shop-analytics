import { useState } from 'react'
import { Card, Row, Col, Select, DatePicker, Spin, Table, Tabs } from 'antd'
import ReactEChartsCore from 'echarts-for-react/lib/core'
import * as echarts from 'echarts/core'
import { LineChart, BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent, DataZoomComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { useSalesTrend, useSalesRanking } from '../../hooks/useData'
import { useFilterStore } from '../../store'
import { formatCurrency, formatNumber } from '../../utils/formatters'
import dayjs from 'dayjs'

echarts.use([LineChart, BarChart, GridComponent, TooltipComponent, LegendComponent, DataZoomComponent, CanvasRenderer])

const { RangePicker } = DatePicker

export default function SalesAnalytics() {
  const { dateRange, setDateRange } = useFilterStore()
  const [dimension, setDimension] = useState('product')

  const { data: trendData, isLoading } = useSalesTrend({
    start_date: dateRange.start_date,
    end_date: dateRange.end_date,
    granularity: 'day',
  })

  const { data: rankingData } = useSalesRanking({
    dimension,
    top_n: 10,
    start_date: dateRange.start_date,
    end_date: dateRange.end_date,
  })

  const trend = trendData?.data

  const trendOption = {
    tooltip: { trigger: 'axis' },
    legend: { data: ['Revenue', 'Avg Order Value'] },
    dataZoom: [{ type: 'inside' }, { type: 'slider' }],
    xAxis: { type: 'category', data: trend?.dates || [], boundaryGap: false },
    yAxis: [
      { type: 'value', name: 'Revenue ($)' },
      { type: 'value', name: 'AOV ($)' },
    ],
    series: [
      {
        name: 'Revenue', type: 'line', smooth: true,
        data: trend?.metrics?.revenue || [],
        areaStyle: { opacity: 0.15 },
        lineStyle: { color: '#1a1a2e' },
      },
      {
        name: 'Avg Order Value', type: 'line', yAxisIndex: 1,
        data: trend?.metrics?.avg_order_value || [],
        lineStyle: { color: '#27ae60' },
      },
    ],
    grid: { left: '3%', right: '4%', bottom: '15%', containLabel: true },
  }

  const rankingColumns = [
    { title: 'Rank', dataIndex: 'rank', key: 'rank', render: (_: any, __: any, i: number) => i + 1 },
    { title: 'Name', dataIndex: 'name', key: 'name' },
    { title: 'Revenue', dataIndex: 'value', key: 'value', render: (v: number) => formatCurrency(v) },
    { title: 'Orders', dataIndex: 'orders', key: 'orders', render: (v: number) => formatNumber(v) },
  ]

  const rankingOption = {
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'value', name: 'Revenue ($)' },
    yAxis: { type: 'category', data: (rankingData?.data?.ranking || []).map((r: any) => r.name).reverse() },
    series: [{
      name: 'Revenue', type: 'bar',
      data: (rankingData?.data?.ranking || []).map((r: any) => r.value).reverse(),
      itemStyle: { color: '#1a1a2e' },
    }],
    grid: { left: '30%', right: '4%', bottom: '3%', containLabel: true },
  }

  return (
    <div>
      <Card style={{ marginBottom: 16 }}>
        <Row gutter={16} align="middle">
          <Col><RangePicker value={[dayjs(dateRange.start_date), dayjs(dateRange.end_date)]}
            onChange={(dates) => {
              if (dates?.[0] && dates?.[1]) {
                setDateRange({ start_date: dates[0].format('YYYY-MM-DD'), end_date: dates[1].format('YYYY-MM-DD') })
              }
            }} /></Col>
          <Col>
            <Select value={dimension} onChange={setDimension} style={{ width: 150 }}
              options={[{ value: 'product', label: 'By Product' }, { value: 'category', label: 'By Category' }]} />
          </Col>
        </Row>
      </Card>

      <Row gutter={[16, 16]}>
        <Col xs={24} lg={14}>
          <Card title="Revenue & AOV Trend"><Spin spinning={isLoading}>
            <ReactEChartsCore echarts={echarts} option={trendOption} style={{ height: 400 }} />
          </Spin></Card>
        </Col>
        <Col xs={24} lg={10}>
          <Card title="Sales Ranking"><Spin spinning={isLoading}>
            <ReactEChartsCore echarts={echarts} option={rankingOption} style={{ height: 400 }} />
          </Spin></Card>
        </Col>
      </Row>

      <Card title="Ranking Table" style={{ marginTop: 16 }}>
        <Table columns={rankingColumns} dataSource={rankingData?.data?.ranking || []} rowKey="name"
          pagination={false} size="small" />
      </Card>
    </div>
  )
}
