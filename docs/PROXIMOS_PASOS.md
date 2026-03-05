# 📋 Próximos Pasos - GitHub + Render

## ✅ Lo que ya está listo

- [x] Código limpio y organizado
- [x] Archivos de deployment creados (Dockerfile, render.yaml)
- [x] Git inicializado con primer commit
- [x] Documentación completa

---

## 🚀 PASO 1: Crear Repositorio en GitHub

### 1.1 Ve a GitHub

Abre: https://github.com/new

### 1.2 Crea el repositorio

- **Nombre:** `inventario-cie-api`
- **Descripción:** API REST para gestión de inventario del CIE
- **Privado:** ✅ Sí (recomendado para producción)
- **No marques** "Initialize this repository with a README"

Click **"Create repository"**

### 1.3 Sube tu código

GitHub te mostrará comandos. Ejecuta:

```bash
cd "/home/eddy/Proyectos Python/Inventario_CIE"

# Agrega el remote (reemplaza TU_USUARIO con tu usuario de GitHub)
git remote add origin https://github.com/TU_USUARIO/inventario-cie-api.git

# Sube el código
git push -u origin main
```

**¡Listo!** Tu código está en GitHub.

---

## 🚀 PASO 2: Desplegar en Render

### 2.1 Ve a Render

Abre: https://render.com/dashboard

### 2.2 Crea un nuevo servicio

1. Click **"New +"**
2. Selecciona **"Blueprint"**
3. Click **"Connect account"** para conectar GitHub
4. Busca tu repositorio: `inventario-cie-api`
5. Click **"Connect"**

### 2.3 Configura el servicio

Render detectará automáticamente:
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 2.4 Agrega variables de entorno

Click **"Advanced"** > **"Add Environment Variable"** y agrega:

```
SUPABASE_URL=https://tu_proyecto.supabase.co
SUPABASE_KEY=tu_anon_key_aqui
SUPABASE_SERVICE_KEY=tu_service_role_key_aqui
JWT_SECRET_KEY=genera_con_openssl_rand_base64_32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
APP_NAME=Inventario CIE API
DEBUG=false
ALLOWED_ORIGINS=*
```

### 2.5 Click "Apply"

Render comenzará el build (~3-5 minutos).

---

## 🎯 PASO 3: Verificar Deployment

### 3.1 Health Check

Abre en tu navegador:
```
https://inventario-cie-api.onrender.com/health
```

Deberías ver:
```json
{"status": "healthy"}
```

### 3.2 Swagger UI

```
https://inventario-cie-api.onrender.com/docs
```

### 3.3 Prueba el login

```bash
curl -X POST https://inventario-cie-api.onrender.com/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@cie.com", "password": "Admin123!"}'
```

---

## 🔧 PASO 4: Actualizar Supabase CORS

### 4.1 Ve a Supabase Dashboard

https://supabase.com/dashboard/project/tu_proyecto

### 4.2 Configura CORS

1. **Settings** > **API**
2. En **"Site URL"** agrega:
   ```
   https://inventario-cie-api.onrender.com
   ```
3. En **"Redirect URLs"** agrega:
   ```
   https://inventario-cie-api.onrender.com/auth/v1/callback
   ```
4. Click **"Save"**

---

## 📊 PASO 5: Monitoreo

### Ver logs en Render

1. Dashboard > Tu servicio > **"Logs"**
2. Verás logs en tiempo real

### Comandos útiles

```bash
# Ver estado del deployment
curl https://inventario-cie-api.onrender.com/health

# Ver logs (Render CLI)
render logs -f inventario-cie-api
```

---

## 🔄 Actualizar tu API

### Hacer cambios

```bash
# 1. Haz tus cambios en el código
# 2. Prueba localmente

# 3. Commit
git add .
git commit -m "Descripción del cambio"

# 4. Push a GitHub
git push origin main
```

### Deploy automático

Render detectará el push y redeplegará automáticamente en ~3 minutos.

---

## 💰 Costos

| Servicio | Plan | Costo |
|----------|------|-------|
| **Render** | Starter | $7/mes |
| **Supabase** | Free Tier | $0/mes (hasta 500MB) |
| **GitHub** | Free | $0/mes |
| **Total** | | **$7/mes** |

---

## ⚠️ Problemas Comunes

### Build falla en Render

**Causa:** `requirements.txt` incompleto

**Solución:**
```bash
pip freeze > requirements.txt
git push
```

### Timeout en health check

**Causa:** Render usa puerto dinámico

**Solución:** Asegúrate que `main.py` use `os.getenv("PORT", 8000)`

### Error de CORS

**Solución:** Agrega `ALLOWED_ORIGINS` en variables de entorno

### Error de autenticación

**Causa:** Credenciales de Supabase incorrectas

**Solución:** Verifica las variables en Render Dashboard

---

## 📚 Recursos

- [Render Docs](https://render.com/docs)
- [GitHub Docs](https://docs.github.com)
- [Supabase Production](https://supabase.com/docs/guides/platform/going-into-prod)

---

## ✅ Checklist Final

- [ ] Repositorio creado en GitHub
- [ ] Código subido con `git push`
- [ ] Servicio creado en Render
- [ ] Variables de entorno configuradas
- [ ] Health check pasa
- [ ] Swagger UI accesible
- [ ] Supabase CORS actualizado
- [ ] Login funciona en producción

---

**¡Tu API está en producción! 🎉**

¿Necesitas ayuda? Revisa [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
