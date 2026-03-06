# 📦 Inventario CIE API

API REST para gestión de inventario del CIE, construida con **FastAPI** y **Supabase**.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/tu-usuario/inventario-cie-api)

---

## 🚀 Inicio Rápido

### 1. Activar entorno virtual

```bash
cd "/home/eddy/Proyectos Python/Inventario_CIE"
source venv/bin/activate
```

### 2. Iniciar la API

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Abrir Swagger UI

http://localhost:8000/docs

---

## 🔐 Credenciales de Admin

| Campo | Valor |
|-------|-------|
| **Email** | `admin@cie.com` |
| **Password** | `Admin123!` |

---

## 📁 Estructura del Proyecto

```
Inventario_CIE/
├── app/
│   ├── main.py                      # Punto de entrada
│   ├── core/
│   │   ├── config.py                # Configuración
│   │   ├── supabase_client.py       # Cliente Supabase
│   │   └── auth.py                  # Autenticación
│   ├── api/v1/endpoints/
│   │   ├── auth.py                  # Login, register
│   │   ├── inventory.py             # CRUD inventario
│   │   ├── prestamos.py             # Préstamos
│   │   └── movimientos.py           # Auditoría
│   ├── models/
│   │   └── inventory.py             # Modelos (referencia)
│   ├── schemas/
│   │   ├── auth.py                  # Schemas auth
│   │   └── inventory.py             # Schemas CRUD
│   └── services/
│       └── supabase_service.py      # Lógica de negocio
├── docs/
│   ├── ENDPOINTS.md                 # Lista de endpoints
│   └── INICIO_RAPIDO.md             # Guía completa
├── insumo/
│   ├── Inventario.xlsx              # Datos originales
│   ├── schema_supabase.sql          # Schema de la BD
│   └── auth_setup.sql               # Config de autenticación
├── .env                             # Variables de entorno
├── requirements.txt                 # Dependencias
└── README.md                        # Este archivo
```

---

## 📊 Endpoints Principales

### Autenticación (`/api/v1/auth`)
- `POST /register` - Registrar usuario
- `POST /login` - Iniciar sesión
- `GET /me` - Usuario actual

### Inventario (`/api/v1`)
- `GET /equipos` - Listar equipos
- `POST /equipos` - Crear equipo
- `GET /electronica` - Listar electrónica
- `GET /robots` - Listar robots
- `GET /materiales` - Listar materiales

### Préstamos (`/api/v1`)
- `GET /prestamos` - Listar préstamos
- `POST /prestamos` - Crear préstamo
- `POST /prestamos/{id}/devolver` - Devolver

### Movimientos (`/api/v1`)
- `GET /movimientos` - Historial

**Ver lista completa:** http://localhost:8000/docs

---

## 🛠️ Instalación

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno (.env)
# SUPABASE_URL, SUPABASE_KEY, etc.

# Iniciar
uvicorn app.main:app --reload
```

---

## 📚 Documentación

| Archivo | Descripción |
|---------|-------------|
| [`docs/API_FOR_FRONTEND.md`](docs/API_FOR_FRONTEND.md) | **API completa para frontend** |
| [`docs/FRONTEND_RECOMMENDATION.md`](docs/FRONTEND_RECOMMENDATION.md) | **Recomendación de frontend** |
| [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) | Guía de deployment |
| [`docs/PROXIMOS_PASOS.md`](docs/PROXIMOS_PASOS.md) | Paso a paso rápido |
| [`docs/ENDPOINTS.md`](docs/ENDPOINTS.md) | Lista de endpoints |
| [`docs/INICIO_RAPIDO.md`](docs/INICIO_RAPIDO.md) | Inicio rápido |

---

## 🔧 Configuración (.env)

```env
SUPABASE_URL=https://tu_proyecto.supabase.co
SUPABASE_KEY=tu_anon_key
SUPABASE_SERVICE_KEY=tu_service_role_key

JWT_SECRET_KEY=tu_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

APP_NAME=Inventario CIE API
DEBUG=true

# Para producción
ALLOWED_ORIGINS=https://tu-frontend.com
```

---

## 🚀 Deployment

### Deploy a Render

1. Haz click en el botón **"Deploy to Render"** arriba
2. Conecta tu cuenta de GitHub
3. Configura las variables de entorno
4. ¡Listo!

**Ver guía completa:** [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

### Deploy manual

```bash
# Subir a GitHub
git init
git add .
git commit -m "Initial commit"
git push origin main

# Luego en Render: New + > Blueprint > Conectar repo
```

---

## 📝 Notas

- **Base de datos:** Supabase (PostgreSQL)
- **Autenticación:** Supabase Auth con JWT
- **Roles:** admin, inventory, viewer
- **Estado:** ✅ Producción (MVP)

---

**Hecho por: Eddy**
