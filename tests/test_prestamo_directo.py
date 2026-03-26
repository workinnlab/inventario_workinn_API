#!/usr/bin/env python3
"""
Test DIRECTO: Crear préstamo
"""

import requests
from datetime import datetime, timedelta

BASE_URL = "https://inventario-workinn-api.onrender.com/api/v1"

# Login
print("1️⃣ Login...")
response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"email": "eduardopimienta@americana.edu.co", "password": "Admin123!"},
    timeout=60
)
print(f"   Status: {response.status_code}")
token = response.json().get('access_token')
print(f"   Token: {token[:50]}...")

headers = {'Authorization': f'Bearer {token}'}

# Crear equipo
print("\n2️⃣ Crear equipo...")
response = requests.post(
    f"{BASE_URL}/equipos",
    json={
        "nombre": f"Direct Test {int(datetime.now().timestamp())}",
        "marca": "Test",
        "codigo": f"DIRECT-{int(datetime.now().timestamp())}",
        "estado": "disponible"
    },
    headers=headers,
    timeout=60
)
print(f"   Status: {response.status_code}")
print(f"   Response: {response.text[:200]}")
equipo_id = response.json().get('id') if response.status_code == 200 else None

# Crear prestatario
print("\n3️⃣ Crear prestatario...")
response = requests.post(
    f"{BASE_URL}/prestatarios",
    json={
        "nombre": f"Direct {int(datetime.now().timestamp())}",
        "dependencia": "Test",
        "email": f"direct{int(datetime.now().timestamp())}@cie.com"
    },
    headers=headers,
    timeout=60
)
print(f"   Status: {response.status_code}")
print(f"   Response: {response.text[:200]}")
prestatario_id = response.json().get('id') if response.status_code == 200 else None

# Crear préstamo
print("\n4️⃣ Crear préstamo...")
fecha_futura = (datetime.now() + timedelta(days=7)).isoformat().replace('+00:00', 'Z')
print(f"   Fecha: {fecha_futura}")
print(f"   Datos: prestatario_id={prestatario_id}, equipo_id={equipo_id}")

try:
    response = requests.post(
        f"{BASE_URL}/prestamos",
        json={
            "prestatario_id": prestatario_id,
            "equipo_id": equipo_id,
            "fecha_limite": fecha_futura
        },
        headers=headers,
        timeout=60
    )
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text[:500]}")
except Exception as e:
    print(f"   ❌ Exception: {e}")
