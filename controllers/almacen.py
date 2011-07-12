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
    #    'docventa.codbarras','docventa.cantidad','docventa.precio','docventa.sub_total_bruto',
    #    'docventa.total','docventa.cv_anul','docventa.condicion_comercial']
    grid.action_links = ['view']
    grid.action_headers = ['Ver']
    #grid.totals = ['docventa.cantidad','docventa.sub_total_bruto']
    grid.filters = ['almacenes.almacen','almacenes.modo','almacenes.estado',
        'almacenes.fecha_doc', 'almacenes.n_doc_base', 'almacenes.proveedor',
        'almacenes.codbarras']
    #    'docventa.cliente','docventa.codbarras','docventa.condicion_comercial']
    #grid.filter_query = lambda f,v: f==v
    grid.enabled_rows = ['header','filter', 'pager','totals','footer']
    return dict(grid=grid())


@auth.requires(restricciones)
def kardex():
    """
    Kardex de Almacen
    """
    producto = request.vars.producto
    almacen = request.vars.almacen
    form = SQLFORM.factory(
        Field('almacen', db.almacenes_lista, default=almacen, label='Almacén',
          requires=IS_IN_DB(db, db.almacenes_lista, '%(almacen)s', zero='[Seleccionar]',
                            error_message='Seleccione un almacén')),
        Field('producto', 'integer', label='Producto', default=producto, widget = SQLFORM.widgets.autocomplete(
            request, db.maestro.alias, id_field=db.maestro.id, mode=1,
            filterby=db.maestro.genero, filtervalue='1')),
        Field('inicio', 'date', label='Fecha Inicio', default=session.fecha_inicio_alm),
        Field('fin', 'date', label='Fecha Fin', default=session.fecha_fin_alm)
        )
    rows = []
    rows2 = []
    if form.accepts(request.vars, session):
        session.almacen = form.vars.almacen
        session.prod_alm = form.vars.producto
        session.fecha_inicio_alm = form.vars.inicio
        if form.vars.fin:
            session.fecha_fin_alm = form.vars.fin
        else:
            session.fecha_fin_alm = form.vars.inicio
        rows = db((db.almacenes.estado==1) & (db.almacenes.almacen==session.almacen) &
            (db.almacenes.fecha_doc>=session.fecha_inicio_alm) &
            (db.almacenes.fecha_doc<=session.fecha_fin_alm) &
            (db.almacenes.codbarras==session.prod_alm)
            ).select(db.almacenes.n_doc_base,db.almacenes.fecha_doc,
            db.almacenes.operacion_logistica,db.almacenes.ingreso,
            db.almacenes.salida, db.almacenes.almacen_destino, db.operaciones_logisticas.operacion,
            db.almacenes_lista.almacen, db.directorio.nombre_corto,
            left=(db.almacenes.on(db.almacenes.operacion_logistica==db.operaciones_logisticas.id),
            db.almacenes_lista.on(db.almacenes.almacen_destino==db.almacenes_lista.id),
            db.directorio.on(db.almacenes.proveedor==db.directorio.id)),
            orderby=db.almacenes.fecha_doc|db.almacenes.n_doc_base 
            )
        rows2 = db((db.maestro.id==session.prod_alm) &
            (db.maestro.unidad_medida==db.unidades_medida.id)
            ).select(db.unidades_medida.codigo,
            db.maestro.nombre, db.maestro.descripcion, db.maestro.codbarras, db.maestro.id
            )
    return dict(form=form, rows=rows, rows2=rows2)


@auth.requires(restricciones)
def saldos():
    """
    Saldos de Almacen
    """
    query = """select cast(alm.codbarras as UNSIGNED),mae.codbarras,concat(mae.nombre,' ',mae.descripcion),
        sum(if(alm.ingreso is
        NULL,0,alm.ingreso)-if(alm.salida is NULL,0,alm.salida)) saldo from
        almacenes alm left join maestro mae on mae.id=alm.codbarras where
        alm.almacen='%s' and alm.estado='1' and
        alm.fecha_doc>='%s' and alm.fecha_doc<='%s' group by codbarras order by
        alm.codbarras"""
    almacen = request.vars.almacen
    form = SQLFORM.factory(
        Field('almacen', db.almacenes_lista, default=almacen, label='Almacén',
          requires=IS_IN_DB(db, db.almacenes_lista, '%(almacen)s', zero='[Seleccionar]',
                            error_message='Seleccione un almacén')),
        Field('inicio', 'date', label='Fecha Inicio', default=session.fecha_inicio_alm),
        Field('fin', 'date', label='Fecha Fin', default=session.fecha_fin_alm)
        )
    rows = []
    if form.accepts(request.vars, session):
        session.almacen = form.vars.almacen
        session.fecha_inicio_alm = form.vars.inicio
        session.fecha_fin_alm = form.vars.fin
        sql = query % (session.almacen, session.fecha_inicio_alm, session.fecha_fin_alm)
        rows = db.executesql(sql)
    return dict(form=form, rows=rows)
