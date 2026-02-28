# ✅ Task Secure API (FastAPI)

Backend seguro estilo portafolio: Auth + JWT + RBAC + CRUD de tareas con PostgreSQL.

## 🚀 Stack
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic (migraciones)
- JWT (python-jose)
- bcrypt (passlib)

## 🔐 Features
- Registro/Login
- JWT protegido
- Endpoint /me
- CRUD de tasks
- Permisos:
  - user: solo sus tareas
  - admin: puede ver todo

## ▶️ Run
1) Levantar DB
```bash
docker compose up -d