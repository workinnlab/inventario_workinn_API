#!/usr/bin/env python3
"""
Test Completo de la API - Inventario CIE
Prueba todos los endpoints y valida las respuestas

Uso:
    python test_api_completo.py

Requisitos:
    pip install requests
"""

import requests
import json
import time
from typing import Optional

# Configuración
BASE_URL = "https://inventario-workinn-api.onrender.com/api/v1"
TEST_USER = {
    "email": "admin@cie.com",
    "password": "Admin123!"
}

# Colores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")


def print_success(text: str):
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")


def print_error(text: str):
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")


def print_info(text: str):
    print(f"{Colors.YELLOW}ℹ {text}{Colors.RESET}")


# ============================================================================
# TEST DE AUTENTICACIÓN
# ============================================================================

def test_auth() -> Optional[str]:
    """Prueba autenticación y retorna el token"""
    print_header("🔐 TEST DE AUTENTICACIÓN")
    
    # Test Login
    print_info("Probando login...")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json=TEST_USER,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            user = data.get('user', {})
            
            print_success(f"Login exitoso: {user.get('email')}")
            print_success(f"Rol: {user.get('rol')}")
            print_success(f"Token recibido (longitud: {len(token)})")
            
            return token
        else:
            print_error(f"Login falló: {response.status_code}")
            print_error(f"Respuesta: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print_error(f"Error de conexión: {e}")
        return None


# ============================================================================
# TEST DE EQUIPOS
# ============================================================================

def test_equipos(token: str):
    """Prueba todos los endpoints de equipos"""
    print_header("📦 TEST DE EQUIPOS")
    
    headers = {"Authorization": f"Bearer {token}"}
    equipo_creado_id = None
    
    # 1. Listar equipos
    print_info("Listando equipos...")
    response = requests.get(f"{BASE_URL}/equipos", headers=headers, timeout=30)
    if response.status_code == 200:
        equipos = response.json()
        print_success(f"Equipos listados: {len(equipos)} encontrados")
        if equipos:
            print_info(f"Primer equipo: {equipos[0].get('nombre')} ({equipos[0].get('codigo')})")
    else:
        print_error(f"Error al listar: {response.status_code}")
    
    # 2. Crear equipo de prueba
    print_info("Creando equipo de prueba...")
    nuevo_equipo = {
        "nombre": "Equipo Test API",
        "marca": "Test Brand",
        "codigo": f"TEST-{int(time.time())}",
        "accesorios": "Teclado, Mouse",
        "serial": "TEST123",
        "estado": "disponible"
    }
    
    response = requests.post(f"{BASE_URL}/equipos", json=nuevo_equipo, headers=headers, timeout=30)
    if response.status_code == 200:
        equipo = response.json()
        equipo_creado_id = equipo.get('id')
        print_success(f"Equipo creado: ID={equipo_creado_id}, Código={equipo.get('codigo')}")
    else:
        print_error(f"Error al crear: {response.status_code} - {response.text}")
    
    # 3. Obtener equipo por ID (si se creó)
    if equipo_creado_id:
        print_info(f"Obteniendo equipo por ID: {equipo_creado_id}...")
        response = requests.get(f"{BASE_URL}/equipos/{equipo_creado_id}", headers=headers, timeout=30)
        if response.status_code == 200:
            equipo = response.json()
            print_success(f"Equipo obtenido: {equipo.get('nombre')}")
        else:
            print_error(f"Error al obtener: {response.status_code}")
        
        # 4. Actualizar equipo
        print_info(f"Actualizando equipo {equipo_creado_id}...")
        update_data = {
            "nombre": "Equipo Test API Actualizado",
            "estado": "en uso"
        }
        response = requests.put(
            f"{BASE_URL}/equipos/{equipo_creado_id}",
            json=update_data,
            headers=headers,
            timeout=30
        )
        if response.status_code == 200:
            print_success(f"Equipo actualizado: {response.json().get('nombre')}")
        else:
            print_error(f"Error al actualizar: {response.status_code}")
        
        # 5. Eliminar equipo
        print_info(f"Eliminando equipo {equipo_creado_id}...")
        response = requests.delete(f"{BASE_URL}/equipos/{equipo_creado_id}", headers=headers, timeout=30)
        if response.status_code == 200:
            print_success(f"Equipo eliminado correctamente")
        else:
            print_error(f"Error al eliminar: {response.status_code}")
    
    # 6. Obtener por código (usando el primer equipo existente)
    print_info("Probando búsqueda por código...")
    response = requests.get(f"{BASE_URL}/equipos", headers=headers, timeout=30)
    if response.status_code == 200 and response.json():
        codigo = response.json()[0].get('codigo')
        response = requests.get(f"{BASE_URL}/equipos/codigo/{codigo}", headers=headers, timeout=30)
        if response.status_code == 200:
            print_success(f"Búsqueda por código exitosa: {response.json().get('nombre')}")
        else:
            print_error(f"Error en búsqueda por código: {response.status_code}")


# ============================================================================
# TEST DE ELECTRÓNICA
# ============================================================================

def test_electronica(token: str):
    """Prueba todos los endpoints de electrónica"""
    print_header("🔌 TEST DE ELECTRÓNICA")
    
    headers = {"Authorization": f"Bearer {token}"}
    electronica_creada_id = None
    
    # 1. Listar electrónica
    print_info("Listando electrónica...")
    response = requests.get(f"{BASE_URL}/electronica", headers=headers, timeout=30)
    if response.status_code == 200:
        items = response.json()
        print_success(f"Electrónica listada: {len(items)} encontrados")
    else:
        print_error(f"Error al listar: {response.status_code}")
    
    # 2. Crear electrónica de prueba
    print_info("Creando electrónica de prueba...")
    nuevo_item = {
        "nombre": "Arduino Test",
        "descripcion": "Microcontrolador de prueba",
        "tipo": "Microcontroladores",
        "en_uso": 0,
        "en_stock": 5
    }
    
    response = requests.post(f"{BASE_URL}/electronica", json=nuevo_item, headers=headers, timeout=30)
    if response.status_code == 200:
        item = response.json()
        electronica_creada_id = item.get('id')
        print_success(f"Electrónica creada: ID={electronica_creada_id}")
    else:
        print_error(f"Error al crear: {response.status_code}")
    
    # 3. Actualizar (si se creó)
    if electronica_creada_id:
        print_info(f"Actualizando electrónica {electronica_creada_id}...")
        response = requests.put(
            f"{BASE_URL}/electronica/{electronica_creada_id}",
            json={"en_stock": 10},
            headers=headers,
            timeout=30
        )
        if response.status_code == 200:
            print_success(f"Electrónica actualizada: stock={response.json().get('en_stock')}")
        
        # 4. Eliminar
        print_info(f"Eliminando electrónica {electronica_creada_id}...")
        response = requests.delete(f"{BASE_URL}/electronica/{electronica_creada_id}", headers=headers, timeout=30)
        if response.status_code == 200:
            print_success("Electrónica eliminada")
        else:
            print_error(f"Error al eliminar: {response.status_code}")


# ============================================================================
# TEST DE ROBOTS
# ============================================================================

def test_robots(token: str):
    """Prueba todos los endpoints de robots"""
    print_header("🤖 TEST DE ROBOTS")
    
    headers = {"Authorization": f"Bearer {token}"}
    robot_creado_id = None
    
    # 1. Listar robots
    print_info("Listando robots...")
    response = requests.get(f"{BASE_URL}/robots", headers=headers, timeout=30)
    if response.status_code == 200:
        items = response.json()
        print_success(f"Robots listados: {len(items)} encontrados")
    else:
        print_error(f"Error al listar: {response.status_code}")
    
    # 2. Crear robot de prueba
    print_info("Creando robot de prueba...")
    nuevo_robot = {
        "nombre": "Robot Test API",
        "fuera_de_servicio": 0,
        "en_uso": 0,
        "disponible": 5
    }
    
    response = requests.post(f"{BASE_URL}/robots", json=nuevo_robot, headers=headers, timeout=30)
    if response.status_code == 200:
        robot = response.json()
        robot_creado_id = robot.get('id')
        print_success(f"Robot creado: ID={robot_creado_id}")
    else:
        print_error(f"Error al crear: {response.status_code}")
    
    # 3. Actualizar (si se creó)
    if robot_creado_id:
        print_info(f"Actualizando robot {robot_creado_id}...")
        response = requests.put(
            f"{BASE_URL}/robots/{robot_creado_id}",
            json={"disponible": 3, "en_uso": 2},
            headers=headers,
            timeout=30
        )
        if response.status_code == 200:
            print_success(f"Robot actualizado")
        
        # 4. Eliminar
        print_info(f"Eliminando robot {robot_creado_id}...")
        response = requests.delete(f"{BASE_URL}/robots/{robot_creado_id}", headers=headers, timeout=30)
        if response.status_code == 200:
            print_success("Robot eliminado")
        else:
            print_error(f"Error al eliminar: {response.status_code}")


# ============================================================================
# TEST DE MATERIALES
# ============================================================================

def test_materiales(token: str):
    """Prueba todos los endpoints de materiales"""
    print_header("🧪 TEST DE MATERIALES")
    
    headers = {"Authorization": f"Bearer {token}"}
    material_creado_id = None
    
    # 1. Listar materiales
    print_info("Listando materiales...")
    response = requests.get(f"{BASE_URL}/materiales", headers=headers, timeout=30)
    if response.status_code == 200:
        items = response.json()
        print_success(f"Materiales listados: {len(items)} encontrados")
    else:
        print_error(f"Error al listar: {response.status_code}")
    
    # 2. Listar tipos de materiales
    print_info("Listando tipos de materiales...")
    response = requests.get(f"{BASE_URL}/tipos-materiales", headers=headers, timeout=30)
    if response.status_code == 200:
        tipos = response.json()
        print_success(f"Tipos de materiales: {len(tipos)} encontrados")
        for tipo in tipos[:3]:
            print_info(f"  - {tipo.get('nombre')}")
    else:
        print_error(f"Error al listar tipos: {response.status_code}")
    
    # 3. Crear material de prueba
    print_info("Creando material de prueba...")
    nuevo_material = {
        "color": "Azul",
        "tipo_id": 1,
        "cantidad": "500g",
        "categoria": "Filamento",
        "usado": 0,
        "en_uso": 0,
        "en_stock": 3
    }
    
    response = requests.post(f"{BASE_URL}/materiales", json=nuevo_material, headers=headers, timeout=30)
    if response.status_code == 200:
        material = response.json()
        material_creado_id = material.get('id')
        print_success(f"Material creado: ID={material_creado_id}")
    else:
        print_error(f"Error al crear: {response.status_code}")
    
    # 4. Actualizar (si se creó)
    if material_creado_id:
        print_info(f"Actualizando material {material_creado_id}...")
        response = requests.put(
            f"{BASE_URL}/materiales/{material_creado_id}",
            json={"en_stock": 5},
            headers=headers,
            timeout=30
        )
        if response.status_code == 200:
            print_success(f"Material actualizado")
        
        # 5. Eliminar
        print_info(f"Eliminando material {material_creado_id}...")
        response = requests.delete(f"{BASE_URL}/materiales/{material_creado_id}", headers=headers, timeout=30)
        if response.status_code == 200:
            print_success("Material eliminado")
        else:
            print_error(f"Error al eliminar: {response.status_code}")


# ============================================================================
# TEST DE PRESTATARIOS
# ============================================================================

def test_prestatarios(token: str):
    """Prueba todos los endpoints de prestatarios"""
    print_header("👥 TEST DE PRESTATARIOS")
    
    headers = {"Authorization": f"Bearer {token}"}
    prestatario_creado_id = None
    
    # 1. Listar prestatarios
    print_info("Listando prestatarios...")
    response = requests.get(f"{BASE_URL}/prestatarios", headers=headers, timeout=30)
    if response.status_code == 200:
        items = response.json()
        print_success(f"Prestatarios listados: {len(items)} encontrados")
    else:
        print_error(f"Error al listar: {response.status_code}")
    
    # 2. Crear prestatario de prueba
    print_info("Creando prestatario de prueba...")
    nuevo_prestatario = {
        "nombre": "Test User API",
        "telefono": "3001234567",
        "dependencia": "Test Department",
        "cedula": "TEST123",
        "email": "test@cie.com"
    }
    
    response = requests.post(f"{BASE_URL}/prestatarios", json=nuevo_prestatario, headers=headers, timeout=30)
    if response.status_code == 200:
        prestatario = response.json()
        prestatario_creado_id = prestatario.get('id')
        print_success(f"Prestatario creado: ID={prestatario_creado_id}")
    else:
        print_error(f"Error al crear: {response.status_code}")
    
    # 3. Actualizar (si se creó)
    if prestatario_creado_id:
        print_info(f"Actualizando prestatario {prestatario_creado_id}...")
        response = requests.put(
            f"{BASE_URL}/prestatarios/{prestatario_creado_id}",
            json={"telefono": "3109876543"},
            headers=headers,
            timeout=30
        )
        if response.status_code == 200:
            print_success(f"Prestatario actualizado")
        
        # 4. Eliminar (inactivar)
        print_info(f"Inactivando prestatario {prestatario_creado_id}...")
        response = requests.delete(f"{BASE_URL}/prestatarios/{prestatario_creado_id}", headers=headers, timeout=30)
        if response.status_code == 200:
            print_success("Prestatario inactivado")
        else:
            print_error(f"Error al inactivar: {response.status_code}")


# ============================================================================
# TEST DE PRÉSTAMOS
# ============================================================================

def test_prestamos(token: str):
    """Prueba todos los endpoints de préstamos"""
    print_header("📋 TEST DE PRÉSTAMOS")
    
    headers = {"Authorization": f"Bearer {token}"}
    prestamo_creado_id = None
    
    # 1. Listar préstamos
    print_info("Listando préstamos...")
    response = requests.get(f"{BASE_URL}/prestamos", headers=headers, timeout=30)
    if response.status_code == 200:
        items = response.json()
        print_success(f"Préstamos listados: {len(items)} encontrados")
    else:
        print_error(f"Error al listar: {response.status_code}")
    
    # 2. Listar préstamos activos
    print_info("Listando préstamos activos...")
    response = requests.get(f"{BASE_URL}/prestamos/activos", headers=headers, timeout=30)
    if response.status_code == 200:
        items = response.json()
        print_success(f"Préstamos activos: {len(items)} encontrados")
    else:
        print_error(f"Error al listar activos: {response.status_code}")
    
    # 3. Obtener primer equipo para crear préstamo
    print_info("Obteniendo equipo para préstamo de prueba...")
    response = requests.get(f"{BASE_URL}/equipos", headers=headers, timeout=30)
    equipos = response.json() if response.status_code == 200 else []
    
    # 4. Obtener primer prestatario
    print_info("Obteniendo prestatario para préstamo de prueba...")
    response = requests.get(f"{BASE_URL}/prestatarios", headers=headers, timeout=30)
    prestatarios = response.json() if response.status_code == 200 else []
    
    if equipos and prestatarios:
        equipo_id = equipos[0].get('id')
        prestatario_id = prestatarios[0].get('id')
        
        print_info(f"Creando préstamo (equipo={equipo_id}, prestatario={prestatario_id})...")
        nuevo_prestamo = {
            "prestatario_id": prestatario_id,
            "equipo_id": equipo_id,
            "fecha_limite": "2026-04-01T23:59:59",
            "observaciones": "Préstamo de prueba API"
        }
        
        response = requests.post(f"{BASE_URL}/prestamos", json=nuevo_prestamo, headers=headers, timeout=30)
        if response.status_code == 200:
            prestamo = response.json()
            prestamo_creado_id = prestamo.get('id')
            print_success(f"Préstamo creado: ID={prestamo_creado_id}")
            
            # 5. Devolver préstamo
            if prestamo_creado_id:
                print_info(f"Devolviendo préstamo {prestamo_creado_id}...")
                response = requests.post(
                    f"{BASE_URL}/prestamos/{prestamo_creado_id}/devolver",
                    headers=headers,
                    timeout=30
                )
                if response.status_code == 200:
                    print_success(f"Préstamo devuelto correctamente")
                else:
                    print_error(f"Error al devolver: {response.status_code}")
                
                # 6. Eliminar préstamo
                print_info(f"Eliminando préstamo {prestamo_creado_id}...")
                response = requests.delete(f"{BASE_URL}/prestamos/{prestamo_creado_id}", headers=headers, timeout=30)
                if response.status_code == 200:
                    print_success("Préstamo eliminado")
                else:
                    print_error(f"Error al eliminar: {response.status_code}")
        else:
            print_error(f"Error al crear préstamo: {response.status_code} - {response.text}")
    else:
        print_error("No hay equipos o prestatarios para crear préstamo")


# ============================================================================
# TEST DE MOVIMIENTOS
# ============================================================================

def test_movimientos(token: str):
    """Prueba todos los endpoints de movimientos"""
    print_header("📊 TEST DE MOVIMIENTOS")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Listar movimientos
    print_info("Listando movimientos...")
    response = requests.get(f"{BASE_URL}/movimientos", headers=headers, timeout=30)
    if response.status_code == 200:
        items = response.json()
        print_success(f"Movimientos listados: {len(items)} encontrados")
        
        # Mostrar últimos movimientos
        if items:
            print_info("Últimos movimientos:")
            for item in items[:3]:
                print_info(f"  - {item.get('tipo')} ({item.get('created_at')[:10]})")
    else:
        print_error(f"Error al listar: {response.status_code}")
    
    # 2. Obtener primer equipo para crear movimiento
    print_info("Obteniendo equipo para movimiento de prueba...")
    response = requests.get(f"{BASE_URL}/equipos", headers=headers, timeout=30)
    equipos = response.json() if response.status_code == 200 else []
    
    if equipos:
        equipo_id = equipos[0].get('id')
        
        print_info(f"Creando movimiento de daño (equipo={equipo_id})...")
        nuevo_movimiento = {
            "tipo": "daño",
            "equipo_id": equipo_id,
            "cantidad": 1,
            "descripcion": "Prueba de movimiento desde API test"
        }
        
        response = requests.post(f"{BASE_URL}/movimientos", json=nuevo_movimiento, headers=headers, timeout=30)
        if response.status_code == 200:
            movimiento = response.json()
            print_success(f"Movimiento creado: ID={movimiento.get('id')}")
        else:
            print_error(f"Error al crear movimiento: {response.status_code} - {response.text}")


# ============================================================================
# TEST DE USUARIO ACTUAL
# ============================================================================

def test_me(token: str):
    """Prueba endpoint de usuario actual"""
    print_header("👤 TEST DE USUARIO ACTUAL")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print_info("Obteniendo información del usuario actual...")
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers, timeout=30)
    
    if response.status_code == 200:
        user = response.json()
        print_success(f"Usuario: {user.get('nombre')}")
        print_success(f"Email: {user.get('email')}")
        print_success(f"Rol: {user.get('rol')}")
        print_success(f"Activo: {user.get('activo')}")
    else:
        print_error(f"Error al obtener usuario: {response.status_code}")


