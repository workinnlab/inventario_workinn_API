# 📚 Estructura de Endpoints - Inventario CIE API

**Swagger UI:** http://localhost:8000/docs

---

## 🗂️ Organización en Swagger UI

Los endpoints están agrupados por categorías para facilitar la navegación:

### **🔐 Autenticación** (`/api/v1/auth`)

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/register` | Registrar usuario | ❌ |
| POST | `/login` | Iniciar sesión | ❌ |
| POST | `/logout` | Cerrar sesión | ✅ |
| GET | `/me` | Usuario actual | ✅ |
| POST | `/refresh` | Renovar token | ❌ |

---

### **📦 Inventario > Equipos** (`/api/v1/equipos`)

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/` | Listar equipos | ❌ |
| GET | `/{id}` | Obtener equipo | ❌ |
| GET | `/codigo/{codigo}` | Buscar por código | ❌ |
| POST | `/` | Crear equipo | ✅ (admin/inventory) |
| PUT | `/{id}` | Actualizar equipo | ✅ (admin/inventory) |
| DELETE | `/{id}` | Eliminar equipo | ✅ (admin) |

---

### **🔌 Inventario > Electrónica** (`/api/v1/electronica`)

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/` | Listar electrónica | ❌ |
| GET | `/{id}` | Obtener elemento | ❌ |
| POST | `/` | Crear elemento | ✅ (admin/inventory) |
| PUT | `/{id}` | Actualizar elemento | ✅ (admin/inventory) |
| DELETE | `/{id}` | Eliminar elemento | ✅ (admin) |

---

### **🤖 Inventario > Robots** (`/api/v1/robots`)

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/` | Listar robots | ❌ |
| GET | `/{id}` | Obtener robot | ❌ |
| POST | `/` | Crear robot | ✅ (admin/inventory) |
| PUT | `/{id}` | Actualizar robot | ✅ (admin/inventory) |
| DELETE | `/{id}` | Eliminar robot | ✅ (admin) |

---

### **🧪 Inventario > Materiales** (`/api/v1/materiales`)

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/` | Listar materiales | ❌ |
| GET | `/{id}` | Obtener material | ❌ |
| POST | `/` | Crear material | ✅ (admin/inventory) |
| PUT | `/{id}` | Actualizar material | ✅ (admin/inventory) |
| DELETE | `/{id}` | Eliminar material | ✅ (admin) |
| GET | `/tipos-materiales` | Tipos de materiales | ❌ |

---

### **📋 Préstamos > Gestión** (`/api/v1/prestamos`)

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/` | Listar préstamos | ❌ |
| GET | `/activos` | Préstamos activos | ❌ |
| GET | `/{id}` | Obtener préstamo | ❌ |
| POST | `/` | Crear préstamo | ✅ (admin/inventory) |
| PUT | `/{id}` | Actualizar préstamo | ✅ (admin/inventory) |
| POST | `/{id}/devolver` | Devolver préstamo | ✅ (admin/inventory) |
| DELETE | `/{id}` | Eliminar préstamo | ✅ (admin) |

---

### **👥 Préstamos > Prestatarios** (`/api/v1/prestatarios`)

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/` | Listar prestatarios | ❌ |
| GET | `/{id}` | Obtener prestatario | ❌ |
| POST | `/` | Crear prestatario | ✅ (admin/inventory) |
| PUT | `/{id}` | Actualizar prestatario | ✅ (admin/inventory) |
| DELETE | `/{id}` | Inactivar prestatario | ✅ (admin/inventory) |

---

### **📊 Auditoría > Movimientos** (`/api/v1/movimientos`)

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/` | Listar movimientos | ❌ |
| GET | `/{id}` | Obtener movimiento | ❌ |
| POST | `/` | Registrar movimiento | ✅ (admin/inventory) |

---

## 📊 Resumen Total

| Categoría | Endpoints |
|-----------|-----------|
| Autenticación | 5 |
| Inventario > Equipos | 6 |
| Inventario > Electrónica | 5 |
| Inventario > Robots | 5 |
| Inventario > Materiales | 6 |
| Préstamos > Gestión | 7 |
| Préstamos > Prestatarios | 5 |
| Auditoría > Movimientos | 3 |
| **TOTAL** | **42** |

---

## 🔑 Niveles de Autenticación

| Icono | Significado |
|-------|-------------|
| ❌ | Público (no requiere auth) |
| ✅ | Requiere autenticación |

---

## 🎯 Ejemplo de Uso en Swagger

1. **Abre Swagger UI:** http://localhost:8000/docs
2. **Haz login primero:**
   - Ve a `POST /api/v1/auth/login`
   - Ingresa credenciales de admin
   - Copia el `access_token`
3. **Autoriza:**
   - Click en "Authorize" (arriba a la derecha)
   - Pega: `Bearer tu_token`
4. **Prueba endpoints:**
   - Los que tienen 🔒 requieren auth
   - Los verdes son públicos

---

## 📝 Notas

- Los tags con `>` crean subcategorías en Swagger UI
- Esto mejora la organización visual
- Los endpoints públicos están al principio de cada categoría

---

**Documentación generada automáticamente desde la API**
