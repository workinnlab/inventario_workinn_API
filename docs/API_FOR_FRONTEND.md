# 📖 API Documentation - Inventario CIE

**Base URL:** `https://inventario-workinn-api.onrender.com/api/v1`  
**Swagger UI:** https://inventario-workinn-api.onrender.com/docs  
**Versión:** 1.0.0

---

## 🔐 Autenticación

La API usa **JWT Bearer Token** de Supabase Auth.

### **Obtener Token (Login)**

```http
POST /auth/login
Content-Type: application/json

{
  "email": "admin@cie.com",
  "password": "Admin123!"
}
```

**Respuesta Exitosa (200):**
```json
{
  "access_token": "eyJhbGciOiJFUzI1NiIs...",
  "refresh_token": "xd3aeqvscjia",
  "token_type": "bearer",
  "user": {
    "id": "536396ca-2c21-493f-9de5-b1bece9d3a88",
    "email": "admin@cie.com",
    "nombre": "Administrador CIE",
    "rol": "admin",
    "activo": true
  }
}
```

### **Usar Token en Requests**

```http
Authorization: Bearer eyJhbGciOiJFUzI1NiIs...
```

---

## 📦 Equipos

### Listar Equipos

```http
GET /equipos?skip=0&limit=100
Authorization: Bearer {token}
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "nombre": "Portatil",
    "marca": "Lenovo Tinbook 16 G6 IRL",
    "codigo": "PC-01",
    "accesorios": "Cargador",
    "serial": "PW0CC8X4",
    "estado": "disponible",
    "created_at": "2026-03-05T19:58:16.891368Z",
    "updated_at": "2026-03-05T19:58:16.891368Z"
  }
]
```

### Obtener Equipo por ID

```http
GET /equipos/{id}
Authorization: Bearer {token}
```

### Obtener Equipo por Código

```http
GET /equipos/codigo/{codigo}
Authorization: Bearer {token}
```

### Crear Equipo

```http
POST /equipos
Authorization: Bearer {token}
Content-Type: application/json

{
  "nombre": "Laptop Dell",
  "marca": "Dell",
  "codigo": "PC-100",
  "accesorios": "Cargador, Mouse",
  "serial": "ABC123",
  "estado": "disponible"
}
```

### Actualizar Equipo

```http
PUT /equipos/{id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "nombre": "Laptop Dell Actualizada",
  "estado": "en uso"
}
```

### Eliminar Equipo

```http
DELETE /equipos/{id}
Authorization: Bearer {token}
```

---

## 🔌 Electrónica

### Listar Electrónica

```http
GET /electronica?skip=0&limit=100
Authorization: Bearer {token}
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "nombre": "Cargador Steren AA y AAA",
    "descripcion": null,
    "tipo": null,
    "en_uso": 0,
    "en_stock": 5,
    "total": 5,
    "created_at": "2026-03-05T19:58:16.891368Z",
    "updated_at": "2026-03-05T19:58:16.891368Z"
  }
]
```

### Crear Electrónica

```http
POST /electronica
Authorization: Bearer {token}
Content-Type: application/json

{
  "nombre": "Arduino Uno R3",
  "descripcion": "Microcontrolador",
  "tipo": "Microcontroladores",
  "en_uso": 0,
  "en_stock": 10
}
```

### Actualizar Electrónica

```http
PUT /electronica/{id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "en_stock": 15
}
```

### Eliminar Electrónica

```http
DELETE /electronica/{id}
Authorization: Bearer {token}
```

---

## 🤖 Robots

### Listar Robots

```http
GET /robots?skip=0&limit=100
Authorization: Bearer {token}
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "nombre": "Araña Robotica Acebott",
    "fuera_de_servicio": 1,
    "en_uso": 0,
    "disponible": 4,
    "total": 5,
    "created_at": "2026-03-05T19:58:16.891368Z",
    "updated_at": "2026-03-05T19:58:16.891368Z"
  }
]
```

### Crear Robot

