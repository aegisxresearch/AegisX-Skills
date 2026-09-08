# `React` & `Next.js` Patterns

## Overview
Panduan `React` & `Next.js`: hooks, Server Components, App Router, state management, dan performance.

---

## ️ `React` Hooks Patterns

### Custom Hooks
```typescript
// useLocalStorage
function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key)
      return item ? JSON.parse(item) : initialValue
    } catch {
      return initialValue
    }
  })

  const setValue = (value: T | ((val: T) => T)) => {
    const valueToStore = value instanceof Function ? value(storedValue) : value
    setStoredValue(valueToStore)
    window.localStorage.setItem(key, JSON.stringify(valueToStore))
  }

  return [storedValue, setValue] as const
}

// useDebounce
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value)

  useEffect(() => {
    const handler = setTimeout(() => setDebouncedValue(value), delay)
    return () => clearTimeout(handler)
  }, [value, delay])

  return debouncedValue
}

// useFetch
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    const controller = new AbortController()
    
    fetch(url, { signal: controller.signal })
      .then(res => res.json())
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false))
    
    return () => controller.abort()
  }, [url])

  return { data, loading, error }
}
```python

---

## `Next.js` App Router

### Server Components (Default)
```typescript
// app/page.tsx - Server Component (default)
async function HomePage() {
  // Direct database access!
  const posts = await db.post.findMany()
  
  return (
    <main>
      <h1>Blog</h1>
      {posts.map(post => (
        <PostCard key={post.id} post={post} />
      ))}
    </main>
  )
}

export default HomePage
```python

### Client Components
```typescript
// components/InteractiveButton.tsx
'use client'

import { useState } from 'react'

export function InteractiveButton() {
  const [count, setCount] = useState(0)
  
  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  )
}
```python

### Server Actions
```typescript
// actions/user.ts
'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'

export async function createUser(formData: FormData) {
  const name = formData.get('name') as string
  const email = formData.get('email') as string
  
  await db.user.create({
    data: { name, email }
  })
  
  revalidatePath('/users')
  redirect('/users')
}

// Usage in component
<form action={createUser}>
  <input name="name" required />
  <input name="email" type="email" required />
  <button type="submit">Create</button>
</form>
```python

### Data Fetching
```typescript
// Server Component with cache
async function getUser(id: string) {
  const res = await fetch(`https://api.example.com/users/${id}`, {
    next: { revalidate: 3600 } // Cache for 1 hour
  })
  return res.json()
}

// Streaming with Suspense
import { Suspense } from 'react'

async function UserProfile({ id }: { id: string }) {
  const user = await getUser(id)
  return <div>{user.name}</div>
}

export default function Page() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <UserProfile id="1" />
    </Suspense>
  )
}
```python

---

## State Management

### Zustand (Recommended)
```typescript
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface AppState {
  count: number
  increment: () => void
  decrement: () => void
  reset: () => void
}

const useStore = create<AppState>()(
  persist(
    (set) => ({
      count: 0,
      increment: () => set((state) => ({ count: state.count + 1 })),
      decrement: () => set((state) => ({ count: state.count - 1 })),
      reset: () => set({ count: 0 }),
    }),
    { name: 'app-store' }
  )
)

// Usage
function Counter() {
  const { count, increment } = useStore()
  return <button onClick={increment}>Count: {count}</button>
}
```python

### `React` Query / TanStack Query
```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

// Fetch data
function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: () => fetch('/api/users').then(res => res.json()),
  })
}

// Mutate data
function useCreateUser() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (newUser: CreateUserInput) =>
      fetch('/api/users', {
        method: 'POST',
        body: JSON.stringify(newUser),
      }).then(res => res.json()),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] })
    },
  })
}
```python

---

## Performance Patterns

### Code Splitting
```typescript
import dynamic from 'next/dynamic'

const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <p>Loading...</p>,
  ssr: false
})
```python

### Memoization
```typescript
import { memo, useMemo, useCallback } from 'react'

// Memoize expensive computation
const sortedItems = useMemo(() => {
  return items.sort((a, b) => a.name.localeCompare(b.name))
}, [items])

// Memoize callback
const handleClick = useCallback(() => {
  console.log('clicked')
}, [])

// Memoize component
const ExpensiveComponent = memo(function ExpensiveComponent({ data }) {
  return <div>{/* complex rendering */}</div>
})
```python

### Image Optimization
```typescript
import Image from 'next/image'

<Image
  src="/photo.jpg"
  alt="Description"
  width={500}
  height={300}
  placeholder="blur"
  blurDataURL="data:image/jpeg;base64,..."
  priority={true} // For above-the-fold images
/>
```

---

## `Next.js` Checklist

### App Router
- [ ] Use Server Components by default
- [ ] Add 'use client' only when needed
- [ ] Use Server Actions for mutations
- [ ] Implement proper loading states
- [ ] Handle errors with error.tsx

### Performance
- [ ] Use next/image for images
- [ ] Implement code splitting
- [ ] Use `React` Query for data fetching
- [ ] Memoize expensive computations

### SEO
- [ ] Add metadata exports
- [ ] Use generateMetadata for dynamic pages
- [ ] Implement structured data

---

## Kesalahan Umum / Pitfalls

- Client-side state that should be server-side.
- No caching strategy — every request hits the origin.
- Server Actions without error handling — silent failures.
- Ignoring Next.js caching headers — CDN misses.

## Trade-off dan Kapan Tidak Pakai

- Server Components are great for SEO but limit interactivity — use client where needed.
- Server Actions simplify mutations but complicate optimistic UI — weigh them.
- App Router is the future but has migration cost — plan it.

## References
- https://nextjs.org/docs/app
- https://react.dev/learn
- https://tanstack.com/query

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
