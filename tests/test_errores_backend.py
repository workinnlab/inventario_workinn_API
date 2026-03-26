#!/usr/bin/env python3
"""
TEST DE ERRORES DE BACKEND - Inventario CIE
=============================================

Este script prueba TODOS los errores de backend reportados.

Ejecución:
    python tests/test_errores_backend.py

Requisitos:
    pip install requests

Autor: Eddy - Inventario CIE
Fecha: Marzo 2026
"""

import requests
import time
import sys
from datetime import datetime, timedelta
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

# Colores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# ============================================================================
# CLASE DE TEST
# ============================================================================

class TestErroresBackend:
    """Test de errores de backend"""
    
    def __init__(self, base_url: str, base_url_root: str):
        self.base_url = base_url
        self.base_url_root = base_url_root
        self.token: Optional[str] = None
        self.headers: Dict[str, str] = {}
        self.test_ids: Dict[str, int] = {}
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        
    def login(self, email: str, password: str) -> bool:
        """Iniciar sesión y obtener token"""
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
                return True
            
            return False
            
        except Exception as e:
            print(f"Error en login: {str(e)}")
            return False
    
    def make_request(self, method: str, endpoint: str, data: Optional[Dict] = None,
                     headers: Optional[Dict] = None, timeout: int = 120) -> Optional[requests.Response]:
        """Hacer una request a la API (timeout aumentado a 120s para Render cold start)"""
        url = f"{self.base_url}{endpoint}"
        
        if headers is None:
            headers = {}
        
        if self.token and 'Authorization' not in headers:
            headers['Authorization'] = f'Bearer {self.token}'
        
        if 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json'
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, timeout=timeout, params=data)
            elif method.upper() == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=timeout)
            elif method.upper() == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=timeout)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=timeout)
            else:
                return None
                
            return response
            
        except Exception as e:
            return None
    
    def test_result(self, error_num: str, test_name: str, passed: bool, expected: str, actual: str):
        """Imprimir resultado de un test"""
        status = f"{Colors.GREEN}✓ PASÓ{Colors.RESET}" if passed else f"{Colors.RED}✗ FALLÓ{Colors.RESET}"
        print(f"\n{status} [Error #{error_num}] {test_name}")
        
        if not passed:
            print(f"   Esperado: {expected}")
            print(f"   Obtenido: {actual}")
            self.failed += 1
        else:
            self.passed += 1
    
    # ========================================================================
    # TESTS DE ERRORES
    # ========================================================================
    
    def test_error_2_dispositivo_no_encontrado(self):
        """Error #2: "Dispositivo no encontrado" al actualizar"""
        # Crear equipo de prueba
        r1 = self.make_request('POST', '/equipos', {
            "nombre": f"Test Error 2 {int(time.time())}",
            "marca": "Test",
            "codigo": f"TEST-ERR2-{int(time.time())}",
            "estado": "disponible"
        })
        
        if r1 and r1.status_code == 200:
            equipo_id = r1.json().get('id')
            self.test_ids['error_2_equipo'] = equipo_id
            
            # Intentar actualizar
            r2 = self.make_request('PUT', f'/equipos/{equipo_id}', {
                "estado": "dañado"
            })
            
            passed = r2 and r2.status_code == 200
            self.test_result("2", "Actualizar equipo (dispositivo no encontrado)", 
                           passed, "200 OK", str(r2.status_code) if r2 else "Error")
        else:
            self.failed += 1
            self.test_result("2", "Actualizar equipo (setup falló)", 
                           False, "200 OK", str(r1.status_code) if r1 else "Error")
    
    def test_error_3_devolucion_actualiza_equipo(self):
        """Error #3: Devolución no actualiza estado del equipo"""
        # Crear equipo
        r1 = self.make_request('POST', '/equipos', {
            "nombre": f"Test Error 3 {int(time.time())}",
            "marca": "Test",
            "codigo": f"TEST-ERR3-{int(time.time())}",
            "estado": "disponible"
        })
        
        if r1 and r1.status_code == 200:
            equipo_id = r1.json().get('id')
            
            # Crear prestatario
            r2 = self.make_request('POST', '/prestatarios', {
                "nombre": f"Test {int(time.time())}",
                "dependencia": "Test",
                "email": f"test{int(time.time())}@cie.com"
            })
            
            if r2 and r2.status_code == 200:
                prestatario_id = r2.json().get('id')
                
                # Crear préstamo
                r3 = self.make_request('POST', '/prestamos', {
                    "prestatario_id": prestatario_id,
                    "equipo_id": equipo_id
                })
                
                if r3 and r3.status_code == 200:
                    prestamo_id = r3.json().get('id')
                    
                    # Verificar que equipo está 'prestado'
                    r4 = self.make_request('GET', f'/equipos/{equipo_id}')
                    estado_antes = r4.json().get('estado') if r4 else None
                    
                    # Devolver préstamo
                    r5 = self.make_request('POST', f'/prestamos/{prestamo_id}/devolver')
                    
                    # Verificar que equipo está 'disponible'
                    r6 = self.make_request('GET', f'/equipos/{equipo_id}')
                    estado_despues = r6.json().get('estado') if r6 else None
                    
                    passed = estado_antes == 'prestado' and estado_despues == 'disponible'
                    self.test_result("3", "Devolución actualiza estado del equipo",
                                   passed, "disponible", estado_despues)
                    return
        
        self.failed += 1
        self.test_result("3", "Devolución actualiza (setup falló)", False, "disponible", "Error en setup")
    
    def test_error_6_prestamos_vencidos_devolver(self):
        """Error #6: Préstamos vencidos no se pueden devolver"""
        print("\n[DEBUG Error #6] Iniciando test...")

        # Paso 1: Crear equipo
        r1 = self.make_request('POST', '/equipos', {
            "nombre": f"Test Error 6 {int(time.time())}",
            "marca": "Test",
            "codigo": f"TEST-ERR6-{int(time.time())}",
            "estado": "disponible"
        })

        if not (r1 and r1.status_code == 200):
            self.failed += 1
            self.test_result("6", "Crear equipo (setup)", False, "200 OK", str(r1.status_code) if r1 else "Error")
            return

        equipo_id = r1.json().get('id')
        print(f"[DEBUG] Equipo creado: ID={equipo_id}")

        # Paso 2: Crear prestatario ACTIVO
        r2 = self.make_request('POST', '/prestatarios', {
            "nombre": f"Test Activo {int(time.time())}",
            "dependencia": "Test",
            "email": f"testactivo{int(time.time())}@cie.com",
            "activo": True
        })

        if not (r2 and r2.status_code == 200):
            self.failed += 1
            self.test_result("6", "Crear prestatario (setup)", False, "200 OK", str(r2.status_code) if r2 else "Error")
            return

        prestatario_id = r2.json().get('id')
        print(f"[DEBUG] Prestatario creado: ID={prestatario_id}")

        # Paso 3: Crear préstamo CON fecha FUTURA (no se puede con fecha pasada)
        from datetime import datetime, timedelta
        fecha_futura = (datetime.now() + timedelta(days=7)).isoformat().replace('+00:00', 'Z')

        print(f"[DEBUG] Creando préstamo: prestatario_id={prestatario_id}, equipo_id={equipo_id}, fecha={fecha_futura}")

        r3 = self.make_request('POST', '/prestamos', {
            "prestatario_id": prestatario_id,
            "equipo_id": equipo_id,
            "fecha_limite": fecha_futura
        })

        print(f"[DEBUG] Response crear préstamo: Status={r3.status_code if r3 else 'None'}, Text={r3.text[:300] if r3 and hasattr(r3, 'text') else 'None'}")

        if not (r3 and r3.status_code == 200):
            self.failed += 1
            self.test_result("6", "Crear préstamo (setup)", False, "200 OK", str(r3.status_code) if r3 else f"Error: {r3.text[:100] if r3 and hasattr(r3, 'text') else 'None'}")
            return

        prestamo_id = r3.json().get('id')
        print(f"[DEBUG] Préstamo creado: ID={prestamo_id}, fecha_limite={fecha_futura}")

        # Paso 4: Actualizar préstamo para que esté VENCIDO
        # Cambiar fecha_limite al pasado y estado a 'vencido'
        fecha_pasado = (datetime.now() - timedelta(days=30)).isoformat().replace('+00:00', 'Z')

        r4 = self.make_request('PUT', f'/prestamos/{prestamo_id}', {
            "fecha_limite": fecha_pasado,
            "estado": "vencido"
        })

        if not (r4 and r4.status_code == 200):
            self.failed += 1
            self.test_result("6", "Actualizar a vencido (setup)", False, "200 OK", str(r4.status_code) if r4 else f"Error: {r4.text[:100] if r4 else 'None'}")
            return

        print(f"[DEBUG] Préstamo actualizado a vencido")

        # Paso 5: Intentar DEVOLVER el préstamo vencido (ESTO ES LO QUE QUEREMOS PROBAR)
        r5 = self.make_request('POST', f'/prestamos/{prestamo_id}/devolver')

        print(f"[DEBUG] Devolver préstamo: Status={r5.status_code if r5 else 'Error'}, Response={r5.text[:200] if r5 else 'None'}")

        # El test PASÓ si podemos devolver un préstamo vencido
        passed = r5 and r5.status_code == 200
        self.test_result("6", "Devolver préstamo vencido",
                       passed, "200 OK",
                       str(r5.status_code) if r5 else f"Error: {r5.text[:100] if hasattr(r5, 'text') else 'None'}")
    
    def test_error_8_editar_equipo(self):
        """Error #8: No deja editar equipos"""
        # Crear equipo
        r1 = self.make_request('POST', '/equipos', {
            "nombre": f"Test Error 8 {int(time.time())}",
            "marca": "Test",
            "codigo": f"TEST-ERR8-{int(time.time())}",
            "estado": "disponible"
        })
        
        if r1 and r1.status_code == 200:
            equipo_id = r1.json().get('id')
            
            # Intentar editar
            r2 = self.make_request('PUT', f'/equipos/{equipo_id}', {
                "nombre": "Editado Test"
            })
            
            passed = r2 and r2.status_code == 200
            self.test_result("8", "Editar equipo",
                           passed, "200 OK", str(r2.status_code) if r2 else "Error")
        else:
            self.failed += 1
            self.test_result("8", "Editar equipo (setup falló)",
                           False, "200 OK", str(r1.status_code) if r1 else "Error")
    
    def test_error_8_eliminar_equipo(self):
        """Error #8: No deja eliminar equipos"""
        # Crear equipo
        r1 = self.make_request('POST', '/equipos', {
            "nombre": f"Test Error 8 Delete {int(time.time())}",
            "marca": "Test",
            "codigo": f"TEST-ERR8D-{int(time.time())}",
            "estado": "disponible"
        })
        
        if r1 and r1.status_code == 200:
            equipo_id = r1.json().get('id')
            
            # Intentar eliminar
            r2 = self.make_request('DELETE', f'/equipos/{equipo_id}')
            
            passed = r2 and r2.status_code == 200
            self.test_result("8", "Eliminar equipo",
                           passed, "200 OK", str(r2.status_code) if r2 else "Error")
        else:
            self.failed += 1
            self.test_result("8", "Eliminar equipo (setup falló)",
                           False, "200 OK", str(r1.status_code) if r1 else "Error")
    
    def test_error_4_notificaciones_endpoint(self):
        """Error #4: Notificaciones - Verificar endpoints"""
        # Probar endpoint de préstamos por vencer
        r1 = self.make_request('GET', '/prestamos/por-vencer?dias=7')
        
        # Probar endpoint de stock mínimo
        r2 = self.make_request('GET', '/materiales/stock-minimo?minimo=5')
        
        # Probar endpoint de equipos dañados
        r3 = self.make_request('GET', '/equipos?estado=dañado')
        
        passed = all([
            r1 and r1.status_code == 200,
            r2 and r2.status_code == 200,
            r3 and r3.status_code == 200
        ])
        
        self.test_result("4", "Endpoints de notificaciones",
                       passed, "200 OK (3 endpoints)", 
                       f"r1={r1.status_code if r1 else 'Error'}, "
                       f"r2={r2.status_code if r2 else 'Error'}, "
                       f"r3={r3.status_code if r3 else 'Error'}")
    
    def test_error_5_graficas_endpoint(self):
        """Error #5: Gráficas no actualizan - Verificar endpoint"""
        r = self.make_request('GET', '/dashboard/resumen')
        
        if r and r.status_code == 200:
            data = r.json()
            tiene_equipos = 'equipos' in data
            tiene_por_estado = 'por_estado' in data.get('equipos', {})
            
            passed = tiene_equipos and tiene_por_estado
            self.test_result("5", "Endpoint dashboard/resumen",
                           passed, "Datos con equipos.por_estado",
                           "OK" if passed else "Faltan datos")
        else:
            self.failed += 1
            self.test_result("5", "Endpoint dashboard/resumen",
                           False, "200 OK", str(r.status_code) if r else "Error")
    
    def test_error_10_imprimir(self):
        """Error #10: Imagen al imprimir - No crítico"""
        # Este es un error de frontend CSS, no de backend
        self.skipped += 1
        print(f"\n{Colors.YELLOW}⊘ SALTADO{Colors.RESET} [Error #10] Imagen al imprimir (Frontend CSS)")
    
    def test_error_11_se_cae(self):
        """Error #11: Se cae al actualizar - Debug necesario"""
        # Este error requiere debug del frontend
        self.skipped += 1
        print(f"\n{Colors.YELLOW}⊘ SALTADO{Colors.RESET} [Error #11] Se cae al actualizar (Frontend debug)")
    
    def test_error_12_exportaciones(self):
        """Error #12: Exportaciones no actualizan"""
        # Probar endpoint de export JSON
        r1 = self.make_request('GET', '/export/json')
        
        # Probar endpoint de export resumen
        r2 = self.make_request('GET', '/export/resumen')
        
        passed = all([
            r1 and r1.status_code == 200,
            r2 and r2.status_code == 200
        ])
        
        self.test_result("12", "Endpoints de exportación",
                       passed, "200 OK (2 endpoints)",
                       f"r1={r1.status_code if r1 else 'Error'}, "
                       f"r2={r2.status_code if r2 else 'Error'}")
    
    # ========================================================================
    # RESUMEN
    # ========================================================================
    
    def print_summary(self):
        """Imprimir resumen de tests"""
        print(f"\n{Colors.BOLD}{'='*80}{Colors.RESET}")
        print(f"{Colors.BOLD}{'RESUMEN DE TESTS DE ERRORES DE BACKEND':^80}{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*80}{Colors.RESET}\n")
        
        total = self.passed + self.failed + self.skipped
        
        print(f"{Colors.BOLD}Tests ejecutados:{Colors.RESET} {total}")
        print(f"{Colors.GREEN}✓ Pasaron:{Colors.RESET} {self.passed}")
        print(f"{Colors.RED}✗ Fallaron:{Colors.RESET} {self.failed}")
        print(f"{Colors.YELLOW}⊘ Saltados:{Colors.RESET} {self.skipped}")
        print()
        
        if self.failed == 0:
            print(f"{Colors.GREEN}{Colors.BOLD}🎉 ¡TODOS LOS TESTS DE BACKEND PASARON! 🎉{Colors.RESET}")
            return 0
        else:
            porcentaje = (self.passed * 100) // (self.passed + self.failed) if (self.passed + self.failed) > 0 else 0
            print(f"{Colors.YELLOW}{Colors.BOLD}✅ {porcentaje}% DE TESTS DE BACKEND PASARON ({self.passed}/{self.passed + self.failed}){Colors.RESET}")
            return 1

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Función principal"""
    print(f"{Colors.BOLD}{'='*80}{Colors.RESET}")
    print(f"{Colors.BOLD}{'TEST DE ERRORES DE BACKEND - INVENTARIO CIE':^80}{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*80}{Colors.RESET}\n")
    
    print(f"Base URL: {BASE_URL}")
    print(f"Usuario: {ADMIN_USER['email']}")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Esperar cold start de Render
    print(f"{Colors.YELLOW}⏳ Esperando cold start de Render (30 segundos)...{Colors.RESET}\n")
    time.sleep(30)
    
    tester = TestErroresBackend(BASE_URL, BASE_URL_ROOT)
    
    # Login
    print(f"{Colors.BOLD}{'─'*80}{Colors.RESET}")
    print(f"{Colors.BOLD}AUTENTICACIÓN{Colors.RESET}")
    print(f"{Colors.BOLD}{'─'*80}{Colors.RESET}")
    
    if not tester.login(ADMIN_USER['email'], ADMIN_USER['password']):
        print(f"{Colors.RED}✗ No se pudo autenticar - abortando tests{Colors.RESET}")
        return 1
    
    print(f"{Colors.GREEN}✓ Login exitoso{Colors.RESET}\n")
    
    # Tests de errores
    print(f"{Colors.BOLD}{'─'*80}{Colors.RESET}")
    print(f"{Colors.BOLD}TESTS DE ERRORES DE BACKEND{Colors.RESET}")
    print(f"{Colors.BOLD}{'─'*80}{Colors.RESET}")
    
    tester.test_error_2_dispositivo_no_encontrado()
    tester.test_error_3_devolucion_actualiza_equipo()
    tester.test_error_6_prestamos_vencidos_devolver()
    tester.test_error_8_editar_equipo()
    tester.test_error_8_eliminar_equipo()
    tester.test_error_4_notificaciones_endpoint()
    tester.test_error_5_graficas_endpoint()
    tester.test_error_10_imprimir()
    tester.test_error_11_se_cae()
    tester.test_error_12_exportaciones()
    
    # Resumen
    return tester.print_summary()

if __name__ == "__main__":
    sys.exit(main())
