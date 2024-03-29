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
def proveedores():
    """
    Muestra los registros de los proveedores
    """    
    return dict()
    

@auth.requires(restricciones)
def proveedores_agregar():
    """
    Agregar nuevo registro a 'directorio'
    """
    form = SQLFORM(db.directorio, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def proveedores_reporte():
    """
    Muestra el reporte de los proveedores
    """
    grid = webgrid.WebGrid(crud)
    grid.datasource = db(db.directorio.modo==2).select()
    grid.pagesize = 20
    #grid.fields = ['db.catmod.id', 'db.catmod.nombre', 'db.catmod.posicion']
    #grid.filters = ['db.catmod.catmod', 'db.catmod.nombre']
    return dict(grid=grid())


@auth.requires(restricciones)
def cuentas_pagar():
    """
    Muestra los registros de los cuentas por cobrar
    """    
    cuentas = db(db.cuentas_por_pagar).select()
    return dict(cuentas=cuentas)
    

@auth.requires(restricciones)
def cuentas_agregar():
    """
    Agregar nuevo registro a 'cuentas_por_cobrar'
    """
    form = SQLFORM(db.cuentas_por_pagar, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)
    
    

@auth.requires(restricciones)
def cuentas_reporte():
    """
    Muestra el reporte de las cuentas por pagar
    """
    grid = webgrid.WebGrid(crud)
    grid.datasource = db(db.cuentas_por_pagar).select()
    grid.pagesize = 20
    #grid.fields = ['db.catmod.id', 'db.catmod.nombre', 'db.catmod.posicion']
    #grid.filters = ['db.catmod.catmod', 'db.catmod.nombre']
    return dict(grid=grid())
