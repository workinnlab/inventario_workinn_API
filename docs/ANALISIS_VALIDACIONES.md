#!/usr/bin/env python3
"""
Análisis Completo de Validaciones - Inventario CIE
====================================================

Este documento lista TODAS las validaciones necesarias para un sistema de 
inventario y préstamos, y evalúa cuáles están implementadas y cuáles faltan.

Autor: Eddy - Inventario CIE
Fecha: Marzo 2026
"""

# ============================================================================
# VALIDACIONES POR MÓDULO
# ============================================================================

validaciones = {
    "AUTENTICACIÓN Y USUARIOS": {
        "descripcion": "Validaciones para login, registro y gestión de usuarios",
        "validaciones": [
            {
                "id": "AUTH-01",
                "descripcion": "Email único en el sistema",
                "estado": "✅ Implementado (Supabase Auth)",
                "prioridad": "CRÍTICA"
            },
            {
                "id": "AUTH-02",
                "descripcion": "Contraseña mínima 6 caracteres",
                "estado": "✅ Implementado (Supabase Auth)",
                "prioridad": "CRÍTICA"
            },
            {
                "id": "AUTH-03",
                "descripcion": "Email válido (formato email)",
                "estado": "✅ Implementado (Supabase Auth)",
                "prioridad": "CRÍTICA"
            },
            {
                "id": "AUTH-04",
                "descripcion": "Rol válido (admin, inventory, viewer)",
                "estado": "✅ Implementado (BD constraint)",
                "prioridad": "ALTA"
            },
            {
                "id": "AUTH-05",
                "descripcion": "Token expira después de 1 hora",
                "estado": "✅ Implementado (Supabase Auth)",
                "prioridad": "ALTA"
            },
            {
                "id": "AUTH-06",
                "descripcion": "Usuario inactivo no puede hacer login",
                "estado": "⚠️ Parcial (verifica en backend)",
                "prioridad": "ALTA"
            },
            {
                "id": "AUTH-07",
                "descripcion": "Rate limiting en login (prevenir brute force)",
                "estado": "❌ NO IMPLEMENTADO",
                "prioridad": "MEDIA"
            },
            {
                "id": "AUTH-08",
                "descripcion": "Password hash encriptado",
                "estado": "✅ Implementado (Supabase Auth)",
                "prioridad": "CRÍTICA"
            }
        ]
    },
    
    "EQUIPOS": {
        "descripcion": "Validaciones para CRUD de equipos",
        "validaciones": [
            {
                "id": "EQ-01",
                "descripcion": "Código único (no repetir PC-01, PC-02, etc.)",
                "estado": "✅ Implementado (unique constraint en BD)",
                "prioridad": "CRÍTICA"
            },
            {
                "id": "EQ-02",
                "descripcion": "Nombre no vacío",
                "estado": "✅ Implementado (not null en BD)",
                "prioridad": "ALTA"
            },
            {
                "id": "EQ-03",
                "descripcion": "Marca no vacía",
                "estado": "✅ Implementado (not null en BD)",
                "prioridad": "ALTA"
            },
            {
                "id": "EQ-04",
                "descripcion": "Estado válido (disponible, en uso, prestado, mantenimiento, dañado)",
                "estado": "✅ Implementado (check constraint en BD)",
                "prioridad": "ALTA"
            },
            {
                "id": "EQ-05",
                "descripcion": "No eliminar equipo si tiene préstamos activos",
                "estado": "❌ NO IMPLEMENTADO",
                "prioridad": "ALTA"
            },
            {
                "id": "EQ-06",
                "descripcion": "No cambiar a 'disponible' si tiene préstamos activos",
                "estado": "❌ NO IMPLEMENTADO",
                "prioridad": "ALTA"
            },
            {
                "id": "EQ-07",
                "descripcion": "Serial único (opcional pero recomendado)",
                "estado": "❌ NO IMPLEMENTADO",
                "prioridad": "MEDIA"
            },
            {
                "id": "EQ-08",
                "descripcion": "No permitir código vacío o nulo",
                "estado": "✅ Implementado (not null + unique)",
                "prioridad": "ALTA"
            }
        ]
    },
    
    "ELECTRÓNICA": {
        "descripcion": "Validaciones para CRUD de electrónica",
        "validaciones": [
            {
                "id": "EL-01",
                "descripcion": "Nombre no vacío",
                "estado": "✅ Implementado (not null)",
                "prioridad": "ALTA"
            },
            {
                "id": "EL-02",
                "descripcion": "en_uso >= 0",
                "estado": "⚠️ Default 0 pero sin constraint",
                "prioridad": "MEDIA"
            },
            {
                "id": "EL-03",
                "descripcion": "en_stock >= 0",
                "estado": "⚠️ Default 0 pero sin constraint",
                "prioridad": "MEDIA"
            },
            {
                "id": "EL-04",
                "descripcion": "total = en_uso + en_stock",
                "estado": "✅ Implementado (columna generada)",
                "prioridad": "ALTA"
            },
            {
                "id": "EL-05",
                "descripcion": "No permitir valores negativos",
                "estado": "❌ NO IMPLEMENTADO",
                "prioridad": "MEDIA"
            }
        ]
    },
    
    "ROBOTS": {
        "descripcion": "Validaciones para CRUD de robots",
        "validaciones": [
            {
                "id": "RO-01",
                "descripcion": "Nombre no vacío",
                "estado": "✅ Implementado (not null)",
                "prioridad": "ALTA"
            },
            {
                "id": "RO-02",
                "descripcion": "fuera_de_servicio >= 0",
                "estado": "⚠️ Default 0 pero sin constraint",
                "prioridad": "MEDIA"
            },
            {
                "id": "RO-03",
                "descripcion": "en_uso >= 0",
                "estado": "⚠️ Default 0 pero sin constraint",
                "prioridad": "MEDIA"
            },
            {
                "id": "RO-04",
                "descripcion": "disponible >= 0",
                "estado": "⚠️ Default 0 pero sin constraint",
                "prioridad": "MEDIA"
            },
            {
                "id": "RO-05",
                "descripcion": "total = fuera_de_servicio + en_uso + disponible",
                "estado": "✅ Implementado (columna generada)",
                "prioridad": "ALTA"
            },
            {
                "id": "RO-06",
                "descripcion": "No permitir valores negativos",
                "estado": "❌ NO IMPLEMENTADO",
                "prioridad": "MEDIA"
            }
        ]
    },
    
    "MATERIALES": {
        "descripcion": "Validaciones para CRUD de materiales",
        "validaciones": [
            {
                "id": "MA-01",
                "descripcion": "Color no vacío",
                "estado": "✅ Implementado (not null)",
                "prioridad": "ALTA"
            },
            {
                "id": "MA-02",
                "descripcion": "Cantidad no vacía (ej: 1KG, 500ml)",
                "estado": "✅ Implementado (not null)",
                "prioridad": "ALTA"
            },
            {
                "id": "MA-03",
                "descripcion": "Categoría válida (Filamento, Resina, Otro)",
                "estado": "✅ Implementado (check constraint)",
                "prioridad": "ALTA"
            },
            {
                "id": "MA-04",
                "descripcion": "tipo_id referencia válida a tipos_materiales",
                "estado": "✅ Implementado (foreign key)",
                "prioridad": "ALTA"
            },
            {
                "id": "MA-05",
                "descripcion": "usado >= 0",
                "estado": "⚠️ Default 0 pero sin constraint",
                "prioridad": "MEDIA"
            },
            {
                "id": "MA-06",
                "descripcion": "en_uso >= 0",
                "estado": "⚠️ Default 0 pero sin constraint",
                "prioridad": "MEDIA"
            },
            {
                "id": "MA-07",
                "descripcion": "en_stock >= 0",
                "estado": "⚠️ Default 0 pero sin constraint",
                "prioridad": "MEDIA"
            },
            {
                "id": "MA-08",
                "descripcion": "total = usado + en_uso + en_stock",
                "estado": "✅ Implementado (columna generada)",
                "prioridad": "ALTA"
            },
            {
                "id": "MA-09",
                "descripcion": "No permitir stock negativo al restar",
                "estado": "❌ NO IMPLEMENTADO",
                "prioridad": "ALTA"
            }
        ]
    },
    
    "PRESTATARIOS": {
        "descripcion": "Validaciones para CRUD de prestatarios",
        "validaciones": [
            {
                "id": "PR-01",
                "descripcion": "Nombre no vacío",
                "estado": "✅ Implementado (not null)",
                "prioridad": "ALTA"
            },
            {
                "id": "PR-02",
                "descripcion": "Dependencia no vacía",
                "estado": "✅ Implementado (not null)",
                "prioridad": "ALTA"
            },
            {
                "id": "PR-03",
                "descripcion": "Email válido (si se proporciona)",
                "estado": "❌ NO IMPLEMENTADO",
                "prioridad": "MEDIA"
            },
            {
                "id": "PR-04",
                "descripcion": "Teléfono formato válido (si se proporciona)",
                "estado": "❌ NO IMPLEMENTADO",
                "prioridad": "BAJA"
            },
            {
                "id": "PR-05",
                "descripcion": "No eliminar si tiene préstamos activos",
                "estado": "❌ NO IMPLEMENTADO",
                "prioridad": "ALTA"
            },
            {
                "id": "PR-06",
                "descripcion": "Cédula única (opcional)",
                "estado": "❌ NO IMPLEMENTADO",
                "prioridad": "MEDIA"
            }
        ]
    },
    
    "PRÉSTAMOS": {
        "descripcion": "Validaciones para CRUD de préstamos (MÁS CRÍTICAS)",
        "validaciones": [
            {
                "id": "PS-01",
                "descripcion": "Elemento NO puede estar ya prestado (activo)",
                "estado": "✅ IMPLEMENTADO - Mar 2026",
                "prioridad": "CRÍTICA"
            },
            {
                "id": "PS-02",
                "descripcion": "Elemento NO puede estar dañado",
                "estado": "✅ IMPLEMENTADO - Mar 2026",
                "prioridad": "CRÍTICA"
            },
            {
                "id": "PS-03",
                "descripcion": "Elemento NO puede estar en mantenimiento",
                "estado": "✅ IMPLEMENTADO - Mar 2026",
                "prioridad": "CRÍTICA"
            },
            {
                "id": "PS-04",
                "descripcion": "Prestatario debe existir y estar activo",
                "estado": "✅ IMPLEMENTADO - Mar 2026",
                "prioridad": "CRÍTICA"
            },
            {
                "id": "PS-05",
                "descripcion": "Solo UN tipo de elemento por préstamo (equipo O electronica O robot O material)",
                "estado": "✅ Implementado (check constraint)",
                "prioridad": "CRÍTICA"
            },
            {
                "id": "PS-06",
                "descripcion": "fecha_limite >= fecha_prestamo",
                "estado": "❌ NO IMPLEMENTADO",
                "prioridad": "ALTA"
            },
            {
                "id": "PS-07",
                "descripcion": "No eliminar préstamo si está activo",
                "estado": "❌ NO IMPLEMENTADO",
                "prioridad": "ALTA"
            },
            {
                "id": "PS-08",
                "descripcion": "Solo devolver si está 'activo'",
                "estado": "✅ Implementado (verificación en endpoint)",
                "prioridad": "ALTA"
            },
            {
                "id": "PS-09",
                "descripcion": "fecha_devolucion >= fecha_prestamo",
                "estado": "❌ NO IMPLEMENTADO",
                "prioridad": "MEDIA"
            },
            {
                "id": "PS-10",
                "descripcion": "Estado válido (activo, devuelto, vencido, perdido)",
                "estado": "✅ Implementado (check constraint)",
                "prioridad": "ALTA"
            },
            {
                "id": "PS-11",
                "descripcion": "Crear movimiento automático al crear préstamo",
                "estado": "✅ Implementado (trigger)",
                "prioridad": "ALTA"
            },
            {
                "id": "PS-12",
                "descripcion": "Crear movimiento automático al devolver",
                "estado": "✅ Implementado (trigger)",
                "prioridad": "ALTA"
            },
            {
                "id": "PS-13",
                "descripcion": "Actualizar estado del equipo a 'prestado' al crear préstamo",
                "estado": "❌ NO IMPLEMENTADO",
                "prioridad": "MEDIA"
            },
            {
                "id": "PS-14",
                "descripcion": "Actualizar estado del equipo a 'disponible' al devolver",
                "estado": "❌ NO IMPLEMENTADO",
                "prioridad": "MEDIA"
            }
        ]
    },
    
    "MOVIMIENTOS": {
        "descripcion": "Validaciones para auditoría de movimientos",
        "validaciones": [
            {
                "id": "MV-01",
                "descripcion": "Tipo válido (entrada, salida, devolucion, daño, ajuste_stock, baja, transferencia)",
                "estado": "✅ Implementado (check constraint)",
                "prioridad": "ALTA"
            },
            {
                "id": "MV-02",
                "descripcion": "cantidad >= 1",
                "estado": "❌ NO IMPLEMENTADO",
                "prioridad": "MEDIA"
            },
            {
                "id": "MV-03",
                "descripcion": "Solo UN tipo de elemento por movimiento",
                "estado": "✅ Implementado (check constraint)",
                "prioridad": "ALTA"
            },
            {
                "id": "MV-04",
                "descripcion": "Elemento debe existir",
                "estado": "✅ Implementado (foreign key)",
                "prioridad": "ALTA"
            },
            {
                "id": "MV-05",
                "descripcion": "usuario_id válido (si se proporciona)",
                "estado": "⚠️ Referencia a auth.users pero nullable",
                "prioridad": "MEDIA"
            },
            {
                "id": "MV-06",
                "descripcion": "No eliminar movimientos (auditoría debe ser inmutable)",
                "estado": "❌ NO IMPLEMENTADO",
                "prioridad": "ALTA"
            }
        ]
    },
    
    "REGLAS DE NEGOCIO ADICIONALES": {
        "descripcion": "Validaciones específicas del negocio",
        "validaciones": [
            {
                "id": "RN-01",
                "descripcion": "Un prestatario no puede tener más de X préstamos activos simultáneos",
                "estado": "❌ NO IMPLEMENTADO",
                "prioridad": "MEDIA"
            },
            {
                "id": "RN-02",
                "descripcion": "Préstamos no pueden exceder Y días sin renovación",
                "estado": "❌ NO IMPLEMENTADO",
                "prioridad": "MEDIA"
            },
            {
                "id": "RN-03",
                "descripcion": "Alerta automática cuando préstamo está por vencer",
                "estado": "❌ NO IMPLEMENTADO",
                "prioridad": "BAJA"
            },
            {
                "id": "RN-04",
                "descripcion": "Marcar préstamo como 'vencido' automáticamente si pasa fecha_limite",
                "estado": "❌ NO IMPLEMENTADO",
                "prioridad": "MEDIA"
            },
            {
                "id": "RN-05",
                "descripcion": "No permitir prestar si el prestatario tiene préstamos vencidos",
                "estado": "❌ NO IMPLEMENTADO",
                "prioridad": "MEDIA"
            },
            {
                "id": "RN-06",
                "descripcion": "Histórico: no permitir modificar movimientos pasados",
                "estado": "❌ NO IMPLEMENTADO",
                "prioridad": "BAJA"
            },
            {
                "id": "RN-07",
                "descripcion": "Stock mínimo: alertar cuando material esté por agotarse",
                "estado": "❌ NO IMPLEMENTADO",
                "prioridad": "BAJA"
            },
            {
                "id": "RN-08",
                "descripcion": "No permitir dar de baja elemento con préstamos activos",
                "estado": "❌ NO IMPLEMENTADO",
                "prioridad": "ALTA"
            }
        ]
    }
}

