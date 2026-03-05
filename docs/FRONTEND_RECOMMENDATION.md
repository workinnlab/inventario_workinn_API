# 🎨 Recomendación de Frontend - Inventario CIE

## 🏆 Mi Recomendación Principal

### **React + Vite + TypeScript + TailwindCSS**

**¿Por qué?**

| Factor | React + Vite |
|--------|--------------|
| **Curva de aprendizaje** | ⭐⭐⭐⭐ Media-Baja |
| **Rendimiento** | ⭐⭐⭐⭐⭐ Excelente |
| **Comunidad** | ⭐⭐⭐⭐⭐ La más grande |
| **Librerías** | ⭐⭐⭐⭐⭐ Miles disponibles |
| **Empleabilidad** | ⭐⭐⭐⭐⭐ Muy alta |
| **Mantenibilidad** | ⭐⭐⭐⭐⭐ Excelente con TypeScript |

---

## 🚀 Setup Recomendado

### **1. Crear Proyecto**

```bash
# Crear proyecto con Vite
npm create vite@latest inventario-cie-frontend -- --template react-ts

cd inventario-cie-frontend

# Instalar dependencias
npm install

# Instalar TailwindCSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Instalar librerías útiles
npm install @tanstack/react-query axios react-router-dom
npm install -D @types/node
```

### **2. Estructura de Carpetas**

```
inventario-cie-frontend/
├── src/
│   ├── components/
│   │   ├── ui/              # Componentes base (Button, Input)
│   │   ├── layout/          # Layout, Sidebar, Header
│   │   └── inventory/       # Componentes específicos
│   ├── pages/               # Páginas completas
│   ├── services/            # Llamadas a la API
│   ├── hooks/               # Custom hooks
│   ├── contexts/            # Contextos (Auth, Theme)
│   ├── types/               # TypeScript types
│   ├── utils/               # Utilidades
│   ├── App.tsx
│   └── main.tsx
├── public/
├── package.json
├── tailwind.config.js
└── tsconfig.json
```

### **3. Configurar API Service**

```typescript
// src/services/api.ts
import axios from 'axios';

const API_BASE = 'https://inventario-workinn-api.onrender.com/api/v1';

const api = axios.create({
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
      // Token expirado, redirect a login
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
```

### **4. Auth Service**

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

  getToken() {
    return localStorage.getItem('token');
  },

  getUser(): User | null {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  },
};
```

### **5. Inventory Service**

```typescript
// src/services/inventory.ts
import api from './api';

export interface Equipo {
  id: number;
  nombre: string;
  marca: string;
  codigo: string;
  accesorios?: string;
  serial?: string;
  estado: 'disponible' | 'en uso' | 'prestado' | 'mantenimiento' | 'dañado';
  created_at: string;
  updated_at: string;
}

export const equipoService = {
  async getAll(skip = 0, limit = 100): Promise<Equipo[]> {
    const response = await api.get(`/equipos?skip=${skip}&limit=${limit}`);
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

  async create(data: Partial<Equipo>): Promise<Equipo> {
    const response = await api.post('/equipos', data);
    return response.data;
  },

  async update(id: number, data: Partial<Equipo>): Promise<Equipo> {
    const response = await api.put(`/equipos/${id}`, data);
    return response.data;
  },

  async delete(id: number): Promise<void> {
    await api.delete(`/equipos/${id}`);
  },
};
```

### **6. React Query Hook**

```typescript
// src/hooks/useEquipos.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { equipoService, Equipo } from '../services/inventory';

export function useEquipos(skip = 0, limit = 100) {
  return useQuery<Equipo[]>({
    queryKey: ['equipos', skip, limit],
    queryFn: () => equipoService.getAll(skip, limit),
  });
}

export function useEquipo(id: number) {
  return useQuery<Equipo>({
    queryKey: ['equipo', id],
    queryFn: () => equipoService.getById(id),
    enabled: !!id,
  });
}

export function useCreateEquipo() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (data: Partial<Equipo>) => equipoService.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['equipos'] });
    },
  });
}
```

### **7. Componente de Ejemplo**

```typescript
// src/pages/EquiposPage.tsx
import { useState } from 'react';
import { useEquipos, useCreateEquipo } from '../hooks/useEquipos';