```http
POST /robots
Authorization: Bearer {token}
Content-Type: application/json

{
  "nombre": "Carro Acebott",
  "fuera_de_servicio": 0,
  "en_uso": 0,
  "disponible": 5
}
```

### Actualizar Robot

```http
PUT /robots/{id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "disponible": 3,
  "en_uso": 2
}
```

### Eliminar Robot

```http
DELETE /robots/{id}
Authorization: Bearer {token}
```

---

## 🧪 Materiales

### Listar Materiales

```http
GET /materiales?skip=0&limit=100
Authorization: Bearer {token}
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "color": "Natural",
    "tipo_id": 1,
    "cantidad": "1KG",
    "categoria": "Filamento",
    "usado": 1,
    "en_uso": 0,
    "en_stock": 1,
    "total": 2,
    "created_at": "2026-03-05T19:58:16.891368Z",
    "updated_at": "2026-03-05T19:58:16.891368Z"
  }
]
```

### Listar Tipos de Materiales

```http
GET /tipos-materiales
Authorization: Bearer {token}
```

### Crear Material

```http
POST /materiales
Authorization: Bearer {token}
Content-Type: application/json

{
  "color": "Rojo",
  "tipo_id": 1,
  "cantidad": "1KG",
  "categoria": "Filamento",
  "usado": 0,
  "en_uso": 0,
  "en_stock": 5
}
```

### Actualizar Material

```http
PUT /materiales/{id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "en_stock": 10
}
```

### Eliminar Material

```http
DELETE /materiales/{id}
Authorization: Bearer {token}
```

---

## 👥 Prestatarios

### Listar Prestatarios

```http
GET /prestatarios?skip=0&limit=100&activo=true
Authorization: Bearer {token}
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "nombre": "Juan Pérez",
    "telefono": "3001234567",
    "dependencia": "Ingeniería",
    "cedula": "123456789",
    "email": "juan@cie.com",
    "activo": true,
    "created_at": "2026-03-05T19:58:16.891368Z",
    "updated_at": "2026-03-05T19:58:16.891368Z"
  }
]
```

### Crear Prestatario

```http
POST /prestatarios
Authorization: Bearer {token}
Content-Type: application/json

{
  "nombre": "María González",
  "telefono": "3019876543",
  "dependencia": "Investigación",
  "cedula": "987654321",
  "email": "maria@cie.com"
}
```

### Actualizar Prestatario

```http
PUT /prestatarios/{id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "telefono": "3101234567",
  "activo": false
}
```

### Eliminar Prestatario (Inactivar)

```http
DELETE /prestatarios/{id}
Authorization: Bearer {token}
```

---

## 📋 Préstamos

### Listar Préstamos

```http
GET /prestamos?skip=0&limit=100&estado=activo
Authorization: Bearer {token}
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "equipo_id": 1,
    "electronica_id": null,
    "robot_id": null,
    "material_id": null,
    "prestatario_id": 1,
    "fecha_prestamo": "2026-03-05T20:00:00Z",
    "fecha_devolucion": null,
    "fecha_limite": "2026-03-12T20:00:00Z",
    "estado": "activo",
    "observaciones": "Préstamo para proyecto",
    "created_at": "2026-03-05T20:00:00Z",
    "updated_at": "2026-03-05T20:00:00Z"
  }
]
```

### Listar Préstamos Activos

```http
GET /prestamos/activos
Authorization: Bearer {token}
```

### Obtener Préstamo por ID

```http
GET /prestamos/{id}
Authorization: Bearer {token}
```

### Crear Préstamo

```http
POST /prestamos
Authorization: Bearer {token}
Content-Type: application/json

{
  "prestatario_id": 1,
  "equipo_id": 5,
  "fecha_limite": "2026-04-01T23:59:59",
  "observaciones": "Préstamo para proyecto de grado"
}
```

**Nota:** Solo UNO de estos campos: `equipo_id`, `electronica_id`, `robot_id`, `material_id`

### Actualizar Préstamo

```http
PUT /prestamos/{id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "estado": "devuelto",
  "fecha_devolucion": "2026-03-10T15:30:00"
}
```

### Devolver Préstamo

