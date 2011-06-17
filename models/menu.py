# -*- coding: utf-8 -*-

response.title = 'SISVENTI'
response.subtitle = T('customize me!')

#http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'you'
response.meta.description = 'Free and open source full-stack enterprise framework for agile development of fast, scalable, secure and portable database-driven web-based applications. Written and programmable in Python'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Enterprise Framework'
response.meta.copyright = 'Copyright 2007-2010'


# Custom menus
inicio = [(T('Home'), False, URL('default','index'), [])]
        
configuracion = [
            ('Configuración', False, URL('configuracion', 'index'),
            [
                ('General', False, None,
                [
                    ('Artículos', False, URL('configuracion', 'articulos')),
                    ('Casas', False, URL('configuracion', 'casas'),
                    [
                        ('Sub-Casas', False, URL('configuracion', 'sub_casas')),
                    ]),
                    ('Directorio', False, URL('configuracion', 'directorio')),
                    ('Documentos de Identidad', False, URL('configuracion', 'doc_identidad')),
                    ('Empaques', False, URL('configuracion', 'empaques')),
                    ('Estados', False, URL('configuracion', 'estados')),
                    ('Monedas', False, URL('configuracion', 'monedas')),
                    ('Sellos', False, URL('configuracion', 'sellos'),
                    [
                        ('Sub-Sellos', False, URL('configuracion', 'sub_sellos')),
                    ]),
                    ('Tipo de Cambio', False, URL('configuracion', 'tipo_cambio')),
                    ('Tipos', False, URL('configuracion', 'tipos')),
                    ('Transportistas', False, URL('configuracion', 'transportistas')),
                    ('Turnos', False, URL('configuracion', 'turnos')),
                    ('Unidades de Medida', False, URL('configuracion', 'unidades_medida')),
                    ('Usuarios', False, URL('users', 'index'),
                    [
                        ('Nuevo usuario', False, None,
                         [
                            ('Administrador (Sistema)', False, URL('users', 'add', vars={'group':'root'})),
                            ('Administrador (Punto de Venta)', False, URL('users', 'add', vars={'group':'administrador'})),
                            ('Almacenes', False, URL('users', 'add', vars={'group':'almacenes'})),
                            ('Compras', False, URL('users', 'add', vars={'group':'compras'})),
                            ('Reportes', False, URL('users', 'add', vars={'group':'reportes'})),
                            ('Ventas', False, URL('users', 'add', vars={'group':'ventas'})),
                         ])
                     ])
                ]),
                ('Comercial', False, None,
                [
                    ('Comprobantes', False, URL('configuracion', 'comprobantes')),
                    ('Condiciones Comerciales', False, URL('configuracion', 'condiciones_comerciales'))
                ]),
                ('Productos', False, None,
                [
                    ('Componentes', False, None,
                    [
                        ('Recetas', False, None,
                        [
                            ('Mantenimiento General', False, URL('configuracion', 'recetas'))
                        ])
                    ]),
                    ('Gestión de Productos', False, URL('configuracion', 'productos'),
                    [
                        ('Administración POS', False, URL('configuracion', 'productos_pos'))
                    ])
                ]),
                ('Ventas', False, None,
                [
                    ('Formas de Pago', False, URL('configuracion', 'formas_pago')),
                    ('Puntos de Venta', False, URL('configuracion', 'puntos_venta'))
                ])
            ])
        ]
        
almacenes = [('Almacenes', False, None, [])]

por_cobrar = [
            ('Cuentas por Cobrar', False, URL('cobrar', 'index'),
            [
                ('Clientes', False, URL('cobrar', 'clientes'),
                 [
                    ('Agregar', False, URL('cobrar', 'clientes_agregar'), []),
                    ('Reporte', False, URL('cobrar', 'clientes_reporte'), [])
                 ]),
                ('Cuentas', False, URL('cobrar', 'cuentas'),
                 [
                    ('Agregar', False, URL('cobrar', 'cuentas_agregar'), []),
                    ('Reporte', False, URL('cobrar', 'cuentas_reporte'), []),
                 ]),
            ])
        ]
        
por_pagar = [
            ('Cuentas por Pagar', False, URL('pagar', 'index'),
            [
                ('Proveedores', False, URL('pagar', 'proveedores'),
                 [
                    ('Agregar', False, URL('pagar', 'proveedores_agregar'), []),
                    ('Reporte', False, URL('pagar', 'proveedores_reporte'), [])
                 ]),
                ('Cuentas', False, URL('pagar', 'cuentas'),
                 [
                    ('Agregar', False, URL('pagar', 'cuentas_agregar'), []),
                    ('Reporte', False, URL('pagar', 'cuentas_reporte'), []),
                 ]),
            ])
        ]
        
reportes = [('Reportes', False, None, [])]
        
ventas = [
            ('Ventas', False, None,
            [
                ('Delivery', False, URL('ventas', 'delivery'), []),
                ('Dependencias de Productos', False, URL('ventas', 'dependencias_productos'), []),
                ('Descuentos', False, URL('ventas', 'descuentos'), []),
                ('Promociones', False, URL('ventas', 'promociones'), [])
            ])
        ]


# Add menus to type of user
if not auth.user:
    response.menu = inicio
elif auth.has_membership(user_id=auth.user.id, role='root'):
    response.menu = inicio
    response.menu += almacenes
    response.menu += por_cobrar
    response.menu += por_pagar
    response.menu += reportes
    response.menu += ventas
    response.menu += configuracion

        
    """
    response.menu+=[
        (T('This App'), False, URL('admin', 'default', 'design/%s' % request.application),
         [
                (T('Controller'), False,
                 URL('admin', 'default', 'edit/%s/controllers/%s.py' \
                         % (request.application,request.controller=='appadmin' and
                            'default' or request.controller))),
                (T('View'), False,
                 URL('admin', 'default', 'edit/%s/views/%s' \
                         % (request.application,response.view))),
                (T('Layout'), False,
                 URL('admin', 'default', 'edit/%s/views/layout.html' \
                         % request.application)),
                (T('Stylesheet'), False,
                 URL('admin', 'default', 'edit/%s/static/base.css' \
                         % request.application)),
                (T('DB Model'), False,
                 URL('admin', 'default', 'edit/%s/models/db.py' \
                         % request.application)),
                (T('Menu Model'), False,
                 URL('admin', 'default', 'edit/%s/models/menu.py' \
                         % request.application)),
                (T('Database'), False,
                 URL(request.application, 'appadmin', 'index')),

                (T('Errors'), False,
                 URL('admin', 'default', 'errors/%s' \
                         % request.application)),

                (T('About'), False,
                 URL('admin', 'default', 'about/%s' \
                         % request.application)),

                ]
       )]"""
