# -*- coding: utf-8 -*-

db = DAL('mysql://root:root@localhost/sisventi_old')

# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
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
    Field('registration_date', 'date', default=today, writable=False, readable=False, label=T('Fecha de registro')),
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
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('modo', 'integer', default=0, notnull=True), 
    Field('codigo', 'string', default='', notnull=True), 
    Field('nombre', 'string', default='', notnull=True), 
    Field('simbolo', 'string', default='', notnull=True), 
    Field('orden', 'integer', default=0, notnull=True), 
    migrate=False)
    

db.define_table('puntos_venta',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True),
    Field('codigo', 'string', default='', notnull=True), 
    Field('nombre', 'string', default='', notnull=True), 
    Field('distrito', 'string', default='', notnull=True), 
    Field('direccion', 'string', default='', notnull=True), 
    Field('posicion', 'integer', default=0, notnull=True), 
    Field('posicion2', 'integer', default=0, notnull=True), 
    Field('alias', 'string', default='', notnull=True), 
    Field('cab1', 'string', default='', notnull=True), 
    Field('cab2', 'string', default='', notnull=True), 
    Field('cab3', 'string', default='', notnull=True), 
    Field('cab4', 'string', default='', notnull=True), 
    Field('impt', 'string', default='', notnull=True), 
    Field('modimp', 'integer', default=0, notnull=True), 
    Field('modmon', 'integer', default=0, notnull=True), 
    Field('moneda', db.monedas,
          requires=IS_IN_DB(db, db.monedas, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione una moneda')), 
    Field('wincha', 'string', default='', notnull=True), 
    Field('money_drawer', 'string', default='', notnull=True), 
    Field('area', 'integer', default=0, notnull=True), 
    Field('replic_srv', 'string', default='', notnull=True), 
    Field('replic_db', 'string', default='', notnull=True), 
    Field('replic_user', 'string', default='', notnull=True), 
    Field('replic_passwd', 'string', default='', notnull=True), 
    Field('prodimp', 'string', default='', notnull=True), 
    Field('prodkey', 'string', default='', notnull=True), 
    Field('facmerma', 'double', default=0.0, notnull=True), 
    migrate=False)


db.define_table('almacenes_lista',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True),
    Field('almacen', 'string', default='', notnull=True), 
    Field('descripcion', 'string', default='', notnull=True), 
    Field('area', 'string', default='', notnull=True), 
    Field('pv', 'string', default='', notnull=True), 
    Field('usuario', 'string', default='', notnull=True), 
    Field('ubigeo', 'string', default='', notnull=True), 
    Field('direccion', 'string', default='', notnull=True), 
    Field('tipo_doc', 'integer', default=0, notnull=True), 
    Field('doc_id', 'string', default='', notnull=True), 
    migrate=False)


db.define_table('condiciones_comerciales',
    Field('id', 'integer'),
    Field('condicion', 'string', default='', notnull=True), 
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('modo', 'integer', default=0, notnull=True), 
    Field('descripcion', 'string', default='', notnull=True), 
    Field('codigo', 'integer', default=0, notnull=True), 
    Field('dias', 'integer', default=0, notnull=True), 
    Field('posicion', 'integer', default=0, notnull=True), 
    migrate=False)
    

db.define_table('directorio',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('modo', 'integer', default=0, notnull=True), 
    Field('nombre_corto', 'string', default='', notnull=True), 
    Field('razon_social', 'string', default='', notnull=True), 
    Field('rubro', 'integer', default=0, notnull=True), 
    Field('nombres', 'string', default='', notnull=True), 
    Field('apellidos', 'string', default='', notnull=True), 
    Field('tipo_doc', 'string', default='', notnull=True), 
    Field('doc_id', 'string', default='', notnull=True), 
    Field('doc_id_aux', 'string', default='', notnull=True), 
    Field('ubigeo', 'string', default='', notnull=True), 
    Field('direccion', 'string', default='', notnull=True), 
    Field('codigo_postal', 'string', default='', notnull=True), 
    Field('pais', 'string', default='', notnull=True), 
    Field('referencia', 'string', default='', notnull=True), 
    Field('condicion', db.condiciones_comerciales,
          requires=IS_IN_DB(db, db.condiciones_comerciales, '%(condicion)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione una condición')), 
    Field('tiempo_cred', 'integer', default=0, notnull=True), 
    Field('linea_credito', 'double', default=0.0, notnull=True), 
    Field('representante_legal', 'string', default='', notnull=True), 
    Field('cargo', 'string', default='', notnull=True), 
    Field('fecha', 'date', notnull=True), 
    Field('sexo', 'string',
          requires=IS_IN_SET(['Masculino', 'Femenino'], zero='[Seleccionar]',
                             error_message='Seleccione el sexo')), 
    Field('preferente', 'integer', default=0, notnull=True), 
    migrate=False)

    
db.define_table('transportistas',
    Field('id', 'integer'),
    Field('codigo', 'string', default='', notnull=True), 
    Field('emp_doc_id', 'string', default='', notnull=True), 
    Field('doc_id', 'string', default='', notnull=True), 
    Field('nombres', 'string', default='', notnull=True), 
    Field('apellidos', 'string', default='', notnull=True), 
    Field('ubigeo', 'string', default='', notnull=True), 
    Field('direccion', 'string', default='', notnull=True), 
    Field('posicion', 'integer', default=0, notnull=True), 
    migrate=False)
    

db.define_table('turnos',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('turno', 'string', default='', notnull=True), 
    Field('descripcion', 'string', default='', notnull=True), 
    Field('hora_inicio', 'time', default=datetime.time(0,0,0), notnull=True), 
    Field('hora_fin', 'time', default=datetime.time(0,0,0), notnull=True), 
    migrate=False)


db.define_table('articulos',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('articulo', 'string', default='', notnull=True), 
    Field('nombre', 'string', default='', notnull=True), 
    Field('posicion', 'integer', default=0, notnull=True), 
    migrate=False)


db.define_table('catmod',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('catmod', 'string', default='', notnull=True), 
    Field('nombre', 'string', default='', notnull=True), 
    Field('posicion', 'integer', default=0, notnull=True), 
    migrate=False)


db.define_table('empaques',
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('empaque', 'string', default='', notnull=True), 
    Field('nombre', 'string', default='', notnull=True), 
    Field('posicion', 'integer', default=0, notnull=True),
    migrate=False)


db.define_table('sub_casas',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('sub_casa', 'string', default='', notnull=True), 
    Field('nombre', 'string', default='', notnull=True), 
    Field('posicion', 'integer', default=0, notnull=True), 
    migrate=False)


db.define_table('sellos',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('sello', 'string', default='', notnull=True), 
    Field('nombre', 'string', default='', notnull=True), 
    Field('posicion', 'integer', default=0, notnull=True), 
    migrate=False)


