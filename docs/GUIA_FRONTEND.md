# 📘 GUÍA PARA FRONTEND - Inventario CIE API

**Fecha:** Marzo 2026  
**Versión API:** 1.0.0  
**Base URL:** `https://inventario-workinn-api.onrender.com/api/v1`

---

## 📋 **ÍNDICE**

1. [Configuración Inicial](#configuración-inicial)
2. [Autenticación](#autenticación)
3. [Alertas y Notificaciones](#alertas-y-notificaciones)
4. [Dashboard](#dashboard)
5. [CRUD de Inventario](#crud-de-inventario)
6. [Préstamos](#préstamos)
7. [Exportación y Backup](#exportación-y-backup)
8. [Manejo de Errores](#manejo-de-errores)
9. [Ejemplos de Código](#ejemplos-de-código)

---

## 🔧 **CONFIGURACIÓN INICIAL**

### **Variables de Entorno**

```env
# .env o .env.local
VITE_API_BASE_URL=https://inventario-workinn-api.onrender.com/api/v1
```

### **Configuración de Axios**

```typescript
// src/services/api.ts
import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE_URL;

export const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para manejar errores
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expirado
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
```

---

## 🔐 **AUTENTICACIÓN**

### **Login**

```typescript
// src/services/auth.ts
import api from './api';

export interface LoginRequest {
  email: string;
  password: string;
}

export interface User {
  id: string;
  email: string;
  nombre: string;
  rol: 'admin' | 'inventory' | 'viewer';
  activo: boolean;
}

export const authService = {
  async login(data: LoginRequest) {
    const response = await api.post('/auth/login', data);
    const { access_token, user } = response.data;
    
    localStorage.setItem('token', access_token);
    localStorage.setItem('user', JSON.stringify(user));
    
    return { token: access_token, user };
  },

  async logout() {
    await api.post('/auth/logout');
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },

  async getCurrentUser(): Promise<User> {
    const response = await api.get('/auth/me');
    return response.data;
  },

  getToken(): string | null {
    return localStorage.getItem('token');
  },

  getUser(): User | null {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  },
};
```

### **Ejemplo de Uso en Componente**

```tsx
// src/pages/Login.tsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../services/auth';

export function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await authService.login({ email, password });
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error al iniciar sesión');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
        required
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Contraseña"
        required
      />
      {error && <div className="error">{error}</div>}
      <button type="submit">Iniciar Sesión</button>
    </form>
  );
}
```

---

## 🚨 **ALERTAS Y NOTIFICACIONES**

### **1. Alertas de Préstamos por Vencer**

```typescript
// src/services/prestamos.ts
import api from './api';

export interface Prestamo {
  id: number;
  prestatario_id: number;
  equipo_id?: number;
  fecha_limite: string;
  estado: 'activo' | 'devuelto' | 'vencido';
}

export const prestamoService = {
  // Obtener préstamos por vencer en X días
  async getPorVencer(dias: number = 7): Promise<Prestamo[]> {
    const response = await api.get(`/prestamos/por-vencer?dias=${dias}`);
    return response.data;
  },

  // Obtener préstamos activos
  async getActivos(): Promise<Prestamo[]> {
    const response = await api.get('/prestamos/activos');
    return response.data;
  },
};
```

### **Componente de Alerta**

```tsx
// src/components/AlertasPrestamos.tsx
import { useEffect, useState } from 'react';
import { prestamoService } from '../services/prestamos';

export function AlertasPrestamos() {
  const [porVencer, setPorVencer] = useState([]);
  const [vencidos, setVencidos] = useState([]);

  useEffect(() => {
    async function loadAlertas() {
      // Préstamos por vencer (7 días)
      const porVencerData = await prestamoService.getPorVencer(7);
      setPorVencer(porVencerData);

      // Préstamos vencidos
      const activosData = await prestamoService.getActivos();
      const vencidosData = activosData.filter((p: any) => {
        const fechaLimite = new Date(p.fecha_limite);
        return fechaLimite < new Date();
      });
      setVencidos(vencidosData);
    }

    loadAlertas();
  }, []);

  return (
    <div className="alertas">
      {/* Alerta Roja - Vencidos */}
      {vencidos.length > 0 && (
        <div className="alert alert-danger">
          <h3>🔴 Préstamos Vencidos ({vencidos.length})</h3>
          <ul>
            {vencidos.map((p: any) => (
              <li key={p.id}>
                Préstamo #{p.id} - Venció: {new Date(p.fecha_limite).toLocaleDateString()}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Alerta Amarilla - Por Vencer */}
      {porVencer.length > 0 && (
        <div className="alert alert-warning">
          <h3>🟡 Préstamos por Vencer ({porVencer.length})</h3>
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

---

### **2. Alertas de Stock Mínimo**

```typescript
// src/services/materiales.ts
import api from './api';

export interface Material {
  id: number;
  color: string;
  cantidad: string;
  en_stock: number;
  categoria: 'Filamento' | 'Resina' | 'Otro';
}

export const materialService = {
  // Obtener materiales con stock bajo
  async getStockMinimo(minimo: number = 5): Promise<Material[]> {
    const response = await api.get(`/materiales/stock-minimo?minimo=${minimo}`);
    return response.data;
  },
};
```

### **Componente de Alerta de Stock**

```tsx
// src/components/AlertasStock.tsx
import { useEffect, useState } from 'react';
import { materialService } from '../services/materiales';

export function AlertasStock() {
  const [stockBajo, setStockBajo] = useState([]);

  useEffect(() => {
    async function loadStock() {
      const data = await materialService.getStockMinimo(5);
      setStockBajo(data);
    }

    loadStock();
  }, []);

  return (
    <div className="alertas">
      {stockBajo.length > 0 && (
        <div className="alert alert-warning">
          <h3>⚠️ Stock Bajo ({stockBajo.length} materiales)</h3>
          <table>
            <thead>
              <tr>
                <th>Material</th>
                <th>Categoría</th>
                <th>Stock Actual</th>
              </tr>
            </thead>
            <tbody>
              {stockBajo.map((m: any) => (
                <tr key={m.id}>
                  <td>{m.color} - {m.cantidad}</td>
                  <td>{m.categoria}</td>
                  <td className="stock-bajo">{m.en_stock}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <button onClick={() => window.location.href = '/materiales'}>
            Ver todos los materiales
          </button>
        </div>
      )}
    </div>
  );
}
```

---

### **3. Alertas de Equipos Dañados**

```typescript
// src/services/equipos.ts
import api from './api';

export interface Equipo {
  id: number;
  nombre: string;
  marca: string;
  codigo: string;
  estado: 'disponible' | 'en uso' | 'prestado' | 'mantenimiento' | 'dañado';
}

export const equipoService = {
  async getByEstado(estado: string): Promise<Equipo[]> {
    const response = await api.get(`/equipos?estado=${estado}`);
    return response.data;
  },
};
```

### **Componente de Alerta de Equipos**

```tsx
// src/components/AlertasEquipos.tsx
import { useEffect, useState } from 'react';
import { equipoService } from '../services/equipos';

export function AlertasEquipos() {
  const [danados, setDanados] = useState([]);
  const [mantenimiento, setMantenimiento] = useState([]);

  useEffect(() => {
    async function loadEquipos() {
      const danadosData = await equipoService.getByEstado('dañado');
      setDanados(danadosData);

      const mantenimientoData = await equipoService.getByEstado('mantenimiento');
      setMantenimiento(mantenimientoData);
    }

    loadEquipos();
  }, []);

  return (
    <div className="alertas">
      {danados.length > 0 && (
        <div className="alert alert-danger">
          <h3>❌ Equipos Dañados ({danados.length})</h3>
          <ul>
            {danados.map((e: any) => (
              <li key={e.id}>
                {e.nombre} ({e.codigo}) - {e.marca}
              </li>
            ))}
          </ul>
        </div>
      )}

      {mantenimiento.length > 0 && (
        <div className="alert alert-info">
          <h3>🔧 En Mantenimiento ({mantenimiento.length})</h3>
          <ul>
            {mantenimiento.map((e: any) => (
              <li key={e.id}>
                {e.nombre} ({e.codigo})
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
```

---

## 📊 **DASHBOARD**

### **Servicio de Dashboard**

```typescript
// src/services/dashboard.ts
import api from './api';

export interface DashboardResumen {
  fecha: string;
  totales: {
    equipos: number;
    electronica: number;
    robots: number;
    materiales: number;
    prestatarios: number;
    prestamos: number;
  };
  equipos: {
    por_estado: Record<string, number>;
    disponibles: number;
    en_uso: number;
    prestados: number;
    danados: number;
  };
  prestamos: {
    por_estado: Record<string, number>;
    activos: number;
    devueltos: number;
    vencidos: number;
    por_vencer_7_dias: number;
  };
}

export const dashboardService = {
  async getResumen(): Promise<DashboardResumen> {
    const response = await api.get('/dashboard/resumen');
    return response.data;
  },

  async getMovimientosHistorial(dias: number = 30) {
    const response = await api.get(`/dashboard/movimientos-historial?dias=${dias}`);
    return response.data;
  },

  async getTopPrestatarios(limite: number = 10) {
    const response = await api.get(`/dashboard/top-prestatarios?limite=${limite}`);
    return response.data;
  },
};
```

### **Componente de Dashboard**

```tsx
// src/pages/Dashboard.tsx
import { useEffect, useState } from 'react';
import { dashboardService } from '../services/dashboard';
import { AlertasPrestamos } from '../components/AlertasPrestamos';
import { AlertasStock } from '../components/AlertasStock';
import { AlertasEquipos } from '../components/AlertasEquipos';

export function Dashboard() {
  const [resumen, setResumen] = useState(null);

  useEffect(() => {
    async function loadDashboard() {
      const data = await dashboardService.getResumen();
      setResumen(data);
    }

    loadDashboard();
  }, []);

  if (!resumen) return <div>Cargando...</div>;

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>

      {/* Alertas */}
      <AlertasPrestamos />
      <AlertasStock />
      <AlertasEquipos />

      {/* Tarjetas de Totales */}
      <div className="tarjetas">
        <div className="tarjeta">
          <h3>📦 Equipos</h3>
          <p className="numero">{resumen.totales.equipos}</p>
        </div>
        <div className="tarjeta">
          <h3>🔌 Electrónica</h3>
          <p className="numero">{resumen.totales.electronica}</p>
        </div>
        <div className="tarjeta">
          <h3>🤖 Robots</h3>
          <p className="numero">{resumen.totales.robots}</p>
        </div>
        <div className="tarjeta">
          <h3>🧪 Materiales</h3>
          <p className="numero">{resumen.totales.materiales}</p>
        </div>
        <div className="tarjeta">
          <h3>📋 Préstamos</h3>
          <p className="numero">{resumen.totales.prestamos}</p>
        </div>
      </div>

      {/* Equipos por Estado */}
      <div className="grafica">
        <h3>Equipos por Estado</h3>
        <ul>
          <li>✅ Disponibles: {resumen.equipos.disponibles}</li>
          <li>🔄 En Uso: {resumen.equipos.en_uso}</li>
          <li>📤 Prestados: {resumen.equipos.prestados}</li>
          <li>❌ Dañados: {resumen.equipos.danados}</li>
        </ul>
      </div>

      {/* Préstamos por Estado */}
      <div className="grafica">
        <h3>Préstamos por Estado</h3>
        <ul>
          <li className="activo">🟢 Activos: {resumen.prestamos.activos}</li>
          <li className="devuelto">⚪ Devueltos: {resumen.prestamos.devueltos}</li>
          <li className="vencido">🔴 Vencidos: {resumen.prestamos.vencidos}</li>
          <li className="por-vencer">🟡 Por Vencer: {resumen.prestamos.por_vencer_7_dias}</li>
        </ul>
      </div>
    </div>
  );
}
```

---

## 📦 **CRUD DE INVENTARIO**

### **Equipos**

```typescript
// src/services/equipos.ts
import api from './api';

export interface EquipoCreate {
  nombre: string;
  marca: string;
  codigo: string;
  accesorios?: string;
  serial?: string;
  estado: 'disponible' | 'en uso' | 'prestado' | 'mantenimiento' | 'dañado';
}

export const equipoService = {
  async getAll(): Promise<Equipo[]> {
    const response = await api.get('/equipos');
    return response.data;
  },

  async getById(id: number): Promise<Equipo> {
    const response = await api.get(`/equipos/${id}`);
    return response.data;
  },

  async getByCodigo(codigo: string): Promise<Equipo> {
    const response = await api.get(`/equipos/codigo/${codigo}`);
    return response.data;
  },

  async create(data: EquipoCreate): Promise<Equipo> {
    const response = await api.post('/equipos', data);
    return response.data;
  },

  async update(id: number, data: Partial<EquipoCreate>): Promise<Equipo> {
    const response = await api.put(`/equipos/${id}`, data);
    return response.data;
  },

  async delete(id: number): Promise<void> {
    await api.delete(`/equipos/${id}`);
  },
};
```

### **Componente de Lista de Equipos**

```tsx
// src/pages/Equipos.tsx
import { useEffect, useState } from 'react';
import { equipoService, Equipo } from '../services/equipos';

export function Equipos() {
  const [equipos, setEquipos] = useState<Equipo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function loadEquipos() {
      try {
        const data = await equipoService.getAll();
        setEquipos(data);
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Error al cargar equipos');
      } finally {
        setLoading(false);
      }
    }

    loadEquipos();
  }, []);

  if (loading) return <div>Cargando...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="equipos-page">
      <h1>Equipos</h1>
      <button onClick={() => window.location.href = '/equipos/nuevo'}>
        Nuevo Equipo
      </button>

      <table>
        <thead>
          <tr>
            <th>Código</th>
            <th>Nombre</th>
            <th>Marca</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {equipos.map((equipo) => (
            <tr key={equipo.id}>
              <td>{equipo.codigo}</td>
              <td>{equipo.nombre}</td>
              <td>{equipo.marca}</td>
              <td>
                <span className={`estado estado-${equipo.estado}`}>
                  {equipo.estado}
                </span>
              </td>
              <td>
                <button onClick={() => window.location.href = `/equipos/${equipo.id}`}>
                  Ver
                </button>
                <button onClick={() => window.location.href = `/equipos/${equipo.id}/editar`}>
                  Editar
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

## 📋 **PRÉSTAMOS**

### **Crear Préstamo**

```tsx
// src/pages/PrestamoNuevo.tsx
import { useState, useEffect } from 'react';
import { prestamoService } from '../services/prestamos';
import { equipoService } from '../services/equipos';
import { prestatarioService } from '../services/prestatarios';

export function PrestamoNuevo() {
  const [formData, setFormData] = useState({
    prestatario_id: '',
    equipo_id: '',
    fecha_limite: '',
    observaciones: '',
  });
  const [equipos, setEquipos] = useState([]);
  const [prestatarios, setPrestatarios] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    async function loadData() {
      const equiposData = await equipoService.getAll();
      setEquipos(equiposData.filter((e: any) => e.estado === 'disponible'));

      const prestatariosData = await prestatarioService.getAll();
      setPrestatarios(prestatariosData.filter((p: any) => p.activo));
    }

    loadData();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await prestamoService.create({
        prestatario_id: Number(formData.prestatario_id),
        equipo_id: Number(formData.equipo_id),
        fecha_limite: formData.fecha_limite,
        observaciones: formData.observaciones,
      });
      window.location.href = '/prestamos';
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error al crear préstamo');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h1>Nuevo Préstamo</h1>

      {error && <div className="error">{error}</div>}

      <div>
        <label>Prestatario:</label>
        <select
          value={formData.prestatario_id}
          onChange={(e) => setFormData({ ...formData, prestatario_id: e.target.value })}
          required
        >
          <option value="">Seleccionar</option>
          {prestatarios.map((p: any) => (
            <option key={p.id} value={p.id}>
              {p.nombre} - {p.dependencia}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label>Equipo:</label>
        <select
          value={formData.equipo_id}
          onChange={(e) => setFormData({ ...formData, equipo_id: e.target.value })}
          required
        >
          <option value="">Seleccionar</option>
          {equipos.map((e: any) => (
            <option key={e.id} value={e.id}>
              {e.nombre} ({e.codigo})
            </option>
          ))}
        </select>
      </div>

      <div>
        <label>Fecha Límite:</label>
        <input
          type="datetime-local"
          value={formData.fecha_limite}
          onChange={(e) => setFormData({ ...formData, fecha_limite: e.target.value })}
          required
        />
        <small>Máximo 30 días desde hoy</small>
      </div>

      <div>
        <label>Observaciones:</label>
        <textarea
          value={formData.observaciones}
          onChange={(e) => setFormData({ ...formData, observaciones: e.target.value })}
        />
      </div>

      <button type="submit">Crear Préstamo</button>
    </form>
  );
}
```

---

## 💾 **EXPORTACIÓN Y BACKUP**

### **Exportar Datos**

```typescript
// src/services/export.ts
import api from './api';

export const exportService = {
  // Exportar todo en JSON
  async exportJSON() {
    const response = await api.get('/export/json');
    return response.data;
  },

  // Exportar resumen
  async exportResumen() {
    const response = await api.get('/export/resumen');
    return response.data;
  },

  // Descargar archivo JSON
  downloadJSON(data: any, filename: string) {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  },
};
```

### **Componente de Exportar**

```tsx
// src/components/Exportar.tsx
import { exportService } from '../services/export';

export function Exportar() {
  const handleExportJSON = async () => {
    try {
      const data = await exportService.exportJSON();
      exportService.downloadJSON(data, `backup_inventario_${new Date().toISOString().split('T')[0]}.json`);
    } catch (err: any) {
      alert('Error al exportar: ' + err.response?.data?.detail);
    }
  };

  return (
    <div>
      <h1>Exportar Datos</h1>
      <button onClick={handleExportJSON}>
        📥 Descargar Backup JSON
      </button>
    </div>
  );
}
```

---

## ⚠️ **MANEJO DE ERRORES**

### **Errores Comunes**

```typescript
// src/utils/errorHandler.ts

export function handleError(error: any): string {
  if (error.response) {
    // Error de la API
    const status = error.response.status;
    const detail = error.response.data?.detail;

    switch (status) {
      case 400:
        return `Error: ${detail}`;
      case 401:
        return 'Sesión expirada. Por favor inicia sesión nuevamente.';
      case 403:
        return 'No tienes permisos para realizar esta acción.';
      case 404:
        return 'El recurso no fue encontrado.';
      case 422:
        return `Datos inválidos: ${JSON.stringify(detail)}`;
      case 500:
        return 'Error interno del servidor. Intenta más tarde.';
      default:
        return detail || 'Error desconocido';
    }
  } else if (error.request) {
    // Error de red
    return 'Error de conexión. Verifica tu internet.';
  } else {
    // Error genérico
    return error.message || 'Error desconocido';
  }
}
```

---

## 📚 **RECURSOS ADICIONALES**

| Recurso | URL |
|---------|-----|
| Swagger UI | https://inventario-workinn-api.onrender.com/docs |
| ReDoc | https://inventario-workinn-api.onrender.com/redoc |
| Health Check | https://inventario-workinn-api.onrender.com/health |

---

## 🎯 **CHECKLIST DE IMPLEMENTACIÓN**

- [ ] Configurar axios con interceptor de token
- [ ] Implementar login/logout
- [ ] Crear servicio de autenticación
- [ ] Implementar dashboard con alertas
- [ ] Crear componente de alertas de préstamos
- [ ] Crear componente de alertas de stock
- [ ] Crear componente de alertas de equipos
- [ ] Implementar CRUD de equipos
- [ ] Implementar CRUD de préstamos
- [ ] Implementar exportación de datos
- [ ] Agregar manejo de errores
- [ ] Agregar validación de formularios
- [ ] Agregar loading states
- [ ] Implementar routing protegido

---

**Fecha:** Marzo 2026  
**Versión:** 1.0.0  
**API: ✅ 100% Completa - Lista para Producción**
