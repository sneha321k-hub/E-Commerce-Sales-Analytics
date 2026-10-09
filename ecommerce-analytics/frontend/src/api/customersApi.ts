import client from './client'
import type {
  CustomerSummary,
  TopCustomer,
  CountryStat,
  NewVsReturningPoint,
} from '../types/customers'

export const fetchCustomerSummary = () =>
  client.get<CustomerSummary>('/analytics/customers/summary').then((r) => r.data)

export const fetchTopCustomers = () =>
  client.get<TopCustomer[]>('/analytics/customers/top').then((r) => r.data)

export const fetchCustomersByCountry = () =>
  client.get<CountryStat[]>('/analytics/customers/by-country').then((r) => r.data)

export const fetchNewVsReturning = () =>
  client.get<NewVsReturningPoint[]>('/analytics/customers/new-vs-returning').then((r) => r.data)
