export interface TopProduct {
  product_id: number
  name: string
  category: string
  revenue: number
  units_sold: number
}

export interface CategoryStat {
  category: string
  revenue: number
  orders: number
}

export interface ProductReturnRate {
  product_id: number
  name: string
  category: string
  total_orders: number
  returned_orders: number
  return_rate: number
}
