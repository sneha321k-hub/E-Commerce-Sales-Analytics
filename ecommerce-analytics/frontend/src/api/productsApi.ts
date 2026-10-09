import client from './client'
import type { TopProduct, CategoryStat, ProductReturnRate } from '../types/products'

export const fetchTopProducts = () =>
  client.get<TopProduct[]>('/analytics/products/top').then((r) => r.data)

export const fetchProductsByCategory = () =>
  client.get<CategoryStat[]>('/analytics/products/by-category').then((r) => r.data)

export const fetchReturnRates = () =>
  client.get<ProductReturnRate[]>('/analytics/products/return-rate').then((r) => r.data)
