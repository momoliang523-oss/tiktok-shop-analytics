/**
 * Data formatting utilities
 */

export function formatCurrency(value: number, currency: string = 'USD'): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(value)
}

export function formatNumber(value: number): string {
  return new Intl.NumberFormat('en-US').format(value)
}

export function formatPercent(value: number, decimals: number = 2): string {
  return (value * 100).toFixed(decimals) + '%'
}

export function formatLargeNumber(value: number): string {
  if (value >= 1e9) {
    return (value / 1e9).toFixed(1) + 'B'
  } else if (value >= 1e6) {
    return (value / 1e6).toFixed(1) + 'M'
  } else if (value >= 1e3) {
    return (value / 1e3).toFixed(1) + 'K'
  }
  return value.toString()
}

export function truncate(str: string, length: number): string {
  if (!str) return ''
  return str.length > length ? str.substring(0, length) + '...' : str
}
