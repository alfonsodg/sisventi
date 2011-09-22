# -*- coding: utf-8 -*-

db = DAL('mysql://root@localhost/sisventi')

# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'maestrcontroller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []

import datetime
from gluon.tools import Mail, Auth, Crud, Service, PluginManager, prettydate

mail = Mail()                                  # mailer
auth = Auth(db)                                # authentication/authorization
crud = Crud(db)                                # for CRUD helpers using auth
service = Service()                            # for json, xml, jsonrpc, xmlrpc, amfrpc
plugins = PluginManager()
today = datetime.date.today()
now = datetime.datetime.now()

# Custom auth_user table
db.define_table(
    auth.settings.table_user_name,
    Field('username', length=128, default='', label=T('Usuario'), unique=True),
    Field('first_name', length=128, default='', label=T('Nombres')),
    Field('last_name', length=128, default='', label=T('Apellidos')),
    Field('email', length=128, default='', unique=True, label=T('Correo electrónico')),
    Field('password', 'password', length=512, readable=False, label=T('Contraseña')),
    Field('registration_date', 'date', default=today, writable=False, readable=False, label=T('Tiempo Registro')),
    Field('registration_key', length=512, writable=False, readable=False, default=''),
    Field('reset_password_key', length=512, writable=False, readable=False, default=''),
    Field('registration_id', length=512, writable=False, readable=False, default='')
)

custom_auth_table = db[auth.settings.table_user_name] # get the custom_auth_table
custom_auth_table.username.requires = [
    IS_NOT_EMPTY(error_message='Campo obligatorio'),
    IS_NOT_IN_DB(db, custom_auth_table.username, error_message=T('El nombre de usuario ya está registrado'))]
custom_auth_table.first_name.requires = [
    IS_NOT_EMPTY(error_message='Campo obligatorio')]
custom_auth_table.last_name.requires = [
    IS_NOT_EMPTY(error_message='Campo obligatorio')]
custom_auth_table.password.requires = [
    IS_NOT_EMPTY(error_message='Campo obligatorio'),
    CRYPT()]
custom_auth_table.email.requires = [
    IS_EMAIL(error_message=auth.messages.invalid_email),
    IS_NOT_IN_DB(db, custom_auth_table.email, error_message=T('El correo ya está registrado'))]

auth.settings.table_user = custom_auth_table


mail.settings.server = 'logging' or 'smtp.gmail.com:587'  # your SMTP server
mail.settings.sender = 'you@gmail.com'         # your email
mail.settings.login = 'username:password'      # your credentials or None

auth.settings.hmac_key = 'sha512:a58dabf0-5503-4058-b583-f13a0b4add4f'   # before define_tables()
auth.define_tables(username=True)                           # creates all needed tables
auth.settings.mailer = mail                    # for user email verification
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.messages.verify_email = 'Click on the link http://'+request.env.http_host+URL('default','user',args=['verify_email'])+'/%(key)s to verify your email'
auth.settings.reset_password_requires_verification = True
auth.messages.reset_password = 'Click on the link http://'+request.env.http_host+URL('default','user',args=['reset_password'])+'/%(key)s to reset your password'
crud.settings.auth = None        # =auth to enforce authorization on crud


# Actions disabled
auth.settings.actions_disabled.append('register')


# Language
T.force('es-es')


# Tables
db.define_table('monedas',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False), 
    Field('modo', 'integer', default=0, notnull=False), 
    Field('codigo', 'string', default='', label='Código', notnull=False), 
    Field('nombre', 'string', default='', notnull=False), 
    Field('simbolo', 'string', default='', label='Símbolo', notnull=False), 
    Field('orden', 'integer', default=0, notnull=False) 
)
    
db.define_table('almacenes_lista',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('almacen', 'string', default='', notnull=False), 
    Field('descripcion', 'string', default='', notnull=False),
    Field('modo', 'integer', default=0, notnull=False), 
    Field('area', 'string', default='', notnull=False), 
    Field('ubigeo', 'string', default='', notnull=False), 
    Field('direccion', 'string', default='', notnull=False), 
    Field('tipo_doc', 'integer', default=0, notnull=False), 
    Field('doc_id', 'string', default='', notnull=False)
)


db.define_table('puntos_venta',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('codigo', 'string', default='', notnull=False), 
    Field('nombre', 'string', default='', notnull=False), 
    Field('distrito', 'string', default='', notnull=False), 
    Field('direccion', 'string', default='', label='Dirección', notnull=False), 
    Field('pos_1', 'integer', default=0, label='Posición 1', notnull=False), 
    Field('pos_2', 'integer', default=0, label='Posición 2', notnull=False),
    Field('almacen', db.almacenes_lista, label='Almacén',
          requires=IS_IN_DB(db, db.almacenes_lista, '%(almacen)s', zero='[Seleccionar]',
                            error_message='Seleccione un almacén')),
    Field('alias', 'string', default='', notnull=False), 
    Field('area', 'integer', default=0, notnull=False), 
    Field('factor_merma', 'double', default=0.0, label='Factor Merma', notnull=False)
)


db.define_table('condiciones_comerciales',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('condicion', 'string', default='', label='Condición', notnull=False), 
    Field('modo', 'integer', default=0, notnull=False), 
    Field('descripcion', 'string', default='', label='Descripción', notnull=False), 
    Field('codigo', 'integer', default=0, label='Código', notnull=False), 
    Field('dias', 'integer', default=0, label='Días', notnull=False), 
    Field('posicion', 'integer', default=0, label='Posición', notnull=False)
)


db.define_table('documentos_identidad', 
    Field('id', 'string'), 
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('nombre', 'string', default='', notnull=False),
    Field('longitud', 'integer', default=9, notnull=False)
)


db.define_table('directorio',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False), 
    Field('modo', 'string',
          requires=IS_IN_SET({'1':'Cliente', '2':'Proveedor'}, zero='[Seleccionar]',
                             error_message='Seleccione el modo')),
    Field('razon_social', 'string', default='', notnull=False, label='Razón Social'),
    Field('nombre_corto', 'string', default=''), 
    Field('rubro', 'integer', default=0, notnull=False), 
    Field('nombres', 'string', default='', notnull=False), 
    Field('apellidos', 'string', default='', notnull=False), 
    Field('tipo_doc', db.documentos_identidad, label='Tipo de Documento',
          requires=IS_IN_DB(db, db.documentos_identidad, '%(nombre)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione una tipo de documento')), 
    Field('doc_id', 'string', default='', notnull=False, label='ID del Documento'), 
    Field('doc_id_aux', 'string', default='', label='ID Auxiliar del Documento'),
    Field('pais', 'string', default='Perú', notnull=False, label='País'),
    Field('ubigeo', 'string', default='', notnull=False, label='Departamento'), 
    Field('direccion', 'string', default='', notnull=False, label='Dirección'), 
    Field('codigo_postal', 'string', default='', label='Código Postal'), 
    Field('referencia', 'string', default=''), 
    Field('condicion', db.condiciones_comerciales, label='Condición',
          requires=IS_IN_DB(db, db.condiciones_comerciales, '%(condicion)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione una condición')), 
    Field('tiempo_cred', 'integer', default=0, notnull=False, label='Días a Pagar'),
    Field('intervalo', 'integer', default=0, notnull=False, label='Intervalo'),
    Field('interes', 'double', default=0.0, notnull=False, label='Interés'), 
    Field('linea_credito', 'double', default=0.0, notnull=False, label='Línea de Crédito'), 
    Field('representante_legal', 'string', default=''), 
    Field('cargo', 'string', default=''), 
    Field('fecha', 'date', notnull=False, default=datetime.date.today()), 
    Field('sexo', 'string',
          requires=IS_IN_SET({'1':'ND', '2':'Masculino', '3':'Femenino'}, zero='[Seleccionar]',
                             error_message='Seleccione el sexo')), 
    Field('preferente', 'boolean', default=False)
)

    
db.define_table('transportistas',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False), 
    Field('codigo', 'string', default='', label='Código', notnull=False), 
    Field('emp_doc_id', 'string', default='', notnull=False), 
    Field('doc_id', 'string', default='', notnull=False), 
    Field('nombres', 'string', default='', notnull=False), 
    Field('apellidos', 'string', default='', notnull=False), 
    Field('ubigeo', 'string', default='', notnull=False), 
    Field('direccion', 'string', default='', label='Dirección', notnull=False), 
    Field('posicion', 'integer', default=0, label='Posición', notnull=False)
)
    

db.define_table('turnos',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False), 
    Field('turno', 'string', default='', notnull=False), 
    Field('descripcion', 'string', default='', label='Descripción', notnull=False), 
    Field('hora_inicio', 'time', default=datetime.time(0,0,0), label='Hora de Inicio', notnull=False), 
    Field('hora_fin', 'time', default=datetime.time(0,0,0), label='Hora de Fin', notnull=False)
)


