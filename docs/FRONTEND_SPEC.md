# 📖 Frontend Inventario CIE - Especificación Técnica Completa

**Documento para iniciar desarrollo del frontend con React + Vite + Vercel**

---

## 📋 **Información del Proyecto**

| Campo | Valor |
|-------|-------|
| **Nombre** | Inventario CIE Frontend |
| **API Backend** | https://inventario-workinn-api.onrender.com/api/v1 |
| **Deploy** | Vercel (gratuito) |
| **Framework** | React 18 + Vite |
| **Lenguaje** | TypeScript |
| **Estilos** | TailwindCSS |
| **Estado** | Producción (API lista) |

---

## 🎯 **Objetivo del Proyecto**

Crear un dashboard web para gestionar el inventario del CIE que permita:

1. ✅ Autenticar usuarios (login/logout)
2. ✅ Gestionar equipos de cómputo (CRUD)
3. ✅ Gestionar electrónica (CRUD)
4. ✅ Gestionar robots (CRUD)
5. ✅ Gestionar materiales (CRUD)
6. ✅ Gestionar prestatarios (CRUD)
7. ✅ Gestionar préstamos (crear, devolver, listar)
8. ✅ Ver historial de movimientos

---

## 🛠️ **Stack Tecnológico Requerido**

### **Core**

```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "react-router-dom": "^6.20.0",
  "typescript": "^5.3.0",
  "vite": "^5.0.0"
}
```

### **HTTP & API**

```json
{
  "axios": "^1.6.0",
  "@tanstack/react-query": "^5.10.0"
}
```

### **Forms & Validación**

```json
{
  "react-hook-form": "^7.49.0",
  "zod": "^3.22.0",
  "@hookform/resolvers": "^3.3.0"
}
```

### **UI & Estilos**

```json
{
  "tailwindcss": "^3.4.0",
  "postcss": "^8.4.0",
  "autoprefixer": "^10.4.0",
  "lucide-react": "^0.300.0",
  "clsx": "^2.0.0",
  "tailwind-merge": "^2.2.0"
}
```

### **Componentes UI (Opcional - Recomendado)**

```json
{
  "@radix-ui/react-dialog": "^1.0.0",
  "@radix-ui/react-dropdown-menu": "^2.0.0",
  "@radix-ui/react-label": "^2.0.0",
  "@radix-ui/react-select": "^2.0.0",
  "@radix-ui/react-toast": "^1.1.0",
  "class-variance-authority": "^0.7.0"
}
```

---

## 📁 **Estructura de Carpetas**

```
inventario-cie-frontend/
├── public/
│   └── logo.svg
├── src/
│   ├── app/                    # Si usas file-based routing (opcional)
│   ├── components/
│   │   ├── ui/                 # Componentes base reutilizables
│   │   │   ├── button.tsx
│   │   │   ├── input.tsx
│   │   │   ├── table.tsx
│   │   │   ├── modal.tsx
│   │   │   ├── select.tsx
│   │   │   └── toast.tsx
│   │   ├── layout/             # Layout principal
│   │   │   ├── sidebar.tsx
│   │   │   ├── header.tsx
│   │   │   └── protected-route.tsx
│   │   └── inventory/          # Componentes específicos
│   │       ├── equipo-form.tsx
│   │       ├── equipo-table.tsx
│   │       ├── prestamo-form.tsx
│   │       └── ...
│   ├── pages/                  # Páginas completas
│   │   ├── login.tsx
│   │   ├── dashboard.tsx
│   │   ├── equipos.tsx
│   │   ├── electronica.tsx
│   │   ├── robots.tsx
│   │   ├── materiales.tsx
│   │   ├── prestatarios.tsx
│   │   └── prestamos.tsx
│   ├── services/               # Llamadas a la API
│   │   ├── api.ts              # Configuración de axios
│   │   ├── auth.ts
│   │   ├── equipos.ts
│   │   ├── electronica.ts
│   │   ├── robots.ts
│   │   ├── materiales.ts
│   │   ├── prestatarios.ts
│   │   ├── prestamos.ts
│   │   └── movimientos.ts
│   ├── hooks/                  # Custom hooks
│   │   ├── useAuth.ts
│   │   ├── useEquipos.ts
│   │   ├── usePrestamos.ts
│   │   └── ...
│   ├── contexts/               # Contextos de React
│   │   └── auth-context.tsx
│   ├── types/                  # Tipos de TypeScript
│   │   └── index.ts
│   ├── utils/                  # Utilidades
│   │   ├── cn.ts               # classnames helper
│   │   └── formatters.ts
│   ├── lib/
│   │   └── api.ts              # Configuración base de API
│   ├── App.tsx
│   ├── main.tsx
│   └── vite-env.d.ts
├── .env                        # Variables de entorno
├── .env.example
├── .gitignore
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.js
├── postcss.config.js
└── README.md
```

