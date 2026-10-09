export interface SalesKPIs {
  total_revenue: number
  total_orders: number
  average_order_value: number
  total_customers: number
}

export interface TrendPoint {
  date: string
  revenue: number
  orders: number
}

export interface ChannelStat {
  channel: string
  revenue: number
  orders: number
}

export interface OrderStatusStat {
  status: string
  count: number
}
