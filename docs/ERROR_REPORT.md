# 🐛 REPORTE DE ERRORES - Inventario CIE

**Fecha:** Marzo 2026  
**Total Errores:** 15  
**Prioridad:** Crítica

---

## 📊 **RESUMEN**

| Categoría | Cantidad | Prioridad |
|-----------|----------|-----------|
| 🔴 Backend | 5 | Crítica |
| 🟡 Frontend | 10 | Media |

---

## 🔴 **ERRORES DE BACKEND (Prioridad Crítica)**

### **#2: "Dispositivo no encontrado" al actualizar equipos**

**Síntoma:**
- Al editar un equipo, sale error "dispositivo no encontrado"

**Causa Probable:**
- El endpoint PUT `/equipos/{id}` no está encontrando el ID
- Posible problema de RLS o el ID no se está pasando correctamente

**Solución Backend:**
```python
# Verificar que el endpoint recibe el ID correctamente
@router.put("/equipos/{equipo_id}")
def actualizar_equipo(equipo_id: int, equipo: EquipoUpdate, supabase: Client = Depends(get_supabase)):
    print(f"Actualizando equipo ID: {equipo_id}")  # Debug
    # ...
```

**Estado:** ⏳ Pendiente

---

### **#3: Devolución no actualiza estado del equipo**

**Síntoma:**
- Después de devolver un equipo, en la lista de dañados aparece pero al buscarlo sigue como "prestado"

**Causa:**
- El endpoint POST `/prestamos/{id}/devolver` actualiza el estado del préstamo pero NO del equipo

**Solución Backend:**
```python
@router.post("/prestamos/{prestamo_id}/devolver")
def devolver_prestamo(prestamo_id: int, supabase: Client = Depends(get_supabase)):
    # ... existing code ...
    
    # Actualizar estado del equipo a 'disponible'
    if prestamo.get('equipo_id'):
        supabase.table("equipos").update({"estado": "disponible"}).eq("id", prestamo['equipo_id']).execute()
```

**Estado:** ✅ Implementado (verificar que funcione)

---

### **#6: Préstamos vencidos no se pueden devolver**

**Síntoma:**
- Si un préstamo está "vencido", no deja marcarlo como devuelto

**Causa:**
- Validación en el endpoint solo permite devolver si está "activo"

**Solución Backend:**
```python
# En devolver_prestamo
if prestamo.estado not in ['activo', 'vencido']:  # Permitir vencidos también
    raise HTTPException(status_code=400, detail="El préstamo no está activo")
```

**Estado:** ⏳ Pendiente

---

### **#8: No deja editar/actualizar/eliminar desde la web**

**Síntoma:**
- Botones de editar/eliminar no funcionan

**Causa:**
- Frontend no está enviando el token
- O endpoints PUT/DELETE están bloqueados por RLS

**Solución:**
```typescript
// Frontend - Asegurar que el token se envía
api.put(`/equipos/${id}`, data); // El interceptor agrega el token
```

**Estado:** ⏳ Pendiente (verificar frontend)

---

### **#9: No se puede editar el estado de los equipos**

**Síntoma:**
- No hay opción para cambiar disponible/dañado/etc.

**Causa:**
- Frontend no tiene el selector de estados
- O el backend no acepta todos los estados

**Solución Backend:**
```sql
-- Agregar estado 'arreglado'
ALTER TABLE equipos DROP CONSTRAINT IF EXISTS equipos_estado_check;
ALTER TABLE equipos ADD CONSTRAINT equipos_estado_check 
CHECK (estado IN ('disponible', 'en uso', 'prestado', 'mantenimiento', 'dañado', 'arreglado'));
```

**Estado:** ✅ SQL creado (`fix_estado_arreglado.sql`)

---

## 🟡 **ERRORES DE FRONTEND (Prioridad Media)**

### **#1: No hay opción "arreglado"**

**Síntoma:**
- No se puede cambiar de "dañado" a "arreglado"

**Solución Frontend:**
```tsx
<select value={estado} onChange={...}>
  <option value="disponible">Disponible</option>
  <option value="dañado">Dañado</option>
  <option value="arreglado">Arreglado</option>  {/* Agregar */}
  {/* ... más estados */}
</select>
```

**Estado:** ⏳ Pendiente Frontend

---

### **#4: Notificaciones no funcionan**

**Síntoma:**
- No muestra todas las notificaciones
- No deja interactuar

**Causa:**
- Frontend no está consumiendo los endpoints de alertas
- O no hay sistema de notificaciones implementado

**Solución Frontend:**
```typescript
// Consumir endpoint de alertas
const alertas = await api.get('/prestamos/por-vencer?dias=7');
// Mostrar en UI
```

**Estado:** ⏳ Pendiente Frontend

---

### **#5: Gráfica de equipos por estado no se actualiza**