db.define_table('casas',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('casa', 'string', default='', notnull=True), 
    Field('nombre', 'string', default='', notnull=True), 
    Field('posicion', 'integer', default=0, notnull=True), 
    migrate=False)
    

db.define_table('sub_sellos',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('sub_sello', 'string', default='', notnull=True), 
    Field('nombre', 'string', default='', notnull=True), 
    Field('posicion', 'integer', default=0, notnull=True), 
    migrate=False)


db.define_table('status',
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('status', 'string', default='', notnull=True), 
    Field('nombre', 'string', default='', notnull=True), 
    Field('posicion', 'integer', default=0, notnull=True), 
    migrate=False)


db.define_table('tipos',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('tipo', 'string', default='', notnull=True), 
    Field('nombre', 'string', default='', notnull=True), 
    Field('posicion', 'integer', default=0, notnull=True),
    migrate=False)


db.define_table('unidades_medida',
    Field('id', 'integer'),
    Field('codigo', 'string', default='', notnull=True), 
    Field('descripcion', 'string', default='', notnull=True), 
    Field('modo', 'integer', default=0, notnull=True), 
    Field('abreviatura_origen', 'string', default='', notnull=True), 
    Field('abreviatura_destino', 'string', default='', notnull=True), 
    Field('factor', 'double', default=0.0, notnull=True), 
    migrate=False)


db.define_table('generos',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True),
    Field('genero', 'string', default='', notnull=True), 
    Field('nombre', 'string', default='', notnull=True), 
    Field('posicion', 'integer', default=0, notnull=True), 
    migrate=False)


