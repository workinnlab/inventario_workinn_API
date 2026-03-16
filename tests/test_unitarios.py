"""
Tests unitarios para inventario_workinn_API
Cubre: services/inventory_service.py y schemas/inventory.py + schemas/auth.py
No requiere conexión a Supabase ni a la API desplegada.
"""
import pytest
from unittest.mock import MagicMock
from datetime import datetime
from pydantic import ValidationError


# ============================================================================
# IMPORTS DE SCHEMAS
# Ajusta las rutas si la estructura de tu proyecto difiere
# ============================================================================
from app.schemas.inventory import (
    EquipoCreate,
    EquipoUpdate,
    ElectronicaBase,
    RobotBase,
    MaterialCreate,
    PrestamoCreate,
    MovimientoCreate,
    PrestatarioCreate,
)
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    RefreshTokenRequest,
)

# ============================================================================
# IMPORTS DE SERVICES
# ============================================================================
from app.services.supabase_service import (
    get_equipo_by_id,
    get_equipo_by_codigo,
    create_equipo,
    update_equipo,
    delete_equipo,
    delete_prestatario,
    update_prestatario,
    create_tipo_material,
    get_prestamos,
    get_prestamos_activos,
)


# ============================================================================
# HELPERS
# ============================================================================

def make_supabase_mock(data=None):
    """
    Crea un mock del cliente de Supabase que retorna `data`
    en cualquier cadena de llamadas (.table().select().eq().execute(), etc.)
    """
    mock = MagicMock()
    response = MagicMock()
    response.data = data if data is not None else []

    # Cualquier método encadenado retorna el mismo mock,
    # y .execute() retorna el response con los datos simulados
    chain = MagicMock()
    chain.execute.return_value = response
    chain.select.return_value = chain
    chain.insert.return_value = chain
    chain.update.return_value = chain
    chain.delete.return_value = chain
    chain.eq.return_value = chain
    chain.range.return_value = chain
    chain.order.return_value = chain

    mock.table.return_value = chain
    return mock, chain, response


# ============================================================================
# TESTS — SERVICES: EQUIPOS
# ============================================================================

class TestGetEquipoById:

    def test_retorna_equipo_cuando_existe(self):
        equipo = {"id": 1, "nombre": "Laptop Dell", "marca": "Dell", "codigo": "PC-01"}
        supabase, _, _ = make_supabase_mock(data=[equipo])

        resultado = get_equipo_by_id(supabase, 1)

        assert resultado == equipo
        assert resultado["codigo"] == "PC-01"

    def test_retorna_none_cuando_no_existe(self):
        supabase, _, _ = make_supabase_mock(data=[])

        resultado = get_equipo_by_id(supabase, 999)

        assert resultado is None

    def test_llama_a_tabla_correcta(self):
        supabase, chain, _ = make_supabase_mock(data=[])

        get_equipo_by_id(supabase, 1)

        supabase.table.assert_called_once_with("equipos")

    def test_filtra_por_id_correcto(self):
        supabase, chain, _ = make_supabase_mock(data=[])

        get_equipo_by_id(supabase, 42)

        chain.eq.assert_called_once_with("id", 42)


class TestGetEquipoByCodigo:

    def test_retorna_equipo_por_codigo(self):
        equipo = {"id": 2, "nombre": "Monitor LG", "marca": "LG", "codigo": "MON-01"}
        supabase, _, _ = make_supabase_mock(data=[equipo])

        resultado = get_equipo_by_codigo(supabase, "MON-01")

        assert resultado["codigo"] == "MON-01"

    def test_retorna_none_si_codigo_no_existe(self):
        supabase, _, _ = make_supabase_mock(data=[])

        resultado = get_equipo_by_codigo(supabase, "INEXISTENTE")

        assert resultado is None


class TestCreateEquipo:

    def test_crea_equipo_y_retorna_datos(self):
        equipo_creado = {"id": 5, "nombre": "Teclado", "marca": "Logitech", "codigo": "TEC-01"}
        supabase, _, _ = make_supabase_mock(data=[equipo_creado])

        data = {"nombre": "Teclado", "marca": "Logitech", "codigo": "TEC-01"}
        resultado = create_equipo(supabase, data)

        assert resultado["id"] == 5
        assert resultado["nombre"] == "Teclado"

    def test_retorna_none_si_insert_falla(self):
        supabase, _, _ = make_supabase_mock(data=[])

        resultado = create_equipo(supabase, {"nombre": "X", "marca": "Y", "codigo": "Z"})

        assert resultado is None


class TestUpdateEquipo:

    def test_actualiza_y_retorna_equipo(self):
        equipo_actualizado = {"id": 1, "nombre": "Laptop HP", "marca": "HP", "codigo": "PC-01"}
        supabase, _, _ = make_supabase_mock(data=[equipo_actualizado])

        resultado = update_equipo(supabase, 1, {"nombre": "Laptop HP", "marca": "HP"})

        assert resultado["marca"] == "HP"

    def test_retorna_none_si_no_encuentra(self):
        supabase, _, _ = make_supabase_mock(data=[])

        resultado = update_equipo(supabase, 999, {"nombre": "X"})

        assert resultado is None