**Síntoma:**
- Los números bajan pero la barra sigue igual

**Causa:**
- State management no está refrescando la gráfica
- O la gráfica no se re-renderiza

**Solución Frontend:**
```tsx
// Asegurar que la gráfica se actualice
useEffect(() => {
  loadDashboard(); // Recargar datos
}, [equipos]); // Cuando equipos cambie
```

**Estado:** ⏳ Pendiente Frontend

---

### **#7: Input de números no deja borrar el 0**

**Síntoma:**
- Al borrar todo en un input numérico, queda un 0

**Causa:**
- Input type="number" siempre tiene un valor

**Solución Frontend:**
```tsx
<input
  type="text"  // Cambiar a text
  value={valor}
  onChange={(e) => setValor(e.target.value)}
  pattern="[0-9]*"  // Solo números
/>
```

**Estado:** ⏳ Pendiente Frontend

---

### **#10: Imagen distorsionada al imprimir**

**Síntoma:**
- Al imprimir resumen, imagen se ve mal

**Causa:**
- Asset roto o CSS de impresión

**Solución Frontend:**
```css
@media print {
  img {
    max-width: 100%;
    height: auto;
  }
}
```

**Estado:** ⏳ Pendiente Frontend

---

### **#11: Se cae al actualizar la página**

**Síntoma:**
- Al hacer F5, la app crashea

**Causa:**
- Error de JavaScript
- O ruta no encontrada

**Solución Frontend:**
```tsx
// Revisar consola del navegador
console.error(error);
```

**Estado:** ⏳ Pendiente (debug)

---

### **#12: Exportaciones no actualizan**

**Síntoma:**
- Al exportar, datos viejos

**Causa:**
- Cache o state no refresca

**Solución Frontend:**
```typescript
// Forzar recarga antes de exportar
const data = await api.get('/export/json', { cache: 'no-cache' });
```

**Estado:** ⏳ Pendiente Frontend

---

### **#13: No puede pedir ayuda**

**Síntoma:**
- ¿Botón de ayuda no funciona?

**Causa:**
- No implementado o enlace roto

**Solución:**
```tsx
<a href="mailto:soporte@cie.com">Pedir Ayuda</a>
```

**Estado:** ⏳ Pendiente Frontend

---

### **#14: Modo oscuro se ve mal**

**Síntoma:**
- Colores incorrectos en modo oscuro

**Causa:**
- Variables CSS no definidas

**Solución Frontend:**
```css
.dark {
  --background: #1a1a1a;
  --foreground: #ffffff;
  /* ... más variables */
}
```

**Estado:** ⏳ Pendiente Frontend

---

### **#15: Icono de robots no hace hover**

**Síntoma:**
- Icono no se ilumina al pasar el mouse

**Causa:**
- CSS hover no definido

**Solución Frontend:**
```css
.icon-robot {
  transition: color 0.2s;
}

.icon-robot:hover {
  color: blue;
}
```

**Estado:** ⏳ Pendiente Frontend

---

## 🎯 **PLAN DE ACCIÓN**

### **Semana 1: Backend Crítico**
- [ ] Fix #2: Endpoint PUT /equipos/{id}
- [ ] Fix #3: Verificar que devolución actualiza equipo
- [ ] Fix #6: Permitir devolver vencidos
- [ ] Fix #9: Ejecutar SQL de estado 'arreglado'

### **Semana 2: Frontend Crítico**
- [ ] Fix #8: Verificar tokens en CRUD
- [ ] Fix #1: Agregar estado 'arreglado' en UI
- [ ] Fix #7: Inputs numéricos
- [ ] Fix #11: Debug de crash al actualizar

### **Semana 3: Frontend Medio**
- [ ] Fix #4: Sistema de notificaciones
- [ ] Fix #5: Actualizar gráficas
- [ ] Fix #10: CSS de impresión
- [ ] Fix #12: Cache de exportaciones
- [ ] Fix #14: Modo oscuro
- [ ] Fix #15: Hover de iconos
- [ ] Fix #13: Botón de ayuda

---

## 📝 **COMPROBACIÓN RÁPIDA**

### **Test Backend:**

```bash
# Test #2: Actualizar equipo
curl -X PUT https://inventario-workinn-api.onrender.com/api/v1/equipos/1 \
  -H "Authorization: Bearer TU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"estado": "dañado"}'

# Test #3: Devolver préstamo
curl -X POST https://inventario-workinn-api.onrender.com/api/v1/prestamos/1/devolver \
  -H "Authorization: Bearer TU_TOKEN"

# Test #6: Devolver vencido
# (Crear préstamo, esperar que venza, intentar devolver)
```

---

**Última Actualización:** Marzo 2026  
**Estado:** 🔴 5 Backend Pendientes, 🟡 10 Frontend Pendientes
