#!/usr/bin/env python3
"""
Test rápido: Crear préstamo simple
"""

import requests

BASE_URL = "https://inventario-workinn-api.onrender.com/api/v1"

# Login
response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"email": "eduardopimienta@americana.edu.co", "password": "Admin123!"}
)
token = response.json().get('access_token')
print(f"✅ Token: {token[:50]}...")

headers = {'Authorization': f'Bearer {token}'}

# Test 1: Crear préstamo SIN fecha_limite
print("\n1️⃣ Crear préstamo SIN fecha_limite:")
response = requests.post(
    f"{BASE_URL}/prestamos",
    json={"prestatario_id": 1, "equipo_id": 1},
    headers=headers
)
print(f"   Status: {response.status_code}")
print(f"   Response: {response.text[:200]}")

# Test 2: Crear préstamo CON fecha_limite
print("\n2️⃣ Crear préstamo CON fecha_limite:")
from datetime import datetime, timedelta
fecha_futura = (datetime.now() + timedelta(days=7)).isoformat().replace('+00:00', 'Z')

response = requests.post(
    f"{BASE_URL}/prestamos",
    json={"prestatario_id": 1, "equipo_id": 1, "fecha_limite": fecha_futura},
    headers=headers
)
print(f"   Status: {response.status_code}")
print(f"   Response: {response.text[:200]}")