class TestDeleteEquipo:

    def test_retorna_true_cuando_elimina(self):
        supabase, _, _ = make_supabase_mock(data=[{"id": 1}])

        resultado = delete_equipo(supabase, 1)

        assert resultado is True

    def test_retorna_false_cuando_no_existe(self):
        supabase, _, _ = make_supabase_mock(data=[])

        resultado = delete_equipo(supabase, 999)

        assert resultado is False


# ============================================================================
# TESTS — SERVICES: PRESTATARIOS
# ============================================================================

class TestDeletePrestatario:
    """
    delete_prestatario hace borrado LÓGICO: marca activo=False.
    No debe borrar el registro de la BD.
    """

    def test_borrado_logico_no_elimina_registro(self):
        prestatario_actualizado = {"id": 1, "nombre": "Juan", "activo": False}
        supabase, chain, _ = make_supabase_mock(data=[prestatario_actualizado])

        delete_prestatario(supabase, 1)

        # Nunca debe llamar a .delete()
        chain.delete.assert_not_called()

    def test_borrado_logico_marca_activo_false(self):
        prestatario_actualizado = {"id": 1, "activo": False}
        supabase, chain, _ = make_supabase_mock(data=[prestatario_actualizado])

        delete_prestatario(supabase, 1)

        # Debe llamar a update con activo=False
        chain.update.assert_called_once_with({"activo": False})


# ============================================================================
# TESTS — SERVICES: TIPOS DE MATERIALES
# ============================================================================

class TestCreateTipoMaterial:
    """
    create_tipo_material tiene lógica especial:
    si el tipo ya existe, lo retorna sin duplicar.
    """

    def test_retorna_existente_sin_crear_duplicado(self):
        tipo_existente = {"id": 1, "nombre": "Filamento"}
        supabase, chain, _ = make_supabase_mock(data=[tipo_existente])

        resultado = create_tipo_material(supabase, "Filamento")

        # No debe llamar a insert porque ya existe
        chain.insert.assert_not_called()
        assert resultado["nombre"] == "Filamento"

    def test_crea_nuevo_si_no_existe(self):
        tipo_nuevo = {"id": 2, "nombre": "Resina"}

        # Primera llamada (verificar si existe): vacía
        # Segunda llamada (insert): retorna el nuevo tipo
        supabase = MagicMock()
        response_vacio = MagicMock()
        response_vacio.data = []
        response_nuevo = MagicMock()
        response_nuevo.data = [tipo_nuevo]

        chain_select = MagicMock()
        chain_select.execute.return_value = response_vacio
        chain_select.eq.return_value = chain_select

        chain_insert = MagicMock()
        chain_insert.execute.return_value = response_nuevo

        chain_table = MagicMock()
        chain_table.select.return_value = chain_select
        chain_table.insert.return_value = chain_insert

        supabase.table.return_value = chain_table

        resultado = create_tipo_material(supabase, "Resina")

        chain_table.insert.assert_called_once_with({"nombre": "Resina"})
        assert resultado["nombre"] == "Resina"


# ============================================================================
# TESTS — SERVICES: PRÉSTAMOS
# ============================================================================

class TestGetPrestamos:

    def test_filtra_por_estado_cuando_se_indica(self):
        supabase, chain, _ = make_supabase_mock(data=[])

        get_prestamos(supabase, estado="activo")

        chain.eq.assert_called_once_with("estado", "activo")

    def test_no_filtra_si_estado_es_none(self):
        supabase, chain, _ = make_supabase_mock(data=[])

        get_prestamos(supabase, estado=None)

        chain.eq.assert_not_called()


class TestGetPrestamosActivos:

    def test_llama_con_estado_activo(self):
        supabase, chain, _ = make_supabase_mock(data=[])

        get_prestamos_activos(supabase)

        chain.eq.assert_called_once_with("estado", "activo")

    def test_retorna_lista_de_prestamos(self):
        prestamos = [{"id": 1, "estado": "activo"}, {"id": 2, "estado": "activo"}]
        supabase, _, _ = make_supabase_mock(data=prestamos)

        resultado = get_prestamos_activos(supabase)

        assert len(resultado) == 2


# ============================================================================
# TESTS — SCHEMAS: EQUIPO
# ============================================================================

class TestEquipoCreate:

    def test_crea_equipo_valido(self):
        equipo = EquipoCreate(nombre="Laptop", marca="Dell", codigo="PC-01")
        assert equipo.nombre == "Laptop"
        assert equipo.codigo == "PC-01"

    def test_campos_opcionales_son_none_por_defecto(self):
        equipo = EquipoCreate(nombre="Laptop", marca="Dell", codigo="PC-01")
        assert equipo.accesorios is None
        assert equipo.serial is None
        assert equipo.estado is None

    def test_falla_sin_nombre(self):
        with pytest.raises(ValidationError):
            EquipoCreate(marca="Dell", codigo="PC-01")

    def test_falla_sin_marca(self):
        with pytest.raises(ValidationError):
            EquipoCreate(nombre="Laptop", codigo="PC-01")

    def test_falla_sin_codigo(self):
        with pytest.raises(ValidationError):
            EquipoCreate(nombre="Laptop", marca="Dell")


