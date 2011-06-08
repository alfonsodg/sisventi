# -*- coding: utf-8 -*-

restricciones = auth.has_membership('root') or \
                auth.has_membership('administrador') or \
                auth.has_membership('ventas')


@auth.requires(restricciones)
def index():
    return dict()


@auth.requires(restricciones)
def delivery():
    """
    Muestra registros de ventas por delivery
    """
    deliveries = db(db.delivery).select()
    return dict(deliveries=deliveries)


@auth.requires(restricciones)
def delivery_agregar():
    """
    Agregar registro a 'delivery'
    """
    form = SQLFORM(db.delivery, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


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
