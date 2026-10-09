interface KpiCardProps {
  title: string
  value: string
  subtitle?: string
}

export default function KpiCard({ title, value, subtitle }: KpiCardProps) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5">
      <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">{title}</p>
      <p className="mt-1 text-2xl font-semibold text-gray-800">{value}</p>
      {subtitle && <p className="mt-1 text-xs text-gray-400">{subtitle}</p>}
    </div>
  )
}