```http
POST /prestamos/{id}/devolver
Authorization: Bearer {token}
```

### Eliminar Préstamo

```http
DELETE /prestamos/{id}
Authorization: Bearer {token}
```

---

## 📊 Movimientos (Auditoría)

### Listar Movimientos

```http
GET /movimientos?skip=0&limit=100&tipo=salida
Authorization: Bearer {token}
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "tipo": "salida",
    "equipo_id": 1,
    "electronica_id": null,
    "robot_id": null,
    "material_id": null,
    "cantidad": 1,
    "prestamo_id": 1,
    "usuario_id": "536396ca-2c21-493f-9de5-b1bece9d3a88",
    "descripcion": "Préstamo a Juan Pérez",
    "ubicacion_anterior": null,
    "ubicacion_nueva": null,
    "created_at": "2026-03-05T20:00:00Z"
  }
]
```

### Obtener Movimiento por ID

```http
GET /movimientos/{id}
Authorization: Bearer {token}
```

### Crear Movimiento

```http
POST /movimientos
Authorization: Bearer {token}
Content-Type: application/json

{
  "tipo": "daño",
  "equipo_id": 3,
  "cantidad": 1,
  "descripcion": "Pantalla rota"
}
```

**Tipos válidos:** `entrada`, `salida`, `devolucion`, `daño`, `ajuste_stock`, `baja`, `transferencia`

---

## 🔑 Autenticación

### Registrar Usuario

```http
POST /auth/register
Content-Type: application/json

{
  "email": "nuevo@cie.com",
  "password": "Password123!",
  "nombre": "Nuevo Usuario",
  "rol": "viewer"
}
```

**Roles válidos:** `admin`, `inventory`, `viewer`

### Iniciar Sesión

```http
POST /auth/login
Content-Type: application/json

{
  "email": "admin@cie.com",
  "password": "Admin123!"
}
```

### Obtener Usuario Actual

```http
GET /auth/me
Authorization: Bearer {token}
```

### Cerrar Sesión

```http
POST /auth/logout
Authorization: Bearer {token}
```

### Renovar Token

```http
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "xd3aeqvscjia"
}
```

---

## ⚠️ Códigos de Error

| Código | Descripción |
|--------|-------------|
| `200` | Éxito |
| `201` | Creado |
| `400` | Bad Request (datos inválidos) |
| `401` | No autorizado (token inválido/expirado) |
| `403` | Prohibido (sin permisos) |
| `404` | No encontrado |
| `500` | Error interno del servidor |

**Ejemplo de Error:**
```json
{
  "detail": "Equipo no encontrado"
}
```

---

## 📝 Notas Importantes

1. **Token Expiración:** El access_token dura 1 hora
2. **Refresh Token:** Úsalo para obtener nuevo access_token sin login
3. **CORS:** La API permite todos los orígenes (*)
4. **Cold Start:** En Render, la primera petición puede tardar ~30 segundos
5. **HTTPS:** Siempre usa HTTPS en producción

---

## 🧪 Ejemplo en JavaScript/TypeScript

```typescript
const API_BASE = 'https://inventario-workinn-api.onrender.com/api/v1';

class InventarioAPI {
  private token: string | null = null;

  async login(email: string, password: string) {
    const response = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    
    const data = await response.json();
    this.token = data.access_token;
    return data;
  }

  async getEquipos(skip = 0, limit = 100) {
    const response = await fetch(
      `${API_BASE}/equipos?skip=${skip}&limit=${limit}`,
      {
        headers: { 'Authorization': `Bearer ${this.token}` }
      }
    );
    return response.json();
  }

  async createEquipo(equipo: any) {
    const response = await fetch(`${API_BASE}/equipos`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.token}`
      },
      body: JSON.stringify(equipo)
    });
    return response.json();
  }
}

// Uso
const api = new InventarioAPI();
await api.login('admin@cie.com', 'Admin123!');
const equipos = await api.getEquipos();
console.log(equipos);
```

---

**Documentación generada para consumo desde frontend**  
**Última actualización:** Marzo 2026