---

## 🔐 **Autenticación**

### **Endpoint de Login**

```
POST https://inventario-workinn-api.onrender.com/api/v1/auth/login
Content-Type: application/json

Request:
{
  "email": "admin@cie.com",
  "password": "Admin123!"
}

Response (200):
{
  "access_token": "eyJhbGciOiJFUzI1NiIs...",
  "refresh_token": "xd3aeqvscjia",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "admin@cie.com",
    "nombre": "Administrador CIE",
    "rol": "admin",
    "activo": true
  }
}
```

### **Endpoint de Registro**

```
POST https://inventario-workinn-api.onrender.com/api/v1/auth/register
Content-Type: application/json

Request:
{
  "email": "nuevo@cie.com",
  "password": "Password123!",
  "nombre": "Nuevo Usuario",
  "rol": "viewer"  // admin, inventory, viewer
}
```

### **Endpoint de Usuario Actual**

```
GET https://inventario-workinn-api.onrender.com/api/v1/auth/me
Authorization: Bearer {token}

Response (200):
{
  "id": "uuid",
  "nombre": "Administrador CIE",
  "email": "admin@cie.com",
  "rol": "admin",
  "activo": true,
  "created_at": "2026-03-05T...",
  "updated_at": "2026-03-05T..."
}
```

### **Endpoint de Logout**

```
POST https://inventario-workinn-api.onrender.com/api/v1/auth/logout
Authorization: Bearer {token}
```

### **Implementación del Servicio de Auth**

```typescript
// src/services/auth.ts
import api from '@/lib/api';

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  nombre: string;
  rol: 'admin' | 'inventory' | 'viewer';
}

export interface User {
  id: string;
  email: string;
  nombre: string;
  rol: 'admin' | 'inventory' | 'viewer';
  activo: boolean;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: 'bearer';
  user: User;
}

export const authService = {
  /**
   * Iniciar sesión
   */
  async login(data: LoginRequest): Promise<LoginResponse> {
    const response = await api.post('/auth/login', data);
    const { access_token, refresh_token, token_type, user } = response.data;
    
    // Guardar en localStorage
    localStorage.setItem('token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
    localStorage.setItem('user', JSON.stringify(user));
    
    return { access_token, refresh_token, token_type, user };
  },

  /**
   * Registrar nuevo usuario (solo admins)
   */
  async register(data: RegisterRequest): Promise<User> {
    const response = await api.post('/auth/register', data);
    return response.data;
  },

  /**
   * Cerrar sesión
   */
  async logout(): Promise<void> {
    try {
      await api.post('/auth/logout');
    } finally {
      // Limpiar localStorage incluso si falla el request
      localStorage.removeItem('token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user');
    }
  },

  /**
   * Obtener usuario actual
   */
  async getCurrentUser(): Promise<User> {
    const response = await api.get('/auth/me');
    return response.data;
  },

  /**
   * Obtener token del localStorage
   */
  getToken(): string | null {
    return localStorage.getItem('token');
  },

  /**
   * Obtener usuario del localStorage
   */
  getUser(): User | null {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  },

  /**
   * Verificar si está autenticado
   */
  isAuthenticated(): boolean {
    return !!this.getToken();
  },

  /**
   * Verificar si tiene rol específico
   */
  hasRole(roles: string[]): boolean {
    const user = this.getUser();
    return user ? roles.includes(user.rol) : false;
  },
};
```

---

## 📦 **Endpoints de la API - Resumen Completo**

### **Base URL**

```
https://inventario-workinn-api.onrender.com/api/v1
```

