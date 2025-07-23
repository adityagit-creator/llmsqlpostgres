## 🗃️ PostgreSQL Database Schema

Here is the detailed schema for the tables used in your **LLM SQL Chatbot**:

---

### 📋 Table: `users`

This table stores information about the users.

| Column      | Type            | Description                                      |
|-------------|-----------------|--------------------------------------------------|
| `id`        | `INT PRIMARY KEY` | A unique identifier for each user.              |
| `name`      | `VARCHAR(255)`  | The full name of the user.                       |
| `email`     | `VARCHAR(255) UNIQUE` | The email address of the user (must be unique). |
| `created_at`| `TIMESTAMP`     | The timestamp when the user record was created.  |

---

### 📦 Table: `products`

This table stores information about the products available.

| Column   | Type              | Description                                                         |
|----------|-------------------|---------------------------------------------------------------------|
| `id`     | `INT PRIMARY KEY` | A unique identifier for each product.                              |
| `name`   | `VARCHAR(255)`    | The name of the product.                                           |
| `price`  | `DECIMAL(10, 2)`  | The price of the product (up to 10 digits total, 2 after decimal). |
| `stock`  | `INT`             | The current stock quantity of the product.                         |

---

### 🧾 Table: `orders`

This table stores information about customer orders, linking users to products.

| Column       | Type              | Description                                                                 |
|--------------|-------------------|-----------------------------------------------------------------------------|
| `id`         | `INT PRIMARY KEY` | A unique identifier for each order.                                        |
| `user_id`    | `INT`             | A foreign key referencing `users.id`, indicating which user placed the order. |
| `product_id` | `INT`             | A foreign key referencing `products.id`, indicating which product was ordered. |
| `quantity`   | `INT`             | The quantity of the product ordered.                                       |
| `order_date` | `TIMESTAMP`       | The timestamp when the order was placed.                                   |

---
