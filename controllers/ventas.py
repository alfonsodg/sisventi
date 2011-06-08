# -*- coding: utf-8 -*-

def index():
    return dict()


def delivery():
    """
    Muestra registros de ventas por delivery
    """
    deliveries = db(db.delivery).select()
    return dict(deliveries=deliveries)


def delivery_agregar():
    """
    Agregar registro a 'delivery'
    """
    form = SQLFORM(db.delivery, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


def dependencias_productos():
    """
    Dependencias de los productos
    """
    dependencias = db(db.maestro_dependencias).select()
    return dict(dependencias=dependencias)


def dependencias_productos_agregar():
    """
    Agregar registro a 'maestro_dependencias'
    """
    form = SQLFORM(db.maestro_dependencias, submit_button='Aceptar')
    return dict(form=form)