db.define_table('articulos',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False), 
    Field('articulo', 'string', default='', label='Artículo', notnull=False), 
    Field('nombre', 'string', default='', notnull=False), 
    Field('posicion', 'integer', default=0, label='Posición', notnull=False)
)


db.define_table('catmod',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False), 
    Field('catmod', 'string', default='', label='Categoría Modo', notnull=False), 
    Field('nombre', 'string', default='', notnull=False), 
    Field('posicion', 'integer', default=0, label='Posición', notnull=False)
)


db.define_table('empaques',
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False), 
    Field('empaque', 'string', default='', notnull=False), 
    Field('nombre', 'string', default='', notnull=False), 
    Field('posicion', 'integer', default=0, label='Posición', notnull=False)
)


db.define_table('sub_casas',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False), 
    Field('sub_casa', 'string', default='', notnull=False), 
    Field('nombre', 'string', default='', notnull=False), 
    Field('posicion', 'integer', default=0, label='Posición', notnull=False)
)


db.define_table('sellos',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False), 
    Field('sello', 'string', default='', notnull=False), 
    Field('nombre', 'string', default='', notnull=False), 
    Field('posicion', 'integer', default=0, label='Posición', notnull=False)
)


db.define_table('casas',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False), 
    Field('casa', 'string', default='', notnull=False), 
    Field('nombre', 'string', default='', notnull=False), 
    Field('posicion', 'integer', default=0, label='Posición', notnull=False)
)
    

db.define_table('sub_sellos',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False), 
    Field('sub_sello', 'string', default='', notnull=False), 
    Field('nombre', 'string', default='', notnull=False), 
    Field('posicion', 'integer', default=0, label='Posición', notnull=False)
)


db.define_table('status',
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False), 
    Field('status', 'string', default='', label='Estado', notnull=False), 
    Field('nombre', 'string', default='', notnull=False), 
    Field('posicion', 'integer', default=0, label='Posición', notnull=False)
)


db.define_table('tipos',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False), 
    Field('tipo', 'string', default='', notnull=False), 
    Field('nombre', 'string', default='', notnull=False), 
    Field('posicion', 'integer', default=0, label='Posición', notnull=False)
)


db.define_table('unidades_medida',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('codigo', 'string', default='', label='Código', notnull=False), 
    Field('descripcion', 'string', default='', label='Descripción', notnull=False), 
    Field('modo', 'integer', default=0, notnull=False), 
    Field('abreviatura_origen', 'string', default='', notnull=False), 
    Field('abreviatura_destino', 'string', default='', notnull=False), 
    Field('factor', 'double', default=0.0, notnull=False)
)


db.define_table('generos',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('genero', 'string', default='', label='Género', notnull=False), 
    Field('nombre', 'string', default='', notnull=False), 
    Field('posicion', 'integer', default=0, label='Posición', notnull=False)
)


