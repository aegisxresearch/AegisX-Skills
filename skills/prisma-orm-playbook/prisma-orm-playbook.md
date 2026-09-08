# Prisma ORM Playbook

## Overview
Panduan Prisma ORM: schema design, queries, relations, migrations, dan best practices.

---

## ️ Schema Design

### Basic Schema
```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  name      String?
  posts     Post[]
  profile   Profile?
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")

  @@map("users")
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  Int      @map("author_id")
  tags      Tag[]
  createdAt DateTime @default(now()) @map("created_at")

  @@map("posts")
}

model Tag {
  id    Int    @id @default(autoincrement())
  name  String @unique
  posts Post[]

  @@map("tags")
}
```

### Relations
```prisma
// One-to-One
model User {
  id      Int     @id @default(autoincrement())
  profile Profile?
}

model Profile {
  id     Int  @id @default(autoincrement())
  user   User @relation(fields: [userId], references: [id])
  userId Int  @unique @map("user_id")
}

// Many-to-Many (implicit)
model Post {
  id   Int  @id @default(autoincrement())
  tags Tag[]
}

model Tag {
  id    Int    @id @default(autoincrement())
  posts Post[]
}

// Many-to-Many (explicit - for extra fields)
model Post {
  id         Int          @id @default(autoincrement())
  categories PostCategory[]
}

model Category {
  id    Int          @id @default(autoincrement())
  posts PostCategory[]
}

model PostCategory {
  post       Post     @relation(fields: [postId], references: [id])
  postId     Int      @map("post_id")
  category   Category @relation(fields: [categoryId], references: [id])
  categoryId Int      @map("category_id")
  assignedAt DateTime @default(now()) @map("assigned_at")

  @@id([postId, categoryId])
  @@map("post_categories")
}
```python

---

## Query Patterns

### Basic CRUD
```typescript
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

// Create
const user = await prisma.user.create({
  data: {
    email: 'john@example.com',
    name: 'John Doe',
  }
})

// Read
const user = await prisma.user.findUnique({
  where: { email: 'john@example.com' }
})

// Update
const user = await prisma.user.update({
  where: { id: 1 },
  data: { name: 'Jane Doe' }
})

// Delete
await prisma.user.delete({
  where: { id: 1 }
})
```typescript

### Relations Query
```typescript
// Include relations
const userWithPosts = await prisma.user.findUnique({
  where: { id: 1 },
  include: {
    posts: {
      where: { published: true },
      orderBy: { createdAt: 'desc' },
      take: 10
    },
    profile: true
  }
})

// Select specific fields
const users = await prisma.user.findMany({
  select: {
    id: true,
    email: true,
    _count: {
      select: { posts: true }
    }
  }
})
```typescript

### Filtering
```typescript
// Complex filtering
const posts = await prisma.post.findMany({
  where: {
    AND: [
      { published: true },
      {
        OR: [
          { title: { contains: 'prisma', mode: 'insensitive' } },
          { tags: { some: { name: 'typescript' } } }
        ]
      }
    ]
  },
  include: {
    author: {
      select: { name: true, email: true }
    }
  }
})
```typescript

### Pagination
```typescript
// Cursor-based pagination
const posts = await prisma.post.findMany({
  take: 20,
  skip: 1, // Skip the cursor
  cursor: { id: lastId },
  orderBy: { id: 'asc' }
})

// Offset pagination
const posts = await prisma.post.findMany({
  skip: (page - 1) * limit,
  take: limit,
  orderBy: { createdAt: 'desc' }
})
```python

---

## Transactions

### Interactive Transactions
```typescript
const transferOutcome = await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({
    data: { email: 'john@example.com' }
  })
  
  const profile = await tx.profile.create({
    data: {
      userId: user.id,
      bio: 'Hello!'
    }
  })
  
  return { user, profile }
})
```python

### Batch Operations
```typescript
// Create many
await prisma.post.createMany({
  data: [
    { title: 'Post 1', authorId: 1 },
    { title: 'Post 2', authorId: 1 },
    { title: 'Post 3', authorId: 2 },
  ]
})

// Update many
await prisma.post.updateMany({
  where: { published: false },
  data: { published: true }
})
```typescript

---

## Raw Queries

```typescript
// Raw query
const users = await prisma.$queryRaw`
  SELECT * FROM users 
  WHERE email = ${email}
`

// Raw query with Prisma raw
const users = await prisma.$queryRaw(
  'SELECT * FROM users WHERE email = $1',
  email
)

// Execute raw (for INSERT, UPDATE, DELETE)
await prisma.$executeRaw`
  UPDATE users SET name = ${name} WHERE id = ${id}
`
```

---

## Migrations

```bash
# Create migration
npx prisma migrate dev --name add_user_table

# Apply migrations in production
npx prisma migrate deploy

# Reset database (development only!)
npx prisma migrate reset

# Generate client
npx prisma generate

# Open Prisma Studio (GUI)
npx prisma studio
```

---

## Best Practices

### Schema
- [ ] Use `@@map` for snake_case table names
- [ ] Use `@map` for snake_case column names
- [ ] Add `@default(now())` for timestamps
- [ ] Use `@unique` for required unique fields
- [ ] Add proper relations with foreign keys

### Queries
- [ ] Use `select` instead of `include` when possible
- [ ] Always use `where` to filter results
- [ ] Use `take` to limit results
- [ ] Use cursor-based pagination for large datasets

### Performance
- [ ] Use `$transaction` for related operations
- [ ] Avoid N+1 queries with `include`
- [ ] Use `createMany` for bulk inserts
- [ ] Add database indexes for frequent queries

---

## Kesalahan Umum / Pitfalls

- No migrations in version control — schema drift.
- N+1 queries from lazy loading relations.
- Raw SQL mixed with the ORM inconsistently.
- No transaction wrapping on multi-write operations.

## Trade-off dan Kapan Tidak Pakai

- Prisma is convenient but abstracts SQL — learn SQL for complex queries.
- Migrations are automated but review them — they can be destructive.
- Prisma's query engine adds overhead — consider raw SQL for hot paths.

## References
- https://www.prisma.io/docs
- https://www.prisma.io/docs/concepts/components/prisma-client
- https://www.prisma.io/docs/concepts/components/prisma-migrate

---

## Checklist

- [ ] Schema reflects the domain model, not the other way around
- [ ] All relations use explicit `onDelete` behavior
- [ ] Migrations are reviewed before apply
- [ ] Transactions wrap multi-write operations
- [ ] N+1 queries eliminated with `include` or `select`

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
