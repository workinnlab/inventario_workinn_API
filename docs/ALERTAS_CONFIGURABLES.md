# 🔔 SISTEMA DE ALERTAS CONFIGURABLES - Inventario CIE

**Fecha:** Marzo 2026  
**Estado:** ✅ Implementado - Fase 1 (Configuración Global)

---

## 📋 **ÍNDICE**

1. [Problema que Resuelve](#problema-que-resuelve)
2. [Solución Implementada](#solución-implementada)
3. [Configuraciones Disponibles](#configuraciones-disponibles)
4. [Cómo Usar](#cómo-usar)
5. [Ejemplos para el Frontend](#ejemplos-para-el-frontend)
6. [Próximas Fases](#próximas-fases)

---

## 🤔 **PROBLEMA QUE RESUELVE**

### **Antes:**

```typescript
// Hardcodeado en el frontend
const stockBajo = await materialService.getStockMinimo(5); // ¿Por qué 5?
const porVencer = await prestamoService.getPorVencer(7); // ¿Por qué 7 días?
```

**Problemas:**
1. ❌ ¿Quién decide que 5 es "stock bajo"?
2. ❌ ¿Qué pasa si algunos materiales deben alertar a los 10 y otros a los 3?
3. ❌ ¿Qué pasa si quieren alertas a 14 días en vez de 7?
4. ❌ ¿Cada usuario tiene diferentes preferencias?

---

## ✅ **SOLUCIÓN IMPLEMENTADA**

### **Tabla de Configuración Global**

```sql
create table configuracion_alertas (
  id bigint primary key,
  clave text unique not null,
  valor int not null,
  descripcion text,
  updated_at timestamptz default now()
);
```

**Ventajas:**
- ✅ El admin puede cambiar umbrales sin tocar código
- ✅ Valores por defecto razonables
- ✅ Fácil de implementar
- ✅ Suficiente para empezar

---

## ⚙️ **CONFIGURACIONES DISPONIBLES**

| Clave | Valor Default | Descripción |
|-------|---------------|-------------|
| `stock_minimo_default` | 5 | Stock mínimo por defecto para materiales |
| `prestamo_por_vencer_dias` | 7 | Días para alerta de préstamo por vencer |
| `prestamo_limite_dias` | 30 | Límite de días para préstamo |
| `prestamos_maximos_por_usuario` | 5 | Máximo préstamos activos por usuario |
| `alertar_stock_bajo` | 1 | Activar/desactivar alertas de stock bajo (1=sí, 0=no) |
| `alertar_prestamos_vencidos` | 1 | Activar/desactivar alertas de préstamos vencidos |
| `alertar_equipos_danados` | 1 | Activar/desactivar alertas de equipos dañados |

---

## 🛠️ **CÓMO USAR**

### **1. Ejecutar SQL en Supabase**

```bash
# En Supabase Dashboard > SQL Editor
# Ejecutar: insumo/configuracion_alertas.sql
```

### **2. Ver Configuración Actual**

```bash
curl https://inventario-workinn-api.onrender.com/api/v1/configuracion/alertas
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "clave": "stock_minimo_default",
    "valor": 5,
    "descripcion": "Stock mínimo por defecto para materiales"
  },
  {
    "id": 2,
    "clave": "prestamo_por_vencer_dias",
    "valor": 7,
    "descripcion": "Días para alerta de préstamo por vencer"
  }
]
```

### **3. Actualizar Configuración**

```bash
# Cambiar stock mínimo de 5 a 10
curl -X PUT https://inventario-workinn-api.onrender.com/api/v1/configuracion/alertas/stock_minimo_default \
  -H "Authorization: Bearer TU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"valor": 10}'
```

### **4. Usar en Alertas**

```bash
# Ahora las alertas usarán el nuevo valor
curl https://inventario-workinn-api.onrender.com/api/v1/materiales/stock-minimo
# Usará stock_minimo_default = 10 en vez de 5
```

---

## 💻 **EJEMPLOS PARA EL FRONTEND**

### **Servicio de Configuración**

```typescript
// src/services/configuracion.ts
import api from './api';

export interface ConfiguracionAlerta {
  id: number;
  clave: string;
  valor: number;
  descripcion?: string;
}

export const configuracionService = {
  // Obtener todas las configuraciones
  async getAll(): Promise<ConfiguracionAlerta[]> {
    const response = await api.get('/configuracion/alertas');
    return response.data;
  },

  // Obtener configuración específica
  async getByClave(clave: string): Promise<ConfiguracionAlerta> {
    const response = await api.get(`/configuracion/alertas/${clave}`);
    return response.data;
  },

  // Actualizar configuración
  async update(clave: string, valor: number): Promise<ConfiguracionAlerta> {
    const response = await api.put(`/configuracion/alertas/${clave}`, { valor });
    return response.data;
  },

  // Obtener valor numérico directamente
  async getValor(clave: string): Promise<number> {
    const config = await this.getByClave(clave);
    return config.valor;
  },
};
```

### **Servicio de Materiales Actualizado**

```typescript
// src/services/materiales.ts
import api from './api';
import { configuracionService } from './configuracion';

export const materialService = {
  // Obtener materiales con stock bajo
  async getStockBajo(minimo?: number): Promise<Material[]> {
    // Si no se proporciona minimo, usar configuración global
    if (minimo === undefined) {
      const config = await configuracionService.getValor('stock_minimo_default');
      minimo = config;
    }
    
    const response = await api.get(`/materiales/stock-minimo?minimo=${minimo}`);
    return response.data;
  },
};
```

### **Servicio de Préstamos Actualizado**

```typescript
// src/services/prestamos.ts
import api from './api';
import { configuracionService } from './configuracion';

export const prestamoService = {
  // Obtener préstamos por vencer
  async getPorVencer(dias?: number): Promise<Prestamo[]> {
    // Si no se proporciona dias, usar configuración global
    if (dias === undefined) {
      const config = await configuracionService.getValor('prestamo_por_vencer_dias');
      dias = config;
    }
    
    const response = await api.get(`/prestamos/por-vencer?dias=${dias}`);
    return response.data;
  },
};
```

### **Componente de Alertas Inteligente**

```tsx
// src/components/AlertasInteligentes.tsx
import { useEffect, useState } from 'react';
import { materialService } from '../services/materiales';
import { prestamoService } from '../services/prestamos';
import { configuracionService } from '../services/configuracion';

export function AlertasInteligentes() {
  const [stockBajo, setStockBajo] = useState([]);
  const [porVencer, setPorVencer] = useState([]);
  const [configuracion, setConfiguracion] = useState(null);

  useEffect(() => {
    async function loadAlertas() {
      // Obtener configuración
      const stockMinimo = await configuracionService.getValor('stock_minimo_default');
      const diasPorVencer = await configuracionService.getValor('prestamo_por_vencer_dias');
      
      setConfiguracion({
        stockMinimo,
        diasPorVencer
      });

      // Obtener alertas con configuración
      const stockBajoData = await materialService.getStockBajo(); // Usa configuración
      setStockBajo(stockBajoData);

      const porVencerData = await prestamoService.getPorVencer(); // Usa configuración
      setPorVencer(porVencerData);
    }

    loadAlertas();
  }, []);

  if (!configuracion) return <div>Cargando...</div>;

  return (
    <div className="alertas">
      {/* Alerta de Stock Bajo */}
      {stockBajo.length > 0 && (
        <div className="alert alert-warning">
          <h3>⚠️ Stock Bajo ({stockBajo.length} materiales)</h3>
          <p>Umbral configurado: {configuracion.stockMinimo} unidades</p>
          <ul>
            {stockBajo.map((m: any) => (
              <li key={m.id}>
                {m.color} - {m.cantidad} - Stock: {m.en_stock}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Alerta de Préstamos por Vencer */}
      {porVencer.length > 0 && (
        <div className="alert alert-warning">
          <h3>🟡 Préstamos por Vencer ({porVencer.length})</h3>
          <p>Umbral configurado: {configuracion.diasPorVencer} días</p>
          <ul>
            {porVencer.map((p: any) => (
              <li key={p.id}>
                Préstamo #{p.id} - Vence: {new Date(p.fecha_limite).toLocaleDateString()}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
```

### **Página de Configuración de Alertas**

```tsx
// src/pages/ConfiguracionAlertas.tsx
import { useEffect, useState } from 'react';
import { configuracionService, ConfiguracionAlerta } from '../services/configuracion';

export function ConfiguracionAlertas() {
  const [configuraciones, setConfiguraciones] = useState<ConfiguracionAlerta[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadConfig() {
      const data = await configuracionService.getAll();
      setConfiguraciones(data);
      setLoading(false);
    }

    loadConfig();
  }, []);

  const handleUpdate = async (clave: string, nuevoValor: number) => {
    try {
      await configuracionService.update(clave, nuevoValor);
      alert('Configuración actualizada');
      
      // Recargar
      const data = await configuracionService.getAll();
      setConfiguraciones(data);
    } catch (err: any) {
      alert('Error al actualizar: ' + err.response?.data?.detail);
    }
  };

  if (loading) return <div>Cargando...</div>;

  return (
    <div className="configuracion-page">
      <h1>Configuración de Alertas</h1>
      <p>Define los umbrales para las alertas del sistema</p>

      <table>
        <thead>
          <tr>
            <th>Configuración</th>
            <th>Valor Actual</th>
            <th>Descripción</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {configuraciones.map((config) => (
            <tr key={config.id}>
              <td>{config.clave}</td>
              <td>
                <input
                  type="number"
                  defaultValue={config.valor}
                  id={`valor-${config.id}`}
                  className="input-valor"
                />
              </td>
              <td>{config.descripcion}</td>
              <td>
                <button
                  onClick={() => {
                    const input = document.getElementById(`valor-${config.id}`) as HTMLInputElement;
                    handleUpdate(config.clave, Number(input.value));
                  }}
                >
                  Guardar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

---

## 📊 **PRÓXIMAS FASES**

### **Fase 2: Configuración por Material**

```sql
-- Agregar columnas a materiales
alter table materiales add column stock_minimo int default 5;
alter table materiales add column alertar_stock_bajo boolean default true;
```

**Ventaja:** Cada material puede tener su propio umbral.

### **Fase 3: Preferencias por Usuario**

```sql
-- Tabla de preferencias por usuario
create table preferencias_alertas_usuario (
  id bigint primary key,
  usuario_id uuid references auth.users(id),
  clave text not null,
  valor int not null,
  unique(usuario_id, clave)
);
```

**Ventaja:** Cada usuario configura SUS alertas.

---

## 🎯 **RESUMEN**

| Característica | Estado | Descripción |
|----------------|--------|-------------|
| Configuración Global | ✅ Implementada | Admin define umbrales globales |
| Endpoints de Configuración | ✅ Implementados | CRUD de configuraciones |
| Alertas Usan Configuración | ✅ Implementado | Endpoints leen configuración |
| Configuración por Material | ⏳ Pendiente (Fase 2) | Cada material tiene su umbral |
| Preferencias por Usuario | ⏳ Pendiente (Fase 3) | Cada usuario configura las suyas |

---

## 📝 **ENDPOINTS**

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/configuracion/alertas` | Listar configuraciones | ✅ |
| GET | `/configuracion/alertas/{clave}` | Obtener configuración | ✅ |
| PUT | `/configuracion/alertas/{clave}` | Actualizar configuración | ✅ Admin |
| POST | `/configuracion/alertas` | Crear configuración | ✅ Admin |
| GET | `/materiales/stock-minimo?minimo={opcional}` | Stock bajo | ✅ |
| GET | `/prestamos/por-vencer?dias={opcional}` | Por vencer | ✅ |

---

**Fecha:** Marzo 2026  
**Estado:** ✅ Fase 1 Implementada - Lista para Producción