### **Equipos**

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/equipos` | Listar equipos | ❌ |
| GET | `/equipos/{id}` | Obtener por ID | ❌ |
| GET | `/equipos/codigo/{codigo}` | Buscar por código | ❌ |
| POST | `/equipos` | Crear equipo | ✅ admin/inventory |
| PUT | `/equipos/{id}` | Actualizar equipo | ✅ admin/inventory |
| DELETE | `/equipos/{id}` | Eliminar equipo | ✅ admin |

**Modelo Equipo:**
```typescript
interface Equipo {
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
```

### **Electrónica**

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/electronica` | Listar electrónica | ❌ |
| GET | `/electronica/{id}` | Obtener por ID | ❌ |
| POST | `/electronica` | Crear electrónica | ✅ admin/inventory |
| PUT | `/electronica/{id}` | Actualizar | ✅ admin/inventory |
| DELETE | `/electronica/{id}` | Eliminar | ✅ admin |

**Modelo Electrónica:**
```typescript
interface Electronica {
  id: number;
  nombre: string;
  descripcion?: string;
  tipo?: string;
  en_uso: number;
  en_stock: number;
  total: number;
  created_at: string;
  updated_at: string;
}
```

### **Robots**

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/robots` | Listar robots | ❌ |
| GET | `/robots/{id}` | Obtener por ID | ❌ |
| POST | `/robots` | Crear robot | ✅ admin/inventory |
| PUT | `/robots/{id}` | Actualizar | ✅ admin/inventory |
| DELETE | `/robots/{id}` | Eliminar | ✅ admin |

**Modelo Robot:**
```typescript
interface Robot {
  id: number;
  nombre: string;
  fuera_de_servicio: number;
  en_uso: number;
  disponible: number;
  total: number;
  created_at: string;
  updated_at: string;
}
```

### **Materiales**

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/materiales` | Listar materiales | ❌ |
| GET | `/materiales/{id}` | Obtener por ID | ❌ |
| GET | `/tipos-materiales` | Listar tipos | ❌ |
| POST | `/materiales` | Crear material | ✅ admin/inventory |
| PUT | `/materiales/{id}` | Actualizar | ✅ admin/inventory |
| DELETE | `/materiales/{id}` | Eliminar | ✅ admin |

**Modelo Material:**
```typescript
interface Material {
  id: number;
  color: string;
  tipo_id?: number;
  cantidad: string;
  categoria: 'Filamento' | 'Resina' | 'Otro';
  usado: number;
  en_uso: number;
  en_stock: number;
  total: number;
  created_at: string;
  updated_at: string;
}
```

### **Prestatarios**

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/prestatarios` | Listar prestatarios | ❌ |
| GET | `/prestatarios/{id}` | Obtener por ID | ❌ |
| POST | `/prestatarios` | Crear prestatario | ✅ admin/inventory |
| PUT | `/prestatarios/{id}` | Actualizar | ✅ admin/inventory |
| DELETE | `/prestatarios/{id}` | Inactivar | ✅ admin/inventory |

**Modelo Prestatario:**
```typescript
interface Prestatario {
  id: number;
  nombre: string;
  telefono?: string;
  dependencia: string;
  cedula?: string;
  email?: string;
  activo: boolean;
  created_at: string;
  updated_at: string;
}
```

### **Préstamos**

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/prestamos` | Listar préstamos | ❌ |
| GET | `/prestamos/activos` | Préstamos activos | ❌ |
| GET | `/prestamos/{id}` | Obtener por ID | ❌ |
| POST | `/prestamos` | Crear préstamo | ✅ admin/inventory |
| PUT | `/prestamos/{id}` | Actualizar | ✅ admin/inventory |
| POST | `/prestamos/{id}/devolver` | Devolver | ✅ admin/inventory |
| DELETE | `/prestamos/{id}` | Eliminar | ✅ admin |

**Modelo Préstamo:**
```typescript
interface Prestamo {
  id: number;
  equipo_id?: number;
  electronica_id?: number;
  robot_id?: number;
  material_id?: number;
  prestatario_id: number;
  fecha_prestamo: string;
  fecha_devolucion?: string;
  fecha_limite?: string;
  estado: 'activo' | 'devuelto' | 'vencido' | 'perdido';
  observaciones?: string;
  created_at: string;
  updated_at: string;
}
```

### **Movimientos**

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/movimientos` | Listar movimientos | ❌ |
| GET | `/movimientos/{id}` | Obtener por ID | ❌ |
| POST | `/movimientos` | Crear movimiento | ✅ admin/inventory |

**Modelo Movimiento:**
```typescript
interface Movimiento {
  id: number;
  tipo: 'entrada' | 'salida' | 'devolucion' | 'daño' | 'ajuste_stock' | 'baja' | 'transferencia';
  equipo_id?: number;
  electronica_id?: number;
  robot_id?: number;
  material_id?: number;
  cantidad: number;
  prestamo_id?: number;
  usuario_id?: string;
  descripcion?: string;
  ubicacion_anterior?: string;
  ubicacion_nueva?: string;
  created_at: string;
}
```

---

## 🔧 **Configuración de la API**

### **Archivo: src/lib/api.ts**

```typescript
import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';

export const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://inventario-workinn-api.onrender.com/api/v1';

// Crear instancia de axios
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 segundos
});

