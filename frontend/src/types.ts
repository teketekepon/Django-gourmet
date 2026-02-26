export type User = {
  id: number
  username: string
  email: string
}

export type Category = {
  id: number
  title: string
}

export type Dish = {
  id: number
  user_id: number
  username: string
  category_id: number
  category_title: string
  title: string
  comment: string
  image_url: string | null
  posted_at: string
}

