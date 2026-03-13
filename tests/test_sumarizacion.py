#!/usr/bin/env python3
"""
Test de Sumarización de Inventario - Inventario CIE
=====================================================

Este script prueba y genera reportes de sumarización del inventario:
- Total de elementos por categoría
- Movimientos por tipo
- Préstamos por estado
- Resumen general del laboratorio

Uso:
    python test_sumarizacion.py

Requisitos:
    pip install requests

Autor: Eddy - Inventario CIE
Fecha: Marzo 2026
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Any

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

BASE_URL = "https://inventario-workinn-api.onrender.com/api/v1"
BASE_URL_ROOT = "https://inventario-workinn-api.onrender.com"

# Usuario admin para tests
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
    MAGENTA = '\033[95m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# ============================================================================
# UTILIDADES
# ============================================================================

def print_header(text: str):
    """Imprimir encabezado principal"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(80)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.RESET}\n")

def print_section(text: str):
    """Imprimir sección"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'─'*80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'─'*80}{Colors.RESET}\n")

def print_subsection(text: str):
    """Imprimir sub-sección"""
    print(f"\n{Colors.YELLOW}▸ {text}{Colors.RESET}\n")

def print_success(text: str):
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text: str):
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_info(text: str):
    print(f"{Colors.BLUE}ℹ {text}{Colors.RESET}")

def print_table(headers: List[str], rows: List[List[str]]):
    """Imprimir tabla formateada"""
    # Calcular anchos de columna
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))
    
    # Imprimir headers
    header_row = " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    print(f"{Colors.BOLD}{header_row}{Colors.RESET}")
    print("-" * len(header_row))
    
    # Imprimir filas
    for row in rows:
        print(" | ".join(str(cell).ljust(widths[i]) for i, cell in enumerate(row)))

# ============================================================================
# CLASE DE SUMARIZACIÓN
# ============================================================================

class InventarioSumarizer:
    """Clase para generar reportes de sumarización del inventario"""
    
    def __init__(self, base_url: str, base_url_root: str):
        self.base_url = base_url
        self.base_url_root = base_url_root
        self.token: str = None
        self.headers: Dict[str, str] = {}
        
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
                print_success(f"Login exitoso: {data.get('user', {}).get('email')}")
                return True
            
            print_error(f"Login falló: {response.status_code}")
            return False
            
        except Exception as e:
            print_error(f"Error en login: {str(e)}")
            return False
    
    def get_data(self, endpoint: str) -> List[Dict]:
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
    
    def sumarizar_por_categoria(self) -> Dict[str, Any]:
        """Sumarizar inventario por categoría"""
        print_subsection("📦 Inventario por Categoría")
        
        categorias = {}
        
        # Equipos
        equipos = self.get_data('/equipos')
        categorias['equipos'] = {
            'total': len(equipos),
            'items': equipos,
            'por_estado': {}
        }
        
        # Contar por estado
        for equipo in equipos:
            estado = equipo.get('estado', 'desconocido')
            categorias['equipos']['por_estado'][estado] = \
                categorias['equipos']['por_estado'].get(estado, 0) + 1
        
        # Electrónica
        electronica = self.get_data('/electronica')
        categorias['electronica'] = {
            'total': len(electronica),
            'items': electronica,
            'en_uso': sum(item.get('en_uso', 0) for item in electronica),
            'en_stock': sum(item.get('en_stock', 0) for item in electronica),
            'total_general': sum(item.get('total', 0) for item in electronica)
        }
        
        # Robots
        robots = self.get_data('/robots')
        categorias['robots'] = {
            'total': len(robots),
            'items': robots,
            'fuera_servicio': sum(item.get('fuera_de_servicio', 0) for item in robots),
            'en_uso': sum(item.get('en_uso', 0) for item in robots),
            'disponible': sum(item.get('disponible', 0) for item in robots),
            'total_general': sum(item.get('total', 0) for item in robots)
        }
        
        # Materiales
        materiales = self.get_data('/materiales')
        categorias['materiales'] = {
            'total': len(materiales),
            'items': materiales,
            'por_categoria': {},
            'usado': sum(item.get('usado', 0) for item in materiales),
            'en_uso': sum(item.get('en_uso', 0) for item in materiales),
            'en_stock': sum(item.get('en_stock', 0) for item in materiales),
            'total_general': sum(item.get('total', 0) for item in materiales)
        }
        
        # Contar materiales por categoría
        for material in materiales:
            cat = material.get('categoria', 'Otro')
            categorias['materiales']['por_categoria'][cat] = \
                categorias['materiales']['por_categoria'].get(cat, 0) + 1
        
        # Imprimir resumen
        print_table(
            ['Categoría', 'Total Items', 'En Uso', 'En Stock', 'Total General'],
            [
                ['📦 Equipos', str(categorias['equipos']['total']), '-', '-', '-'],
                ['🔌 Electrónica', str(categorias['electronica']['total']), 
                 str(categorias['electronica']['en_uso']), 
                 str(categorias['electronica']['en_stock']),
                 str(categorias['electronica']['total_general'])],
                ['🤖 Robots', str(categorias['robots']['total']),
                 str(categorias['robots']['en_uso']),
                 str(categorias['robots']['disponible']),
                 str(categorias['robots']['total_general'])],
                ['🧪 Materiales', str(categorias['materiales']['total']),
                 str(categorias['materiales']['en_uso']),
                 str(categorias['materiales']['en_stock']),
                 str(categorias['materiales']['total_general'])]
            ]
        )
        
        # Total general del inventario
        total_items = (
            categorias['equipos']['total'] +
            categorias['electronica']['total'] +
            categorias['robots']['total'] +
            categorias['materiales']['total']
        )
        
        print(f"\n{Colors.BOLD}Total General de Items en Inventario: {total_items}{Colors.RESET}")
        
        return categorias
    
    def sumarizar_prestamos(self) -> Dict[str, Any]:
        """Sumarizar préstamos por estado"""
        print_subsection("📋 Préstamos por Estado")
        
        prestamos = self.get_data('/prestamos')
        prestamos_activos = self.get_data('/prestamos/activos')
        
        resumen = {
            'total': len(prestamos),
            'activos': len(prestamos_activos) if prestamos_activos else 0,
            'por_estado': {}
        }
        
        # Contar por estado
        for prestamo in prestamos:
            estado = prestamo.get('estado', 'desconocido')
            resumen['por_estado'][estado] = \
                resumen['por_estado'].get(estado, 0) + 1
        
        # Imprimir tabla
        rows = []
        for estado, count in resumen['por_estado'].items():
            icon = '🟢' if estado == 'activo' else '🔴' if estado == 'vencido' else '⚪'
            rows.append([estado.title(), str(count), icon])

        print_table(['Estado', 'Cantidad', ''],
                   [[r[0], r[1], r[2]] for r in rows])
        
        print(f"\n{Colors.BOLD}Total Préstamos: {resumen['total']}{Colors.RESET}")
        print(f"{Colors.GREEN}Préstamos Activos: {resumen['activos']}{Colors.RESET}")
        
        return resumen
    
    def sumarizar_movimientos(self) -> Dict[str, Any]:
        """Sumarizar movimientos por tipo"""
        print_subsection("📊 Movimientos por Tipo")
        
        movimientos = self.get_data('/movimientos')
        
        resumen = {
            'total': len(movimientos),
            'por_tipo': {}
        }
        
        # Contar por tipo
        for movimiento in movimientos:
            tipo = movimiento.get('tipo', 'desconocido')
            resumen['por_tipo'][tipo] = \
                resumen['por_tipo'].get(tipo, 0) + 1
        
        # Iconos por tipo
        iconos = {
            'entrada': '📥',
            'salida': '📤',
            'devolucion': '↩️',
            'daño': '❌',
            'ajuste_stock': '🔧',
            'baja': '🗑️',
            'transferencia': '🔄'
        }
        
        # Imprimir tabla
        rows = []
        for tipo, count in resumen['por_tipo'].items():
            icon = iconos.get(tipo, '📌')
            rows.append([tipo.title(), str(count), icon])

        print_table(['Tipo', 'Cantidad', ''],
                   [[r[0], r[1], r[2]] for r in rows])
        
        print(f"\n{Colors.BOLD}Total Movimientos Registrados: {resumen['total']}{Colors.RESET}")
        
        return resumen
    
    def generar_reporte_prestatarios(self) -> Dict[str, Any]:
        """Reporte de prestatarios"""
        print_subsection("👥 Prestatarios Registrados")
        
        prestatarios = self.get_data('/prestatarios')
        
        resumen = {
            'total': len(prestatarios),
            'activos': 0,
            'inactivos': 0,
            'por_dependencia': {}
        }
        
        # Contar activos/inactivos y por dependencia
        for prestatario in prestatarios:
            if prestatario.get('activo', False):
                resumen['activos'] += 1
            else:
                resumen['inactivos'] += 1
            
            dep = prestatario.get('dependencia', 'Sin dependencia')
            resumen['por_dependencia'][dep] = \
                resumen['por_dependencia'].get(dep, 0) + 1
        
        # Imprimir tabla
        rows = [
            ['Activos', str(resumen['activos']), '🟢'],
            ['Inactivos', str(resumen['inactivos']), '🔴'],
            ['Total', str(resumen['total']), '📊']
        ]
        
        print_table(['Estado', 'Cantidad', ''], rows)
        
        # Dependencias
        if resumen['por_dependencia']:
            print(f"\n{Colors.YELLOW}Por Dependencia:{Colors.RESET}")
            for dep, count in sorted(resumen['por_dependencia'].items(), key=lambda x: x[1], reverse=True):
                print(f"  • {dep}: {count}")
        
        return resumen
    
    def generar_reporte_detallado_equipos(self, equipos: List[Dict]):
        """Reporte detallado de equipos por estado"""
        print_subsection("📦 Detalle de Equipos por Estado")
        
        por_estado = {}
        for equipo in equipos:
            estado = equipo.get('estado', 'desconocido')
            if estado not in por_estado:
                por_estado[estado] = []
            por_estado[estado].append(equipo)
        
        for estado, items in por_estado.items():
            icon = '🟢' if estado == 'disponible' else '🔴' if estado == 'dañado' else '🟡'
            print(f"\n{icon} {Colors.BOLD}{estado.title()}: {len(items)} equipos{Colors.RESET}")
            
            # Mostrar primeros 5
            for item in items[:5]:
                print(f"   • {item.get('nombre')} ({item.get('codigo')}) - {item.get('marca')}")
            
            if len(items) > 5:
                print(f"   ... y {len(items) - 5} más")
    
    def generar_resumen_ejecutivo(self, categorias: Dict, prestamos: Dict, 
                                   movimientos: Dict, prestatarios: Dict):
        """Generar resumen ejecutivo del laboratorio"""
        print_header("📊 RESUMEN EJECUTIVO DEL LABORATORIO")
        
        # Calcular totales
        total_items = (
            categorias['equipos']['total'] +
            categorias['electronica']['total'] +
            categorias['robots']['total'] +
            categorias['materiales']['total']
        )
        
        total_en_uso = (
            categorias['electronica'].get('en_uso', 0) +
            categorias['robots'].get('en_uso', 0) +
            categorias['materiales'].get('en_uso', 0)
        )
        
        # KPIs principales
        kpis = [
            ['📦 Total Items en Inventario', str(total_items)],
            ['🔌 Total Electrónica', str(categorias['electronica']['total'])],
            ['🤖 Total Robots', str(categorias['robots']['total'])],
            ['🧪 Total Materiales', str(categorias['materiales']['total'])],
            ['📋 Préstamos Activos', str(prestamos['activos'])],
            ['👥 Prestatarios Activos', str(prestatarios['activos'])],
            ['📊 Movimientos Totales', str(movimientos['total'])],
        ]
        
        print_table(['Indicador', 'Valor'], kpis)
        
        # Estado del sistema
        print(f"\n{Colors.BOLD}Estado del Sistema:{Colors.RESET}")
        
        if prestamos['activos'] > 0:
            print(f"  {Colors.YELLOW}⚠ Hay {prestamos['activos']} préstamos activos{Colors.RESET}")
        else:
            print(f"  {Colors.GREEN}✓ No hay préstamos activos{Colors.RESET}")
        
        if movimientos['por_tipo'].get('daño', 0) > 0:
            print(f"  {Colors.RED}❌ {movimientos['por_tipo'].get('daño', 0)} equipos reportados con daño{Colors.RESET}")
        
        # Timestamp del reporte
        print(f"\n{Colors.CYAN}Reporte generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}")
    
    def ejecutar_test_completo(self) -> bool:
        """Ejecutar test completo de sumarización"""
        print_header("🧪 TEST DE SUMARIZACIÓN DE INVENTARIO")
        
        # Login
        print_section("1. Autenticación")
        if not self.login(ADMIN_USER['email'], ADMIN_USER['password']):
            print_error("No se pudo autenticar - abortando test")
            return False
        
        # Sumarizar por categoría
        print_section("2. Sumarización por Categoría")
        categorias = self.sumarizar_por_categoria()
        
        # Sumarizar préstamos
        print_section("3. Sumarización de Préstamos")
        prestamos = self.sumarizar_prestamos()
        
        # Sumarizar movimientos
        print_section("4. Sumarización de Movimientos")
        movimientos = self.sumarizar_movimientos()
        
        # Reporte de prestatarios
        print_section("5. Reporte de Prestatarios")
        prestatarios = self.generar_reporte_prestatarios()
        
        # Detalle de equipos
        print_section("6. Detalle de Equipos")
        self.generar_reporte_detallado_equipos(categorias['equipos']['items'])
        
        # Resumen ejecutivo
        print_section("7. Resumen Ejecutivo")
        self.generar_resumen_ejecutivo(categorias, prestamos, movimientos, prestatarios)
        
        print_header("✅ TEST DE SUMARIZACIÓN COMPLETADO")
        
        return True

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Función principal"""
    print_header("🔬 SISTEMA DE SUMARIZACIÓN - INVENTARIO CIE")
    print_info(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_info(f"API: {BASE_URL}")
    
    sumarizer = InventarioSumarizer(BASE_URL, BASE_URL_ROOT)
    
    exit_code = 0 if sumarizer.ejecutar_test_completo() else 1
    
    return exit_code

if __name__ == "__main__":
    import sys
    sys.exit(main())
