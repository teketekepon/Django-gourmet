import { apiFetch, authTokenStore } from './client'
import type { Category, Dish, User } from '../types'

type LoginResponse = { access: string }

export async function login(username: string, password: string): Promise<void> {
  const data = await apiFetch<LoginResponse>('/api/auth/login/', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
    headers: { 'Content-Type': 'application/json' },
    retryOn401: false,
  })
  authTokenStore.set(data.access)
}

export async function signup(username: string, email: string, password: string): Promise<void> {
  await apiFetch<User>('/api/auth/signup/', {
    method: 'POST',
    body: JSON.stringify({ username, email, password }),
    headers: { 'Content-Type': 'application/json' },
    retryOn401: false,
  })
}

export async function me(): Promise<User> {
  return apiFetch<User>('/api/auth/me/')
}

export async function logout(): Promise<void> {
  await apiFetch<void>('/api/auth/logout/', { method: 'POST' })
  authTokenStore.set(null)
}

export async function fetchCategories(): Promise<Category[]> {
  return apiFetch<Category[]>('/api/categories/')
}

export async function fetchDishes(params?: {
  category?: string
  mine?: boolean
  user?: number
}): Promise<Dish[]> {
  const query = new URLSearchParams()
  if (params?.category) query.set('category', params.category)
  if (params?.mine) query.set('mine', 'true')
  if (params?.user) query.set('user', String(params.user))
  const suffix = query.toString() ? `?${query.toString()}` : ''
  return apiFetch<Dish[]>(`/api/dishes/${suffix}`)
}

export async function fetchDish(id: number): Promise<Dish> {
  return apiFetch<Dish>(`/api/dishes/${id}/`)
}

export async function createDish(formData: FormData): Promise<void> {
  await apiFetch('/api/dishes/', {
    method: 'POST',
    body: formData,
  })
}

export async function deleteDish(id: number): Promise<void> {
  await apiFetch(`/api/dishes/${id}/`, {
    method: 'DELETE',
  })
}

