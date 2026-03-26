#!/usr/bin/env python3
"""
DEBUG: Error #6 - Préstamos vencidos
=====================================

Investigar por qué falla crear préstamo con fecha en el pasado
"""

import requests
import time
from datetime import datetime, timedelta

BASE_URL = "https://inventario-workinn-api.onrender.com/api/v1"

ADMIN_USER = {
    "email": "eduardopimienta@americana.edu.co",
    "password": "Admin123!"
}

def get_token():
    """Obtener token de admin"""
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json=ADMIN_USER
    )
    if response.status_code == 200:
        return response.json().get('access_token')
    return None

def main():
    print("="*80)
    print("DEBUG: Error #6 - Préstamos vencidos")
    print("="*80)
    
    token = get_token()
    if not token:
        print("❌ No se pudo obtener token")
        return
    
    print(f"✅ Token obtenido")
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Paso 1: Crear equipo
    print("\n1️⃣ Creando equipo...")
    equipo_data = {
        "nombre": f"Debug Error 6 {int(time.time())}",
        "marca": "Test",
        "codigo": f"DEBUG-ERR6-{int(time.time())}",
        "estado": "disponible"
    }
    
    response = requests.post(f"{BASE_URL}/equipos", json=equipo_data, headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"   ❌ Error: {response.text}")
        return
    
    equipo_id = response.json().get('id')
    print(f"   ✅ Equipo creado: ID={equipo_id}")
    
    # Paso 2: Crear prestatario
    print("\n2️⃣ Creando prestatario...")
    prestatario_data = {
        "nombre": f"Debug {int(time.time())}",
        "dependencia": "Test",
        "email": f"debug{int(time.time())}@cie.com"
    }
    
    response = requests.post(f"{BASE_URL}/prestatarios", json=prestatario_data, headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"   ❌ Error: {response.text}")
        return
    
    prestatario_id = response.json().get('id')
    print(f"   ✅ Prestatario creado: ID={prestatario_id}")
    
    # Paso 3: Crear préstamo con fecha en el pasado
    print("\n3️⃣ Creando préstamo con fecha en el pasado...")
    fecha_pasado = (datetime.now() - timedelta(days=30)).isoformat()
    fecha_pasado_str = fecha_pasado.replace('+00:00', 'Z')
    
    prestamo_data = {
        "prestatario_id": prestatario_id,
        "equipo_id": equipo_id,
        "fecha_limite": fecha_pasado_str,
        "observaciones": "Test de préstamo vencido"
    }
    
    print(f"   Fecha límite: {fecha_pasado_str}")
    print(f"   Datos: {prestamo_data}")
    
    response = requests.post(f"{BASE_URL}/prestamos", json=prestamo_data, headers=headers)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text}")
    
    if response.status_code != 200:
        print(f"   ❌ Error al crear préstamo vencido")
        
        # Intentar con fecha futura
        print("\n4️⃣ Intentando con fecha FUTURA...")
        fecha_futura = (datetime.now() + timedelta(days=7)).isoformat()
        fecha_futura_str = fecha_futura.replace('+00:00', 'Z')
        
        prestamo_data['fecha_limite'] = fecha_futura_str
        print(f"   Fecha límite: {fecha_futura_str}")
        
        response = requests.post(f"{BASE_URL}/prestamos", json=prestamo_data, headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            prestamo_id = response.json().get('id')
            print(f"   ✅ Préstamo creado (fecha futura): ID={prestamo_id}")
            
            # Ahora intentar devolver
            print("\n5️⃣ Intentando devolver préstamo...")
            response = requests.post(f"{BASE_URL}/prestamos/{prestamo_id}/devolver", headers=headers)
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text}")
    else:
        prestamo_id = response.json().get('id')
        print(f"   ✅ Préstamo vencido creado: ID={prestamo_id}")
        
        # Intentar devolver
        print("\n5️⃣ Intentando devolver préstamo vencido...")
        response = requests.post(f"{BASE_URL}/prestamos/{prestamo_id}/devolver", headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")

if __name__ == "__main__":
    main()
