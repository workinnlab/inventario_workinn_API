# 🚀 Inicio Rápido - Inventario CIE API

## ✅ API Ya está corriendo

**Swagger UI:** http://localhost:8000/docs

---

## 🔐 PASO 1: Configurar Autenticación en Supabase

### Ejecutar SQL en Supabase

1. Abre tu proyecto en Supabase: https://supabase.com/dashboard
2. Ve a **SQL Editor**
3. Copia y pega el contenido de `insumo/auth_setup.sql`
4. Ejecuta el script

Esto creará:
- Tabla `perfiles` vinculada a `auth.users`
- Trigger para crear perfil automáticamente
- Políticas RLS básicas

---

## 👤 PASO 2: Crear Usuario Admin

### Opción A: Desde Swagger UI (Recomendado)

1. Abre http://localhost:8000/docs
2. Busca **POST /api/v1/auth/register**
3. Click en "Try it out"
4. Ingresa este JSON:
   ```json
   {
     "email": "admin@cie.com",
     "password": "Admin123!",
     "nombre": "Administrador CIE",
     "rol": "admin"
   }
   ```
5. Click "Execute"
6. Deberías recibir:
   ```json
   {
     "id": "uuid...",
     "email": "admin@cie.com",
     "nombre": "Administrador CIE",
     "rol": "admin",
     "activo": true
   }
   ```

### Opción B: Desde terminal

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@cie.com",
    "password": "Admin123!",
    "nombre": "Administrador CIE",
    "rol": "admin"
  }'
```

---

## 🔑 PASO 3: Iniciar Sesión

### Desde Swagger UI

1. Busca **POST /api/v1/auth/login**
2. Click "Try it out"
3. Ingresa:
   ```json
   {
     "email": "admin@cie.com",
     "password": "Admin123!"
   }
   ```
4. Click "Execute"
5. Copia el `access_token` de la respuesta

### Desde terminal

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@cie.com",
    "password": "Admin123!"
  }'
```

---

## 🔓 PASO 4: Autorizar en Swagger

1. En Swagger UI, click en el botón **"Authorize"** (arriba a la derecha)
2. En "Value", pega el token así:
   ```
   Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```
3. Click "Authorize"
4. ¡Listo! Ahora puedes probar endpoints protegidos

---

## 📊 Endpoints Principales

### Inventario
- `GET /api/v1/equipos` - Listar equipos
- `POST /api/v1/equipos` - Crear equipo (requiere auth)
- `GET /api/v1/electronica` - Listar electrónica
- `GET /api/v1/robots` - Listar robots
- `GET /api/v1/materiales` - Listar materiales

### Préstamos
- `GET /api/v1/prestatarios` - Listar prestatarios
- `POST /api/v1/prestamos` - Crear préstamo (requiere auth)

### Movimientos
- `GET /api/v1/movimientos` - Historial de movimientos

### Auth
- `GET /api/v1/auth/me` - Usuario actual (requiere auth)

---

## 🛠️ Comandos Útiles

### Reiniciar la API

```bash
pkill -f uvicorn
cd "/home/eddy/Proyectos Python/Inventario_CIE"
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Ver logs

```bash
# Si está corriendo en background
tail -f /tmp/uvicorn.log
```

### Verificar que corre

```bash
curl http://localhost:8000/
```

---

## 📝 Credenciales de Ejemplo

| Rol | Email | Contraseña |
|-----|-------|------------|
| Admin | admin@cie.com | Admin123! |
| Inventory | inventory@cie.com | Inventory123! |
| Viewer | viewer@cie.com | Viewer123! |

**Nota:** Debes crear cada usuario con el endpoint `/register`

---

## ⚠️ Solución de Problemas

### Error: "Database error saving new user"

**Causa:** Falta ejecutar el script SQL en Supabase

**Solución:**
1. Ejecuta `insumo/auth_setup.sql` en Supabase SQL Editor
2. Intenta registrar de nuevo

### Error: "Token inválido o expirado"

**Causa:** El token expiró (dura 1 hora)

**Solución:**
1. Haz login de nuevo
2. Copia el nuevo token
3. Vuelve a autorizar en Swagger

### La API no inicia

**Causa:** Puerto 8000 ocupado

**Solución:**
```bash
pkill -f uvicorn
sleep 2
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📚 Más Información

- [Análisis del Proyecto](docs/ANALISIS_PROYECTO.md)
- [Guía de Autenticación](docs/AUTENTICACION.md)

---

**¡Listo! Tu API está funcionando** 🎉