# ============================================================================
# RESUMEN
# ============================================================================

def calcular_resumen():
    """Calcular resumen de validaciones"""
    total = 0
    implementadas = 0
    parcial = 0
    no_implementadas = 0
    
    por_prioridad = {
        "CRÍTICA": {"total": 0, "implementadas": 0},
        "ALTA": {"total": 0, "implementadas": 0},
        "MEDIA": {"total": 0, "implementadas": 0},
        "BAJA": {"total": 0, "implementadas": 0}
    }
    
    for modulo, datos in validaciones.items():
        for val in datos["validaciones"]:
            total += 1
            prioridad = val["prioridad"]
            por_prioridad[prioridad]["total"] += 1
            
            if val["estado"].startswith("✅"):
                implementadas += 1
                por_prioridad[prioridad]["implementadas"] += 1
            elif "⚠️" in val["estado"] or "Parcial" in val["estado"]:
                parcial += 1
            elif val["estado"].startswith("❌"):
                no_implementadas += 1
    
    return {
        "total": total,
        "implementadas": implementadas,
        "parcial": parcial,
        "no_implementadas": no_implementadas,
        "por_prioridad": por_prioridad
    }

# ============================================================================
# MAIN - IMPRIMIR REPORTE
# ============================================================================

if __name__ == "__main__":
    print("="*80)
    print("ANÁLISIS COMPLETO DE VALIDACIONES - INVENTARIO CIE".center(80))
    print("="*80)
    print()
    
    for modulo, datos in validaciones.items():
        print(f"\n{'='*80}")
        print(f"📋 {modulo}")
        print(f"   {datos['descripcion']}")
        print(f"{'='*80}\n")
        
        for val in datos["validaciones"]:
            icono = val["estado"].split(" ")[0]
            print(f"{icono} [{val['id']}] {val['descripcion']}")
            print(f"   Estado: {val['estado']}")
            print(f"   Prioridad: {val['prioridad']}")
            print()
    
    # Resumen
    resumen = calcular_resumen()
    
    print("\n" + "="*80)
    print("📊 RESUMEN GENERAL")
    print("="*80)
    print(f"\nTotal validaciones: {resumen['total']}")
    print(f"✅ Implementadas: {resumen['implementadas']} ({resumen['implementadas']*100//resumen['total']}%)")
    print(f"⚠️  Parcialmente: {resumen['parcial']}")
    print(f"❌ No implementadas: {resumen['no_implementadas']}")
    
    print("\n📊 POR PRIORIDAD:")
    for prioridad, datos in resumen['por_prioridad'].items():
        pct = datos['implementadas']*100//datos['total'] if datos['total'] > 0 else 0
        print(f"  {prioridad}: {datos['implementadas']}/{datos['total']} ({pct}%)")
    
    print("\n" + "="*80)
    print("🔧 VALIDACIONES CRÍTICAS FALTANTES (IMPLEMENTAR PRIMERO)")
    print("="*80)
    
    for modulo, datos in validaciones.items():
        for val in datos["validaciones"]:
            if val["prioridad"] == "CRÍTICA" and val["estado"].startswith("❌"):
                print(f"\n❌ [{val['id']}] {val['descripcion']}")
                print(f"   Módulo: {modulo}")
    
    print("\n" + "="*80)
    print("🔧 VALIDACIONES ALTA PRIORIDAD FALTANTES")
    print("="*80)
    
    for modulo, datos in validaciones.items():
        for val in datos["validaciones"]:
            if val["prioridad"] == "ALTA" and val["estado"].startswith("❌"):
                print(f"\n❌ [{val['id']}] {val['descripcion']}")
                print(f"   Módulo: {modulo}")
    
    print("\n" + "="*80)