export function EquiposPage() {
  const [skip, setSkip] = useState(0);
  const { data: equipos, isLoading, error } = useEquipos(skip, 10);
  const createEquipo = useCreateEquipo();

  if (isLoading) return <div>Cargando...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Equipos</h1>
      
      <button
        onClick={() => createEquipo.mutate({
          nombre: 'Nuevo Equipo',
          marca: 'Marca',
          codigo: `PC-${Date.now()}`,
          estado: 'disponible'
        })}
        className="bg-blue-500 text-white px-4 py-2 rounded mb-4"
      >
        Crear Equipo
      </button>

      <table className="w-full border">
        <thead>
          <tr className="bg-gray-100">
            <th className="p-2 border">Código</th>
            <th className="p-2 border">Nombre</th>
            <th className="p-2 border">Marca</th>
            <th className="p-2 border">Estado</th>
          </tr>
        </thead>
        <tbody>
          {equipos?.map((equipo) => (
            <tr key={equipo.id} className="hover:bg-gray-50">
              <td className="p-2 border">{equipo.codigo}</td>
              <td className="p-2 border">{equipo.nombre}</td>
              <td className="p-2 border">{equipo.marca}</td>
              <td className="p-2 border">
                <span className={`px-2 py-1 rounded text-sm ${
                  equipo.estado === 'disponible' 
                    ? 'bg-green-100 text-green-800'
                    : 'bg-yellow-100 text-yellow-800'
                }`}>
                  {equipo.estado}
                </span>
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

## 🎯 Alternativas

### **Opción 2: Next.js (Recomendado para SEO)**

**Ventajas:**
- ✅ Server-side rendering
- ✅ Mejor SEO
- ✅ Routing automático
- ✅ API routes integradas

**Setup:**
```bash
npx create-next-app@latest inventario-cie --typescript --tailwind --app
```

**Ideal para:** Si necesitas que el frontend sea indexable por Google

---

### **Opción 3: Vue 3 + Vite**

**Ventajas:**
- ✅ Más simple que React
- ✅ Excelente documentación
- ✅ Menos boilerplate

**Setup:**
```bash
npm create vite@latest inventario-cie -- --template vue-ts
npm install axios vue-router pinia
```

**Ideal para:** Si prefieres Vue sobre React

---

### **Opción 4: Angular**

**Ventajas:**
- ✅ Framework completo (todo incluido)
- ✅ TypeScript nativo
- ✅ Enterprise-grade

**Setup:**
```bash
npm install -g @angular/cli
ng new inventario-cie
```

**Ideal para:** Proyectos enterprise grandes

---

### **Opción 5: SvelteKit**

**Ventajas:**
- ✅ Menos código
- ✅ Mejor rendimiento
- ✅ Más simple

**Setup:**
```bash
npm create svelte@latest inventario-cie
```

**Ideal para:** Proyectos pequeños/medianos, preferencia por simplicidad

---

## 📊 Comparativa

| Framework | Curva | Rendimiento | Empleo | Recomendado para |
|-----------|-------|-------------|--------|------------------|
| **React + Vite** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **Tu caso** ✅ |
| Next.js | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | SEO crítico |
| Vue 3 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Preferencia Vue |
| Angular | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Enterprise |
| SvelteKit | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Proyectos pequeños |

---

## 🎨 UI Libraries Recomendadas

### **Para React:**

1. **shadcn/ui** (Mi recomendación)
   ```bash
   npx shadcn-ui@latest init
   ```
   - Componentes hermosos
   - Totalmente personalizable
   - Basado en Tailwind

2. **Mantine**
   ```bash
   npm install @mantine/core @mantine/hooks
   ```
   - 100+ componentes
   - Hooks incluidos
   - Excelente docs

3. **Chakra UI**
   ```bash
   npm install @chakra-ui/react
   ```
   - Fácil de usar
   - Accesible
   - Themeable

---

## 📱 Mi Stack Recomendado para Tu Proyecto

```json
{
  "framework": "React 18",
  "build": "Vite",
  "language": "TypeScript",
  "styling": "TailwindCSS",
  "ui": "shadcn/ui",
  "state": "React Query + Context",
  "routing": "React Router v6",
  "http": "Axios",
  "forms": "React Hook Form",
  "validation": "Zod"
}
```

**Comando de setup completo:**

```bash
npm create vite@latest inventario-cie-frontend -- --template react-ts
cd inventario-cie-frontend
npm install

# Tailwind
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Librerías
npm install @tanstack/react-query axios react-router-dom
npm install @shadcn/ui
npm install react-hook-form zod @hookform/resolvers
npm install lucide-react  # Iconos

npx shadcn-ui@latest init
```

---

## 🚀 Próximos Pasos

1. **Elige el framework** (React + Vite recomendado)
2. **Configura el proyecto** con el setup de arriba
3. **Crea los services** para consumir la API
4. **Implementa Auth** (login, logout, protected routes)
5. **Crea las páginas:**
   - `/login` - Login
   - `/dashboard` - Dashboard principal
   - `/equipos` - CRUD de equipos
   - `/electronica` - CRUD de electrónica
   - `/robots` - CRUD de robots
   - `/materiales` - CRUD de materiales
   - `/prestamos` - Gestión de préstamos
   - `/prestatarios` - CRUD de prestatarios

---

## 📚 Recursos

- [React Docs](https://react.dev)
- [Vite Docs](https://vitejs.dev)
- [TailwindCSS](https://tailwindcss.com)
- [React Query](https://tanstack.com/query)
- [shadcn/ui](https://ui.shadcn.com)
- [TypeScript](https://typescriptlang.org)

---

**¿Quieres que te cree el proyecto frontend con este stack?**