db.define_table('sub_generos',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True),
    Field('genero', db.generos,
          requires=IS_IN_DB(db, db.generos, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un género')),
    Field('sub_genero', 'string', default='', notnull=True), 
    Field('nombre', 'string', default='', notnull=True), 
    Field('posicion', 'integer', default=0, notnull=True), 
    migrate=False)


db.define_table('categorias',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('categoria', 'string', default='', notnull=True), 
    Field('nombre', 'string', default='', notnull=True), 
    Field('posicion', 'integer', default=0, notnull=True),     
    migrate=False)


db.define_table('maestro',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('codbarras', 'string', default='', notnull=True), 
    Field('pv', db.puntos_venta, label='Punto de Venta',
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')), 
    Field('grupo_venta', 'string', default='', notnull=True), 
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
    Field('proveedor', db.directorio,
          requires=IS_IN_DB(db, db.directorio, '%(razon_social)s', zero='[Seleccionar]',
                            error_message='Seleccione un proveedor')), 
    Field('moneda', db.monedas,
          requires=IS_IN_DB(db, db.monedas, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione una moneda')), 
    Field('precio', 'double', default=0.0, notnull=True), 
    Field('modo_impuesto', 'integer', default=0, notnull=True), 
    Field('impuesto', 'string', default='', notnull=True), 
    Field('nombre', 'string', default='', notnull=True), 
    Field('descripcion', 'string', default='', notnull=True), 
    Field('alias', 'string', default='', notnull=True), 
    Field('descuento', 'integer', default=0, notnull=True), 
    Field('dependencia', 'integer', default=0, notnull=True), 
    Field('unidad_medida_valor', 'double', default=0.0, notnull=True), 
    Field('aux_num_data', 'integer', default=0, notnull=True), 
    Field('stock_min', 'double', default=0.0, notnull=True), 
    Field('stock_max', 'double', default=0.0, notnull=True), 
    Field('reposicion', 'integer', default=0, notnull=True), 
    Field('ventas_key', 'integer', default=0, notnull=True), 
    Field('fecha', 'date', notnull=True), 
    Field('unidad_medida', db.unidades_medida,
          requires=IS_IN_DB(db, db.unidades_medida, '%(descripcion)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione una unidad de medida')), 
    migrate=False)
    

db.define_table('operaciones_logisticas',
    Field('id', 'integer'),
    Field('registro', 'datetime', default=now, label='Fecha de Registro', notnull=True),
    Field('operacion', 'string', default='', notnull=True),
    Field('modo', 'integer', default=0, notnull=True), 
    Field('descripcion', 'string', default='', notnull=True), 
    Field('operacion_relac', 'string', default='', notnull=True), 
    Field('almacen_relac', 'string', default='', notnull=True), 
    migrate=False)

    
db.define_table('almacenes',
    Field('id', 'integer'),
    Field('registro', 'datetime', default=now, label='Fecha de Registro', notnull=True),
    Field('modo', 'integer', default=0, notnull=True),
    Field('pv', db.puntos_venta, label='Punto de Venta', default='', notnull=True),
    Field('tiempo', 'datetime', notnull=True),  
    Field('estado', 'integer', default=1, notnull=True),
    Field('user_ing', db.auth_user, default='', notnull=True),  
    Field('operacion_logistica', db.operaciones_logisticas, default='', notnull=True),  
    Field('compra_n_doc_prefijo', 'string', default='', notnull=True),  
    Field('compra_n_doc_base', 'integer', default=0, notnull=True),  
    Field('compra_n_doc_sufijo', 'string', default='', notnull=True),  
    Field('proveedor_n_doc', 'string', default='', notnull=True),  
    Field('modo_doc', 'integer', default=0, notnull=True),
    Field('tipo_doc', 'integer', default=0, notnull=True),  
    Field('fecha_doc', 'date', notnull=True),
    Field('n_doc_prefijo', 'string', default='', notnull=True),  
    Field('n_doc_base', 'integer', default=0, notnull=True),  
    Field('n_doc_sufijo', 'string', default='', notnull=True),  
    Field('proveedor', db.directorio, default='', notnull=True),  
    Field('proveedor_tipo_doc', 'string', default='', notnull=True),  
    Field('proveedor_condicion', 'integer', default=0, notnull=True),  
    Field('proveedor_fecha_doc', 'date', notnull=True),
    Field('proveedor_moneda_doc', 'integer', default=0, notnull=True), 
    Field('proveedor_total_doc', 'double', default=0.0, notnull=True), 
    Field('almacen_origen', db.almacenes_lista, default='', notnull=True),
    Field('almacen_destino', db.almacenes_lista, default='', notnull=True), 
    Field('articulo', db.articulos, default='', notnull=True), 
    Field('codbarras_padre', 'string', default='', notnull=True), 
    Field('codbarras', db.maestro, default='', notnull=True), 
    Field('pedido', 'integer', default=1, notnull=True),
    Field('cantidad_exp', 'double', default=0.0, notnull=True),
    Field('cantidad_ing', 'double', default=0.0, notnull=True), 
    Field('peso_exp', 'double', default=0.0, notnull=True), 
    Field('peso_ing', 'double', default=0.0, notnull=True), 
    Field('tipo', 'string', default='', notnull=True), 
    Field('precio', 'double', default=0.0, notnull=True), 
    Field('fecha_prod', 'date', notnull=True), 
    Field('fecha_venc', 'date', notnull=True), 
    Field('extra_data', 'string', default='', notnull=True), 
    Field('transportista', db.transportistas, default='', notnull=True), 
    Field('vehiculo', 'string', default='', notnull=True), 
    Field('grupo', 'integer', default=0, notnull=True), 
    Field('turno', db.turnos, default='', notnull=True), 
    Field('masa', 'string', default='', notnull=True), 
    Field('temperatura', 'double', default=0.0, notnull=True), 
    Field('peso', 'double', default=0.0, notnull=True), 
    Field('hora_inicial', 'time', notnull=True), 
    Field('hora_final', 'time', notnull=True), 
    Field('n_serie', 'string', default='', notnull=True), 
    Field('n_prefijo_relacion', 'string', default='', notnull=True), 
    Field('n_doc_relacion', 'integer', default=0, notnull=True), 
    Field('observaciones', 'string', default='', notnull=True), 
    migrate=False)


db.define_table('almacenes_ubicacion',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('almacen', 'string', default='', notnull=True), 
    Field('codbarras', 'string', default='', notnull=True), 
    Field('ubicacion', 'string', default='', notnull=True), 
    migrate=False)


db.define_table('areas',
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('area', 'string', default='', notnull=True), 
    Field('nombre', 'string', default='', notnull=True), 
    Field('descripcion', 'string', default='', notnull=True), 
    Field('posicion', 'integer', default=0, notnull=True), 
    migrate=False)


db.define_table('backup',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('tiempo', 'datetime', notnull=True), 
    Field('log', 'string', default='', notnull=True), 
    migrate=False)


db.define_table('bancos',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('pv', 'integer', default=0, notnull=True), 
    Field('fechav', 'date', notnull=True),
    Field('fechad', 'date', notnull=True), 
    Field('banco', 'string', default='', notnull=True), 
    Field('monto', 'double', default=0.0, notnull=True), 
    Field('cambio', 'double', default=0.0, notnull=True), 
    Field('glosa1', 'string', default='', notnull=True), 
    Field('glosa2', 'string', default='', notnull=True), 
    Field('agencia', 'string', default='', notnull=True), 
    migrate=False)


db.define_table('clientes_preferentes', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('doc_id', 'string', default='', notnull=True), 
    Field('tiempo', 'datetime', notnull=True), 
    Field('promocion', 'string', default='', notnull=True), 
    Field('tarjeta', 'string', default='', notnull=True), 
    Field('user_ing', db.auth_user,
          requires=IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione un usuario')), 
    migrate=False)


db.define_table('compras_ordenes', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('tiempo', 'datetime', notnull=True), 
    Field('n_doc_prefijo', 'string', default='', notnull=True), 
    Field('n_doc_base', 'integer', default=0, notnull=True), 
    Field('n_doc_sufijo', 'string', default='', notnull=True), 
    Field('estado', 'integer', default=1, notnull=True), 
    Field('area', db.areas,
          requires=IS_IN_DB(db, db.areas, '%(area)s', zero='[Seleccionar]',
                            error_message='Seleccione un área')), 
    Field('forma_pago', 'string', default='', notnull=True), 
    Field('codbarras', db.maestro,
          requires=IS_IN_DB(db, db.maestro, '%(codbarras)s', zero='[Seleccionar]',
                            error_message='Seleccione un código de barras')), 
    Field('cantidad', 'double', default=0.0, notnull=True), 
    Field('cantidad_proveedor', 'double', default=0.0, notnull=True), 
    Field('moneda', db.monedas,
          requires=IS_IN_DB(db, db.monedas, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione una moneda')), 
    Field('precio_neto', 'double', default=0.0, notnull=True), 
    Field('precio_imp', 'double', default=0.0, notnull=True), 
    Field('precio_bruto', 'double', default=0.0, notnull=True), 
    Field('sub_total_neto', 'double', default=0.0, notnull=True), 
    Field('sub_total_imp', 'double', default=0.0, notnull=True), 
    Field('sub_total_bruto', 'double', default=0.0, notnull=True), 
    Field('proveedor', db.directorio,
          requires=IS_IN_DB(db, db.directorio, '%(razon_social)s', zero='[Seleccionar]',
                            error_message='Seleccione un proveedor')), 
    Field('total_neto', 'double', default=0.0, notnull=True), 
    Field('total_imp', 'double', default=0.0, notnull=True), 
    Field('total_bruto', 'double', default=0.0, notnull=True), 
    Field('total_texto', 'string', default='', notnull=True), 
    Field('fecha_entrega', 'date', notnull=True), 
    Field('lugar_entrega', 'string', default='', notnull=True), 
    Field('user_req', 'string', default='', notnull=True), 
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
    Field('tiempo_anul', 'datetime', notnull=True), 
    Field('observaciones', 'string', default='', notnull=True), 
    migrate=False)


db.define_table('control_insumos', 
    Field('id', 'integer'), 
    Field('codbarras_padre', 'string', default='', notnull=True), 
    Field('codbarras_hijo', 'string', default='', notnull=True), 
    Field('gramos', 'double', default=0.0, notnull=True), 
    Field('adicional', 'double', default=0.0, notnull=True), 
    Field('estado', 'integer', default=0, notnull=True), 
    Field('truco', 'integer', default=0, notnull=True), 
    Field('orden', 'integer', default=0, notnull=True), 
    Field('modo', 'integer', default=0, notnull=True), 
    migrate=False)


db.define_table('control_produccion', 
    Field('id', 'integer'), 
    Field('fecha', 'date', notnull=True), 
    Field('turno', 'string', default='', notnull=True), 
    Field('producto', 'string', default='', notnull=True), 
    Field('producto_derivado', 'string', default='', notnull=True), 
    migrate=False)


db.define_table('criterio',
    Field('id', 'integer'),
    Field('cp', 'string', default='', notnull=True), 
    Field('grupo_distribucion', 'string', default='', notnull=True), 
    Field('turno', 'string', default='', notnull=True), 
    Field('porcentaje', 'double', default=100.0, notnull=True), 
    Field('codbarras', db.maestro,
          requires=IS_IN_DB(db, db.maestro, '%(codbarras)s', zero='[Seleccionar]',
                            error_message='Seleccione un código de barras')), 
    migrate=False)


db.define_table('criterio2',
    Field('id', 'integer'),
    Field('turno', 'string', default='', notnull=True), 
    Field('cp', 'string', default='', notnull=True), 
    migrate=False)


db.define_table('delivery',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True, writable=False), 
    Field('pv', db.puntos_venta, label='Punto de Venta',
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')), 
    Field('tiempo', 'datetime', notnull=True), 
    Field('numero', 'integer', default=0, notnull=True, label='Número'), 
    Field('cliente', 'string', default='', notnull=True), 
    Field('docnum', 'integer', default=0, notnull=True, label='Documento'), 
    Field('carac1', 'string', default='', notnull=True, label='Característica 1'), 
    Field('carac2', 'string', default='', notnull=True, label='Característica 2'), 
    Field('carac3', 'string', default='', notnull=True, label='Característica 3'), 
    migrate=False)


db.define_table('directorio_auxiliar', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Fecha de Registro', default=now), 
    Field('doc_id', 'string', default='', notnull=True), 
    Field('telefono', 'string', default='', notnull=True), 
    Field('tel_prio', 'integer', default=0, notnull=True), 
    Field('fax', 'string', default='', notnull=True), 
    Field('fax_prio', 'integer', default=0, notnull=True), 
    Field('email', 'string', default='', notnull=True), 
    Field('ema_prio', 'integer', default=0, notnull=True), 
    Field('web', 'string', default='', notnull=True), 
    Field('web_prio', 'integer', default=0, notnull=True), 
    Field('contacto', 'string', default='', notnull=True), 
    Field('con_prio', 'integer', default=0, notnull=True), 
    Field('telefono_c', 'string', default='', notnull=True), 
    Field('tec_prio', 'integer', default=0, notnull=True), 
    Field('email_c', 'string', default='', notnull=True), 
    Field('emc_prio', 'integer', default=0, notnull=True), 
    migrate=False)


db.define_table('documentos_comerciales', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('modo', 'integer', default=0, notnull=True), 
    Field('documento', 'integer', default=0, notnull=True), 
    Field('doc_reg', 'string', default='', notnull=True), 
    Field('nombre', 'string', default='', notnull=True), 
    Field('pv', db.puntos_venta,
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')), 
    Field('caja', 'integer', default=0, notnull=True), 
    Field('prefijo', 'string', default='', notnull=True), 
    Field('correlativo', 'integer', default=0, notnull=True), 
    Field('sufijo', 'string', default='', notnull=True), 
    Field('copia', 'integer', default=0, notnull=True), 
    Field('detalle', 'integer', default=0, notnull=True), 
    Field('limite', 'integer', default=0, notnull=True), 
    Field('impresion', 'integer', default=0, notnull=True), 
    Field('impuestos', 'string', default='', notnull=True), 
    migrate=False)


db.define_table('documentos_identidad', 
    Field('id', 'string'), 
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True),
    Field('nombre', 'string', default='', notnull=True), 
    migrate=False)


db.define_table('docventa',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('pv', db.puntos_venta, label='Punto de Venta',
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')), 
    Field('caja', 'integer', default=0, notnull=True), 
    Field('fecha_vta', 'date', notnull=True), 
    Field('tiempo', 'datetime', notnull=True), 
    Field('n_doc_base', 'integer', default=0, notnull=True), 
    Field('estado', 'string', default='', notnull=True), 
    Field('comprobante', 'integer', default=0, notnull=True), 
    Field('cliente', 'string', default='', notnull=True), 
    Field('cv_ing', 'integer', default=0, notnull=True), 
    Field('fp', 'integer', default=0, notnull=True), 
    Field('vales', 'string', default='', notnull=True), 
    Field('sello', 'string', default='', notnull=True), 
    Field('codigo', 'string', default='',  notnull=True), 
    Field('detalle', 'string', default='',  notnull=True), 
    Field('precio', 'double', default=0.0, notnull=True), 
    Field('cantidad', 'integer', default=0, notnull=True), 
    Field('sub_total_bruto', 'double', default=0.0, notnull=True), 
    Field('sub_total_impto', 'string', default='', notnull=True), 
    Field('sub_total_neto', 'double', default=0.0, notnull=True), 
    Field('total', 'double', default=0.0, notnull=True), 
    Field('detalle_impto', 'string', default='', notnull=True), 
    Field('total_neto', 'double', default=0.0, notnull=True), 
    Field('mntsol', 'double', default=0.0, notnull=True), 
    Field('mntdol', 'double', default=0.0, notnull=True), 
    Field('cv_anul', 'integer', default=0, notnull=True), 
    Field('imod', 'integer', default=0, notnull=True), 
    Field('n_doc_sufijo', 'string', default='', notnull=True), 
    Field('n_doc_prefijo', 'string', default='', notnull=True), 
    Field('data_1', 'string', default='', notnull=True), 
    Field('fecha_vto', 'date', notnull=True), 
    Field('condicion_comercial', db.condiciones_comerciales,
          requires=IS_IN_DB(db, db.condiciones_comerciales, zero='[Seleccionar]',
                            error_message='Seleccione una condición')), 
    migrate=False)


db.define_table('factores_merma', 
    Field('id', 'integer'), 
    Field('fecha', 'date', notnull=True), 
    Field('cp', 'string', default='', notnull=True), 
    Field('codbarras', db.maestro,
          requires=IS_IN_DB(db, db.maestro, '%(codbarras)s', zero='[Seleccionar]',
                            error_message='Seleccione un código de barras')), 
    Field('valor', 'double', default=0.0, notnull=True), 
    Field('modo', 'integer', default=0, notnull=True), 
    migrate=False)


db.define_table('formas_pago',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True),
    Field('forma_pago', 'string', default='', notnull=True), 
    Field('nombre', 'string', default='', notnull=True), 
    migrate=False)


db.define_table('grupo_distribucion',
    Field('id', 'integer'), 
    Field('grupo_distribucion', 'string', default='', notnull=True), 
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('turno', db.turnos,
          requires=IS_IN_DB(db, db.turnos, '%(turno)s', zero='[Seleccionar]',
                            error_message='Seleccione un turno')), 
    Field('descripcion', 'string', default='', notnull=True), 
    Field('prioridad', 'integer', default=0, notnull=True), 
    migrate=False)


db.define_table('impuestos',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('codigo', 'string', default='', notnull=True), 
    Field('abreviatura', 'string', default='', notnull=True), 
    Field('nombre', 'string', default='', notnull=True), 
    Field('valor', 'double', default=0.0, notnull=True), 
    Field('modo', 'integer', default=0, notnull=True), 
    migrate=False)


db.define_table('maestro_auxiliar', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('codbarras', db.maestro,
          requires=IS_IN_DB(db, db.maestro, '%(codbarras)s', zero='[Seleccionar]',
                            error_message='Seleccione un código de barras')), 
    Field('nombre', 'string', default='', notnull=True), 
    Field('valor', 'string', default='', notnull=True), 
    Field('prioridad', 'integer', default=0, notnull=True), 
    migrate=False)


db.define_table('maestro_dependencias', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True, writable=False), 
    Field('pv', db.puntos_venta, label='Punto de Venta',
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')), 
    Field('modo', 'integer'), 
    Field('codbarras', db.maestro, label='Código de Barras',
          requires=IS_IN_DB(db, db.maestro, '%(codbarras)s', zero='[Seleccionar]',
                            error_message='Seleccione un código de barras')), 
    Field('data', 'string', default='', notnull=True), 
    Field('estado', 'integer', default=1, notnull=True), 
    Field('user_ing', db.auth_user,
          requires=IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione un usuario')),
    migrate=False)


db.define_table('maestro_descuentos', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('tiempo', 'datetime', notnull=True), 
    Field('pv', db.puntos_venta,
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')), 
    Field('modo', 'integer', default=0, notnull=True), 
    Field('codbarras', db.maestro,
          requires=IS_IN_DB(db, db.maestro, '%(codbarras)s', zero='[Seleccionar]',
                            error_message='Seleccione un código de barras')), 
    Field('descuento', 'double', default=0.0, notnull=True), 
    Field('monto_req', 'double', default=0.0, notnull=True), 
    Field('user_nivel', 'integer', default=0, notnull=True), 
    Field('fecha_inicio', 'date', notnull=True), 
    Field('hora_inicio', 'time', default=datetime.time(0,0,0), notnull=True), 
    Field('fecha_fin', 'date', notnull=True), 
    Field('hora_fin', 'time', default=datetime.time(0,0,0), notnull=True), 
    Field('estado', 'integer', default=1, notnull=True), 
    Field('user_ing', db.auth_user,
          requires=IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione un usuario')), 
    migrate=False)


db.define_table('maestro_posiciones',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('modo', 'integer', default=0, notnull=True), 
    Field('codbarras', db.maestro,
          requires=IS_IN_DB(db, db.maestro, '%(codbarras)s', zero='[Seleccionar]',
                            error_message='Seleccione un código de barras')), 
    Field('posicion', 'integer', default=0, notnull=True), 
    migrate=False)


db.define_table('maestro_proveedores', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('codbarras', db.maestro,
          requires=IS_IN_DB(db, db.maestro, '%(codbarras)s', zero='[Seleccionar]',
                            error_message='Seleccione un código de barras')), 
    Field('proveedor', db.directorio,
          requires=IS_IN_DB(db, db.directorio, '%(razon_social)s', zero='[Seleccionar]',
                            error_message='Seleccione un proveedor')), 
    Field('unidad_medida', db.unidades_medida,
          requires=IS_IN_DB(db, db.unidades_medida, '%(descripcion)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione una unidad de medida')), 
    migrate=False)


db.define_table('maestro_valores', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('tiempo', 'datetime', notnull=True), 
    Field('pv', db.puntos_venta,
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')),
    Field('codbarras', db.maestro,
          requires=IS_IN_DB(db, db.maestro, '%(codbarras)s', zero='[Seleccionar]',
                            error_message='Seleccione un código de barras')), 
    Field('precio', 'double', default=0.0, notnull=True), 
    Field('user_ing', db.auth_user,
          requires=IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione un usuario')), 
    migrate=False)


db.define_table('modos_logisticos', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('modo_logistico', 'string', default='', notnull=True), 
    Field('descripcion', 'string', default='', notnull=True), 
    migrate=False)


db.define_table('modos_pvr', 
    Field('id', 'integer'), 
    Field('tabla', 'string', default='', notnull=True), 
    Field('modo', 'integer', default=0, notnull=True), 
    Field('descripcion', 'string', default='', notnull=True), 
    Field('modo_tabla', 'integer', default=0, notnull=True), 
    migrate=False)


db.define_table('pedidos', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('fecha', 'date', notnull=True), 
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
    Field('tipo', 'integer', default=0, notnull=True), 
    Field('user_req', db.auth_user,
          requires=IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione un usuario')), 
    Field('n_doc_prefijo', 'string', default='', notnull=True), 
    Field('n_doc_base', 'integer', default=0, notnull=True), 
    Field('n_doc_sufijo', 'string', default='', notnull=True), 
    Field('codbarras_padre', 'string', default='', notnull=True), 
    Field('codbarras', db.maestro,
          requires=IS_IN_DB(db, db.maestro, '%(codbarras)s', zero='[Seleccionar]',
                            error_message='Seleccione un código de barras')), 
    Field('cantidad', 'double', default=0.0, notnull=True), 
    Field('peso', 'double', default=0.0, notnull=True), 
    Field('detalle', 'string', default='', notnull=True), 
    Field('modo', 'integer', default=0, notnull=True), 
    Field('estado', 'integer', default=1, notnull=True), 
    Field('user_ing', db.auth_user,
          requires=IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione un usuario')), 
    migrate=False)


db.define_table('pedidos_emergencia_produccion', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('fecha', 'date'), 
    Field('pv', db.puntos_venta,
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')),
    Field('turno', db.turnos,
          requires=IS_IN_DB(db, db.turnos, '%(turno)s', zero='[Seleccionar]',
                            error_message='Seleccione un turno')), 
    Field('codbarras', db.maestro,
          requires=IS_IN_DB(db, db.maestro, '%(codbarras)s', zero='[Seleccionar]',
                            error_message='Seleccione un código de barras')), 
    Field('cantidad', 'double', default=0.0, notnull=True), 
    Field('modo', 'integer', default=0, notnull=True), 
    migrate=False)


db.define_table('pesos_operaciones',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('codbarras', db.maestro,
          requires=IS_IN_DB(db, db.maestro, '%(codbarras)s', zero='[Seleccionar]',
                            error_message='Seleccione un código de barras')), 
    Field('peso_neto', 'double', default=0.0, notnull=True), 
    Field('peso_tara', 'double', default=0.0, notnull=True), 
    migrate=False)


db.define_table('pos_administracion', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('pv', db.puntos_venta,
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')),
    Field('caja', 'integer', default=0, notnull=True), 
    Field('user_ing', db.auth_user,
          requires=IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione un usuario')), 
    Field('user_out', db.auth_user,
          requires=IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione un usuario')), 
    Field('apertura', 'datetime', notnull=True), 
    Field('cierre', 'datetime', notnull=True), 
    migrate=False)


db.define_table('produccion_datos', 
    Field('id', 'integer'), 
    Field('fecha', 'date', notnull=True), 
    Field('turno', db.turnos,
          requires=IS_IN_DB(db, db.turnos, '%(turno)s', zero='[Seleccionar]',
                            error_message='Seleccione un turno')), 
    Field('grupo_distribucion', db.grupo_distribucion,
          requires=IS_IN_DB(db, db.grupo_distribucion, '%(grupo_distribucion)s', zero='[Seleccionar]',
                            error_message='Seleccione un grupo de distribución')), 
    Field('pv', db.puntos_venta,
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')), 
    Field('codbarras', db.maestro,
          requires=IS_IN_DB(db, db.maestro, '%(codbarras)s', zero='[Seleccionar]',
                            error_message='Seleccione un código de barras')), 
    Field('codbarras_hijo', 'string', default='', notnull=True), 
    Field('cantidad', 'double', default=0.0, notnull=True), 
    Field('modo', 'integer', default=0, notnull=True), 
    migrate=False)


db.define_table('produccion_derivados', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('modo', 'integer', default=0, notnull=True), 
    Field('turno', db.turnos,
          requires=IS_IN_DB(db, db.turnos, '%(turno)s', zero='[Seleccionar]',
                            error_message='Seleccione un turno')), 
    Field('tipo', 'integer', default=0, notnull=True), 
    Field('cp_base', 'string', default='', notnull=True), 
    Field('cp_aux', 'string', default='', notnull=True), 
    Field('user_ing', db.auth_user,
          requires=IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione un usuario')), 
    Field('fecha', 'date', notnull=True), 
    Field('n_doc_prefijo', 'string', default='', notnull=True), 
    Field('n_doc_base', 'string', default='', notnull=True), 
    Field('n_doc_sufijo', 'string', default='', notnull=True), 
    Field('codbarras', db.maestro,
          requires=IS_IN_DB(db, db.maestro, '%(codbarras)s', zero='[Seleccionar]',
                            error_message='Seleccione un código de barras')), 
    Field('ing_produccion', 'double', default=0.0, notnull=True), 
    Field('ing_traslado', 'double', default=0.0, notnull=True), 
    Field('ing_varios', 'double', default=0.0, notnull=True), 
    Field('sal_ventas', 'double', default=0.0, notnull=True), 
    Field('sal_merma', 'double', default=0.0, notnull=True), 
    Field('sal_consumo_int', 'double', default=0.0, notnull=True), 
    Field('sal_traslado', 'double', default=0.0, notnull=True), 
    Field('sal_varios', 'double', default=0.0, notnull=True), 
    migrate=False)


db.define_table('produccion_estadistica', 
    Field('id', 'integer'), 
    Field('fecha', 'date', notnull=True), 
    Field('turno', db.turnos,
          requires=IS_IN_DB(db, db.turnos, '%(turno)s', zero='[Seleccionar]',
                            error_message='Seleccione un turno')), 
    Field('pv', db.puntos_venta,
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')),
    Field('codbarras_abuelo', 'string', default='', notnull=True), 
    Field('codbarras_padre', 'string', default='', notnull=True), 
    Field('codbarras_hijo', 'string', default='', notnull=True), 
    Field('cantidad_abuelo', 'double', default=0.0, notnull=True), 
    Field('cantidad_padre', 'double', default=0.0, notnull=True), 
    Field('porcentaje_padre', 'double', default=0.0, notnull=True), 
    Field('cantidad_hijo', 'double', default=0.0, notnull=True), 
    Field('porcentaje_hijo', 'double', default=0.0, notnull=True), 
    Field('modo', 'integer', default=0, notnull=True), 
    Field('porcentaje_general', 'double', default=0.0, notnull=True), 
    migrate=False)


db.define_table('produccion_pedidos', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('fecha', 'date', notnull=True), 
    Field('pv', db.puntos_venta,
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')),
    Field('turno', db.turnos,
          requires=IS_IN_DB(db, db.turnos, '%(turno)s', zero='[Seleccionar]',
                            error_message='Seleccione un turno')), 
    Field('modo', 'integer', default=0, notnull=True), 
    Field('codbarras', db.maestro,
          requires=IS_IN_DB(db, db.maestro, '%(codbarras)s', zero='[Seleccionar]',
                            error_message='Seleccione un código de barras')), 
    Field('cantidad', 'double', default=0.0, notnull=True), 
    migrate=False)


db.define_table('produccion_planeamiento', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True), 
    Field('fecha', 'date', notnull=True), 
    Field('codbarras_padre', 'string', default='', notnull=True), 
    Field('codbarras', db.maestro,
          requires=IS_IN_DB(db, db.maestro, '%(codbarras)s', zero='[Seleccionar]',
                            error_message='Seleccione un código de barras')), 
    Field('codbarras_hijo', 'string', default='', notnull=True), 
    Field('cantidad_prod', 'double', default=0.0, notnull=True), 
    Field('condicion_pedido', 'string', default='', notnull=True), 
    Field('grupo_distribucion', db.grupo_distribucion,
          requires=IS_IN_DB(db, db.grupo_distribucion, '%(grupo_distribucion)s', zero='[Seleccionar]',
                            error_message='Seleccione un grupo de distribución')), 
    Field('cp', 'string', default='', notnull=True), 
    Field('turno', db.turnos,
          requires=IS_IN_DB(db, db.turnos, '%(turno)s', zero='[Seleccionar]',
                            error_message='Seleccione un turno')),
    migrate=False)


db.define_table('produccion_planeamiento_aux', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True),
    Field('fecha', 'date', notnull=True), 
    Field('codbarras', db.maestro,
          requires=IS_IN_DB(db, db.maestro, '%(codbarras)s', zero='[Seleccionar]',
                            error_message='Seleccione un código de barras')), 
    Field('cantidad_prod', 'double', default=0.0, notnull=True), 
    Field('condicion_pedido', 'string', default='', notnull=True), 
    Field('grupo_distribucion', db.grupo_distribucion,
          requires=IS_IN_DB(db, db.grupo_distribucion, '%(grupo_distribucion)s', zero='[Seleccionar]',
                            error_message='Seleccione un grupo de distribución')),
    Field('cp', 'string', default='', notnull=True), 
    Field('turno', db.turnos,
          requires=IS_IN_DB(db, db.turnos, '%(turno)s', zero='[Seleccionar]',
                            error_message='Seleccione un turno')),
    migrate=False)


db.define_table('produccion_rendimiento', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True),
    Field('fecha', 'date', notnull=True), 
    Field('turno', db.turnos,
          requires=IS_IN_DB(db, db.turnos, '%(turno)s', zero='[Seleccionar]',
                            error_message='Seleccione un turno')),
    Field('modo', 'integer', default=1, notnull=True), 
    Field('tipo', 'integer', default=0, notnull=True), 
    Field('codbarras', db.maestro,
          requires=IS_IN_DB(db, db.maestro, '%(codbarras)s', zero='[Seleccionar]',
                            error_message='Seleccione un código de barras')), 
    Field('cantidad', 'double', default=0.0, notnull=True), 
    Field('masa', 'string', default='', notnull=True), 
    Field('peso', 'double', default=0.0, notnull=True), 
    Field('temperatura', 'double', default=0.0, notnull=True), 
    Field('hora_inicial', 'time', default=datetime.time(0,0,0), notnull=True), 
    Field('hora_final', 'time', default=datetime.time(0,0,0), notnull=True), 
    migrate=False)


db.define_table('promociones', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True),
    Field('pv', db.puntos_venta,
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')),
    Field('codigo', 'string', default='', notnull=True), 
    Field('nombre', 'string', default='', notnull=True), 
    Field('porcentaje', 'double', default=0.0, notnull=True), 
    Field('valor', 'double', default=0.0, notnull=True), 
    Field('modo', 'integer', default=0, notnull=True), 
    Field('codbarras', db.maestro,
          requires=IS_IN_DB(db, db.maestro, '%(codbarras)s', zero='[Seleccionar]',
                            error_message='Seleccione un código de barras')), 
    Field('cantidad', 'integer', default=1, notnull=True), 
    Field('limite', 'integer', default=0, notnull=True), 
    Field('cond_modo', 'integer', default=0, notnull=True), 
    Field('cond_valor', 'integer', default=0, notnull=True), 
    Field('cond_fecha_inic', 'date', notnull=True), 
    Field('cond_hora_inic', 'time', default=datetime.time(0,0,0), notnull=True), 
    Field('cond_fecha_term', 'date', notnull=True), 
    Field('cond_hora_term', 'time', default=datetime.time(0,0,0), notnull=True), 
    Field('estado', 'integer', default=0, notnull=True), 
    migrate=False)


db.define_table('puntos_venta_grupos', 
    Field('id', 'integer'), 
    Field('cp', 'string', default='', notnull=True), 
    Field('grupo_distribucion', db.grupo_distribucion,
          requires=IS_IN_DB(db, db.grupo_distribucion, '%(grupo_distribucion)s', zero='[Seleccionar]',
                            error_message='Seleccione un grupo de distribución')), 
    Field('turno', db.turnos,
          requires=IS_IN_DB(db, db.turnos, '%(turno)s', zero='[Seleccionar]',
                            error_message='Seleccione un turno')), 
    Field('porcentaje', 'double', default=100.0, notnull=True), 
    Field('codbarras', db.maestro,
          requires=IS_IN_DB(db, db.maestro, '%(codbarras)s', zero='[Seleccionar]',
                            error_message='Seleccione un código de barras')), 
    Field('modo', 'integer', default=0, notnull=True), 
    migrate=False)


db.define_table('puntos_venta_relaciones', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True),
    Field('pv_padre', 'string', default='', notnull=True), 
    Field('pv_hijo', 'string', default='', notnull=True), 
    Field('modo', 'integer', default=0, notnull=True), 
    migrate=False)


db.define_table('puntos_venta_satelites',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True),
    Field('pv_padre', 'string', default='', notnull=True), 
    Field('pv_hijo', 'string', default='', notnull=True), 
    Field('modo', 'integer', default=0, notnull=True), 
    migrate=False)


db.define_table('recetas', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True),
    Field('codbarras_padre', db.maestro,
          requires=IS_IN_DB(db, db.maestro, '%(codbarras)s', zero='[Seleccionar]',
                            error_message='Seleccione un código de barras')), 
    Field('cantidad', 'double', default=0.0, notnull=True), 
    Field('codbarras_hijo', db.maestro,
          requires=IS_IN_DB(db, db.maestro, '%(codbarras)s', zero='[Seleccionar]',
                            error_message='Seleccione un código de barras')), 
    Field('modo', 'integer', default=0, notnull=True), 
    Field('estado', 'integer', default=1, notnull=True), 
    Field('orden', 'integer', default=0, notnull=True), 
    migrate=False)


db.define_table('relaciones', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True),
    Field('codbarras_padre', db.maestro,
          requires=IS_IN_DB(db, db.maestro, '%(codbarras)s', zero='[Seleccionar]',
                            error_message='Seleccione un código de barras')), 
    Field('codbarras_hijo', db.maestro,
          requires=IS_IN_DB(db, db.maestro, '%(codbarras)s', zero='[Seleccionar]',
                            error_message='Seleccione un código de barras')), 
    Field('modo', 'integer', default=0, notnull=True), 
    Field('orden', 'integer', default=0, notnull=True), 
    migrate=False)


db.define_table('rendimientos_sintesis', 
    Field('id', 'integer'), 
    Field('fecha', 'date', notnull=True), 
    Field('turno', db.turnos,
          requires=IS_IN_DB(db, db.turnos, '%(turno)s', zero='[Seleccionar]',
                            error_message='Seleccione un turno')), 
    Field('tipo', 'integer', default=0, notnull=True), 
    Field('cantidad', 'double', default=0.0, notnull=True), 
    Field('peso', 'double', default=0.0, notnull=True), 
    Field('merma', 'double', default=0.0, notnull=True), 
    Field('rendimiento', 'double', default=0.0, notnull=True), 
    migrate=False)


db.define_table('reportes_configuracion', 
    Field('id', 'integer'), 
    Field('codigo_reporte', 'string', default='', notnull=True), 
    Field('detalle_reporte', 'string', default='', notnull=True), 
    Field('turno', db.turnos,
          requires=IS_IN_DB(db, db.turnos, '%(turno)s', zero='[Seleccionar]',
                            error_message='Seleccione un turno')),
    Field('pv', db.puntos_venta,
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')), 
    Field('grupo_distribucion', db.grupo_distribucion,
          requires=IS_IN_DB(db, db.grupo_distribucion, '%(grupo_distribucion)s', zero='[Seleccionar]',
                            error_message='Seleccione un grupo de distribución')), 
    Field('modo', 'integer', default=0, notnull=True), 
    Field('codigo_dato', 'string', default='', notnull=True), 
    Field('array', 'string', default='', notnull=True), 
    Field('codbarras_abuelo', 'string', default='', notnull=True), 
    Field('codbarras_padre', 'string', default='', notnull=True), 
    Field('codbarras_hijo', 'string', default='', notnull=True), 
    Field('descripcion', 'string', default='', notnull=True), 
    Field('posicion', 'integer', default=0, notnull=True), 
    migrate=False)


db.define_table('rubros',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True),
    Field('rubro', 'string', default='', notnull=True), 
    Field('nombre', 'string', default='', notnull=True), 
    Field('descripcion', 'string', default='', notnull=True), 
    Field('posicion', 'integer', default=0, notnull=True), 
    migrate=False)


db.define_table('tablas_modos', 
    Field('id', 'integer'), 
    Field('tabla', 'string', default='', notnull=True), 
    Field('modo', 'string', default='', notnull=True), 
    Field('descripcion', 'string', default='', notnull=True), 
    migrate=False)


db.define_table('tipos_cambio', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True),
    Field('moneda', db.monedas,
          requires=IS_IN_DB(db, db.monedas, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione una moneda')), 
    Field('area', db.areas,
          requires=IS_IN_DB(db, db.areas, '%(area)s', zero='[Seleccionar]',
                            error_message='Seleccione un área')), 
    Field('modo', 'integer', default=0, notnull=True), 
    Field('fecha', 'date', notnull=True), 
    Field('hora', 'time', default=datetime.time(0,0,0), notnull=True), 
    Field('valor', 'double', default=0.0, notnull=True), 
    Field('user_ing', db.auth_user,
          requires=IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione un usuario')), 
    migrate=False)


db.define_table('transferencias_produccion', 
    Field('id', 'integer'), 
    Field('codbarras', db.maestro,
          requires=IS_IN_DB(db, db.maestro, '%(codbarras)s', zero='[Seleccionar]',
                            error_message='Seleccione un código de barras')), 
    Field('descripcion', 'string', default='', notnull=True), 
    Field('total', 'integer', default=0, notnull=True), 
    Field('transferencia', 'integer', default=0, notnull=True), 
    Field('produccion', 'integer', default=0, notnull=True), 
    Field('turno', db.turnos,
          requires=IS_IN_DB(db, db.turnos, '%(turno)s', zero='[Seleccionar]',
                            error_message='Seleccione un turno')), 
    Field('fecha', 'date', notnull=True), 
    migrate=False)


db.define_table('ubigeo_departamentos',
    Field('id', 'integer'),
    Field('departamento', 'string', default='', notnull=True), 
    Field('descripcion', 'string', default='', notnull=True), 
    migrate=False)


db.define_table('ubigeo_provincias',
    Field('id', 'integer'),
    Field('departamento', 'string', default='', notnull=True), 
    Field('provincia', 'string', default='', notnull=True), 
    Field('descripcion', 'string', default='', notnull=True), 
    migrate=False)


db.define_table('ubigeo_detalle',
    Field('id', 'integer'),
    Field('departamento', 'string', default='', notnull=True), 
    Field('provincia', 'string', default='', notnull=True), 
    Field('ubigeo', 'string', default='', notnull=True), 
    Field('descripcion', 'string', default='', notnull=True), 
    migrate=False)


db.define_table('variaciones_derivados', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True),
    Field('codbarras', db.maestro,
          requires=IS_IN_DB(db, db.maestro, '%(codbarras)s', zero='[Seleccionar]',
                            error_message='Seleccione un código de barras')), 
    Field('tiempo_ini', 'datetime', notnull=True), 
    Field('tiempo_fin', 'datetime', notnull=True), 
    Field('porcentaje', 'double', default=0.0, notnull=True), 
    Field('cp', 'string', default='', notnull=True), 
    Field('turno', db.turnos,
          requires=IS_IN_DB(db, db.turnos, '%(turno)s', zero='[Seleccionar]',
                            error_message='Seleccione un turno')), 
    Field('modo', 'integer', default=0, notnull=True), 
    migrate=False)


db.define_table('vehiculos',
    Field('id', 'integer'),
    Field('codigo', 'string', default='', notnull=True), 
    Field('doc_id', 'string', default='', notnull=True), 
    Field('registro', 'string', default='', notnull=True), 
    Field('marca', 'string', default='', notnull=True), 
    Field('modelo', 'string', default='', notnull=True), 
    Field('tipo', 'string', default='', notnull=True), 
    Field('caracteristicas', 'string', default='', notnull=True), 
    Field('posicion', 'integer', default=0, notnull=True), 
    migrate=False)


db.define_table('ventas_bancos_cuentas',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True),
    Field('codigo', 'string', default='', notnull=True), 
    Field('entidad', 'string', default='', notnull=True), 
    Field('moneda', db.monedas,
          requires=IS_IN_DB(db, db.monedas, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione una moneda')), 
    migrate=False)


db.define_table('ventas_bancos_operaciones', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True),
    Field('pv', db.puntos_venta,
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')), 
    Field('fechav', 'date', notnull=True), 
    Field('fechad', 'date', notnull=True), 
    Field('banco', 'string', default='', notnull=True), 
    Field('monto', 'double', default=0.0, notnull=True), 
    Field('cambio', 'double', default=0.0, notnull=True), 
    Field('glosa1', 'string', default='', notnull=True), 
    Field('glosa2', 'string', default='', notnull=True), 
    Field('agencia', 'string', default='', notnull=True), 
    migrate=False)


db.define_table('ventas_grupos',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True),
    Field('codigo', 'string', default='', notnull=True), 
    Field('nombre', 'string', default='', notnull=True), 
    Field('atajo', 'string', default='', notnull=True), 
    Field('articulo', 'string', default='', notnull=True), 
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
    Field('aux_data', 'integer', default=0, notnull=True), 
    migrate=False)


db.define_table('ventas_operaciones', 
    Field('id', 'integer'), 
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True),
    Field('pv', db.puntos_venta,
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')), 
    Field('caja', 'integer', default=0, notnull=True), 
    Field('tiempo', 'datetime', notnull=True), 
    Field('n_doc_prefijo', 'string', default='', notnull=True), 
    Field('n_doc_base', 'string', default='', notnull=True), 
    Field('n_doc_sufijo', 'string', default='', notnull=True), 
    Field('estado', 'integer', default=0, notnull=True), 
    Field('documento', 'integer', default=0, notnull=True), 
    Field('cliente', 'string', default='', notnull=True), 
    Field('user_ing', db.auth_user,
          requires=IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione un usuario')), 
    Field('user_null', db.auth_user,
          requires=IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s',
                            zero='[Seleccionar]',
                            error_message='Seleccione un usuario')), 
    Field('forma_pago', 'string', default='', notnull=True), 
    Field('vales', 'string', default='', notnull=True), 
    Field('sello', db.sellos,
          requires=IS_IN_DB(db, db.sellos, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un sello')), 
    Field('codbarras', db.maestro,
          requires=IS_IN_DB(db, db.maestro, '%(codbarras)s', zero='[Seleccionar]',
                            error_message='Seleccione un código de barras')), 
    Field('precio', 'double', default=0.0, notnull=True), 
    Field('cantidad', 'integer', default=0, notnull=True), 
    Field('total', 'double', default=0.0, notnull=True), 
    Field('monto_local', 'double', default=0.0, notnull=True), 
    Field('monto_dolar', 'double', default=0.0, notnull=True), 
    Field('data_1', 'string', default='', notnull=True), 
    Field('data_2', 'string', default='', notnull=True), 
    Field('imod', 'integer', default=0, notnull=True), 
    migrate=False)


db.define_table('ventas_resumen',
    Field('id', 'integer'),
    Field('registro', 'datetime', label='Fecha de Registro', default=now, notnull=True),
    Field('pv', db.puntos_venta,
          requires=IS_IN_DB(db, db.puntos_venta, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un punto de venta')), 
    Field('fecha', 'date', notnull=True), 
    Field('cnt_doc', 'integer', default=0, notnull=True), 
    Field('total_neto', 'double', default=0.0, notnull=True), 
    Field('total_igv', 'double', default=0.0, notnull=True), 
    Field('total_srv', 'double', default=0.0, notnull=True), 
    Field('total_bruto', 'double', default=0.0, notnull=True), 
    Field('status', 'integer', default=1, notnull=True), 
    Field('condicion_comercial', 'integer', default=1, notnull=True), 
    migrate=False)


# Representations
db.auth_membership.user_id.represent = lambda ID: db.auth_user(ID).first_name + ' ' + db.auth_user(ID).last_name
db.auth_membership.group_id.represent = lambda ID: db.auth_group(ID).role
