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
