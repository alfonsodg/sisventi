# -*- coding: utf-8 -*-

restricciones = auth.has_membership('root') or \
                auth.has_membership('administrador') or \
                auth.has_membership('ventas')

today = datetime.date.today()

@auth.requires(restricciones)
def index():
    return dict()


def data():
    return dict(form=crud())


@auth.requires(restricciones)
def pedidos():
    """
    Muestra registros de ventas por delivery
    """
    grid = webgrid.WebGrid(crud)
    grid.datasource = db(db.pedidos).select()
    grid.pagesize = 20
    grid.crud_function = 'data'
    grid.fields = ['pedidos.fecha', 'pedidos.pv', 'pedidos.n_doc_base',
        'pedidos.codbarras', 'pedidos.cantidad', 'pedidos.modo',
        'pedidos.estado', 'pedidos.user_ing'
    ]
    grid.totals = ['pedidos.cantidad']
    grid.filters = ['pedidos.fecha', 'pedidos.pv', 'pedidos.n_doc_base',
        'pedidos.codbarras', 'pedidos.estado', 'pedidos.user_ing'
    ]
    return dict(grid=grid())


@auth.requires(restricciones)
def delivery():
    """
    Muestra registros de ventas por delivery
    """
    grid = webgrid.WebGrid(crud)
    grid.datasource = db(db.delivery).select()
    grid.pagesize = 20
    return dict(grid=grid())


@auth.requires(restricciones)
def operaciones():
    """
    Documentos de venta
    """
    grid = webgrid.WebGrid(crud)
    grid.datasource = db(db.docventa)
    grid.pagesize = 20
    grid.crud_function = 'data'
    grid.fields = ['docventa.pv','docventa.caja','docventa.fecha_vta','docventa.n_doc_base',
        'docventa.estado','docventa.comprobante','docventa.cliente','docventa.cv_ing',
        'docventa.codbarras','docventa.cantidad','docventa.precio','docventa.sub_total_bruto',
        'docventa.total','docventa.cv_anul','docventa.condicion_comercial']
    grid.action_links = ['view']
    grid.action_headers = ['Ver']
    grid.totals = ['docventa.cantidad','docventa.sub_total_bruto']
    grid.filters = ['docventa.fecha_vta','docventa.estado','docventa.comprobante',
        'docventa.cliente','docventa.codbarras','docventa.condicion_comercial','docventa.cv_ing']
    #grid.filter_query = lambda f,v: f==v
    grid.enabled_rows = ['header','filter', 'pager','totals','footer']
    return dict(grid=grid())


def totales():
    """
    Ventas Totales
    """
    form = SQLFORM.factory(
        Field('inicio', 'date', label='Fecha Inicio', default=session.fecha_inicio_vta),
        Field('fin', 'date', label='Fecha Fin', default=session.fecha_fin_vta)
        )
    rows = []
    if form.accepts(request.vars, session):
        session.fecha_inicio_vta = form.vars.inicio
        if form.vars.fin:
            session.fecha_fin_vta = form.vars.fin
        else:
            session.fecha_fin_vta = form.vars.inicio
        rows = db((db.docventa.estado==1) & (db.docventa.fecha_vta>=session.fecha_inicio_vta) &
            (db.docventa.fecha_vta<=session.fecha_fin_vta)
            ).select(db.docventa.comprobante,db.docventa.n_doc_base,db.docventa.total,
            groupby=db.docventa.comprobante|db.docventa.n_doc_base)
    return dict(form=form, rows=rows)


def totales_productos():
    """
    Ventas Totales por Productos
    """
    producto = request.vars.producto
    form = SQLFORM.factory(
        Field('producto', 'integer', label='Producto', default=producto, widget = SQLFORM.widgets.autocomplete(
            request, db.maestro.alias, id_field=db.maestro.id, mode=1,
            filterby=db.maestro.genero, filtervalue='2')),
        Field('inicio', 'date', label='Fecha Inicio', default=session.fecha_inicio_vta),
        Field('fin', 'date', label='Fecha Fin', default=session.fecha_fin_vta)
        )
    rows = []
    if form.accepts(request.vars, session):
        session.producto = form.vars.producto
        session.fecha_inicio_vta = form.vars.inicio
        if form.vars.fin:
            session.fecha_fin_vta = form.vars.fin
        else:
            session.fecha_fin_vta = form.vars.inicio
        if session.producto:
            rows = db((db.docventa.estado==1) & (db.docventa.fecha_vta>=session.fecha_inicio_vta) &
                (db.docventa.fecha_vta<=session.fecha_fin_vta) &
                (db.docventa.codbarras==session.producto)
                ).select(db.docventa.comprobante,db.docventa.n_doc_base,db.docventa.codbarras,
                db.maestro.alias,db.docventa.sub_total_bruto,
                left=db.docventa.on(db.docventa.codbarras==db.maestro.id),
                groupby=db.docventa.comprobante|db.docventa.n_doc_base)
        else:
            rows = db((db.docventa.estado==1) & (db.docventa.fecha_vta>=session.fecha_inicio_vta) &
                (db.docventa.fecha_vta<=session.fecha_fin_vta) #&
                #(db.docventa.codbarras==session.producto)
                ).select(db.docventa.comprobante,db.docventa.n_doc_base,db.docventa.codbarras,
                db.maestro.alias,db.docventa.sub_total_bruto,
                left=db.docventa.on(db.docventa.codbarras==db.maestro.id),
                groupby=db.docventa.comprobante|db.docventa.n_doc_base)
    return dict(form=form, rows=rows)


def totales_comprobantes():
    """
    Ventas Totales
    """
    comprobante = request.vars.comprobante
    form = SQLFORM.factory(
        Field('comprobante', db.documentos_comerciales, default=comprobante, label='Documento Comercial',
          requires=IS_IN_DB(db, db.documentos_comerciales, '%(nombre)s', zero='[Seleccionar]',
                            error_message='Seleccione un comprobante')),
        Field('inicio', 'date', label='Fecha Inicio', default=session.fecha_inicio_vta),
        Field('fin', 'date', label='Fecha Fin', default=session.fecha_fin_vta)
        )
    rows = []
    if form.accepts(request.vars, session):
        session.comprobante = form.vars.comprobante
        session.fecha_inicio_vta = form.vars.inicio
        if form.vars.fin:
            session.fecha_fin_vta = form.vars.fin
        else:
            session.fecha_fin_vta = form.vars.inicio
        rows = db((db.docventa.estado==1) & (db.docventa.fecha_vta>=session.fecha_inicio_vta) &
            (db.docventa.fecha_vta<=session.fecha_fin_vta) &
            (db.docventa.comprobante==session.comprobante)
            ).select(db.docventa.comprobante,db.docventa.n_doc_base,db.docventa.total,
            groupby=db.docventa.comprobante|db.docventa.n_doc_base)
    return dict(form=form, rows=rows)
