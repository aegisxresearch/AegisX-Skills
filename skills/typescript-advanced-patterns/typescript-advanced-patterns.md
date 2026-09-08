# `TypeScript` Advanced Patterns

## Overview
Panduan `TypeScript` lanjutan: generics, utility types, type guards, dan design patterns.

---

## Generics

### Basic Generics
```typescript
// Generic function
function identity<T>(arg: T): T {
  return arg
}

const greeting = identity<string>("hello") // string
const result2 = identity(42) // number (inferred)

// Generic interface
interface ApiResponse<T> {
  data: T
  status: number
  message: string
}

type UserResponse = ApiResponse<User>
type PostResponse = ApiResponse<Post[]>
```typescript

### Generic Constraints
```typescript
// Constrain to object types
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key]
}

const user = { name: "John", age: 30 }
const name = getProperty(user, "name") // string
const age = getProperty(user, "age") // number

// Constrain to specific types
function merge<T extends object, U extends object>(a: T, b: U): T & U {
  return { ...a, ...b }
}
```python

### Generic Classes
```typescript
class Repository<T extends { id: number }> {
  private items: T[] = []
  
  add(item: T): void {
    this.items.push(item)
  }
  
  findById(id: number): T | undefined {
    return this.items.find(item => item.id === id)
  }
  
  filter(predicate: (item: T) => boolean): T[] {
    return this.items.filter(predicate)
  }
}

// Usage
const userRepo = new Repository<User>()
userRepo.add({ id: 1, name: "John", email: "john@example.com" })
```typescript

---

## ️ Utility Types

### Built-in Utility Types
```typescript
interface User {
  id: number
  name: string
  email: string
  age: number
}

// Partial - all optional
type PartialUser = Partial<User>
// { id?: number; name?: string; ... }

// Required - all required
type RequiredUser = Required<PartialUser>

// Pick - select specific fields
type UserBasic = Pick<User, "id" | "name">
// { id: number; name: string }

// Omit - remove specific fields
type UserWithoutEmail = Omit<User, "email">
// { id: number; name: string; age: number }

// Record - key-value type
type UserMap = Record<string, User>
// { [key: string]: User }

// Readonly
type ReadonlyUser = Readonly<User>

// ReturnType
function createUser() { return { id: 1, name: "John" } }
type CreateUserReturn = ReturnType<typeof createUser>
```

### Custom Utility Types
```typescript
// Make specific fields required
type RequireField<T, K extends keyof T> = T & Required<Pick<T, K>>

// Make specific fields optional
type OptionalField<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>

// Deep partial
type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P]
}

// Deep readonly
type DeepReadonly<T> = {
  readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P]
}

// Extract nullable fields
type NullableKeys<T> = {
  [K in keyof T]: null extends T[K] ? K : undefined extends T[K] ? K : never
}[keyof T]

// Usage
type UserWithRequiredEmail = RequireField<User, "email">
```typescript

---

## Type Guards

### Built-in Type Guards
```typescript
// typeof
function isString(value: unknown): value is string {
  return typeof value === "string"
}

// instanceof
function isError(value: unknown): value is Error {
  return value instanceof Error
}

// in
interface Dog { bark(): void }
interface Cat { meow(): void }

function makeSound(animal: Dog | Cat) {
  if ("bark" in animal) {
    animal.bark() // Dog
  } else {
    animal.meow() // Cat
  }
}
```typescript

### Custom Type Guards
```typescript
// Discriminated unions
type Result<T> = 
  | { success: true; data: T }
  | { success: false; error: string }

function isSuccess<T>(outcome: Result<T>): outcome is { success: true; data: T } {
  return outcome.success === true
}

// Usage
function handleOutcome(outcome: Result<User>) {
  if (isSuccess(outcome)) {
    console.log(outcome.data.name) // `TypeScript` knows data exists
  } else {
    console.log(outcome.error)
  }
}
```python

---

## ️ Design Patterns

### Builder Pattern
```typescript
class QueryBuilder<T> {
  private conditions: string[] = []
  private orderByField?: string
  private limitValue?: number
  
  where(condition: string): this {
    this.conditions.push(condition)
    return this
  }
  
  orderBy(field: string): this {
    this.orderByField = field
    return this
  }
  
  limit(n: number): this {
    this.limitValue = n
    return this
  }
  
  build(): string {
    let query = "SELECT * FROM users"
    if (this.conditions.length) {
      query += ` WHERE ${this.conditions.join(" AND ")}`
    }
    if (this.orderByField) {
      query += ` ORDER BY ${this.orderByField}`
    }
    if (this.limitValue) {
      query += ` LIMIT ${this.limitValue}`
    }
    return query
  }
}

// Usage
const query = new QueryBuilder()
  .where("age > 18")
  .where("status = 'active'")
  .orderBy("name")
  .limit(10)
  .build()
```python

### Factory Pattern
```typescript
interface PaymentProcessor {
  process(amount: number): Promise<boolean>
}

class StripeProcessor implements PaymentProcessor {
  async process(amount: number): Promise<boolean> {
    console.log(`Processing $${amount} with Stripe`)
    return true
  }
}

class PayPalProcessor implements PaymentProcessor {
  async process(amount: number): Promise<boolean> {
    console.log(`Processing $${amount} with PayPal`)
    return true
  }
}

class PaymentFactory {
  static create(method: "stripe" | "paypal"): PaymentProcessor {
    switch (method) {
      case "stripe": return new StripeProcessor()
      case "paypal": return new PayPalProcessor()
    }
  }
}

// Usage
const processor = PaymentFactory.create("stripe")
await processor.process(100)
```python

### Observer Pattern
```typescript
type EventHandler<T> = (data: T) => void

class EventEmitter<Events extends Record<string, unknown>> {
  private handlers = new Map<string, Set<EventHandler<any>>>()
  
  on<K extends keyof Events>(event: K, handler: EventHandler<Events[K]>): void {
    if (!this.handlers.has(event as string)) {
      this.handlers.set(event as string, new Set())
    }
    this.handlers.get(event as string)!.add(handler)
  }
  
  emit<K extends keyof Events>(event: K, data: Events[K]): void {
    this.handlers.get(event as string)?.forEach(handler => handler(data))
  }
}

// Usage
interface UserEvents {
  created: { id: number; name: string }
  deleted: { id: number }
}

const emitter = new EventEmitter<UserEvents>()
emitter.on("created", (data) => console.log(`User created: ${data.name}`))
emitter.emit("created", { id: 1, name: "John" })
```

---

## `TypeScript` Checklist

### Types
- [ ] Use `interface` for object shapes
- [ ] Use `type` for unions and intersections
- [ ] Use `enum` for constant sets
- [ ] Use `unknown` instead of `any`
- [ ] Use `as const` for literal types

### Patterns
- [ ] Use discriminated unions for state machines
- [ ] Use type guards for runtime checks
- [ ] Use generics for reusable components
- [ ] Use utility types to transform types

---

## Kesalahan Umum / Pitfalls

- Using `any` liberally — defeats the type system.
- Overly clever generics — unreadable by the team.
- Type guards that lie — runtime behavior differs from type claims.
- Discriminated unions without a discriminant — unsafe narrowing.

## Trade-off dan Kapan Tidak Pakai

- Strict typing costs boilerplate but prevents whole classes of bugs.
- Generic utilities are powerful but can obscure intent — name them well.
- Type-level programming is clever but hard to maintain — use sparingly.

## References
- https://www.typescriptlang.org/docs/handbook/
- https://www.typescriptlang.org/docs/handbook/utility-types.html
- https://github.com/type-challenges/type-challenges

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
