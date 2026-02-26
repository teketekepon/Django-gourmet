import { useEffect, useMemo, useState } from 'react'
import type { FormEvent, ReactElement } from 'react'
import { Link, Navigate, Route, Routes, useNavigate, useParams, useSearchParams } from 'react-router-dom'
import './App.css'
import { createDish, deleteDish, fetchCategories, fetchDish, fetchDishes, login, logout, me, signup } from './api/services'
import type { Category, Dish, User } from './types'

function Layout({ user, onLogout }: { user: User | null; onLogout: () => Promise<void> }) {
  return (
    <div className="app-shell">
      <header className="app-header">
        <Link to="/" className="brand">Gourmet</Link>
        <nav>
          <Link to="/">一覧</Link>
          {user && <Link to="/post">投稿</Link>}
          {user && <Link to="/mypage">マイページ</Link>}
          {!user && <Link to="/login">ログイン</Link>}
          {!user && <Link to="/signup">サインアップ</Link>}
          {user && (
            <button onClick={() => void onLogout()} className="linklike">ログアウト</button>
          )}
        </nav>
      </header>
      <main className="app-main">
        <Routes>
          <Route path="/" element={<DishListPage user={user} />} />
          <Route path="/dish/:id" element={<DishDetailPage user={user} />} />
          <Route path="/login" element={user ? <Navigate to="/" /> : <LoginPage />} />
          <Route path="/signup" element={user ? <Navigate to="/" /> : <SignupPage />} />
          <Route path="/post" element={<Protected user={user}><PostDishPage /></Protected>} />
          <Route path="/mypage" element={<Protected user={user}><MyPage /></Protected>} />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </main>
    </div>
  )
}

function Protected({ user, children }: { user: User | null; children: ReactElement }) {
  if (!user) return <Navigate to="/login" replace />
  return children
}

function DishListPage({ user }: { user: User | null }) {
  const [categories, setCategories] = useState<Category[]>([])
  const [dishes, setDishes] = useState<Dish[]>([])
  const [searchParams, setSearchParams] = useSearchParams()
  const selectedCategory = searchParams.get('category') ?? ''

  useEffect(() => {
    void fetchCategories().then(setCategories)
  }, [])

  useEffect(() => {
    void fetchDishes({ category: selectedCategory || undefined })
      .then(setDishes)
  }, [selectedCategory])

  return (
    <section>
      <h1>料理一覧</h1>
      <select
        value={selectedCategory}
        onChange={(e) => {
          const value = e.target.value
          setSearchParams(value ? { category: value } : {})
        }}
      >
        <option value="">すべてのカテゴリ</option>
        {categories.map((c) => (
          <option value={String(c.id)} key={c.id}>{c.title}</option>
        ))}
      </select>
      <DishGrid dishes={dishes} currentUserId={user?.id} />
    </section>
  )
}

function DishGrid({ dishes, currentUserId }: { dishes: Dish[]; currentUserId?: number }) {
  if (!dishes.length) return <p>投稿がありません。</p>
  return (
    <ul className="dish-grid">
      {dishes.map((d) => (
        <li key={d.id} className="dish-card">
          <Link to={`/dish/${d.id}`}>
            {d.image_url ? <img src={d.image_url} alt={d.title} /> : <div className="placeholder">No image</div>}
            <h3>{d.title}</h3>
          </Link>
          <p>{d.category_title} / {d.username}</p>
          {currentUserId === d.user_id && <small>あなたの投稿</small>}
        </li>
      ))}
    </ul>
  )
}

