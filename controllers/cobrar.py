# -*- coding: utf-8 -*-

restricciones = auth.has_membership('root') or \
                auth.has_membership('administrador')

                
@auth.requires(restricciones)
def index():
    """
    Muestra los registros de cuentas por cobrar
    """    
    return dict()


@auth.requires(restricciones)
def clientes():
    """
    Muestra los registros de los clientes
    """    
    return dict()
    

@auth.requires(restricciones)
def clientes_agregar():
    """
    Agregar nuevo registro a 'directorio'
    """
    form = SQLFORM(db.directorio, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def clientes_reporte():
    """
    Muestra el reporte de los clientes
    """
    return dict()


@auth.requires(restricciones)
def cuentas():
    """
    Muestra los registros de los cuentas por cobrar
    """    
    return dict()
    

@auth.requires(restricciones)
def cuentas_agregar():
    """
    Agregar nuevo registro a 'cuentas_por_cobrar'
    """
    form = SQLFORM(db.cuentas_por_cobrar, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def cuentas_reporte():
    """
    Muestra el reporte de las cuentas por cobrar
    """
    return dict()
