import { useState } from 'react'
import { BrowserRouter, Routes, Route, useNavigate, useLocation } from 'react-router-dom'
import { Layout, Menu, Typography } from 'antd'
import {
  DashboardOutlined, LineChartOutlined, AppstoreOutlined, UserOutlined,
  SoundOutlined, PlayCircleOutlined, GlobalOutlined, FileTextOutlined,
} from '@ant-design/icons'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

import Dashboard from './pages/dashboard/Dashboard'
import SalesAnalytics from './pages/sales/SalesAnalytics'
import ProductsAnalytics from './pages/products/ProductsAnalytics'
import CustomersAnalytics from './pages/customers/CustomersAnalytics'
import MarketingAnalytics from './pages/marketing/MarketingAnalytics'
import LiveAnalytics from './pages/live/LiveAnalytics'
import TrafficAnalytics from './pages/traffic/TrafficAnalytics'
import Reports from './pages/reports/Reports'

const { Sider } = Layout
const { Title } = Typography

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { refetchOnWindowFocus: false, retry: 1 },
  },
})

const menuItems = [
  { key: '/dashboard', icon: <DashboardOutlined />, label: 'Dashboard' },
  { key: '/sales', icon: <LineChartOutlined />, label: 'Sales Analytics' },
  { key: '/products', icon: <AppstoreOutlined />, label: 'Product (SKU) Analytics' },
  { key: '/customers', icon: <UserOutlined />, label: 'Customer Analytics' },
  { key: '/marketing', icon: <SoundOutlined />, label: 'Marketing Analytics' },
  { key: '/live', icon: <PlayCircleOutlined />, label: 'Live Analytics' },
  { key: '/traffic', icon: <GlobalOutlined />, label: 'Traffic & LTV/CAC' },
  { key: '/reports', icon: <FileTextOutlined />, label: 'Reports' },
]

function AppLayout() {
  const navigate = useNavigate()
  const location = useLocation()
  const [collapsed, setCollapsed] = useState(false)

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider collapsible collapsed={collapsed} onCollapse={setCollapsed} theme="dark">
        <div style={{ padding: '16px', textAlign: 'center' }}>
          <Title level={5} style={{ color: '#fff', margin: 0 }}>
            {collapsed ? 'TSA' : 'TikTok Analytics'}
          </Title>
        </div>
        <Menu theme="dark" mode="inline" selectedKeys={[location.pathname]}
          items={menuItems} onClick={({ key }) => navigate(key)} />
      </Sider>
      <Layout>
        <Layout.Content style={{ padding: 24, background: '#f0f2f5', minHeight: '100vh' }}>
          <Routes>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/sales" element={<SalesAnalytics />} />
            <Route path="/products" element={<ProductsAnalytics />} />
            <Route path="/customers" element={<CustomersAnalytics />} />
            <Route path="/marketing" element={<MarketingAnalytics />} />
            <Route path="/live" element={<LiveAnalytics />} />
            <Route path="/traffic" element={<TrafficAnalytics />} />
            <Route path="/reports" element={<Reports />} />
            <Route path="/" element={<Dashboard />} />
            <Route path="*" element={<Dashboard />} />
          </Routes>
        </Layout.Content>
      </Layout>
    </Layout>
  )
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AppLayout />
      </BrowserRouter>
    </QueryClientProvider>
  )
}
