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
        'docventa.codigo','docventa.cantidad','docventa.precio','docventa.sub_total_bruto',
        'docventa.total','docventa.cv_anul','docventa.condicion_comercial']
    grid.action_links = ['view']
    grid.action_headers = ['Ver']
    grid.totals = ['docventa.cantidad','docventa.sub_total_bruto']
    grid.filters = ['docventa.fecha_vta','docventa.estado','docventa.comprobante',
        'docventa.cliente','docventa.codigo','docventa.condicion_comercial']
    #grid.filter_query = lambda f,v: f==v
    grid.enabled_rows = ['header','filter', 'pager','totals','footer']
    return dict(grid=grid())


def totales():
    """
    Ventas Totales
    """
    form = SQLFORM.factory(
        Field('inicio', 'date', label='Fecha Inicio', default=session.fecha_inicio_vta),
        Field('fin', 'date', label='Fecha Fin', default=session.fecha_fin_vta))
    rows = []
    if form.accepts(request.vars, session):
        #response.flash = 'form accepted'
        session.fecha_inicio_vta = form.vars.inicio
        session.fecha_fin_vta = form.vars.fin
        rows = db((db.docventa.estado==1) & (db.docventa.fecha_vta>=session.fecha_inicio_vta) &
            (db.docventa.fecha_vta<=session.fecha_fin_vta)
            ).select(db.docventa.comprobante,db.docventa.n_doc_base,db.docventa.total,
            groupby=db.docventa.comprobante|db.docventa.n_doc_base)
    #elif form.errors:
        #response.flash = 'form has errors'
    return dict(form=form, rows=rows)






@auth.requires(restricciones)
def dependencias_productos():
    """
    Dependencias de los productos
    """
    dependencias = db(db.maestro_dependencias).select()
    return dict(dependencias=dependencias)


@auth.requires(restricciones)
def dependencias_productos_agregar():
    """
    Agregar registro a 'maestro_dependencias'
    """
    form = SQLFORM(db.maestro_dependencias, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def descuentos():
    """
    Descuentos aplicados a las ventas 
    """
    descuentos = db(db.maestro_descuentos).select()
    return dict(descuentos=descuentos)


@auth.requires(restricciones)
def descuentos_agregar():
    """
    Agregar registro a 'maestro_descuentos'
    """
    form = SQLFORM(db.maestro_descuentos, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def promociones():
    """
    Promociones para las ventas
    """
    promociones = db(db.promociones).select()
    return dict(promociones=promociones)


@auth.requires(restricciones)
def promociones_agregar():
    """
    Agregar registro a 'promociones'
    """
    form = SQLFORM(db.promociones, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)
