import { useState, useEffect } from 'react'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'
import KpiCard from '../components/KpiCard'
import {
  fetchCustomerSummary,
  fetchTopCustomers,
  fetchCustomersByCountry,
  fetchNewVsReturning,
} from '../api/customersApi'
import type { CustomerSummary, TopCustomer, CountryStat, NewVsReturningPoint } from '../types/customers'

const usd = (v: number) =>
  new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(v)

export default function CustomerAnalyticsPage() {
  const [summary, setSummary] = useState<CustomerSummary | null>(null)
  const [topCustomers, setTopCustomers] = useState<TopCustomer[]>([])
  const [byCountry, setByCountry] = useState<CountryStat[]>([])
  const [newVsReturning, setNewVsReturning] = useState<NewVsReturningPoint[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    Promise.all([
      fetchCustomerSummary(),
      fetchTopCustomers(),
      fetchCustomersByCountry(),
      fetchNewVsReturning(),
    ])
      .then(([s, t, c, n]) => {
        setSummary(s)
        setTopCustomers(t)
        setByCountry(c)
        setNewVsReturning(n)
      })
      .catch(() => setError('Failed to load customer data.'))
      .finally(() => setLoading(false))
  }, [])

  if (loading)
    return (
      <div className="flex items-center justify-center h-64 text-gray-400 text-sm">Loading…</div>
    )
  if (error) return <p className="text-red-600 text-sm">{error}</p>

  return (
    <div className="space-y-6">
      <h1 className="text-lg font-semibold text-gray-800">Customer Analytics</h1>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <KpiCard
          title="Total Customers"
          value={(summary?.total_customers ?? 0).toLocaleString()}
        />
        <KpiCard
          title="New This Month"
          value={(summary?.new_this_month ?? 0).toLocaleString()}
        />
        <KpiCard
          title="Returning Customers"
          value={(summary?.returning_customers ?? 0).toLocaleString()}
        />
      </div>

      {/* New vs Returning Chart */}
      <div className="bg-white rounded-xl border border-gray-200 p-5">
        <h2 className="text-sm font-semibold text-gray-700 mb-4">New vs Returning (Last 6 Months)</h2>
        <ResponsiveContainer width="100%" height={240}>
          <BarChart data={newVsReturning} margin={{ top: 4, right: 16, bottom: 0, left: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey="month" tick={{ fontSize: 11 }} tickLine={false} />
            <YAxis tick={{ fontSize: 11 }} tickLine={false} />
            <Tooltip />
            <Legend iconType="circle" iconSize={8} wrapperStyle={{ fontSize: 12 }} />
            <Bar dataKey="new_customers" name="New" fill="#3b82f6" radius={[4, 4, 0, 0]} />
            <Bar dataKey="returning_customers" name="Returning" fill="#8b5cf6" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Top Customers + Country Breakdown */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
        {/* Top Customers */}
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <h2 className="text-sm font-semibold text-gray-700 mb-4">Top 10 Customers by Spend</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-100">
                  <th className="text-left py-2 px-3 text-xs font-medium text-gray-500">Name</th>
                  <th className="text-left py-2 px-3 text-xs font-medium text-gray-500">Email</th>
                  <th className="text-right py-2 px-3 text-xs font-medium text-gray-500">Orders</th>
                  <th className="text-right py-2 px-3 text-xs font-medium text-gray-500">Spend</th>
                </tr>
              </thead>
              <tbody>
                {topCustomers.map((c) => (
                  <tr key={c.customer_id} className="border-b border-gray-50 hover:bg-gray-50">
                    <td className="py-2 px-3 text-gray-800">{c.name}</td>
                    <td className="py-2 px-3 text-gray-500 text-xs">{c.email}</td>
                    <td className="py-2 px-3 text-right text-gray-700">{c.order_count}</td>
                    <td className="py-2 px-3 text-right font-medium text-blue-700">
                      {usd(c.total_spend)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* By Country */}
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <h2 className="text-sm font-semibold text-gray-700 mb-4">Revenue by Country</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-100">
                  <th className="text-left py-2 px-3 text-xs font-medium text-gray-500">Country</th>
                  <th className="text-right py-2 px-3 text-xs font-medium text-gray-500">Customers</th>
                  <th className="text-right py-2 px-3 text-xs font-medium text-gray-500">Revenue</th>
                </tr>
              </thead>
              <tbody>
                {byCountry.map((c) => (
                  <tr key={c.country} className="border-b border-gray-50 hover:bg-gray-50">
                    <td className="py-2 px-3 text-gray-800">{c.country}</td>
                    <td className="py-2 px-3 text-right text-gray-700">{c.customer_count}</td>
                    <td className="py-2 px-3 text-right font-medium text-blue-700">
                      {usd(c.revenue)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  )
}
