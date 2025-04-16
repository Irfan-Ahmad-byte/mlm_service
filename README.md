# 🧩 MLM Microservice

A sophisticated and production-ready Multi-Level Marketing (MLM) microservice built using **FastAPI**, **PostgreSQL**, and **Redis**. It manages user network hierarchies, spillover logic, bonus calculations, rank evaluations, and reporting — designed to integrate into larger microservices architectures.

---

## 🚀 Features

### ✅ MLM Tree Management
- Register users with `parent_id`
- Forced matrix support via **MAX_CHILDREN spillover logic**
- Automatically assigns `level` in the network
- Fetch user downlines

### 💸 Bonus System
- Referral-based bonus distribution (direct & indirect)
- Configurable per-level bonus amounts
- Trigger-based logic (referral, purchase, etc.)
- Bonus status management (pending, paid)
- Bonus history for each user

### 🎖 Rank Evaluation
- Dynamic rank assignment (e.g., Bronze, Silver, Gold)
- Based on downline size or custom rules

### 📅 Weekly Reports
- Get last 7-day earnings for a user
- Used for payouts or user analytics

### ⚡ Redis Caching
- Caches user data and downlines
- Speeds up network queries and reduces DB load

---

## 📦 Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (SQLAlchemy + Alembic)
- **Cache**: Redis
- **Containerization**: Docker
- **Testing**: Manual seed script via `test_data.py`

---


## 🔐 Environment Variables

Set ENV VARS according to the `.env.example` file given in the `app/configs` directory.

## 🧪 Running Test Data Seeder

```bash
python test_data.py
```

This will:
- Create a root MLM user
- Add multiple children
- Trigger referral bonuses

---

## 🛠️ Bonus Configuration

```python
MAX_CHILDREN = 3

BONUS_MAP = {
    1: 10.0,  # Direct
    2: 5.0,
    3: 2.0,
    4: 1.0
}

RANKS = [
    ("Bronze", 3),
    ("Silver", 10),
    ("Gold", 25),
    ("Diamond", 50)
]
```

---

## 📬 API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| `POST` | `/mlm/register` | Add user to MLM tree |
| `GET`  | `/mlm/downline/{user_id}` | Get user’s direct downlines |
| `POST` | `/mlm/bonus` | Trigger bonus distribution |
| `GET`  | `/mlm/bonus/user/{user_id}` | Get user bonus history |
| `GET`  | `/mlm/bonus?status=pending` | Admin: list bonuses |
| `PATCH`| `/mlm/bonus/{id}/mark-paid` | Admin: mark bonus paid |
| `POST` | `/mlm/rank/evaluate/{user_id}` | Evaluate and assign rank |
| `GET`  | `/mlm/report/weekly/{user_id}` | Weekly report of earnings |

---

## 🧠 Author

**Irfan Ahmad** – Backend Engineer  
📧 [Contact](mailto:irfan.ahmad.mlka@gmail.com) | 🔗 [GitHub](https://github.com/Irfan-Ahmad-byte)

---

## 📌 Notes

This microservice is designed to work with an external **[Authentication Service](https://github.com/irfan-ahmad-byte/jwt_authentication_service.git)** for user registration and login. The `user_id` is assumed to be passed in from that service.

This microservice has also been integrated into an **[MLM Gateway](https://github.com/irfan-ahmad-byte/mlm_demo.git)** along with the **[Authentication Service](https://github.com/irfan-ahmad-byte/jwt_authentication_service.git)**
---

## 🦀 Rust Version

A Rust implementation of the same MLM logic, built for ultra-performance using Actix, SeaORM, and Redis, also exists [here](https://github.com/irfan-ahmad-byte/mlm_service_rust.git)