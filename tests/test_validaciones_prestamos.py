#!/usr/bin/env python3
"""
Test de Validaciones de Préstamos - Inventario CIE
===================================================

Este script prueba las validaciones CRÍTICAS del sistema de préstamos:
1. NO permitir prestar un elemento que YA ESTÁ PRESTADO
2. NO permitir prestar un elemento que está DAÑADO
3. NO permitir prestar un elemento en MANTENIMIENTO
4. SÍ permitir prestar un elemento DISPONIBLE
5. Validar que se pueda devolver y luego prestar de nuevo

Uso:
    python test_validaciones_prestamos.py

Requisitos:
    pip install requests

Autor: Eddy - Inventario CIE
Fecha: Marzo 2026
"""

import requests
import time
from datetime import datetime
from typing import Dict, Optional

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

BASE_URL = "https://inventario-workinn-api.onrender.com/api/v1"
BASE_URL_ROOT = "https://inventario-workinn-api.onrender.com"

ADMIN_USER = {
    "email": "eduardopimienta@americana.edu.co",
    "password": "Admin123!"
}

# Colores
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# ============================================================================
# UTILIDADES
# ============================================================================

def print_header(text: str):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(80)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.RESET}\n")

def print_section(text: str):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'─'*80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'─'*80}{Colors.RESET}\n")

def print_success(text: str):
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text: str):
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_info(text: str):
    print(f"{Colors.BLUE}ℹ {text}{Colors.RESET}")

def print_warning(text: str):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")

def print_test_result(test_name: str, passed: bool, expected: str, actual: str):
    """Imprimir resultado de un test individual"""
    status = f"{Colors.GREEN}✓ PASÓ{Colors.RESET}" if passed else f"{Colors.RED}✗ FALLÓ{Colors.RESET}"
    print(f"\n{status} - {test_name}")
    print(f"   Esperado: {expected}")
    print(f"   Obtenido: {actual}")
    return passed

# ============================================================================
# CLASE DE TEST
# ============================================================================

