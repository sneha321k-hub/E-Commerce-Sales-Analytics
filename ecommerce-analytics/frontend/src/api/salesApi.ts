import client from './client'
import type { SalesKPIs, TrendPoint, ChannelStat, OrderStatusStat } from '../types/sales'

export const fetchSalesKPIs = () =>
  client.get<SalesKPIs>('/analytics/sales/kpis').then((r) => r.data)

export const fetchSalesTrend = (days: number) =>
  client.get<TrendPoint[]>(`/analytics/sales/trend?days=${days}`).then((r) => r.data)

export const fetchSalesByChannel = () =>
  client.get<ChannelStat[]>('/analytics/sales/by-channel').then((r) => r.data)

export const fetchOrderStatus = () =>
  client.get<OrderStatusStat[]>('/analytics/sales/order-status').then((r) => r.data)