// Interceptor para agregar token
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

// Interceptor para manejar errores
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Token expirado o inválido
      localStorage.removeItem('token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user');
      
      // Redirigir a login (si no estamos ya)
      if (window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default api;
```

### **Archivo: .env**

```env
VITE_API_URL=https://inventario-workinn-api.onrender.com/api/v1
```

### **Archivo: .env.example**

```env
VITE_API_URL=https://inventario-workinn-api.onrender.com/api/v1
```

---

## 🎨 **Configuración de TailwindCSS**

### **Archivo: tailwind.config.js**

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ["class"],
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [],
}
```

### **Archivo: src/index.css**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 221.2 83.2% 53.3%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 221.2 83.2% 53.3%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;
    --primary: 217.2 91.2% 59.8%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 224.3 76.3% 48%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}
```

---

## 🔒 **Roles y Permisos**

### **Tabla de Permisos**

| Función | Admin | Inventory | Viewer |
|---------|-------|-----------|--------|
| Ver inventario | ✅ | ✅ | ✅ |
| Crear items | ✅ | ✅ | ❌ |
| Editar items | ✅ | ✅ | ❌ |
| Eliminar items | ✅ | ❌ | ❌ |
| Gestionar préstamos | ✅ | ✅ | ❌ |
| Crear movimientos | ✅ | ✅ | ❌ |
| Ver usuarios | ✅ | ❌ | ❌ |
| Crear usuarios | ✅ | ❌ | ❌ |

### **Hook useAuth**

```typescript
// src/hooks/useAuth.ts
import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authService, User } from '@/services/auth';

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  isAuthenticated: boolean;
  hasRole: (roles: string[]) => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Cargar usuario del localStorage al iniciar
    const storedUser = authService.getUser();
    const storedToken = authService.getToken();
    
    if (storedUser && storedToken) {
      setUser(storedUser);
      setToken(storedToken);
    }
    setLoading(false);
  }, []);

  const login = async (email: string, password: string) => {
    const response = await authService.login({ email, password });
    setUser(response.user);
    setToken(response.access_token);
  };

  const logout = async () => {
    await authService.logout();
    setUser(null);
    setToken(null);
  };

  const hasRole = (roles: string[]): boolean => {
    return user ? roles.includes(user.rol) : false;
  };

  return (
    <AuthContext.Provider value={{
      user,
      token,
      loading,
      login,
      logout,
      isAuthenticated: !!token,
      hasRole,
    }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
```

### **Protected Route**

```typescript
// src/components/layout/protected-route.tsx
import { Navigate } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';

interface ProtectedRouteProps {
  children: React.ReactNode;
  allowedRoles?: string[];
}

export function ProtectedRoute({ children, allowedRoles }: ProtectedRouteProps) {
  const { isAuthenticated, hasRole, loading } = useAuth();

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (allowedRoles && !hasRole(allowedRoles)) {
    return <Navigate to="/dashboard" replace />;
  }

  return <>{children}</>;
}
```

---

## 📄 **Archivos de Configuración**

### **Archivo: vite.config.ts**

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 5173,
    open: true,
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
});
```

### **Archivo: tsconfig.json**

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### **Archivo: package.json**

```json
{
  "name": "inventario-cie-frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.0",
    "@tanstack/react-query": "^5.10.0",
    "react-hook-form": "^7.49.0",
    "zod": "^3.22.0",
    "@hookform/resolvers": "^3.3.0",
    "lucide-react": "^0.300.0",
    "clsx": "^2.0.0",
    "tailwind-merge": "^2.2.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.40",
    "@types/react-dom": "^18.2.17",
    "@typescript-eslint/eslint-plugin": "^6.12.0",
    "@typescript-eslint/parser": "^6.12.0",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.16",
    "eslint": "^8.54.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.4",
    "postcss": "^8.4.32",
    "tailwindcss": "^3.4.0",
    "typescript": "^5.3.2",
    "vite": "^5.0.4"
  }
}
```

---

## 🚀 **Deploy en Vercel**

### **Paso 1: Subir a GitHub**

```bash
git init
git add .
git commit -m "Initial commit - Inventario CIE Frontend"

# Crear repositorio en GitHub y hacer push
git remote add origin https://github.com/workinnlab/inventario-cie-frontend.git
git branch -M main
git push -u origin main
```

### **Paso 2: Crear Proyecto en Vercel**

1. **Ve a:** https://vercel.com/new
2. **Click:** "Continue with GitHub"
3. **Importa tu repositorio:** `inventario-cie-frontend`
4. **Configura:**
   - **Framework Preset:** Vite
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
   - **Install Command:** `npm install`

### **Paso 3: Variables de Entorno**

En Vercel > Settings > Environment Variables, agrega:

```
VITE_API_URL=https://inventario-workinn-api.onrender.com/api/v1
```

### **Paso 4: Deploy**

Click **"Deploy"** y espera ~30 segundos.

**URL final:** `https://inventario-cie-frontend.vercel.app`

---

## 📝 **Consideraciones Importantes**

### **1. CORS**

La API ya tiene CORS habilitado (`*`), pero para producción puedes restringir:

```python
# En tu backend (app/main.py)
allowed_origins = [
    "https://inventario-cie-frontend.vercel.app",
    "http://localhost:5173"
]
```

### **2. Token Expiración**

- El `access_token` dura **1 hora**
- El `refresh_token` se usa para obtener nuevo access_token
- Implementa refresh automático antes de que expire

### **3. Cold Start de Render**

La API en Render tiene cold start (~30 segundos la primera petición). Considera:

- Usar UptimeRobot para mantenerla activa
- Mostrar loading state mientras carga

### **4. Manejo de Errores**

```typescript
try {
  await api.post('/equipos', data);
} catch (error: any) {
  if (error.response?.status === 400) {
    // Error de validación
    console.error(error.response.data.detail);
  } else if (error.response?.status === 401) {
    // No autorizado
    window.location.href = '/login';
  } else if (error.response?.status === 404) {
    // No encontrado
  } else if (error.response?.status === 500) {
    // Error del servidor
  } else {
    // Error de red
  }
}
```

### **5. Estados de Carga**

```typescript
const [loading, setLoading] = useState(false);
const [error, setError] = useState<string | null>(null);

const handleSubmit = async () => {
  setLoading(true);
  setError(null);
  
  try {
    await api.post('/equipos', data);
  } catch (err: any) {
    setError(err.response?.data?.detail || 'Error al crear equipo');
  } finally {
    setLoading(false);
  }
};
```

---

## 📚 **Recursos Adicionales**

| Recurso | URL |
|---------|-----|
| Documentación API | https://inventario-workinn-api.onrender.com/docs |
| Vercel Docs | https://vercel.com/docs |
| Vite Docs | https://vitejs.dev |
| React Router | https://reactrouter.com |
| TailwindCSS | https://tailwindcss.com |
| React Query | https://tanstack.com/query |
| React Hook Form | https://react-hook-form.com |

---

## ✅ **Checklist de Implementación**

- [ ] Configurar proyecto Vite + React + TypeScript
- [ ] Configurar TailwindCSS
- [ ] Configurar axios con interceptores
- [ ] Implementar AuthContext y useAuth
- [ ] Crear página de Login
- [ ] Crear ProtectedRoute
- [ ] Crear Layout con Sidebar
- [ ] Implementar servicios para cada módulo
- [ ] Crear página de Dashboard
- [ ] Crear CRUD de Equipos
- [ ] Crear CRUD de Electrónica
- [ ] Crear CRUD de Robots
- [ ] Crear CRUD de Materiales
- [ ] Crear CRUD de Prestatarios
- [ ] Crear gestión de Préstamos
- [ ] Crear vista de Movimientos
- [ ] Subir a GitHub
- [ ] Deploy en Vercel
- [ ] Configurar variables de entorno en Vercel
- [ ] Producers flujo completo

---

**Documento creado:** Marzo 2026  
**API Backend:** https://inventario-workinn-api.onrender.com  
**Versión:** 1.0.0
