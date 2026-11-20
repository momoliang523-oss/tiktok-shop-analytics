import { Card, Row, Col, Spin, Table, Descriptions, Tag } from 'antd'
import ReactEChartsCore from 'echarts-for-react/lib/core'
import * as echarts from 'echarts/core'
import { BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { useCampaigns, useRoi } from '../../hooks/useData'
import { useFilterStore } from '../../store'
import { formatCurrency } from '../../utils/formatters'

echarts.use([BarChart, GridComponent, TooltipComponent, LegendComponent, CanvasRenderer])

export default function MarketingAnalytics() {
  const { dateRange } = useFilterStore()
  const params = { start_date: dateRange.start_date, end_date: dateRange.end_date }

  const { data: campaignData, isLoading } = useCampaigns(params)
  const { data: roiData } = useRoi(params)

  const campaigns = campaignData?.data?.campaigns || []
  const roiStats = roiData?.data

  const roiByChannelOption = {
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: roiStats?.by_channel?.map((c: any) => c.channel) || [] },
    yAxis: { type: 'value', name: 'ROI (x)' },
    series: [{
      name: 'ROI', type: 'bar',
      data: roiStats?.by_channel?.map((c: any) => c.roi) || [],
      itemStyle: { color: '#1a1a2e' },
    }],
  }

  const columns = [
    { title: 'Campaign', dataIndex: 'name', key: 'name' },
    { title: 'Type', dataIndex: 'type', key: 'type', render: (v: string) => <Tag>{v}</Tag> },
    { title: 'Status', dataIndex: 'status', key: 'status', render: (v: string) =>
      <Tag color={v === 'active' ? 'green' : 'blue'}>{v}</Tag> },
    { title: 'Budget', dataIndex: 'budget', key: 'budget', render: (v: number) => formatCurrency(v) },
    { title: 'Cost', dataIndex: 'cost', key: 'cost', render: (v: number) => formatCurrency(v) },
    { title: 'Revenue', dataIndex: 'revenue', key: 'revenue', render: (v: number) => formatCurrency(v) },
    { title: 'ROI', dataIndex: 'roi', key: 'roi', render: (v: number) => <Tag color={v > 3 ? 'green' : 'orange'}>{v.toFixed(1)}x</Tag> },
    { title: 'Orders', dataIndex: 'orders', key: 'orders' },
  ]

  return (
    <div>
      <Row gutter={[16, 16]} style={{ marginBottom: 16 }}>
        <Col xs={12} sm={6}><Card><Descriptions title="Total Revenue" column={1}>{formatCurrency(roiStats?.overall_roi?.total_revenue || 0)}</Descriptions></Card></Col>
        <Col xs={12} sm={6}><Card><Descriptions title="Total Cost" column={1}>{formatCurrency(roiStats?.overall_roi?.total_cost || 0)}</Descriptions></Card></Col>
        <Col xs={12} sm={6}><Card><Descriptions title="Overall ROI" column={1}><Tag color="green">{roiStats?.overall_roi?.roi?.toFixed(1)}x</Tag></Descriptions></Card></Col>
        <Col xs={12} sm={6}><Card><Descriptions title="Profit Margin" column={1}>{(roiStats?.overall_roi?.profit_margin * 100 || 0).toFixed(1)}%</Descriptions></Card></Col>
      </Row>

      <Row gutter={[16, 16]}>
        <Col xs={24} lg={12}>
          <Card title="ROI by Channel"><Spin spinning={isLoading}>
            <ReactEChartsCore echarts={echarts} option={roiByChannelOption} style={{ height: 350 }} />
          </Spin></Card>
        </Col>
        <Col xs={24} lg={12}>
          <Card title="ROI by Campaign Type">
            <Table columns={[
              { title: 'Type', dataIndex: 'type', key: 'type' },
              { title: 'Revenue', dataIndex: 'revenue', key: 'revenue', render: (v: number) => formatCurrency(v) },
              { title: 'Cost', dataIndex: 'cost', key: 'cost', render: (v: number) => formatCurrency(v) },
              { title: 'ROI', dataIndex: 'roi', key: 'roi', render: (v: number) => <Tag color={v > 3 ? 'green' : 'orange'}>{v.toFixed(1)}x</Tag> },
            ]} dataSource={roiStats?.by_campaign_type || []} rowKey="type" size="small" pagination={false} />
          </Card>
        </Col>
      </Row>

      <Card title="Campaign Performance" style={{ marginTop: 16 }}>
        <Table columns={columns} dataSource={campaigns} rowKey="campaign_id" size="small" />
      </Card>
    </div>
  )
}
