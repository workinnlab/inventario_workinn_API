# 🚀 Guía de Deployment - Render + GitHub

## 📋 Requisitos Previos

1. Cuenta en [GitHub](https://github.com)
2. Cuenta en [Render](https://render.com)
3. Proyecto en [Supabase](https://supabase.com)

---

## 🎯 Paso a Paso

### **Paso 1: Subir a GitHub**

#### 1.1 Inicializar repositorio

```bash
cd "/home/eddy/Proyectos Python/Inventario_CIE"
git init
```

#### 1.2 Agregar archivos

```bash
git add .
git commit -m "Initial commit - Inventario CIE API"
```

#### 1.3 Crear repositorio en GitHub

1. Ve a https://github.com/new
2. Nombre: `inventario-cie-api`
3. Privado: ✅ (recomendado)
4. Click **"Create repository"**

#### 1.4 Subir a GitHub

```bash
# Copia el comando que te da GitHub
git remote add origin https://github.com/TU_USUARIO/inventario-cie-api.git
git branch -M main
git push -u origin main
```

---

### **Paso 2: Configurar Render**

#### 2.1 Crear nuevo servicio

1. Ve a https://render.com/dashboard
2. Click **"New +"** > **"Blueprint"**
3. Conecta tu cuenta de GitHub
4. Selecciona el repositorio `inventario-cie-api`

#### 2.2 Configurar variables de entorno

En Render, ve a **Environment** y agrega:

```env
# Supabase
SUPABASE_URL=https://tu_proyecto.supabase.co
SUPABASE_KEY=tu_anon_key
SUPABASE_SERVICE_KEY=tu_service_role_key

# JWT
JWT_SECRET_KEY=genera_uno_nuevo_con_openssl
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# App
APP_NAME=Inventario CIE API
DEBUG=false

# CORS (opcional)
ALLOWED_ORIGINS=https://tu-frontend.com
```

#### 2.3 Desplegar

1. Click **"Apply"**
2. Render comenzará el build
3. Espera ~5 minutos
4. ¡Listo! Tu API estará en: `https://inventario-cie-api.onrender.com`

---

### **Paso 3: Verificar Deployment**

#### 3.1 Health check

```bash
curl https://inventario-cie-api.onrender.com/health
```

Debería responder:
```json
{"status": "healthy"}
```

#### 3.2 Swagger UI

Abre: `https://inventario-cie-api.onrender.com/docs`

#### 3.3 Probar login

```bash
curl -X POST https://inventario-cie-api.onrender.com/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@cie.com",
    "password": "Admin123!"
  }'
```

---

## 🔧 Configuración de Supabase para Producción

### 1. Habilitar Email Confirmation (Opcional)

En Supabase Dashboard > Authentication > Settings:
- ✅ Enable email confirmations

### 2. Configurar CORS en Supabase

En Supabase Dashboard > Settings > API:
- Agrega tu URL de Render a **"Site URL"**
- Agrega a **"Redirect URLs"**:
  ```
  https://inventario-cie-api.onrender.com/auth/v1/callback
  ```

### 3. Actualizar RLS Policies

Asegúrate que las políticas RLS permitan acceso desde la API:

```sql
-- Ver políticas actuales
SELECT * FROM pg_policies WHERE tablename = 'perfiles';
```

---

## 📊 Monitoreo y Logs

### Ver logs en Render

1. Ve a Render Dashboard
2. Click en tu servicio
3. Pestaña **"Logs"**

### Logs en tiempo real

```bash
# Usando Render CLI
render logs -f inventario-cie-api
```

---

## 🔄 Actualizar el Deployment

### Hacer push de cambios

```bash
# Después de hacer cambios
git add .
git commit -m "Descripción del cambio"
git push origin main
```

Render detectará los cambios y redeplegará automáticamente.

---

## ⚠️ Solución de Problemas

### Error: Build falla

**Causa:** Dependencias faltantes

**Solución:**
```bash
pip freeze > requirements.txt
git push
```

### Error: Timeout en health check

**Causa:** La API tarda en iniciar

**Solución:**
- En Render, aumenta el **Health Check Path** timeout
- O usa un plan más alto

### Error: CORS

**Causa:** Orígenes no configurados

**Solución:**
```env
ALLOWED_ORIGINS=https://tu-frontend.com,https://otro-dominio.com
```

### Error: Database connection

**Causa:** Credenciales de Supabase incorrectas

**Solución:**
- Verifica las variables de entorno en Render
- Asegúrate que Supabase esté activo

---

## 💰 Costos Estimados

| Servicio | Plan | Costo |
|----------|------|-------|
| **Render** | Starter | $7/mes |
| **Supabase** | Free | $0/mes |
| **GitHub** | Free | $0/mes |
| **Total** | | **$7/mes** |

---

## 🎯 Checklist Final

- [ ] Código subido a GitHub
- [ ] Repositorio conectado a Render
- [ ] Variables de entorno configuradas
- [ ] Supabase CORS actualizado
- [ ] Health check pasa
- [ ] Swagger UI accesible
- [ ] Login funciona
- [ ] Logs verificados

---

## 📚 Recursos Adicionales

- [Render Docs](https://render.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Supabase Production](https://supabase.com/docs/guides/platform/going-into-prod)

---

**¡Tu API está en producción! 🎉**