class ValidacionesPrestamosTest:
    """Test de validaciones del sistema de préstamos"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.token: Optional[str] = None
        self.headers: Dict[str, str] = {}
        self.test_ids: Dict[str, int] = {}
        self.passed = 0
        self.failed = 0
        
    def login(self, email: str, password: str) -> bool:
        """Iniciar sesión"""
        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                json={"email": email, "password": password},
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('access_token')
                self.headers = {
                    'Authorization': f'Bearer {self.token}',
                    'Content-Type': 'application/json'
                }
                print_success(f"Login exitoso: {data.get('user', {}).get('email')}")
                return True
            
            print_error(f"Login falló: {response.status_code}")
            return False
            
        except Exception as e:
            print_error(f"Error en login: {str(e)}")
            return False
    
    def get_data(self, endpoint: str) -> list:
        """Obtener datos de un endpoint"""
        try:
            response = requests.get(
                f"{self.base_url}{endpoint}",
                headers=self.headers,
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()
            
            return []
            
        except Exception as e:
            print_error(f"Error al obtener {endpoint}: {str(e)}")
            return []
    
    def create_prestatario(self, nombre: str, dependencia: str) -> Optional[int]:
        """Crear prestatario y retornar ID"""
        try:
            data = {
                "nombre": nombre,
                "telefono": "3001234567",
                "dependencia": dependencia,
                "cedula": f"TEST{int(time.time())}",
                "email": f"test{int(time.time())}@cie.com"
            }
            
            response = requests.post(
                f"{self.base_url}/prestatarios",
                json=data,
                headers=self.headers,
                timeout=60
            )
            
            if response.status_code == 200:
                prestatario = response.json()
                return prestatario.get('id')
            
            return None
            
        except Exception as e:
            print_error(f"Error al crear prestatario: {str(e)}")
            return None
    
    def create_prestamo(self, equipo_id: int, prestatario_id: int, 
                       fecha_limite: str = None) -> tuple:
        """Crear préstamo y retornar (success, status_code, response_data)"""
        try:
            data = {
                "prestatario_id": prestatario_id,
                "equipo_id": equipo_id,
                "fecha_limite": fecha_limite or "2026-12-31T23:59:59",
                "observaciones": "Préstamo de prueba - Test de validaciones"
            }
            
            response = requests.post(
                f"{self.base_url}/prestamos",
                json=data,
                headers=self.headers,
                timeout=60
            )
            
            return (
                response.status_code == 200,
                response.status_code,
                response.json() if response.status_code == 200 else response.text
            )
            
        except Exception as e:
            print_error(f"Error al crear préstamo: {str(e)}")
            return (False, 0, str(e))
    
    def devolver_prestamo(self, prestamo_id: int) -> bool:
        """Devolver préstamo"""
        try:
            response = requests.post(
                f"{self.base_url}/prestamos/{prestamo_id}/devolver",
                headers=self.headers,
                timeout=60
            )
            
            return response.status_code == 200
            
        except Exception as e:
            print_error(f"Error al devolver: {str(e)}")
            return False
    
    def update_equipo_estado(self, equipo_id: int, estado: str) -> bool:
        """Actualizar estado de un equipo"""
        try:
            response = requests.put(
                f"{self.base_url}/equipos/{equipo_id}",
                json={"estado": estado},
                headers=self.headers,
                timeout=60
            )
            
            return response.status_code == 200
            
        except Exception as e:
            print_error(f"Error al actualizar equipo: {str(e)}")
            return False
    
    def get_equipo(self, equipo_id: int) -> Optional[Dict]:
        """Obtener equipo por ID"""
        try:
            response = requests.get(
                f"{self.base_url}/equipos/{equipo_id}",
                headers=self.headers,
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()
            
            return None
            
        except Exception as e:
            print_error(f"Error al obtener equipo: {str(e)}")
            return None
    
    def get_prestamos_activos(self) -> list:
        """Obtener préstamos activos"""
        try:
            response = requests.get(
                f"{self.base_url}/prestamos/activos",
                headers=self.headers,
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()
            
            return []
            
        except Exception as e:
            print_error(f"Error al obtener préstamos activos: {str(e)}")
            return []
    
    def check_equipo_prestado(self, equipo_id: int) -> bool:
        """Verificar si un equipo está prestado (tiene préstamo activo)"""
        prestamos_activos = self.get_prestamos_activos()
        
        for prestamo in prestamos_activos:
            if prestamo.get('equipo_id') == equipo_id:
                return True
        
        return False
    
    # ========================================================================
    # TESTS ESPECÍFICOS
    # ========================================================================
    
    def test_01_prestar_elemento_disponible(self) -> bool:
        """TEST 1: SÍ permitir prestar un elemento DISPONIBLE"""
        print_section("TEST 1: Prestar Elemento Disponible")
        
        # 1. Obtener primer equipo disponible
        equipos = self.get_data('/equipos')
        
        # Buscar uno que esté disponible
        equipo_disponible = None
        for equipo in equipos:
            if equipo.get('estado') == 'disponible':
                # Verificar que no tenga préstamo activo
                if not self.check_equipo_prestado(equipo.get('id')):
                    equipo_disponible = equipo
                    break
        
        if not equipo_disponible:
            print_warning("No hay equipos disponibles para test")
            return True  # No es fallo del test
        
        print_info(f"Equipo seleccionado: {equipo_disponible.get('nombre')} ({equipo_disponible.get('codigo')})")
        print_info(f"Estado: {equipo_disponible.get('estado')}")
        
        # 2. Crear prestatario
        prestatario_id = self.create_prestatario("Test Usuario 1", "Test Dept 1")
        if not prestatario_id:
            print_error("No se pudo crear prestatario")
            self.failed += 1
            return False
        
        print_info(f"Prestatario creado: ID={prestatario_id}")
        
        # 3. Intentar crear préstamo
        success, status_code, response = self.create_prestamo(
            equipo_disponible.get('id'),
            prestatario_id
        )
        
        # 4. Validar resultado
        if success:
            prestamo_id = response.get('id')
            self.test_ids['prestamo_1'] = prestamo_id
            self.test_ids['equipo_1'] = equipo_disponible.get('id')
            self.test_ids['prestatario_1'] = prestatario_id
            
            print_success(f"Préstamo creado exitosamente: ID={prestamo_id}")
            print_success("TEST 1: PASÓ ✓")
            self.passed += 1
            return True
        else:
            print_error(f"Préstamo falló: {status_code} - {response}")
            print_error("TEST 1: FALLÓ ✗")
            self.failed += 1
            return False
    
    def test_02_no_prestar_elemento_ya_prestado(self) -> bool:
        """TEST 2: NO permitir prestar un elemento que YA ESTÁ PRESTADO"""
        print_section("TEST 2: No Prestar Elemento Ya Prestado")
        
        # Usar el equipo del test anterior
        equipo_id = self.test_ids.get('equipo_1')
        if not equipo_id:
            print_warning("No hay equipo de test anterior")
            return True
        
        equipo = self.get_equipo(equipo_id)
        if not equipo:
            print_warning(f"Equipo {equipo_id} no encontrado")
            return True
        
        print_info(f"Equipo: {equipo.get('nombre')} ({equipo.get('codigo')})")
        
        # Verificar que tiene préstamo activo
        prestamos_activos = self.get_prestamos_activos()
        tiene_prestamo = any(p.get('equipo_id') == equipo_id for p in prestamos_activos)
        
        if not tiene_prestamo:
            print_warning("El equipo no tiene préstamo activo - saltando test")
            return True
        
        print_info(f"El equipo TIENE préstamo activo")
        
        # 1. Crear OTRO prestatario
        prestatario_id = self.create_prestatario("Test Usuario 2", "Test Dept 2")
        if not prestatario_id:
            print_error("No se pudo crear prestatario")
            self.failed += 1
            return False
        
        # 2. Intentar crear SEGUNDO préstamo para el MISMO equipo
        print_info("Intentando crear SEGUNDO préstamo para el MISMO equipo...")
        success, status_code, response = self.create_prestamo(equipo_id, prestatario_id)
        
        # 3. Validar resultado - DEBE FALLAR
        if not success:
            print_success(f"Préstamo RECHAZADO correctamente: {status_code}")
            print_success("TEST 2: PASÓ ✓ - El sistema NO permite doble préstamo")
            self.passed += 1
            return True
        else:
            print_error(f"Préstamo CREADO indebidamente: {response}")
            print_error("TEST 2: FALLÓ ✗ - El sistema permitió doble préstamo!")
            self.failed += 1
            return False
    
    def test_03_no_prestar_elemento_danado(self) -> bool:
        """TEST 3: NO permitir prestar un elemento DAÑADO"""
        print_section("TEST 3: No Prestar Elemento Dañado")
        
        # 1. Obtener equipos y buscar uno dañado
        equipos = self.get_data('/equipos')
        
        equipo_danado = None
        for equipo in equipos:
            if equipo.get('estado') == 'dañado':
                equipo_danado = equipo
                break
        
        # Si no hay dañado, marcar uno temporalmente
        if not equipo_danado:
            print_info("No hay equipos dañados - creando uno temporalmente...")
            
            # Usar un equipo de prueba
            equipos_disponibles = [e for e in equipos if e.get('estado') == 'disponible']
            if not equipos_disponibles:
                print_warning("No hay equipos disponibles para marcar como dañado")
                return True
            
            equipo_temp = equipos_disponibles[0]
            
            # Marcar como dañado
            if self.update_equipo_estado(equipo_temp.get('id'), 'dañado'):
                equipo_danado = self.get_equipo(equipo_temp.get('id'))
                self.test_ids['equipo_danado_temp'] = equipo_danado.get('id')
                print_info(f"Equipo marcado como dañado: {equipo_danado.get('nombre')}")
        
        if not equipo_danado:
            print_warning("No se pudo obtener equipo dañado")
            return True
        
        print_info(f"Equipo dañado: {equipo_danado.get('nombre')}")
        print_info(f"Estado: {equipo_danado.get('estado')}")
        
        # 2. Crear prestatario
        prestatario_id = self.create_prestatario("Test Usuario 3", "Test Dept 3")
        if not prestatario_id:
            print_error("No se pudo crear prestatario")
            self.failed += 1
            return False
        
        # 3. Intentar crear préstamo - DEBE FALLAR
        print_info("Intentando crear préstamo de equipo DAÑADO...")
        success, status_code, response = self.create_prestamo(
            equipo_danado.get('id'),
            prestatario_id
        )
        
        # 4. Validar resultado - DEBE FALLAR
        if not success:
            print_success(f"Préstamo RECHAZADO correctamente: {status_code}")
            print_success("TEST 3: PASÓ ✓ - El sistema NO permite prestar equipos dañados")
            self.passed += 1
            return True
        else:
            print_error(f"Préstamo CREADO indebidamente: {response}")
            print_error("TEST 3: FALLÓ ✗ - El sistema permitió prestar equipo dañado!")
            self.failed += 1
            return False
    
    def test_04_devolver_y_prestar_de_nuevo(self) -> bool:
        """TEST 4: Devolver elemento y permitir prestarlo de nuevo"""
        print_section("TEST 4: Devolver y Volver a Prestar")
        
        # Usar el préstamo del test 1
        prestamo_id = self.test_ids.get('prestamo_1')
        equipo_id = self.test_ids.get('equipo_1')
        
        if not prestamo_id or not equipo_id:
            print_warning("No hay préstamo de test anterior")
            return True
        
        print_info(f"Préstamo a devolver: ID={prestamo_id}")
        print_info(f"Equipo: ID={equipo_id}")
        
        # 1. Devolver el préstamo
        print_info("Devolviendo préstamo...")
        devuelto = self.devolver_prestamo(prestamo_id)
        
        if not devuelto:
            print_error("No se pudo devolver el préstamo")
            self.failed += 1
            return False
        
        print_success(f"Préstamo devuelto exitosamente")
        
        # 2. Verificar que el equipo ya no tiene préstamo activo
        prestamos_activos = self.get_prestamos_activos()
        tiene_prestamo = any(p.get('equipo_id') == equipo_id for p in prestamos_activos)
        
        if tiene_prestamo:
            print_error("El equipo aún figura con préstamo activo")
            self.failed += 1
            return False
        
        print_success("El equipo ya NO tiene préstamo activo")
        
        # 3. Crear NUEVO prestatario
        prestatario_id = self.create_prestatario("Test Usuario 4", "Test Dept 4")
        if not prestatario_id:
            print_error("No se pudo crear prestatario")
            self.failed += 1
            return False
        
        # 4. Intentar crear NUEVO préstamo para el MISMO equipo
        print_info("Intentando crear NUEVO préstamo para el MISMO equipo...")
        success, status_code, response = self.create_prestamo(equipo_id, prestatario_id)
        
        # 5. Validar resultado - DEBE FUNCIONAR
        if success:
            print_success(f"Nuevo préstamo creado exitosamente: ID={response.get('id')}")
            print_success("TEST 4: PASÓ ✓ - El sistema permite re-prestar después de devolver")
            self.passed += 1
            return True
        else:
            print_error(f"Préstamo falló: {status_code} - {response}")
            print_error("TEST 4: FALLÓ ✗ - El sistema NO permitió re-prestar!")
            self.failed += 1
            return False
    
    def test_05_no_prestar_elemento_mantenimiento(self) -> bool:
        """TEST 5: NO permitir prestar un elemento en MANTENIMIENTO"""
        print_section("TEST 5: No Prestar Elemento en Mantenimiento")
        
        # 1. Obtener equipos
        equipos = self.get_data('/equipos')
        
        # Buscar uno en mantenimiento o crear uno temporal
        equipo_mantenimiento = None
        for equipo in equipos:
            if equipo.get('estado') == 'mantenimiento':
                equipo_mantenimiento = equipo
                break
        
        # Si no hay, marcar uno temporalmente
        if not equipo_mantenimiento:
            print_info("No hay equipos en mantenimiento - creando uno temporalmente...")
            
            equipos_disponibles = [e for e in equipos if e.get('estado') == 'disponible']
            if not equipos_disponibles:
                print_warning("No hay equipos disponibles")
                return True
            
            equipo_temp = equipos_disponibles[0]
            
            if self.update_equipo_estado(equipo_temp.get('id'), 'mantenimiento'):
                equipo_mantenimiento = self.get_equipo(equipo_temp.get('id'))
                self.test_ids['equipo_mantenimiento_temp'] = equipo_mantenimiento.get('id')
                print_info(f"Equipo marcado como mantenimiento: {equipo_mantenimiento.get('nombre')}")
        
        if not equipo_mantenimiento:
            print_warning("No se pudo obtener equipo en mantenimiento")
            return True
        
        print_info(f"Equipo en mantenimiento: {equipo_mantenimiento.get('nombre')}")
        print_info(f"Estado: {equipo_mantenimiento.get('estado')}")
        
        # 2. Crear prestatario
        prestatario_id = self.create_prestatario("Test Usuario 5", "Test Dept 5")
        if not prestatario_id:
            print_error("No se pudo crear prestatario")
            self.failed += 1
            return False
        
        # 3. Intentar crear préstamo - DEBE FALLAR
        print_info("Intentando crear préstamo de equipo en MANTENIMIENTO...")
        success, status_code, response = self.create_prestamo(
            equipo_mantenimiento.get('id'),
            prestatario_id
        )
        
        # 4. Validar resultado - DEBE FALLAR
        if not success:
            print_success(f"Préstamo RECHAZADO correctamente: {status_code}")
            print_success("TEST 5: PASÓ ✓ - El sistema NO permite prestar equipos en mantenimiento")
            self.passed += 1
            return True
        else:
            print_error(f"Préstamo CREADO indebidamente: {response}")
            print_error("TEST 5: FALLÓ ✗ - El sistema permitió prestar equipo en mantenimiento!")
            self.failed += 1
            return False
    
    def cleanup(self):
        """Limpiar recursos creados durante los tests"""
        print_section("Limpieza de Recursos")
        
        # Restaurar equipos temporales a 'disponible'
        for key in ['equipo_danado_temp', 'equipo_mantenimiento_temp']:
            equipo_id = self.test_ids.get(key)
            if equipo_id:
                print_info(f"Restaurando equipo {equipo_id} a 'disponible'...")
                self.update_equipo_estado(equipo_id, 'disponible')
        
        print_success("Limpieza completada")
    
    def print_summary(self):
        """Imprimir resumen de tests"""
        print_header("RESUMEN DE TESTS DE VALIDACIÓN")
        
        total = self.passed + self.failed
        
        print(f"{Colors.BOLD}Tests ejecutados:{Colors.RESET} {total}")
        print(f"{Colors.GREEN}✓ Pasaron:{Colors.RESET} {self.passed}")
        print(f"{Colors.RED}✗ Fallaron:{Colors.RESET} {self.failed}")
        print()
        
        if self.failed == 0:
            print(f"{Colors.GREEN}{Colors.BOLD}🎉 ¡TODOS LOS TESTS PASARON! 🎉{Colors.RESET}")
            print(f"\n{Colors.CYAN}El sistema de préstamos tiene las validaciones correctas:{Colors.RESET}")
            print(f"  ✓ No permite doble préstamo")
            print(f"  ✓ No permite prestar equipos dañados")
            print(f"  ✓ No permite prestar equipos en mantenimiento")
            print(f"  ✓ Permite re-prestar después de devolver")
            return 0
        else:
            print(f"{Colors.RED}{Colors.BOLD}❌ {self.failed} TEST(S) FALLARON ❌{Colors.RESET}")
            print(f"\n{Colors.YELLOW}Se encontraron problemas en las validaciones de préstamos.{Colors.RESET}")
            return 1
    
    def ejecutar_tests(self) -> int:
        """Ejecutar todos los tests"""
        print_header("🧪 TEST DE VALIDACIONES DE PRÉSTAMOS")
        print_info(f"API: {BASE_URL}")
        print_info(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Login
        print_section("Autenticación")
        if not self.login(ADMIN_USER['email'], ADMIN_USER['password']):
            print_error("No se pudo autenticar")
            return 1
        
        # Ejecutar tests
        self.test_01_prestar_elemento_disponible()
        self.test_02_no_prestar_elemento_ya_prestado()
        self.test_03_no_prestar_elemento_danado()
        self.test_04_devolver_y_prestar_de_nuevo()
        self.test_05_no_prestar_elemento_mantenimiento()
        
        # Limpieza
        self.cleanup()
        
        # Resumen
        return self.print_summary()

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Función principal"""
    tester = ValidacionesPrestamosTest(BASE_URL)
    return tester.ejecutar_tests()

if __name__ == "__main__":
    import sys
    sys.exit(main())