db.define_table('sub_generos',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('genero', db.generos, label='Género',
          requires=IS_IN_DB(db, db.generos, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un género')),
    Field('sub_genero', 'string', default='', label='Sub-Género', notnull=False), 
    Field('nombre', 'string', default='', notnull=False), 
    Field('posicion', 'integer', default=0, label='Posición', notnull=False)
)


db.define_table('categorias',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False), 
    Field('categoria', 'string', default='', label='Categoría', notnull=False), 
    Field('nombre', 'string', default='', notnull=False), 
    Field('posicion', 'integer', default=0, label='Posición', notnull=False)
)


db.define_table('maestro',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False), 
    Field('codbarras', 'string', default='', notnull=False, label='Código'), 
    Field('pv', db.puntos_venta, label='Punto de Venta',
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')), 
    Field('grupo_venta', 'string', default='', notnull=False), 
    Field('articulo', db.articulos,
          requires=IS_IN_DB(db, db.articulos, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un artículo')), 
    Field('casa', db.casas,
          requires=IS_IN_DB(db, db.casas, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione una casa')), 
    Field('sub_casa', db.sub_casas,
          requires=IS_IN_DB(db, db.sub_casas, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione una sub-casa')), 
    Field('genero', db.generos,
          requires=IS_IN_DB(db, db.generos, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un género')), 
    Field('sub_genero', db.sub_generos,
          requires=IS_IN_DB(db, db.sub_generos, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un sub-género')), 
    Field('empaque', db.empaques,
          requires=IS_IN_DB(db, db.empaques, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un empaque')), 
    Field('sello', db.sellos,
          requires=IS_IN_DB(db, db.sellos, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un sello')), 
    Field('sub_sello', db.sub_sellos,
          requires=IS_IN_DB(db, db.sub_sellos, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un sub-sello')), 
    Field('tipo', db.tipos,
          requires=IS_IN_DB(db, db.tipos, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un tipo')), 
    Field('catmod', db.catmod,
          requires=IS_IN_DB(db, db.catmod, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un catmod')), 
    Field('categoria', db.categorias,
          requires=IS_IN_DB(db, db.categorias, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione una categoría')), 
    Field('status', db.status,
          requires=IS_IN_DB(db, db.status, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un status')), 
    Field('moneda', db.monedas,
          requires=IS_IN_DB(db, db.monedas, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione una moneda')), 
    Field('precio', 'double', default=0.0, notnull=False), 
    Field('modo_impuesto', 'integer', default=0, notnull=False, label='Modo de Impuesto'), 
    Field('impuesto', 'string', default='', notnull=False), 
    Field('nombre', 'string', default='', notnull=False), 
    Field('descripcion', 'string', default='', notnull=False, label='Descripción'), 
    Field('alias', 'string', default='', notnull=False), 
    Field('descuento', 'integer', default=0, notnull=False), 
    Field('dependencia', 'integer', default=0, notnull=False), 
    Field('stock_min', 'double', default=0.0, notnull=False), 
    Field('stock_max', 'double', default=0.0, notnull=False), 
    Field('reposicion', 'integer', default=0, notnull=False), 
    Field('unidad_medida', db.unidades_medida,
          requires=IS_IN_DB(db, db.unidades_medida, '%(descripcion)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione una unidad de medida')),
    Field('unidad_medida_valor', 'double', default=0.0, notnull=False),
    Field('ventas_key', 'integer', default=0, notnull=False),
    Field('aux_num_data', 'integer', default=0, notnull=False),
    Field('estado', 'integer', default=1, notnull=False),
    Field('fecha', 'date', notnull=False),
)

db.maestro.codbarras.requires = [
    IS_NOT_EMPTY(error_message='Campo obligatorio'),
    IS_NOT_IN_DB(db, db.maestro.codbarras, error_message=T('El código ya está registrado'))]
db.maestro.descripcion.requires = [
    IS_NOT_EMPTY(error_message='Campo obligatorio'),
    IS_NOT_IN_DB(db, db.maestro.nombre, error_message=T('La descripción ya está en uso'))]
db.maestro.alias.requires = [
    IS_NOT_EMPTY(error_message='Campo obligatorio'),
    IS_NOT_IN_DB(db, db.maestro.alias, error_message=T('El alias ya está registrado'))]


db.define_table('operaciones_logisticas',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('operacion', 'string', default='', label='Operación', notnull=False),
    Field('modo', 'integer', default=1, notnull=False), 
    Field('descripcion', 'string', default='', label='Descripción', notnull=False), 
    Field('operacion_relac', 'string', default='', label='Operación Relación', notnull=False), 
    Field('almacen_relac', 'string', default='', label='Almacén Relación', notnull=False),
    Field('detalle', 'string', default='', label='Detalle', notnull=False)
)

    
db.define_table('almacenes',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('almacen', db.almacenes_lista, label='Almacén',
          requires=IS_IN_DB(db, db.almacenes_lista, '%(almacen)s', zero='[Seleccionar]',
                            error_message='Seleccione un almacén')),
    Field('modo', 'integer', default=1, notnull=False),
    Field('tiempo', 'datetime', default=now, notnull=True),  
    Field('estado', 'integer', default=1, notnull=False),
    Field('user_ing', db.auth_user, default='', notnull=False),
    Field('operacion_logistica', db.operaciones_logisticas, label='Operación Logística',
          requires=IS_IN_DB(db, db.operaciones_logisticas, '%(operacion)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione una Operacion Logística')),
    #Field('operacion_logistica', db.operaciones_logisticas, default='', notnull=False),  
    Field('compra_n_doc_prefijo', 'string', default='', notnull=False),  
    Field('compra_n_doc_base', 'integer', default=0, notnull=False),  
    Field('compra_n_doc_sufijo', 'string', default='', notnull=False),  
    Field('proveedor_n_doc', 'string', default='', notnull=False),  
    Field('modo_doc', 'integer', default=0, notnull=False),
    Field('tipo_doc', 'integer', default=0, notnull=False),  
    Field('fecha_doc', 'date', notnull=True, default=datetime.date.today()),
    Field('n_doc_prefijo', 'string', default='', notnull=False),  
    Field('n_doc_base', 'integer', default=0, notnull=False),  
    Field('n_doc_sufijo', 'string', default='', notnull=False),  
    Field('proveedor', db.directorio, default='', notnull=False),  
    Field('proveedor_tipo_doc', 'string', default='', notnull=False),  
    Field('proveedor_condicion', 'integer', default=0, notnull=False),  
    Field('proveedor_fecha_doc', 'date', notnull=False),
    Field('proveedor_moneda_doc', 'integer', default=0, notnull=False), 
    Field('proveedor_total_doc', 'double', default=0.0, notnull=False), 
    Field('almacen_origen', db.almacenes_lista, label='Almacén Origen',
          requires=IS_IN_DB(db, db.almacenes_lista, '%(almacen)s', zero='[Seleccionar]',
                            error_message='Seleccione un almacén origen')),
    Field('almacen_destino', db.almacenes_lista, label='Almacén Destino',
          requires=IS_IN_DB(db, db.almacenes_lista, '%(almacen)s', zero='[Seleccionar]',
                            error_message='Seleccione un almacén destino')),
    Field('articulo', db.articulos, default='', notnull=False),
    Field('codbarras_padre', db.maestro, label='Código Padre',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('codbarras', db.maestro, label='Código',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código')),
    #Field('codbarras_padre', db.maestro, default='', notnull=False), 
    #Field('codbarras', db.maestro, default='', notnull=False), 
    Field('pedido', 'integer', default=1, notnull=False),
    Field('peso_expresado', 'double', default=0.0, notnull=False), 
    Field('peso', 'double', default=0.0, notnull=False),
    Field('cantidad_expresado', 'double', default=0.0, notnull=False),
    Field('ingreso', 'double', default=0.0, notnull=False), 
    Field('salida', 'double', default=0.0, notnull=False), 
    Field('tipo', 'string', default='', notnull=False), 
    Field('valor', 'double', default=0.0, notnull=False), 
    Field('fecha_produccion', 'date', notnull=False), 
    Field('fecha_vencimiento', 'date', notnull=False), 
    Field('extra_data', 'string', default='', notnull=False), 
    Field('transportista', db.transportistas, default='', notnull=False), 
    Field('vehiculo', 'string', default='', notnull=False), 
    Field('grupo', 'integer', default=0, notnull=False), 
    Field('turno', db.turnos, default='', notnull=False), 
    Field('masa', 'string', default='', notnull=False), 
    Field('temperatura', 'double', default=0.0, notnull=False), 
    Field('peso', 'double', default=0.0, notnull=False), 
    Field('hora_inicial', 'time', notnull=False), 
    Field('hora_final', 'time', notnull=False), 
    Field('n_serie', 'string', default='', notnull=False), 
    Field('n_prefijo_relacion', 'string', default='', notnull=False), 
    Field('n_doc_relacion', 'integer', default=0, notnull=False), 
    Field('n_sufijo_relacion', 'string', default='', notnull=False), 
    Field('observaciones', 'string', default='', notnull=False)
)


db.define_table('almacenes_ubicacion',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('almacen', db.almacenes_lista, label='Almacén',
          requires=IS_IN_DB(db, db.almacenes_lista, '%(almacen)s', zero='[Seleccionar]',
                            error_message='Seleccione un almacén')),
    Field('codbarras', db.maestro, label='Código',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=True),
    Field('ubicacion', 'string', default='', notnull=False)
)


db.define_table('areas',
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False), 
    Field('area', 'string', default='', label='Área', notnull=False), 
    Field('nombre', 'string', default='', notnull=False), 
    Field('descripcion', 'string', default='', label='Descripción', notnull=False), 
    Field('posicion', 'integer', default=0, label='Posición', notnull=False)
)


db.define_table('backup',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False), 
    Field('tiempo', 'datetime', notnull=False), 
    Field('log', 'string', default='', notnull=False)
)


db.define_table('clientes_preferentes', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False), 
    Field('doc_id', 'string', default='', label='ID de Documento', notnull=False), 
    Field('tiempo', 'datetime', default=now, notnull=True), 
    Field('promocion', 'string', default='', label='Promoción', notnull=False), 
    Field('tarjeta', 'string', default='', notnull=False), 
    Field('user_ing', db.auth_user,
          requires=IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione un usuario'))
)


db.define_table('compras_ordenes', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False), 
    Field('tiempo', 'datetime', default=now, notnull=True),  
    Field('n_doc_prefijo', 'string', default='', notnull=False), 
    Field('n_doc_base', 'integer', default=0, notnull=False), 
    Field('n_doc_sufijo', 'string', default='', notnull=False), 
    Field('estado', 'integer', default=1, notnull=False), 
    Field('area', db.areas,
          requires=IS_IN_DB(db, db.areas, '%(area)s', zero='[Seleccionar]',
                            error_message='Seleccione un área')), 
    Field('forma_pago', 'string', default='', notnull=False), 
    Field('codbarras', db.maestro, label='Código',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=True),
    Field('cantidad', 'double', default=0.0, notnull=False), 
    Field('cantidad_proveedor', 'double', default=0.0, notnull=False), 
    Field('moneda', db.monedas,
          requires=IS_IN_DB(db, db.monedas, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione una moneda')), 
    Field('precio_neto', 'double', default=0.0, notnull=False), 
    Field('precio_imp', 'double', default=0.0, notnull=False), 
    Field('precio_bruto', 'double', default=0.0, notnull=False), 
    Field('sub_total_neto', 'double', default=0.0, notnull=False), 
    Field('sub_total_imp', 'double', default=0.0, notnull=False), 
    Field('sub_total_bruto', 'double', default=0.0, notnull=False), 
    Field('proveedor', db.directorio,
          requires=IS_IN_DB(db, db.directorio, '%(razon_social)s', zero='[Seleccionar]',
                            error_message='Seleccione un proveedor')), 
    Field('total_neto', 'double', default=0.0, notnull=False), 
    Field('total_imp', 'double', default=0.0, notnull=False), 
    Field('total_bruto', 'double', default=0.0, notnull=False), 
    Field('total_texto', 'string', default='', notnull=False), 
    Field('fecha_entrega', 'date', notnull=False), 
    Field('lugar_entrega', 'string', default='', notnull=False), 
    Field('user_req', 'string', default='', notnull=False), 
    Field('user_ing', db.auth_user,
          requires=IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione un usuario')), 
    Field('user_aut1', db.auth_user,
          requires=IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione un usuario')), 
    Field('user_aut2', db.auth_user,
          requires=IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione un usuario')), 
    Field('user_anul', db.auth_user,
          requires=IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione un usuario')), 
    Field('tiempo_anul', 'datetime', notnull=False), 
    Field('observaciones', 'string', default='', notnull=False)
)


db.define_table('control_insumos', 
    Field('id', 'integer'),
    Field('codbarras_padre', db.maestro, label='Código Padre',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('codbarras_hijo', db.maestro, label='Código Padre',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('gramos', 'double', default=0.0, notnull=False), 
    Field('adicional', 'double', default=0.0, notnull=False), 
    Field('estado', 'integer', default=0, notnull=False), 
    Field('truco', 'integer', default=0, notnull=False), 
    Field('orden', 'integer', default=0, notnull=False), 
    Field('modo', 'integer', default=0, notnull=False)
)


db.define_table('control_produccion', 
    Field('id', 'integer'), 
    Field('fecha', 'date', notnull=False), 
    Field('turno', 'string', default='', notnull=False), 
    Field('codbarras', 'string', default='', notnull=False), 
    Field('producto_derivado', 'string', default='', notnull=False)
)


#db.control_produccion.codbarras.widget = SQLFORM.widgets.autocomplete(
#     request, db.maestro.alias, id_field=db.maestro.id, mode=1,
#     filterby=db.maestro.genero, filtervalue='1')


db.define_table('criterio',
    Field('id', 'integer'),
    Field('pv', db.puntos_venta,
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')),
    Field('grupo_distribucion', 'string', default='', notnull=False), 
    Field('turno', 'string', default='', notnull=False), 
    Field('porcentaje', 'double', default=100.0, notnull=False), 
    Field('codbarras', db.maestro,
          requires=IS_IN_DB(db, db.maestro, '%(codbarras)s', zero='[Seleccionar]',
                            error_message='Seleccione un código de barras'))
)


db.define_table('delivery',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False), 
    Field('pv', db.puntos_venta, label='Punto de Venta',
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')), 
    Field('tiempo', 'datetime', default=now, notnull=True),  
    Field('numero', 'integer', default=0, notnull=False, label='Número'), 
    Field('cliente', 'string', default='', notnull=False), 
    Field('docnum', 'integer', default=0, notnull=False, label='Documento'), 
    Field('carac1', 'string', default='', notnull=False, label='Característica 1'), 
    Field('carac2', 'string', default='', notnull=False, label='Característica 2'), 
    Field('carac3', 'string', default='', notnull=False, label='Característica 3')
)


db.define_table('directorio_auxiliar', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Tiempo Registro', default=now), 
    Field('doc_id', 'string', default='', notnull=False), 
    Field('telefono', 'string', default='', notnull=False), 
    Field('tel_prio', 'integer', default=0, notnull=False), 
    Field('fax', 'string', default='', notnull=False), 
    Field('fax_prio', 'integer', default=0, notnull=False), 
    Field('email', 'string', default='', notnull=False), 
    Field('ema_prio', 'integer', default=0, notnull=False), 
    Field('web', 'string', default='', notnull=False), 
    Field('web_prio', 'integer', default=0, notnull=False), 
    Field('contacto', 'string', default='', notnull=False), 
    Field('con_prio', 'integer', default=0, notnull=False), 
    Field('telefono_c', 'string', default='', notnull=False), 
    Field('tec_prio', 'integer', default=0, notnull=False), 
    Field('email_c', 'string', default='', notnull=False), 
    Field('emc_prio', 'integer', default=0, notnull=False)
)


db.define_table('documentos_comerciales', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False), 
    Field('modo', 'integer', default=0, notnull=False), 
    Field('documento', 'integer', default=0, notnull=False), 
    Field('doc_reg', 'string', default='', notnull=False), 
    Field('nombre', 'string', default='', notnull=False), 
    Field('pv', db.puntos_venta, label='Punto de Venta',
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')), 
    Field('caja', 'integer', default=0, notnull=False), 
    Field('prefijo', 'string', default='', notnull=False), 
    Field('correlativo', 'integer', default=0, notnull=False), 
    Field('sufijo', 'string', default='', notnull=False), 
    Field('copia', 'integer', default=0, notnull=False), 
    Field('detalle', 'integer', default=0, notnull=False), 
    Field('limite', 'integer', default=0, notnull=False, label='Límite'), 
    Field('impresion', 'integer', default=0, notnull=False, label='Impresión'), 
    Field('impuestos', 'string', default='', notnull=False),
    Field('port', 'string', default='', notnull=False),
    Field('layout', 'string', default='', notnull=False)
)


db.define_table('docventa',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False), 
    Field('pv', db.puntos_venta, label='Punto de Venta',
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')), 
    Field('caja', 'integer', default=0, notnull=False), 
    Field('fecha_vta', 'date', notnull=True, default=datetime.date.today()), 
    Field('tiempo', 'datetime', default=now, notnull=True), 
    Field('n_doc_base', 'integer', default=0, notnull=False), 
    Field('estado', 'integer', default=0, notnull=False), 
    Field('comprobante', 'integer', default=0, notnull=False), 
    Field('cliente', 'string', default='', notnull=False), 
    Field('cv_ing', 'integer', default=0, notnull=False), 
    Field('medios_pago', 'string', default='', notnull=False),
    Field('vales', 'string', default='', notnull=False), 
    Field('sello', 'string', default='', notnull=False), 
    #Field('codigo', 'string', default='',  notnull=False),
    Field('codbarras', db.maestro, label='Código',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('detalle', 'string', default='',  notnull=False),
    #Field('sub_codbarras', 'string', default='', notnull=False),
    Field('sub_codbarras', db.maestro, label='Sub Código',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('precio', 'double', default=0.0, notnull=False), 
    Field('cantidad', 'integer', default=0, notnull=False), 
    Field('sub_total_bruto', 'double', default=0.0, notnull=False), 
    Field('sub_total_impto', 'string', default='', notnull=False), 
    Field('sub_total_neto', 'double', default=0.0, notnull=False), 
    Field('total', 'double', default=0.0, notnull=False), 
    Field('detalle_impto', 'string', default='', notnull=False), 
    Field('total_neto', 'double', default=0.0, notnull=False), 
    Field('mntsol', 'double', default=0.0, notnull=False), 
    Field('mntdol', 'double', default=0.0, notnull=False), 
    Field('cv_anul', 'integer', default=0, notnull=False),
    Field('tiempo_null', 'datetime', default=now, notnull=False), 
    Field('n_doc_sufijo', 'string', default='', notnull=False), 
    Field('n_doc_prefijo', 'string', default='', notnull=False), 
    Field('dist_type', 'integer', default=0, notnull=False), 
    Field('ext_doc', 'integer', default=0, notnull=False),
    Field('ref_cred', 'integer', default=0, notnull=False),
    Field('fecha_vto', 'date', notnull=False),
    Field('condicion_comercial', db.condiciones_comerciales,
          requires=IS_IN_DB(db, db.condiciones_comerciales, zero='[Seleccionar]',
                            error_message='Seleccione una condición'))
)


db.define_table('factores_merma', 
    Field('id', 'integer'), 
    Field('fecha', 'date', notnull=False),
    Field('pv', db.puntos_venta,
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')),
    Field('codbarras', db.maestro,
          requires=IS_IN_DB(db, db.maestro, '%(codbarras)s', zero='[Seleccionar]',
                            error_message='Seleccione un código de barras')), 
    Field('valor', 'double', default=0.0, notnull=False), 
    Field('modo', 'integer', default=0, notnull=False)
)


db.define_table('formas_pago',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('forma_pago', 'string', default='', notnull=False, label='Forma de Pago'), 
    Field('nombre', 'string', default='', notnull=False),
    Field('posicion', 'integer', default=0, notnull=False),
    Field('modo', 'integer', default=0, notnull=False)
)


db.define_table('grupo_distribucion',
    Field('id', 'integer'), 
    Field('grupo_distribucion', 'string', default='', notnull=False), 
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False), 
    Field('turno', db.turnos,
          requires=IS_IN_DB(db, db.turnos, '%(turno)s', zero='[Seleccionar]',
                            error_message='Seleccione un turno')), 
    Field('descripcion', 'string', default='', notnull=False), 
    Field('prioridad', 'integer', default=0, notnull=False)
)


db.define_table('impuestos',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False), 
    Field('codigo', 'string', default='', notnull=False), 
    Field('abreviatura', 'string', default='', notnull=False), 
    Field('nombre', 'string', default='', notnull=False), 
    Field('valor', 'double', default=0.0, notnull=False), 
    Field('modo', 'integer', default=0, notnull=False)
)


db.define_table('maestro_auxiliar', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('codbarras', db.maestro, label='Código',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('nombre', 'string', default='', notnull=False), 
    Field('valor', 'string', default='', notnull=False), 
    Field('prioridad', 'integer', default=0, notnull=False)
)


db.define_table('maestro_dependencias', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False), 
    Field('pv', db.puntos_venta, label='Punto de Venta',
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')), 
    Field('modo', 'integer'),
    Field('codbarras', db.maestro, label='Código',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('data', 'string', default='', notnull=False), 
    Field('estado', 'integer', default=1, notnull=False), 
    Field('user_ing', db.auth_user,
          requires=IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione un usuario'))
)


db.define_table('maestro_descuentos', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('pv', db.puntos_venta, label='Punto de Venta',
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')),
    Field('tiempo', 'datetime', default=now, notnull=True), 
    Field('modo', 'integer', default=0, notnull=False),
    Field('codbarras', db.maestro, label='Código',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('descuento', 'double', default=0.0, notnull=False), 
    Field('monto_req', 'double', default=0.0, notnull=False, label='Monto Requerido'), 
    Field('user_nivel', 'integer', default=0, notnull=False, label='Nivel de Usuario'), 
    Field('fecha_inicio', 'date', notnull=False, label='Fecha de Inicio'), 
    Field('hora_inicio', 'time', default=datetime.time(0,0,0), notnull=False, label='Hora de Inicio'), 
    Field('fecha_fin', 'date', notnull=False, label='Fecha de Fin'), 
    Field('hora_fin', 'time', default=datetime.time(0,0,0), notnull=False, label='Hora de Fin'), 
    Field('estado', 'integer', default=1, notnull=False), 
    Field('user_ing', db.auth_user, label='Usuario Ing.',
          requires=IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione un usuario'))
)


db.define_table('maestro_posiciones',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False), 
    Field('modo', 'integer', default=0, notnull=False),
    Field('codbarras', db.maestro, label='Código',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('posicion', 'integer', default=0, notnull=False)
)


db.define_table('maestro_proveedores', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('codbarras', db.maestro, label='Código',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('proveedor', db.directorio,
          requires=IS_IN_DB(db, db.directorio, '%(razon_social)s', zero='[Seleccionar]',
                            error_message='Seleccione un proveedor')), 
    Field('unidad_medida', db.unidades_medida,
          requires=IS_IN_DB(db, db.unidades_medida, '%(descripcion)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione una unidad de medida'))
)


db.define_table('maestro_valores', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False), 
    Field('fecha', 'date', notnull=False, default=datetime.date.today()), 
    Field('pv', db.puntos_venta,
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')),
    Field('codbarras', db.maestro, label='Código',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('valor', 'double', default=0.0, notnull=False), 
    Field('user_ing', db.auth_user,
          requires=IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione un usuario')),
    Field('estado', 'integer', default=1, notnull=False)
)


db.define_table('modos_logisticos', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False), 
    Field('modo_logistico', 'string', default='', notnull=False), 
    Field('descripcion', 'string', default='', notnull=False)
)


db.define_table('modos_pvr', 
    Field('id', 'integer'), 
    Field('tabla', 'string', default='', notnull=False), 
    Field('modo', 'integer', default=0, notnull=False), 
    Field('descripcion', 'string', default='', notnull=False), 
    Field('modo_tabla', 'integer', default=0, notnull=False)
)


db.define_table('pedidos', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False), 
    Field('fecha', 'date', notnull=False, default=datetime.date.today()), 
    Field('pv', db.puntos_venta,
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')), 
    Field('turno', db.turnos,
          requires=IS_IN_DB(db, db.turnos, '%(turno)s', zero='[Seleccionar]',
                            error_message='Seleccione un turno')), 
    Field('grupo_distribucion', db.grupo_distribucion,
          requires=IS_IN_DB(db, db.grupo_distribucion, '%(grupo_distribucion)s', zero='[Seleccionar]',
                            error_message='Seleccione un grupo de distribución')), 
    Field('area', db.areas,
          requires=IS_IN_DB(db, db.areas, '%(area)s', zero='[Seleccionar]',
                            error_message='Seleccione un área')), 
    Field('genero', db.generos,
          requires=IS_IN_DB(db, db.generos, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un género')), 
    Field('tipo', 'integer', default=0, notnull=False), 
    Field('user_req', db.auth_user,
          requires=IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione un usuario')), 
    Field('n_doc_prefijo', 'string', default='', notnull=False), 
    Field('n_doc_base', 'integer', default=0, notnull=False), 
    Field('n_doc_sufijo', 'string', default='', notnull=False),
    Field('codbarras_padre', db.maestro, label='Código',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('codbarras', db.maestro, label='Código',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('cantidad', 'double', default=0.0, notnull=False),
    Field('precio', 'double', default=0.0, notnull=False), 
    Field('peso', 'double', default=0.0, notnull=False), 
    Field('detalle', 'string', default='', notnull=False), 
    Field('modo', 'integer', default=0, notnull=False), 
    Field('estado', 'integer', default=1, notnull=False),
    Field('cliente', db.directorio,
          requires=IS_IN_DB(db, db.directorio, '%(nombre_corto)s', zero='[Seleccionar]',
                            error_message='Seleccione un cliente')),
    Field('user_ing', db.auth_user,
          requires=IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione un usuario'))
)


db.define_table('pedidos_emergencia_produccion', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False), 
    Field('fecha', 'date'), 
    Field('pv', db.puntos_venta,
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')),
    Field('turno', db.turnos,
          requires=IS_IN_DB(db, db.turnos, '%(turno)s', zero='[Seleccionar]',
                            error_message='Seleccione un turno')),
    Field('codbarras', db.maestro, label='Código',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('cantidad', 'double', default=0.0, notnull=False), 
    Field('modo', 'integer', default=0, notnull=False)
)


db.define_table('pesos_operaciones',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('codbarras', db.maestro, label='Código',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('peso_neto', 'double', default=0.0, notnull=False), 
    Field('peso_tara', 'double', default=0.0, notnull=False)
)


db.define_table('pos_administracion', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False), 
    Field('pv', db.puntos_venta,
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')),
    Field('caja', 'integer', default=0, notnull=False), 
    Field('user_ing', db.auth_user,
          requires=IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione un usuario')), 
    Field('user_out', db.auth_user,
          requires=IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione un usuario')), 
    Field('apertura', 'datetime', notnull=False), 
    Field('cierre', 'datetime', notnull=False),
    Field('estado', 'integer', default=0, notnull=False)
)


db.define_table('produccion_datos', 
    Field('id', 'integer'), 
    Field('fecha', 'date', notnull=False), 
    Field('turno', db.turnos,
          requires=IS_IN_DB(db, db.turnos, '%(turno)s', zero='[Seleccionar]',
                            error_message='Seleccione un turno')), 
    Field('grupo_distribucion', db.grupo_distribucion,
          requires=IS_IN_DB(db, db.grupo_distribucion, '%(grupo_distribucion)s', zero='[Seleccionar]',
                            error_message='Seleccione un grupo de distribución')), 
    Field('pv', db.puntos_venta,
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')),
    Field('codbarras', db.maestro, label='Código',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('codbarras_hijo', 'string', default='', notnull=False), 
    Field('cantidad', 'double', default=0.0, notnull=False), 
    Field('modo', 'integer', default=0, notnull=False)
)


db.define_table('produccion_derivados', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False), 
    Field('modo', 'integer', default=0, notnull=False), 
    Field('turno', db.turnos,
          requires=IS_IN_DB(db, db.turnos, '%(turno)s', zero='[Seleccionar]',
                            error_message='Seleccione un turno')), 
    Field('tipo', 'integer', default=0, notnull=False), 
    #Field('cp_base', 'string', default='', notnull=False),
    Field('pv_base', db.puntos_venta,
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')),
    Field('pv_aux', db.puntos_venta,
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')),
    #Field('cp_aux', 'string', default='', notnull=False), 
    Field('user_ing', db.auth_user,
          requires=IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione un usuario')), 
    Field('fecha', 'date', notnull=False), 
    Field('n_doc_prefijo', 'string', default='', notnull=False), 
    Field('n_doc_base', 'string', default='', notnull=False), 
    Field('n_doc_sufijo', 'string', default='', notnull=False),
    Field('codbarras', db.maestro, label='Código',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('ing_produccion', 'double', default=0.0, notnull=False), 
    Field('ing_traslado', 'double', default=0.0, notnull=False), 
    Field('ing_varios', 'double', default=0.0, notnull=False), 
    Field('sal_ventas', 'double', default=0.0, notnull=False), 
    Field('sal_merma', 'double', default=0.0, notnull=False), 
    Field('sal_consumo_int', 'double', default=0.0, notnull=False), 
    Field('sal_traslado', 'double', default=0.0, notnull=False), 
    Field('sal_varios', 'double', default=0.0, notnull=False)
)


db.define_table('produccion_estadistica', 
    Field('id', 'integer'), 
    Field('fecha', 'date', notnull=False), 
    Field('turno', db.turnos,
          requires=IS_IN_DB(db, db.turnos, '%(turno)s', zero='[Seleccionar]',
                            error_message='Seleccione un turno')), 
    Field('pv', db.puntos_venta,
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')),
    Field('codbarras_abuelo', 'string', default='', notnull=False), 
    Field('codbarras_padre', 'string', default='', notnull=False), 
    Field('codbarras_hijo', 'string', default='', notnull=False), 
    Field('cantidad_abuelo', 'double', default=0.0, notnull=False), 
    Field('cantidad_padre', 'double', default=0.0, notnull=False), 
    Field('porcentaje_padre', 'double', default=0.0, notnull=False), 
    Field('cantidad_hijo', 'double', default=0.0, notnull=False), 
    Field('porcentaje_hijo', 'double', default=0.0, notnull=False), 
    Field('modo', 'integer', default=0, notnull=False), 
    Field('porcentaje_general', 'double', default=0.0, notnull=False)
)


db.define_table('produccion_pedidos', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False), 
    Field('fecha', 'date', notnull=False), 
    Field('pv', db.puntos_venta,
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')),
    Field('turno', db.turnos,
          requires=IS_IN_DB(db, db.turnos, '%(turno)s', zero='[Seleccionar]',
                            error_message='Seleccione un turno')), 
    Field('modo', 'integer', default=0, notnull=False),
    Field('codbarras', db.maestro, label='Código',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('cantidad', 'double', default=0.0, notnull=False)
)


db.define_table('produccion_planeamiento', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False), 
    Field('fecha', 'date', notnull=False), 
    Field('codbarras_padre', db.maestro, label='Código',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('codbarras', db.maestro, label='Código',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('codbarras_hijo', db.maestro, label='Código',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False), 
    Field('cantidad', 'double', default=0.0, notnull=False), 
    Field('condicion_pedido', 'string', default='', notnull=False), 
    Field('grupo_distribucion', db.grupo_distribucion,
          requires=IS_IN_DB(db, db.grupo_distribucion, '%(grupo_distribucion)s', zero='[Seleccionar]',
                            error_message='Seleccione un grupo de distribución')),
    Field('pv', db.puntos_venta,
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')),
    #Field('cp', 'string', default='', notnull=False), 
    Field('turno', db.turnos,
          requires=IS_IN_DB(db, db.turnos, '%(turno)s', zero='[Seleccionar]',
                            error_message='Seleccione un turno'))
)


db.define_table('produccion_planeamiento_aux', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('fecha', 'date', notnull=False),
    Field('codbarras', db.maestro, label='Código',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False), 
    Field('cantidad', 'double', default=0.0, notnull=False), 
    Field('condicion_pedido', 'string', default='', notnull=False), 
    Field('grupo_distribucion', db.grupo_distribucion,
          requires=IS_IN_DB(db, db.grupo_distribucion, '%(grupo_distribucion)s', zero='[Seleccionar]',
                            error_message='Seleccione un grupo de distribución')),
    Field('pv', db.puntos_venta,
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')),
    #Field('cp', 'string', default='', notnull=False), 
    Field('turno', db.turnos,
          requires=IS_IN_DB(db, db.turnos, '%(turno)s', zero='[Seleccionar]',
                            error_message='Seleccione un turno'))
)


db.define_table('produccion_rendimiento', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('fecha', 'date', notnull=False), 
    Field('turno', db.turnos,
          requires=IS_IN_DB(db, db.turnos, '%(turno)s', zero='[Seleccionar]',
                            error_message='Seleccione un turno')),
    Field('modo', 'integer', default=1, notnull=False), 
    Field('tipo', 'integer', default=0, notnull=False),
    Field('codbarras', db.maestro, label='Código',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('cantidad', 'double', default=0.0, notnull=False), 
    Field('masa', 'string', default='', notnull=False), 
    Field('peso', 'double', default=0.0, notnull=False), 
    Field('temperatura', 'double', default=0.0, notnull=False), 
    Field('hora_inicial', 'time', default=datetime.time(0,0,0), notnull=False), 
    Field('hora_final', 'time', default=datetime.time(0,0,0), notnull=False)
)


db.define_table('promociones', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('pv', db.puntos_venta, label='Punto de Venta',
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')),
    Field('codigo', 'string', default='', notnull=False, label='Código'), 
    Field('nombre', 'string', default='', notnull=False), 
    Field('porcentaje', 'double', default=0.0, notnull=False), 
    Field('valor', 'double', default=0.0, notnull=False), 
    Field('modo', 'integer', default=0, notnull=False),
    Field('codbarras', db.maestro, label='Código',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('cantidad', 'integer', default=1, notnull=False), 
    Field('limite', 'integer', default=0, notnull=False, label='Límite'), 
    Field('cond_modo', 'integer', default=0, notnull=False, label='Cond. Modo'), 
    Field('cond_valor', 'integer', default=0, notnull=False, label='Cond. Valor'), 
    Field('cond_fecha_inic', 'date', notnull=False, label='Cond. Fecha de Inicio'), 
    Field('cond_hora_inic', 'time', default=datetime.time(0,0,0), notnull=False, label='Cond. Hora de Inicio'), 
    Field('cond_fecha_term', 'date', notnull=False, label='Cond. Fecha de Fin'), 
    Field('cond_hora_term', 'time', default=datetime.time(0,0,0), notnull=False, label='Cond. Hora de Fin'), 
    Field('estado', 'integer', default=0, notnull=False)
)


db.define_table('puntos_venta_grupos', 
    Field('id', 'integer'),
    Field('pv', db.puntos_venta,
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')),
    Field('grupo_distribucion', db.grupo_distribucion,
          requires=IS_IN_DB(db, db.grupo_distribucion, '%(grupo_distribucion)s', zero='[Seleccionar]',
                            error_message='Seleccione un grupo de distribución')), 
    Field('turno', db.turnos,
          requires=IS_IN_DB(db, db.turnos, '%(turno)s', zero='[Seleccionar]',
                            error_message='Seleccione un turno')), 
    Field('porcentaje', 'double', default=100.0, notnull=False),
    Field('codbarras', db.maestro, label='Código',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('modo', 'integer', default=0, notnull=False)
)


db.define_table('puntos_venta_relaciones', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('pv_padre', db.puntos_venta,
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta padre')), 
    Field('pv_hijo', db.puntos_venta,
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta hijo')), 
    Field('modo', 'integer', default=0, notnull=False)
)


db.define_table('puntos_venta_satelites',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('pv_padre', db.puntos_venta,
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta padre')), 
    Field('pv_hijo', db.puntos_venta,
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta hijo')), 
    Field('modo', 'integer', default=0, notnull=False)
)


db.define_table('recetas', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('codbarras_padre', db.maestro, label='Código Padre',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código')),
    Field('cantidad', 'double', default=0.0, notnull=False),
    Field('codbarras_hijo', db.maestro, label='Código Hijo',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código')), 
    Field('modo', 'integer', default=0, notnull=False), 
    Field('estado', 'integer', default=1, notnull=False), 
    Field('orden', 'integer', default=0, notnull=False)
)


db.define_table('relaciones', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('codbarras_padre', db.maestro, label='Código Padre',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('codbarras_hijo', db.maestro, label='Código Hijo',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('modo', 'integer', default=0, notnull=False), 
    Field('orden', 'integer', default=0, notnull=False)
)


db.define_table('rendimientos_sintesis', 
    Field('id', 'integer'), 
    Field('fecha', 'date', notnull=False), 
    Field('turno', db.turnos,
          requires=IS_IN_DB(db, db.turnos, '%(turno)s', zero='[Seleccionar]',
                            error_message='Seleccione un turno')), 
    Field('tipo', 'integer', default=0, notnull=False), 
    Field('cantidad', 'double', default=0.0, notnull=False), 
    Field('peso', 'double', default=0.0, notnull=False), 
    Field('merma', 'double', default=0.0, notnull=False), 
    Field('rendimiento', 'double', default=0.0, notnull=False)
)


db.define_table('reportes_configuracion', 
    Field('id', 'integer'), 
    Field('codigo_reporte', 'string', default='', notnull=False), 
    Field('detalle_reporte', 'string', default='', notnull=False), 
    Field('turno', db.turnos,
          requires=IS_IN_DB(db, db.turnos, '%(turno)s', zero='[Seleccionar]',
                            error_message='Seleccione un turno')),
    Field('pv', db.puntos_venta,
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')), 
    Field('grupo_distribucion', db.grupo_distribucion,
          requires=IS_IN_DB(db, db.grupo_distribucion, '%(grupo_distribucion)s', zero='[Seleccionar]',
                            error_message='Seleccione un grupo de distribución')), 
    Field('modo', 'integer', default=0, notnull=False), 
    Field('codigo_dato', 'string', default='', notnull=False), 
    Field('array', 'string', default='', notnull=False),
    Field('codbarras_abuelo', db.maestro, label='Código Abuelo',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('codbarras_padre', db.maestro, label='Código Padre',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('codbarras_hijo', db.maestro, label='Código Hijo',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('descripcion', 'string', default='', notnull=False), 
    Field('posicion', 'integer', default=0, notnull=False)
)


db.define_table('rubros',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('rubro', 'string', default='', notnull=False), 
    Field('nombre', 'string', default='', notnull=False), 
    Field('descripcion', 'string', default='', notnull=False), 
    Field('posicion', 'integer', default=0, notnull=False)
)


db.define_table('tablas_modos', 
    Field('id', 'integer'), 
    Field('tabla', 'string', default='', notnull=False), 
    Field('modo', 'string', default='', notnull=False), 
    Field('descripcion', 'string', default='', notnull=False)
)


db.define_table('tipos_cambio', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('area', db.areas,
          requires=IS_IN_DB(db, db.areas, '%(area)s', zero='[Seleccionar]',
                            error_message='Seleccione un área')), 
    Field('moneda', db.monedas,
          requires=IS_IN_DB(db, db.monedas, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione una moneda')), 
    Field('modo', 'integer', default=0, notnull=False), 
    Field('fecha', 'date', notnull=False, default=datetime.date.today()), 
    Field('hora', 'time', default=datetime.time(0,0,0), notnull=False), 
    Field('valor', 'double', default=0.0, notnull=False), 
    Field('user_ing', 'string', default='', notnull=False)
)


db.define_table('transferencias_produccion', 
    Field('id', 'integer'), 
    Field('codbarras', db.maestro,
          requires=IS_IN_DB(db, db.maestro, '%(codbarras)s', zero='[Seleccionar]',
                            error_message='Seleccione un código de barras')), 
    Field('descripcion', 'string', default='', notnull=False), 
    Field('total', 'integer', default=0, notnull=False), 
    Field('transferencia', 'integer', default=0, notnull=False), 
    Field('produccion', 'integer', default=0, notnull=False), 
    Field('turno', db.turnos,
          requires=IS_IN_DB(db, db.turnos, '%(turno)s', zero='[Seleccionar]',
                            error_message='Seleccione un turno')), 
    Field('fecha', 'date', notnull=False)
)


db.define_table('ubigeo_departamentos',
    Field('id', 'integer'),
    Field('departamento', 'string', default='', notnull=False), 
    Field('descripcion', 'string', default='', notnull=False)
)


db.define_table('ubigeo_provincias',
    Field('id', 'integer'),
    Field('departamento', 'string', default='', notnull=False), 
    Field('provincia', 'string', default='', notnull=False), 
    Field('descripcion', 'string', default='', notnull=False)
)


db.define_table('ubigeo_detalle',
    Field('id', 'integer'),
    Field('departamento', 'string', default='', notnull=False), 
    Field('provincia', 'string', default='', notnull=False), 
    Field('ubigeo', 'string', default='', notnull=False), 
    Field('descripcion', 'string', default='', notnull=False)
)


db.define_table('variaciones_derivados', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('codbarras', db.maestro,
          requires=IS_IN_DB(db, db.maestro, '%(codbarras)s', zero='[Seleccionar]',
                            error_message='Seleccione un código de barras')), 
    Field('tiempo_ini', 'datetime', notnull=False), 
    Field('tiempo_fin', 'datetime', notnull=False), 
    Field('porcentaje', 'double', default=0.0, notnull=False),
    Field('pv', db.puntos_venta,
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')),
    Field('turno', db.turnos,
          requires=IS_IN_DB(db, db.turnos, '%(turno)s', zero='[Seleccionar]',
                            error_message='Seleccione un turno')), 
    Field('modo', 'integer', default=0, notnull=False)
)


db.define_table('vehiculos',
    Field('id', 'integer'),
    Field('codigo', 'string', default='', notnull=False), 
    Field('doc_id', 'string', default='', notnull=False), 
    Field('registro', 'string', default='', notnull=False), 
    Field('marca', 'string', default='', notnull=False), 
    Field('modelo', 'string', default='', notnull=False), 
    Field('tipo', 'string', default='', notnull=False), 
    Field('caracteristicas', 'string', default='', notnull=False), 
    Field('posicion', 'integer', default=0, notnull=False)
)


db.define_table('ventas_bancos_cuentas',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('codigo', 'string', default='', notnull=False), 
    Field('entidad', 'string', default='', notnull=False), 
    Field('moneda', db.monedas,
          requires=IS_IN_DB(db, db.monedas, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione una moneda'))
)


db.define_table('ventas_bancos_operaciones', 
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False), 
    Field('pv', db.puntos_venta, label='Punto de Venta',
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')),
    Field('banco', 'string', default='', notnull=False),
    Field('agencia', 'string', default='', notnull=False),
    Field('fecha_venta', 'date', label='Fecha de Venta', notnull=False),
    Field('fecha_deposito', 'date', label='Fecha de Depósito', notnull=False), 
    Field('monto', 'double', default=0.0, notnull=False), 
    Field('cambio', 'double', default=0.0, notnull=False), 
    Field('glosa_1', 'string', default='', label='Comentario 1'), 
    Field('glosa_2', 'string', default='', label='Comentario 2')
)


db.define_table('ventas_grupos',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('codigo', 'string', default='', notnull=False), 
    Field('nombre', 'string', default='', notnull=False), 
    Field('atajo', 'string', default='', notnull=False), 
    Field('articulo', 'string', default='', notnull=False), 
    Field('casa', db.casas,
          requires=IS_IN_DB(db, db.casas, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione una casa')), 
    Field('sello', db.sellos,
          requires=IS_IN_DB(db, db.sellos, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un sello')), 
    Field('genero', db.generos,
          requires=IS_IN_DB(db, db.generos, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un género')), 
    Field('subgenero', db.sub_generos,
          requires=IS_IN_DB(db, db.sub_generos, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un sub-género')), 
    Field('categoria', db.categorias,
          requires=IS_IN_DB(db, db.categorias, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione una categoría')), 
    Field('aux_data', 'integer', default=0, notnull=False)
)


db.define_table('ventas_operaciones', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('pv', db.puntos_venta,
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')), 
    Field('caja', 'integer', default=0, notnull=False), 
    Field('tiempo', 'datetime', default=now, notnull=True),  
    Field('n_doc_prefijo', 'string', default='', notnull=False), 
    Field('n_doc_base', 'string', default='', notnull=False), 
    Field('n_doc_sufijo', 'string', default='', notnull=False), 
    Field('estado', 'integer', default=0, notnull=False), 
    Field('documento', 'integer', default=0, notnull=False), 
    Field('cliente', 'string', default='', notnull=False), 
    Field('user_ing', db.auth_user,
          requires=IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione un usuario')), 
    Field('user_null', db.auth_user,
          requires=IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione un usuario')), 
    Field('forma_pago', 'string', default='', notnull=False), 
    Field('vales', 'string', default='', notnull=False), 
    Field('sello', db.sellos,
          requires=IS_IN_DB(db, db.sellos, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un sello')),
    Field('codbarras', db.maestro, label='Código',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('precio', 'double', default=0.0, notnull=False), 
    Field('cantidad', 'integer', default=0, notnull=False), 
    Field('total', 'double', default=0.0, notnull=False), 
    Field('monto_local', 'double', default=0.0, notnull=False), 
    Field('monto_dolar', 'double', default=0.0, notnull=False), 
    Field('data_1', 'string', default='', notnull=False), 
    Field('data_2', 'string', default='', notnull=False), 
    Field('imod', 'integer', default=0, notnull=False)
)


db.define_table('ventas_resumen',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('pv', db.puntos_venta,
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')), 
    Field('fecha', 'date', notnull=False), 
    Field('cnt_doc', 'integer', default=0, notnull=False), 
    Field('total_neto', 'double', default=0.0, notnull=False), 
    Field('total_igv', 'double', default=0.0, notnull=False), 
    Field('total_srv', 'double', default=0.0, notnull=False), 
    Field('total_bruto', 'double', default=0.0, notnull=False), 
    Field('status', 'integer', default=1, notnull=False), 
    Field('condicion_comercial', 'integer', default=1, notnull=False)
)


db.define_table('cuentas_por_cobrar',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('fecha_doc', 'date', notnull=False, label='Fecha del Documento', default=datetime.date.today()),
    Field('documento', 'string', notnull=False, label='Documento a Pagar'),
    Field('cliente', db.directorio,
          requires=IS_IN_DB(db, db.directorio, '%(nombre_corto)s', zero='[Seleccionar]',
                            error_message='Seleccione un cliente')),
    #Field('cliente', 'string', notnull=False),
    #Field('accion', 'string', notnull=False, label='Acción'),
    Field('accion', 'integer',
          requires=IS_IN_SET({'1':'Cargo', '2':'Abono'}, zero='[Seleccionar]',
                             error_message='Seleccione Acción')),
    Field('neto_ingreso', 'double', notnull=False, label='Monto Neto de Ingreso', default=0.0),
    Field('impuesto_ingreso', 'double', notnull=False, label='Impuesto del Ingreso', default=0.0),
    Field('bruto_ingreso', 'double', notnull=False, label='Monto Bruto del Ingreso', default=0.0),
    Field('neto_salida', 'double', notnull=False, label='Monto Neto de Salida', default=0.0),
    Field('impuesto_salida', 'double', notnull=False, label='Impuesto de Salida', default=0.0),
    Field('bruto_salida', 'double', notnull=False, label='Monto Bruto de Salida', default=0.0),
    Field('fecha', 'date', notnull=False, label='Fecha de Vencimiento', default=datetime.date.today())
)


db.define_table('cuentas_por_pagar',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('fecha_doc', 'date', notnull=False, label='Fecha del Documento', default=datetime.date.today()),
    Field('documento', 'string', notnull=False, label='Documento a Pagar'),
    Field('proveedor', db.directorio,
          requires=IS_IN_DB(db, db.directorio, '%(nombre_corto)s', zero='[Seleccionar]',
                            error_message='Seleccione un proveedor')),
    #Field('proveedor', 'string', notnull=False),
    #Field('accion', 'string', notnull=False, label='Acción'),
    Field('accion', 'integer',
          requires=IS_IN_SET({'1':'Cargo', '2':'Abono'}, zero='[Seleccionar]',
                             error_message='Seleccione Acción')),
    Field('neto_ingreso', 'double', notnull=False, label='Monto Neto de Ingreso', default=0.0),
    Field('impuesto_ingreso', 'double', notnull=False, label='Impuesto del Ingreso', default=0.0),
    Field('bruto_ingreso', 'double', notnull=False, label='Monto Bruto del Ingreso', default=0.0),
    Field('neto_salida', 'double', notnull=False, label='Monto Neto de Salida', default=0.0),
    Field('impuesto_salida', 'double', notnull=False, label='Impuesto de Salida', default=0.0),
    Field('bruto_salida', 'double', notnull=False, label='Monto Bruto de Salida', default=0.0),
    Field('fecha', 'date', notnull=False, label='Fecha de Vencimiento', default=datetime.date.today())
)


db.define_table('inventarios',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('fecha_doc', 'date', notnull=False, label='Fecha del Documento', default=datetime.date.today()),
    Field('documento', 'string', notnull=False, label='Documento'),
    Field('modo', 'integer', default=1, notnull=False), 
    Field('almacen', db.almacenes_lista, label='Almacén',
          requires=IS_IN_DB(db, db.almacenes_lista, '%(almacen)s', zero='[Seleccionar]',
                            error_message='Seleccione un almacén')),
    Field('codbarras', db.maestro, label='Código',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('cantidad', 'double', notnull=False, default=0.0),
    Field('cantidad_p1', 'double', notnull=False, default=0.0),
    Field('cantidad_p2', 'double', notnull=False, default=0.0),
    Field('cantidad_conv', 'double', notnull=False, default=0.0)
)


db.define_table('cuentas',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('codigo', 'string', notnull=False, label='Código', default=''),
    Field('entidad', 'string', notnull=False, default=''),
    Field('moneda', db.monedas,
          requires=IS_IN_DB(db, db.monedas, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione una moneda')),
)


db.define_table('inventarios_control',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('codbarras', db.maestro, label='Código',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('factor', 'double', notnull=False, default=0.0),
    Field('peso_total_1', 'double', notnull=False, default=0.0),
    Field('peso_total_2', 'double', notnull=False, default=0.0),
    Field('peso_tara_1', 'double', notnull=False, default=0.0),
    Field('peso_tara_2', 'double', notnull=False, default=0.0),
    Field('peso_unitario', 'double', notnull=False, default=0.0),
    Field('peso_neto', 'double', notnull=False, default=0.0),
    Field('factor_peso', 'double', notnull=False, default=0.0),
    Field('formula', 'integer', notnull=False, default=1),
)


db.define_table('maestro_pos',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('pv', db.puntos_venta, label='Punto de Venta',
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')),
    Field('caja', 'integer', notnull=False, default=0),
    Field('modo', 'integer', notnull=False, default=1),
    Field('atajo', 'string', notnull=False, default=''),
    Field('denominacion_padre', 'string', notnull=False, label='Denominación Padre', default=''),
    Field('codbarras_padre', db.maestro, label='Código Padre',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('alias_padre', 'string', notnull=False, default=''),
    Field('posicion_padre', 'integer', notnull=False, label='Posición Padre', default=255),
    Field('modo_hijo', 'integer', notnull=False, default=0),
    Field('nivel_hijo', 'integer', notnull=False, default=0),
    Field('denominacion_hijo', 'string', notnull=False, label='Denominación Hijo', default=''),
    Field('codbarras_hijo', db.maestro, label='Código Hijo',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('alias_hijo', 'string', notnull=False, default=''),
    Field('posicion_hijo', 'integer', notnull=False, label='Posición Hijo', default=255)
)


db.define_table('operaciones_vta_aux',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('pv', db.puntos_venta, label='Punto de Venta',
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')),
    Field('caja', 'integer', notnull=False, default=0),
    Field('fecha_venta', 'date', notnull=False, label='Fecha de Venta', default=datetime.date.today()),
    Field('n_doc_prefijo', 'string', notnull=False, default=''),
    Field('n_doc_base', 'integer', notnull=False, default=0),
    Field('n_doc_sufijo', 'string', notnull=False, default=''),
    Field('codbarras_padre', db.maestro, label='Código Padre',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('codbarras_auxiliar', db.maestro, label='Código Auxiliar',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('cantidad', 'double', notnull=False, default=0.0)
)


db.define_table('personal',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('pv', db.puntos_venta, label='Punto de Venta',
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')),
    Field('usuario', db.auth_user,
          requires=IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione un usuario')),
    Field('ingreso', 'datetime', notnull=False),
    Field('salida', 'datetime', notnull=False)
)


db.define_table('pos_configuracion',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('codigo', 'string', notnull=False, label='Código', default=''),
    Field('caja', 'integer', notnull=False, default=0),
    Field('empresa', 'string', notnull=False, default=''),
    Field('nombre', 'string', notnull=False, default=''),
    Field('distrito', 'string', notnull=False, default=''),
    Field('direccion', 'string', notnull=False, label='Dirección', default=''),
    Field('alias', 'string', notnull=False, default=''),
    Field('doc_cabecera', 'string', notnull=False, default=''),
    Field('doc_pie', 'string', notnull=False, default=''),
    Field('impuestos', 'string', notnull=False, default=''),
    Field('modo_impuesto', 'integer', notnull=False, default=0),
    Field('modo_moneda', 'integer', notnull=False, default=0),
    Field('moneda', 'string', notnull=False, default=''),
    Field('wincha', 'string', notnull=False, default=''),
    Field('money_drawer', 'string', notnull=False, default=''),
    Field('productos_resumen', 'string', notnull=False, default=''),
    Field('productos_clave', 'string', notnull=False, default=''),
    Field('tipo_servicio', 'integer', notnull=False, default=1),
    Field('servidor_smtp', 'string', notnull=False, default=''),
    Field('from_smtp', 'string', notnull=False, default=''),
    Field('to_smtp', 'string', notnull=False, default=''),
    Field('fondo_caja', 'double', notnull=False, default=0.0),
    Field('consumo_alerta', 'integer', notnull=False, default=0),
    Field('dia_alerta', 'string', notnull=False, label='Día de Alerta', default=''),
    Field('hora_max', 'time', default=datetime.time(0,0,0), notnull=False),
    Field('datos_modo', 'integer', notnull=False, default=0),
    Field('stock_alerta', 'integer', notnull=False, default=0),
    Field('pos_modo', 'integer', notnull=False, default=0),
    Field('modo_decimal', 'integer', notnull=False, default=0),
    Field('modo_control', 'integer', notnull=False, default=0),
    Field('modo_almacen', 'integer', notnull=False, default=0),
    Field('genero_producto', 'string', notnull=False, default=''),
    Field('operacion_logistica', db.operaciones_logisticas, label='Operación Logística',
          requires=IS_IN_DB(db, db.operaciones_logisticas, '%(operacion)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione una Operacion Logística')),
    Field('almacen_key', 'integer', notnull=False, default=0),
    Field('almacen', db.almacenes_lista, label='Almacén',
          requires=IS_IN_DB(db, db.almacenes_lista, '%(almacen)s', zero='[Seleccionar]',
                            error_message='Seleccione un almacén')),
    Field('moneda_aux', 'string', notnull=False, default=''),
    Field('cond_com', 'integer', notnull=False, default=1),
    Field('costumer_manage', 'integer', notnull=False, default=0),
    Field('doc_pedido', 'integer', notnull=False, default=0)
)


db.define_table('pos_descuentos',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Tiempo Registro', default=now, notnull=False, writable=False),
    Field('pv', db.puntos_venta, label='Punto de Venta',
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')),
    Field('caja', 'integer', notnull=False, default=0),
    Field('codbarras', db.maestro, label='Código',
          requires=IS_IN_DB(db, db.maestro, '%(nombre)s %(descripcion)s', zero='[Seleccionar]',
                            error_message='Seleccione un código'), notnull=False),
    Field('modo', 'integer', notnull=False, default=0),
    Field('descuento', 'double', notnull=False, default=0.0),
    Field('limite', 'double', notnull=False, label='Límite', default=0.0),
    Field('data', 'string', notnull=False, default=''),
    Field('estado', 'integer', notnull=False, default=1),
    Field('user_ing', db.auth_user,
          requires=IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione un usuario'))
)


# Representations
db.auth_membership.user_id.represent = lambda ID: db.auth_user(ID).first_name + ' ' + db.auth_user(ID).last_name
db.auth_membership.group_id.represent = lambda ID: db.auth_group(ID).role



webgrid = local_import('webgrid')
