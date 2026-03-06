#!/usr/bin/env python3
"""Probar endpoint /auth/me después del fix RLS"""

import requests

BASE_URL = "https://inventario-workinn-api.onrender.com/api/v1"

print("=== PROBANDO /auth/me DESPUÉS DEL FIX RLS ===\n")

# 1. Login
print("1️⃣ Obteniendo token fresco...")
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"email": "admin@cie.com", "password": "Admin123!"},
    timeout=30
)

if login_response.status_code != 200:
    print(f"❌ Login falló: {login_response.status_code}")
    print(login_response.text)
    exit(1)

login_data = login_response.json()
token = login_data['access_token']
user = login_data['user']

print(f"✅ Login exitoso!")
print(f"   Email: {user.get('email')}")
print(f"   Nombre: {user.get('nombre')}")
print(f"   Rol: {user.get('rol')}")
print(f"   Token length: {len(token)}")

# 2. Probar /auth/me
print("\n2️⃣ Probando GET /auth/me...")
headers = {"Authorization": f"Bearer {token}"}
me_response = requests.get(f"{BASE_URL}/auth/me", headers=headers, timeout=30)

print(f"\n📊 Respuesta:")
print(f"   Status: {me_response.status_code}")

if me_response.status_code == 200:
    me_data = me_response.json()
    print(f"\n✅ ¡EXITO! /auth/me funciona correctamente\n")
    print(f"📋 Datos del usuario:")
    print(f"   ID: {me_data.get('id')}")
    print(f"   Nombre: {me_data.get('nombre')}")
    print(f"   Email: {me_data.get('email')}")
    print(f"   Rol: {me_data.get('rol')}")
    print(f"   Activo: {me_data.get('activo')}")
    print(f"   Created: {me_data.get('created_at')}")
else:
    print(f"\n❌ Error: {me_response.status_code}")
    print(f"   Respuesta: {me_response.text}")