function DishDetailPage({ user }: { user: User | null }) {
  const { id } = useParams()
  const navigate = useNavigate()
  const [dish, setDish] = useState<Dish | null>(null)

  useEffect(() => {
    if (!id) return
    void fetchDish(Number(id)).then(setDish)
  }, [id])

  if (!dish) return <p>読み込み中...</p>

  return (
    <section>
      <h1>{dish.title}</h1>
      {dish.image_url && <img src={dish.image_url} alt={dish.title} className="detail-image" />}
      <p>{dish.comment}</p>
      <p>{dish.category_title} / {dish.username}</p>
      {user?.id === dish.user_id && (
        <button
          onClick={() => {
            void deleteDish(dish.id).then(() => navigate('/mypage'))
          }}
        >
          削除
        </button>
      )}
    </section>
  )
}

function LoginPage() {
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  async function onSubmit(e: FormEvent) {
    e.preventDefault()
    setError('')
    try {
      await login(username, password)
      navigate('/')
      window.location.reload()
    } catch (err) {
      setError((err as Error).message)
    }
  }

  return (
    <form onSubmit={onSubmit} className="form">
      <h1>ログイン</h1>
      <input value={username} onChange={(e) => setUsername(e.target.value)} placeholder="username" />
      <input value={password} onChange={(e) => setPassword(e.target.value)} placeholder="password" type="password" />
      {error && <p className="error">{error}</p>}
      <button type="submit">ログイン</button>
    </form>
  )
}

function SignupPage() {
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  async function onSubmit(e: FormEvent) {
    e.preventDefault()
    setError('')
    try {
      await signup(username, email, password)
      await login(username, password)
      navigate('/')
      window.location.reload()
    } catch (err) {
      setError((err as Error).message)
    }
  }

  return (
    <form onSubmit={onSubmit} className="form">
      <h1>サインアップ</h1>
      <input value={username} onChange={(e) => setUsername(e.target.value)} placeholder="username" />
      <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="email" type="email" />
      <input value={password} onChange={(e) => setPassword(e.target.value)} placeholder="password" type="password" />
      {error && <p className="error">{error}</p>}
      <button type="submit">登録</button>
    </form>
  )
}

function PostDishPage() {
  const navigate = useNavigate()
  const [categories, setCategories] = useState<Category[]>([])
  const [category, setCategory] = useState('')
  const [title, setTitle] = useState('')
  const [comment, setComment] = useState('')
  const [image, setImage] = useState<File | null>(null)

  useEffect(() => {
    void fetchCategories().then((c) => {
      setCategories(c)
      if (c.length) setCategory(String(c[0].id))
    })
  }, [])

  async function onSubmit(e: FormEvent) {
    e.preventDefault()
    const form = new FormData()
    form.append('category', category)
    form.append('title', title)
    form.append('comment', comment)
    if (image) form.append('image', image)
    await createDish(form)
    navigate('/')
  }

  return (
    <form onSubmit={onSubmit} className="form">
      <h1>料理投稿</h1>
      <select value={category} onChange={(e) => setCategory(e.target.value)}>
        {categories.map((c) => <option key={c.id} value={c.id}>{c.title}</option>)}
      </select>
      <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="タイトル" />
      <textarea value={comment} onChange={(e) => setComment(e.target.value)} placeholder="コメント" />
      <input type="file" accept="image/*" onChange={(e) => setImage(e.target.files?.[0] ?? null)} />
      <button type="submit">投稿</button>
    </form>
  )
}

function MyPage() {
  const [dishes, setDishes] = useState<Dish[]>([])
  useEffect(() => {
    void fetchDishes({ mine: true }).then(setDishes)
  }, [])
  return (
    <section>
      <h1>マイページ</h1>
      <DishGrid dishes={dishes} />
    </section>
  )
}

export default function App() {
  const [user, setUser] = useState<User | null>(null)
  const [resolved, setResolved] = useState(false)

  useEffect(() => {
    void me()
      .then(setUser)
      .catch(() => setUser(null))
      .finally(() => setResolved(true))
  }, [])

  const onLogout = useMemo(
    () => async () => {
      await logout()
      setUser(null)
    },
    [],
  )

  if (!resolved) return <p>認証情報を確認中...</p>

  return <Layout user={user} onLogout={onLogout} />
}

