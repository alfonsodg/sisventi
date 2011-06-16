# -*- coding: utf-8 -*-

restricciones = True


@auth.requires(restricciones)
def index():
    """
    Muestra las opciones de configuracion
    """
    return dict()


@auth.requires(restricciones)
def tipo_cambio():
    """
    Muestra las configuraciones del tipo de cambio
    """
    tipos = db(db.tipos_cambio).select()
    return dict(tipos=tipos)


@auth.requires(restricciones)
def tipo_cambio_agregar():
    """
    Agregar nuevo registro a 'tipos_cambio'
    """
    form = SQLFORM(db.tipos_cambio, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def directorio():
    """
    Muestra las configuraciones del directorio
    """
    directorios = db(db.directorio).select()
    return dict(directorios=directorios)


@auth.requires(restricciones)
def directorio_agregar():
    """
    Agregar nuevo registro a 'directorio'
    """
    form = SQLFORM(db.directorio, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def comprobantes():
    """
    Muestra las configuraciones de los comprobantes
    """
    comprobantes = db(db.documentos_comerciales).select()
    return dict(comprobantes=comprobantes)


@auth.requires(restricciones)
def comprobantes_agregar():
    """
    Agregar nuevo registro a 'documentos_comerciales'
    """
    form = SQLFORM(db.documentos_comerciales, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def formas_pago():
    """
    Muestra las configuraciones de las formas de pago
    """
    formas = db(db.formas_pago).select()
    return dict(formas=formas)


@auth.requires(restricciones)
def formas_pago_agregar():
    """
    Agregar nuevo registro a 'formas_pago'
    """
    form = SQLFORM(db.formas_pago, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def productos():
    """
    Muestra las configuraciones de los productos
    """
    productos = db(db.maestro).select()
    return dict(productos=productos)


@auth.requires(restricciones)
def productos_agregar():
    """
    Agregar nuevo registro a 'maestro'
    """
    form = SQLFORM(db.maestro, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def productos_pos():
    """
    Muestra las configuraciones para productos pos
    """
    productos = db(db.maestro_pos).select()
    return dict(productos=productos)


@auth.requires(restricciones)
def productos_pos_agregar():
    """
    Agregar nuevo registro a 'maestro_pos'
    """
    form = SQLFORM(db.maestro_pos, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def recetas():
    """
    Muestra las configuraciones de las recetas
    """
    recetas = db(db.recetas).select()
    return dict(recetas=recetas)


@auth.requires(restricciones)
def recetas_agregar():
    """
    Agregar nuevo registro a 'recetas'
    """
    form = SQLFORM(db.recetas, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def monedas():
    """
    Muestra las configuraciones para las monedas
    """
    monedas = db(db.monedas).select()
    return dict(monedas=monedas)


@auth.requires(restricciones)
def monedas_agregar():
    """
    Agregar nuevo registro a 'monedas'
    """
    form = SQLFORM(db.monedas, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)
