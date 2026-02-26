type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE'

let accessToken: string | null = null

export const authTokenStore = {
  get: () => accessToken,
  set: (token: string | null) => {
    accessToken = token
  },
}

type RequestOptions = {
  method?: HttpMethod
  body?: BodyInit | null
  headers?: Record<string, string>
  retryOn401?: boolean
}

async function refreshAccessToken(): Promise<string | null> {
  const response = await fetch('/api/auth/refresh/', {
    method: 'POST',
    credentials: 'include',
  })
  if (!response.ok) {
    authTokenStore.set(null)
    return null
  }
  const data = (await response.json()) as { access: string }
  authTokenStore.set(data.access)
  return data.access
}

export async function apiFetch<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const token = authTokenStore.get()
  const response = await fetch(path, {
    method: options.method ?? 'GET',
    body: options.body ?? null,
    credentials: 'include',
    headers: {
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers ?? {}),
    },
  })

  if (response.status === 401 && options.retryOn401 !== false) {
    const refreshed = await refreshAccessToken()
    if (refreshed) {
      return apiFetch<T>(path, { ...options, retryOn401: false })
    }
  }

  if (!response.ok) {
    let detail = `HTTP ${response.status}`
    try {
      const errorData = (await response.json()) as { detail?: string }
      if (errorData.detail) detail = errorData.detail
    } catch {
      // ignore parsing failure
    }
    throw new Error(detail)
  }

  if (response.status === 204) {
    return undefined as T
  }

  return (await response.json()) as T
}

