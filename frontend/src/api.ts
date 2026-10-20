const LOCAL_API_ORIGIN = 'http://localhost:8000'

export function apiOrigin(rawValue: string | undefined = import.meta.env.VITE_API_URL): string {
  const raw = (rawValue || LOCAL_API_ORIGIN).trim().replace(/\/+$/, '')
  if (raw.endsWith('/api')) {
    return raw.slice(0, -4)
  }
  return raw
}
