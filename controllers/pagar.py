# -*- coding: utf-8 -*-

restricciones = auth.has_membership('root') or \
                auth.has_membership('administrador')

                
@auth.requires(restricciones)
def index():
    """
    Muestra los registros de cuentas por pagar
    """    
    return dict()


@auth.requires(restricciones)
def agregar():
    """
    Agregar nueva registro
    """
    form = SQLFORM(db.directorio, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def reporte():
    """
    Muestra el reporte de las cuentas por pagar
    """
    return dict()