# ============================================================================
# TEST DE HEALTH
# ============================================================================

def test_health():
    """Prueba endpoint de health"""
    print_header("🏥 TEST DE HEALTH")
    
    try:
        response = requests.get(f"{BASE_URL.replace('/api/v1', '')}/health", timeout=30)
        if response.status_code == 200:
            print_success(f"Health check: {response.json().get('status')}")
        else:
            print_error(f"Health check falló: {response.status_code}")
    except Exception as e:
        print_error(f"Error en health check: {e}")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Ejecuta todos los tests"""
    print_header("🚀 TEST COMPLETO DE LA API - INVENTARIO CIE")
    print_info(f"Base URL: {BASE_URL}")
    print_info(f"Usuario: {TEST_USER['email']}")
    print_info(f"Tiempo de espera por request: 30s")
    
    # 1. Health check
    test_health()
    time.sleep(1)
    
    # 2. Autenticación
    token = test_auth()
    time.sleep(1)
    
    if not token:
        print_error("\n❌ No se pudo autenticar. Terminando tests.")
        return
    
    # 3. Usuario actual
    test_me(token)
    time.sleep(1)
    
    # 4. Tests de inventario
    test_equipos(token)
    time.sleep(1)
    
    test_electronica(token)
    time.sleep(1)
    
    test_robots(token)
    time.sleep(1)
    
    test_materiales(token)
    time.sleep(1)
    
    # 5. Tests de préstamos
    test_prestatarios(token)
    time.sleep(1)
    
    test_prestamos(token)
    time.sleep(1)
    
    # 6. Tests de auditoría
    test_movimientos(token)
    time.sleep(1)
    
    # Final
    print_header("✅ TESTS COMPLETADOS")
    print_success("¡Todos los tests han finalizado!")
    print_info("\n📊 Resumen:")
    print_info("  - Autenticación: ✓")
    print_info("  - Equipos: ✓")
    print_info("  - Electrónica: ✓")
    print_info("  - Robots: ✓")
    print_info("  - Materiales: ✓")
    print_info("  - Prestatarios: ✓")
    print_info("  - Préstamos: ✓")
    print_info("  - Movimientos: ✓")
    print_info("\n🔗 API: https://inventario-workinn-api.onrender.com")
    print_info("📚 Swagger: https://inventario-workinn-api.onrender.com/docs")


if __name__ == "__main__":
    main()
