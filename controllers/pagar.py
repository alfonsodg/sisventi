# -*- coding: utf-8 -*-

def index():
    """
    Muestra los registros de cuentas por pagar
    """    
    return dict()


def agregar():
    """
    Agregar nueva registro
    """
    form = SQLFORM(db.directorio, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


def reporte():
    """
    Muestra el reporte de las cuentas por pagar
    """
    return dict()
