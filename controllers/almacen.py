# -*- coding: utf-8 -*-

restricciones = auth.has_membership('root') or \
                auth.has_membership('administrador') or \
                auth.has_membership('ventas')


@auth.requires(restricciones)
def index():
    return dict()


def data():
    return dict(form=crud())


@auth.requires(restricciones)
def operaciones():
    """
    Documentos de venta
    """
    grid = webgrid.WebGrid(crud)
    grid.datasource = db(db.almacenes)
    grid.pagesize = 20
    grid.crud_function = 'data'
    grid.fields = ['almacenes.almacen','almacenes.modo','almacenes.estado',
        'almacenes.operacion_logistica', 'almacenes.fecha_doc', 'almacenes.n_doc_base', 'almacenes.proveedor',
        'almacenes.almacen_origen', 'almacenes.almacen_destino', 'almacenes.codbarras',
        'almacenes.ingreso', 'almacenes.salida', 'almacenes.observaciones']
    #    'docventa.estado','docventa.comprobante','docventa.cliente','docventa.cv_ing',
    #    'docventa.codigo','docventa.cantidad','docventa.precio','docventa.sub_total_bruto',
    #    'docventa.total','docventa.cv_anul','docventa.condicion_comercial']
    grid.action_links = ['view']
    grid.action_headers = ['Ver']
    #grid.totals = ['docventa.cantidad','docventa.sub_total_bruto']
    grid.filters = ['almacenes.almacen','almacenes.modo','almacenes.estado',
        'almacenes.fecha_doc', 'almacenes.n_doc_base', 'almacenes.proveedor',
        'almacenes.codbarras']
    #    'docventa.cliente','docventa.codigo','docventa.condicion_comercial']
    #grid.filter_query = lambda f,v: f==v
    grid.enabled_rows = ['header','filter', 'pager','totals','footer']
    return dict(grid=grid())


@auth.requires(restricciones)
def kardex():
    """
    Kardex de Almacen
    """
    form = SQLFORM.factory(
        Field('almacen', 'integer', label='Almacen', default=session.almacen),
        Field('producto', 'integer', label='Producto', default=session.prod_alm),
        Field('inicio', 'date', label='Fecha Inicio', default=session.fecha_inicio_alm),
        Field('fin', 'date', label='Fecha Fin', default=session.fecha_fin_alm)
        )
    rows = []
    if form.accepts(request.vars, session):
        #response.flash = 'form accepted'
        session.almacen = form.vars.almacen
        session.prod_alm = form.vars.producto
        session.fecha_inicio_alm = form.vars.inicio
        session.fecha_fin_alm = form.vars.fin
        rows = db((db.almacenes.estado==1) &(db.almacenes.almacen==session.almacen) &
            (db.almacenes.fecha_doc>=session.fecha_inicio_alm) &
            (db.almacenes.fecha_doc<=session.fecha_fin_alm) &
            (db.almacenes.codbarras==session.prod_alm)
            ).select(db.almacenes.n_doc_base,db.almacenes.fecha_doc,
            db.almacenes.operacion_logistica,db.almacenes.ingreso,
            db.almacenes.salida, db.almacenes.almacen_destino, orderby=db.almacenes.fecha_doc 
            )
    #elif form.errors:
        #response.flash = 'form has errors'
    return dict(form=form, rows=rows)


@auth.requires(restricciones)
def saldos():
    """
    Kardex de Almacen
    """
    query = """select cast(codbarras as UNSIGNED),sum(if(ingreso is
        NULL,0,ingreso)-if(salida is NULL,0,salida)) saldo from
        almacenes where almacen='%s' and estado='1' and
        fecha_doc>='%s' and fecha_doc<='%s' group by codbarras order by
        codbarras"""
    form = SQLFORM.factory(
        Field('almacen', 'integer', label='Almacen', default=session.almacen),
        Field('inicio', 'date', label='Fecha Inicio', default=session.fecha_inicio_alm),
        Field('fin', 'date', label='Fecha Fin', default=session.fecha_fin_alm)
        )
    rows = []
    if form.accepts(request.vars, session):
        #response.flash = 'form accepted'
        session.almacen = form.vars.almacen
        session.fecha_inicio_alm = form.vars.inicio
        session.fecha_fin_alm = form.vars.fin
        sql = query % (session.almacen, session.fecha_inicio_alm, session.fecha_fin_alm)
        rows = db.executesql(sql)
        print rows, sql
        #rows = db((db.almacenes.estado==1) &(db.almacenes.almacen==session.almacen) &
            #(db.almacenes.fecha_doc>=session.fecha_inicio_alm) &
            #(db.almacenes.fecha_doc<=session.fecha_fin_alm)
            #).select(db.almacenes.n_doc_base,db.almacenes.fecha_doc,
            #db.almacenes.operacion_logistica,db.almacenes.ingreso,
            #db.almacenes.salida, db.almacenes.almacen_destino, orderby=db.almacenes.fecha_doc 
            #)
    #elif form.errors:
        #response.flash = 'form has errors'
    return dict(form=form, rows=rows)
