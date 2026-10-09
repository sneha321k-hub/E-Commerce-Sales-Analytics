export interface CustomerSummary {
  total_customers: number
  new_this_month: number
  returning_customers: number
}

export interface TopCustomer {
  customer_id: number
  name: string
  email: string
  total_spend: number
  order_count: number
}

export interface CountryStat {
  country: string
  customer_count: number
  revenue: number
}

export interface NewVsReturningPoint {
  month: string
  new_customers: number
  returning_customers: number
}