class TestEquipoUpdate:

    def test_todos_los_campos_son_opcionales(self):
        # EquipoUpdate no debe fallar con un dict vacío
        update = EquipoUpdate()
        assert update.nombre is None
        assert update.marca is None
        assert update.codigo is None

    def test_actualiza_solo_un_campo(self):
        update = EquipoUpdate(nombre="Nuevo Nombre")
        assert update.nombre == "Nuevo Nombre"
        assert update.marca is None


# ============================================================================
# TESTS — SCHEMAS: ELECTRONICA Y ROBOTS
# ============================================================================

class TestElectronicaBase:

    def test_valores_por_defecto_en_cero(self):
        e = ElectronicaBase(nombre="Arduino")
        assert e.en_uso == 0
        assert e.en_stock == 0

    def test_falla_sin_nombre(self):
        with pytest.raises(ValidationError):
            ElectronicaBase()


class TestRobotBase:

    def test_valores_por_defecto_en_cero(self):
        robot = RobotBase(nombre="NAO")
        assert robot.fuera_de_servicio == 0
        assert robot.en_uso == 0
        assert robot.disponible == 0

    def test_falla_sin_nombre(self):
        with pytest.raises(ValidationError):
            RobotBase()


# ============================================================================
# TESTS — SCHEMAS: PRÉSTAMO
# ============================================================================

class TestPrestamoCreate:

    def test_crea_prestamo_con_equipo(self):
        prestamo = PrestamoCreate(prestatario_id=1, equipo_id=5)
        assert prestamo.prestatario_id == 1
        assert prestamo.equipo_id == 5
        assert prestamo.estado == "activo"

    def test_estado_por_defecto_es_activo(self):
        prestamo = PrestamoCreate(prestatario_id=1)
        assert prestamo.estado == "activo"

    def test_todos_los_items_son_opcionales(self):
        # Un préstamo puede crearse sin item asignado aún
        prestamo = PrestamoCreate(prestatario_id=1)
        assert prestamo.equipo_id is None
        assert prestamo.electronica_id is None
        assert prestamo.robot_id is None
        assert prestamo.material_id is None

    def test_falla_sin_prestatario_id(self):
        with pytest.raises(ValidationError):
            PrestamoCreate()


# ============================================================================
# TESTS — SCHEMAS: AUTH
# ============================================================================

class TestLoginRequest:

    def test_login_valido(self):
        login = LoginRequest(email="user@example.com", password="secreto123")
        assert login.email == "user@example.com"

    def test_falla_con_email_invalido(self):
        with pytest.raises(ValidationError):
            LoginRequest(email="no-es-un-email", password="secreto123")

    def test_falla_con_password_corto(self):
        with pytest.raises(ValidationError):
            LoginRequest(email="user@example.com", password="123")

    def test_password_exactamente_6_caracteres_es_valido(self):
        login = LoginRequest(email="user@example.com", password="123456")
        assert login.password == "123456"


class TestRegisterRequest:

    def test_registro_valido_con_rol_admin(self):
        reg = RegisterRequest(
            email="admin@example.com",
            password="segura123",
            nombre="Admin",
            rol="admin"
        )
        assert reg.rol == "admin"

    def test_registro_valido_con_rol_inventory(self):
        reg = RegisterRequest(
            email="inv@example.com",
            password="segura123",
            nombre="Inventario",
            rol="inventory"
        )
        assert reg.rol == "inventory"

    def test_registro_valido_con_rol_viewer(self):
        reg = RegisterRequest(
            email="view@example.com",
            password="segura123",
            nombre="Lector",
            rol="viewer"
        )
        assert reg.rol == "viewer"

    def test_falla_con_rol_invalido(self):
        with pytest.raises(ValidationError):
            RegisterRequest(
                email="x@example.com",
                password="segura123",
                nombre="X",
                rol="superadmin"  # no permitido
            )

    def test_rol_es_opcional(self):
        reg = RegisterRequest(
            email="x@example.com",
            password="segura123",
            nombre="Usuario"
        )
        assert reg.rol is None

    def test_falla_con_nombre_de_un_caracter(self):
        with pytest.raises(ValidationError):
            RegisterRequest(
                email="x@example.com",
                password="segura123",
                nombre="X"  # min_length=2
            )

    def test_falla_con_email_invalido(self):
        with pytest.raises(ValidationError):
            RegisterRequest(
                email="correo-malo",
                password="segura123",
                nombre="Usuario"
            )


class TestRefreshTokenRequest:

    def test_acepta_token_valido(self):
        req = RefreshTokenRequest(refresh_token="eyJtoken...")
        assert req.refresh_token == "eyJtoken..."

    def test_falla_sin_token(self):
        with pytest.raises(ValidationError):
            RefreshTokenRequest()