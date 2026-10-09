import { useState, useEffect } from 'react'
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'
import { fetchTopProducts, fetchProductsByCategory, fetchReturnRates } from '../api/productsApi'
import type { TopProduct, CategoryStat, ProductReturnRate } from '../types/products'

const usd = (v: number) =>
  new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(v)

const CATEGORY_COLORS: Record<string, string> = {
  Electronics: '#3b82f6',
  Clothing: '#8b5cf6',
  Books: '#06b6d4',
  Home: '#f59e0b',
  Sports: '#22c55e',
}

export default function ProductAnalyticsPage() {
  const [topProducts, setTopProducts] = useState<TopProduct[]>([])
  const [categories, setCategories] = useState<CategoryStat[]>([])
  const [returnRates, setReturnRates] = useState<ProductReturnRate[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    Promise.all([fetchTopProducts(), fetchProductsByCategory(), fetchReturnRates()])
      .then(([t, c, r]) => {
        setTopProducts(t)
        setCategories(c)
        setReturnRates(r)
      })
      .catch(() => setError('Failed to load product data.'))
      .finally(() => setLoading(false))
  }, [])

  if (loading)
    return (
      <div className="flex items-center justify-center h-64 text-gray-400 text-sm">Loading…</div>
    )
  if (error) return <p className="text-red-600 text-sm">{error}</p>

  return (
    <div className="space-y-6">
      <h1 className="text-lg font-semibold text-gray-800">Product Analytics</h1>

      {/* Top Products + Category */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
        {/* Top 10 products */}
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <h2 className="text-sm font-semibold text-gray-700 mb-4">Top 10 Products by Revenue</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart
              data={topProducts}
              layout="vertical"
              margin={{ top: 4, right: 16, bottom: 0, left: 120 }}
            >
              <XAxis
                type="number"
                tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`}
                tick={{ fontSize: 11 }}
                tickLine={false}
              />
              <YAxis
                type="category"
                dataKey="name"
                tick={{ fontSize: 10 }}
                tickLine={false}
                width={120}
              />
              <Tooltip formatter={(v: unknown) => usd(v as number)} />
              <Bar dataKey="revenue" radius={[0, 4, 4, 0]}>
                {topProducts.map((p, i) => (
                  <Cell key={i} fill={CATEGORY_COLORS[p.category] ?? '#94a3b8'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Category revenue share */}
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <h2 className="text-sm font-semibold text-gray-700 mb-4">Revenue by Category</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={categories}
                dataKey="revenue"
                nameKey="category"
                cx="50%"
                cy="50%"
                innerRadius={70}
                outerRadius={110}
                paddingAngle={2}
              >
                {categories.map((c, i) => (
                  <Cell key={i} fill={CATEGORY_COLORS[c.category] ?? '#94a3b8'} />
                ))}
              </Pie>
              <Tooltip formatter={(v: unknown) => usd(v as number)} />
              <Legend iconType="circle" iconSize={8} wrapperStyle={{ fontSize: 12 }} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Return Rate Table */}
      <div className="bg-white rounded-xl border border-gray-200 p-5">
        <h2 className="text-sm font-semibold text-gray-700 mb-4">
          Top 10 Most Returned Products
        </h2>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-100">
                <th className="text-left py-2 px-3 text-xs font-medium text-gray-500">Product</th>
                <th className="text-left py-2 px-3 text-xs font-medium text-gray-500">Category</th>
                <th className="text-right py-2 px-3 text-xs font-medium text-gray-500">Total Orders</th>
                <th className="text-right py-2 px-3 text-xs font-medium text-gray-500">Returns</th>
                <th className="text-right py-2 px-3 text-xs font-medium text-gray-500">Return Rate</th>
              </tr>
            </thead>
            <tbody>
              {returnRates.map((r) => (
                <tr key={r.product_id} className="border-b border-gray-50 hover:bg-gray-50">
                  <td className="py-2 px-3 text-gray-800">{r.name}</td>
                  <td className="py-2 px-3 text-gray-500">{r.category}</td>
                  <td className="py-2 px-3 text-right text-gray-700">{r.total_orders}</td>
                  <td className="py-2 px-3 text-right text-gray-700">{r.returned_orders}</td>
                  <td className="py-2 px-3 text-right font-medium text-orange-600">
                    {(r.return_rate * 100).toFixed(1)}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
