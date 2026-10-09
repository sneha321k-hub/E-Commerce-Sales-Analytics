import { useState, useEffect } from 'react'
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'
import KpiCard from '../components/KpiCard'
import {
  fetchSalesKPIs,
  fetchSalesTrend,
  fetchSalesByChannel,
  fetchOrderStatus,
} from '../api/salesApi'
import type { SalesKPIs, TrendPoint, ChannelStat, OrderStatusStat } from '../types/sales'

const usd = (v: number) =>
  new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(v)

const STATUS_COLORS: Record<string, string> = {
  delivered: '#22c55e',
  shipped: '#3b82f6',
  placed: '#a855f7',
  returned: '#f97316',
  cancelled: '#ef4444',
}

const CHANNEL_COLORS = ['#3b82f6', '#8b5cf6', '#06b6d4']

const DAY_OPTIONS = [7, 30, 90]

export default function SalesOverviewPage() {
  const [kpis, setKpis] = useState<SalesKPIs | null>(null)
  const [trend, setTrend] = useState<TrendPoint[]>([])
  const [channels, setChannels] = useState<ChannelStat[]>([])
  const [statuses, setStatuses] = useState<OrderStatusStat[]>([])
  const [days, setDays] = useState(30)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    setLoading(true)
    setError('')
    Promise.all([fetchSalesKPIs(), fetchSalesByChannel(), fetchOrderStatus()])
      .then(([k, c, s]) => {
        setKpis(k)
        setChannels(c)
        setStatuses(s)
      })
      .catch(() => setError('Failed to load sales data.'))
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    fetchSalesTrend(days).then(setTrend).catch(() => {})
  }, [days])

  if (loading)
    return (
      <div className="flex items-center justify-center h-64 text-gray-400 text-sm">
        Loading…
      </div>
    )
  if (error)
    return <p className="text-red-600 text-sm">{error}</p>

  return (
    <div className="space-y-6">
      <h1 className="text-lg font-semibold text-gray-800">Sales Overview</h1>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 xl:grid-cols-4 gap-4">
        <KpiCard title="Total Revenue" value={usd(kpis?.total_revenue ?? 0)} />
        <KpiCard title="Total Orders" value={(kpis?.total_orders ?? 0).toLocaleString()} />
        <KpiCard title="Avg. Order Value" value={usd(kpis?.average_order_value ?? 0)} />
        <KpiCard title="Total Customers" value={(kpis?.total_customers ?? 0).toLocaleString()} />
      </div>

      {/* Revenue Trend */}
      <div className="bg-white rounded-xl border border-gray-200 p-5">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-sm font-semibold text-gray-700">Revenue Trend</h2>
          <div className="flex gap-2">
            {DAY_OPTIONS.map((d) => (
              <button
                key={d}
                onClick={() => setDays(d)}
                className={`text-xs px-3 py-1 rounded-full border transition-colors ${
                  days === d
                    ? 'bg-blue-600 text-white border-blue-600'
                    : 'border-gray-300 text-gray-600 hover:border-blue-400'
                }`}
              >
                {d}d
              </button>
            ))}
          </div>
        </div>
        <ResponsiveContainer width="100%" height={240}>
          <LineChart data={trend} margin={{ top: 4, right: 16, bottom: 0, left: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey="date" tick={{ fontSize: 11 }} tickLine={false} />
            <YAxis tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`} tick={{ fontSize: 11 }} tickLine={false} />
            <Tooltip formatter={(v: unknown) => usd(v as number)} />
            <Line type="monotone" dataKey="revenue" stroke="#3b82f6" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Channel + Status */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
        {/* Revenue by Channel */}
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <h2 className="text-sm font-semibold text-gray-700 mb-4">Revenue by Channel</h2>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={channels} margin={{ top: 4, right: 16, bottom: 0, left: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="channel" tick={{ fontSize: 11 }} tickLine={false} />
              <YAxis tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`} tick={{ fontSize: 11 }} tickLine={false} />
              <Tooltip formatter={(v: unknown) => usd(v as number)} />
              <Bar dataKey="revenue" radius={[4, 4, 0, 0]}>
                {channels.map((_, i) => (
                  <Cell key={i} fill={CHANNEL_COLORS[i % CHANNEL_COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Order Status */}
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <h2 className="text-sm font-semibold text-gray-700 mb-4">Order Status</h2>
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Pie
                data={statuses}
                dataKey="count"
                nameKey="status"
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={90}
                paddingAngle={2}
              >
                {statuses.map((s, i) => (
                  <Cell key={i} fill={STATUS_COLORS[s.status] ?? '#94a3b8'} />
                ))}
              </Pie>
              <Tooltip />
              <Legend iconType="circle" iconSize={8} wrapperStyle={{ fontSize: 12 }} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}
