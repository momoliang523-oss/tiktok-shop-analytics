import { useState } from 'react'
import { Card, Button, Select, DatePicker, Table, Tag, message, Space } from 'antd'
import { DownloadOutlined, ReloadOutlined } from '@ant-design/icons'
import { api } from '../../services/api'
import dayjs from 'dayjs'

const { RangePicker } = DatePicker

export default function Reports() {
  const [reportType, setReportType] = useState('comprehensive')
  const [dateRange, setDateRange] = useState<[dayjs.Dayjs, dayjs.Dayjs]>([
    dayjs().subtract(30, 'day'), dayjs()
  ])
  const [tasks, setTasks] = useState<any[]>([])
  const [loading, setLoading] = useState(false)

  const handleGenerate = async () => {
    setLoading(true)
    try {
      const { data } = await api.generateReport({
        report_type: reportType,
        start_date: dateRange[0].format('YYYY-MM-DD'),
        end_date: dateRange[1].format('YYYY-MM-DD'),
        include_charts: true,
        include_tables: true,
      })
      message.success(`Report task created: ${data.task_id}`)
      setTasks(prev => [data, ...prev])
    } catch (err) {
      message.error('Failed to generate report')
    }
    setLoading(false)
  }

  const handleCheckStatus = async (taskId: string) => {
    try {
      const { data } = await api.getReportStatus(taskId)
      setTasks(prev => prev.map(t => t.task_id === taskId ? data : t))
      if (data.status === 'completed') {
        message.success('Report ready for download')
      }
    } catch {
      message.error('Failed to check status')
    }
  }

  const handleDownload = (taskId: string) => {
    window.open(`/api/v1/reports/download/${taskId}`, '_blank')
  }

  const columns = [
    { title: 'Task ID', dataIndex: 'task_id', key: 'task_id' },
    { title: 'Type', dataIndex: 'report_type', key: 'type', render: (v: string) => <Tag>{v}</Tag> },
    { title: 'Status', dataIndex: 'status', key: 'status',
      render: (v: string) => <Tag color={v === 'completed' ? 'green' : v === 'processing' ? 'blue' : 'orange'}>{v}</Tag> },
    { title: 'Period', key: 'period', render: (_: any, r: any) => `${r.start_date} ~ ${r.end_date}` },
    { title: 'Actions', key: 'actions', render: (_: any, r: any) => (
      <Space>
        {r.status !== 'completed' ? (
          <Button size="small" icon={<ReloadOutlined />} onClick={() => handleCheckStatus(r.task_id)}>Check</Button>
        ) : (
          <Button size="small" type="primary" icon={<DownloadOutlined />} onClick={() => handleDownload(r.task_id)}>Download</Button>
        )}
      </Space>
    )},
  ]

  return (
    <div>
      <Card title="Generate Report" style={{ marginBottom: 16 }}>
        <Space direction="vertical" size="middle" style={{ width: '100%' }}>
          <Space wrap>
            <Select value={reportType} onChange={setReportType} style={{ width: 200 }}
              options={[
                { value: 'comprehensive', label: 'Comprehensive Report' },
                { value: 'sales', label: 'Sales Report' },
                { value: 'products', label: 'Product Report' },
                { value: 'customers', label: 'Customer Report' },
                { value: 'marketing', label: 'Marketing Report' },
              ]} />
            <RangePicker value={dateRange} onChange={(dates) => dates && setDateRange(dates)} />
            <Button type="primary" loading={loading} onClick={handleGenerate}>
              Generate Report
            </Button>
          </Space>
        </Space>
      </Card>

      <Card title="Report Tasks">
        <Table columns={columns} dataSource={tasks} rowKey="task_id" size="small" pagination={false}
          locale={{ emptyText: 'No report tasks yet. Generate one above!' }} />
      </Card>
    </div>
  )
}
