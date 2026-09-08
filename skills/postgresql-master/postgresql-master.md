# `PostgreSQL` Master

## Overview
Panduan lengkap `PostgreSQL`: indexing, query optimization, partitioning, dan production configuration.

---

## ️ Schema Design

### Table Structure
```sql
-- Users table with proper constraints
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

-- Orders table with foreign key
CREATE TABLE orders (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    total DECIMAL(10, 2) NOT NULL CHECK (total >= 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Indexes
    CONSTRAINT valid_status CHECK (status IN ('pending', 'processing', 'shipped', 'delivered'))
);
```sql

---

## Indexing Strategies

### When to Create Index
```sql
-- ✅ Create index on frequently queried columns
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- ✅ Composite index for multi-column queries
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- ✅ Partial index (index only relevant rows)
CREATE INDEX idx_orders_pending ON orders(created_at) 
WHERE status = 'pending';

-- ✅ Covering index (includes all needed columns)
CREATE INDEX idx_users_email_name ON users(email) INCLUDE (name);
```sql

### Index Types
| Type | Use Case | Example |
|------|----------|---------|
| B-tree | Equality, range | `WHERE id = 1`, `WHERE created_at > NOW()` |
| Hash | Equality only | `WHERE email = 'x@y.com'` |
| GIN | Full-text search, arrays | `WHERE tags @> ARRAY['python']` |
| GiST | Geospatial, range | PostGIS, `WHERE tsvector @@ to_tsquery()` |
| BRIN | Large sequential tables | Time-series data |

### Check Index Usage
```sql
-- Find unused indexes
SELECT indexrelname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;

-- Analyze query performance
EXPLAIN (ANALYZE, BUFFERS) 
SELECT * FROM users WHERE email = 'test@example.com';
```sql

---

## Query Optimization

### Slow Query Diagnosis
```sql
-- Enable timing
\timing on

-- Analyze query plan
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.created_at > NOW() - INTERVAL '30 days'
GROUP BY u.id
HAVING COUNT(o.id) > 5;
```sql

### Common Optimizations
```sql
-- ✅ Use EXISTS instead of IN for subqueries
-- Bad
SELECT * FROM users WHERE id IN (SELECT user_id FROM orders);

-- Good
SELECT * FROM users u WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.id
);

-- ✅ Use JOIN instead of correlated subquery
-- Bad
SELECT *, (SELECT COUNT(*) FROM orders WHERE user_id = users.id) as order_count;

-- Good
SELECT u.*, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
GROUP BY u.id;

-- ✅ Use LIMIT for large results
SELECT * FROM orders ORDER BY created_at DESC LIMIT 20;

-- ✅ Use pagination with cursor (not OFFSET)
-- Bad
SELECT * FROM orders ORDER BY id LIMIT 20 OFFSET 1000;

-- Good
SELECT * FROM orders WHERE id > 1000 ORDER BY id LIMIT 20;
```python

---

## Pagination Patterns

### Cursor-Based (Recommended)
```sql
-- First page
SELECT * FROM orders 
ORDER BY id 
LIMIT 20;

-- Next page (use last id from previous page)
SELECT * FROM orders 
WHERE id > 12345  -- last_id from previous page
ORDER BY id 
LIMIT 20;
```sql

### Keyset Pagination
```sql
-- More flexible cursor
SELECT * FROM orders 
WHERE (created_at, id) < ('2024-01-15', 99999)
ORDER BY created_at DESC, id DESC
LIMIT 20;
```sql

---

## Partitioning

### Range Partitioning (Time-series)
```sql
CREATE TABLE events (
    id BIGSERIAL,
    user_id BIGINT NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    payload JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
) PARTITION BY RANGE (created_at);

-- Create partitions
CREATE TABLE events_2024_01 PARTITION OF events
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE events_2024_02 PARTITION OF events
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
```sql

### Auto-create Partitions
```sql
-- Use pg_partman for automatic partition management
CREATE EXTENSION pg_partman;

SELECT partman.create_parent(
    p_parent_table := 'public.events',
    p_control := 'created_at',
    p_type := 'range',
    p_interval := 'monthly'
);
```sql

---

## ️ Production Checklist

### Security
- [ ] Use SSL connections
- [ ] Implement row-level security (RLS)
- [ ] Encrypt sensitive columns
- [ ] Regular backups configured
- [ ] Monitor for slow queries

### Performance
- [ ] Add indexes for common queries
- [ ] Configure shared_buffers (25% of RAM)
- [ ] Set effective_cache_size (75% of RAM)
- [ ] Enable pg_stat_statements
- [ ] Regular VACUUM and ANALYZE

### Monitoring
```sql
-- Enable monitoring
CREATE EXTENSION pg_stat_statements;

-- Top 10 slowest queries
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Connection count
SELECT count(*) FROM pg_stat_activity;
```

---

## Quick Reference

### Common Commands
```sql
-- Database info
\l              -- List databases
\dt             -- List tables
\d table_name   -- Describe table
\di             -- List indexes

-- Maintenance
VACUUM ANALYZE; -- Clean up and update stats
REINDEX TABLE;  -- Rebuild indexes
```

---

## References
- https://www.postgresql.org/docs/current/
- https://use-the-index-luke.com/
- https://pganalyze.com/

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
