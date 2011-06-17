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


@auth.requires(restricciones)
def puntos_venta():
    """
    Muestra las configuraciones para los puntos de venta
    """
    puntos = db(db.puntos_venta).select()
    return dict(puntos=puntos)


@auth.requires(restricciones)
def puntos_venta_agregar():
    """
    Agregar nuevo registro a 'puntos_venta'
    """
    form = SQLFORM(db.puntos_venta, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def condiciones_comerciales():
    """
    Muestra las configuraciones para las condiciones comerciales
    """
    condiciones = db(db.condiciones_comerciales).select()
    return dict(condiciones=condiciones)


@auth.requires(restricciones)
def condiciones_comerciales_agregar():
    """
    Agregar nuevo registro a 'condiciones_comerciales'
    """
    form = SQLFORM(db.condiciones_comerciales, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def doc_identidad():
    """
    Muestra las configuraciones para los documentos de identidad
    """
    documentos = db(db.documentos_identidad).select()
    return dict(documentos=documentos)


@auth.requires(restricciones)
def doc_identidad_agregar():
    """
    Agregar nuevo registro a 'documentos_identidad'
    """
    form = SQLFORM(db.documentos_identidad, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def transportistas():
    """
    Muestra las configuraciones para los transportistas
    """
    transportistas = db(db.transportistas).select()
    return dict(transportistas=transportistas)


@auth.requires(restricciones)
def transportistas_agregar():
    """
    Agregar nuevo registro a 'transportistas'
    """
    form = SQLFORM(db.transportistas, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def turnos():
    """
    Muestra las configuraciones para los turnos
    """
    turnos = db(db.turnos).select()
    return dict(turnos=turnos)


@auth.requires(restricciones)
def turnos_agregar():
    """
    Agregar nuevo registro a 'turnos'
    """
    form = SQLFORM(db.turnos, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def articulos():
    """
    Muestra las configuraciones para los articulos
    """
    articulos = db(db.articulos).select()
    return dict(articulos=articulos)


@auth.requires(restricciones)
def articulos_agregar():
    """
    Agregar nuevo registro a 'articulos'
    """
    form = SQLFORM(db.articulos, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def empaques():
    """
    Muestra las configuraciones para los empaques
    """
    empaques = db(db.empaques).select()
    return dict(empaques=empaques)


@auth.requires(restricciones)
def empaques_agregar():
    """
    Agregar nuevo registro a 'empaques'
    """
    form = SQLFORM(db.empaques, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def sellos():
    """
    Muestra las configuraciones para los sellos
    """
    sellos = db(db.sellos).select()
    return dict(sellos=sellos)


@auth.requires(restricciones)
def sellos_agregar():
    """
    Agregar nuevo registro a 'sellos'
    """
    form = SQLFORM(db.sellos, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def casas():
    """
    Muestra las configuraciones para las casas
    """
    casas = db(db.casas).select()
    return dict(casas=casas)


@auth.requires(restricciones)
def casas_agregar():
    """
    Agregar nuevo registro a 'casas'
    """
    form = SQLFORM(db.casas, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def sub_casas():
    """
    Muestra las configuraciones para las sub-casas
    """
    subcasas = db(db.sub_casas).select()
    return dict(subcasas=subcasas)


@auth.requires(restricciones)
def sub_casas_agregar():
    """
    Agregar nuevo registro a 'sub_casas'
    """
    form = SQLFORM(db.sub_casas, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def sub_sellos():
    """
    Muestra las configuraciones para los sub-sellos
    """
    subsellos = db(db.sub_sellos).select()
    return dict(subsellos=subsellos)


@auth.requires(restricciones)
def sub_sellos_agregar():
    """
    Agregar nuevo registro a 'sub_sellos'
    """
    form = SQLFORM(db.sub_sellos, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def estados():
    """
    Muestra las configuraciones para los estados
    """
    estados = db(db.status).select()
    return dict(estados=estados)


@auth.requires(restricciones)
def estados_agregar():
    """
    Agregar nuevo registro a 'status'
    """
    form = SQLFORM(db.status, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def tipos():
    """
    Muestra las configuraciones para los tipos
    """
    tipos = db(db.tipos).select()
    return dict(tipos=tipos)


@auth.requires(restricciones)
def tipos_agregar():
    """
    Agregar nuevo registro a 'tipos'
    """
    form = SQLFORM(db.tipos, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def unidades_medida():
    """
    Muestra las configuraciones para las unidades de medida
    """
    unidades = db(db.unidades_medida).select()
    return dict(unidades=unidades)


@auth.requires(restricciones)
def unidades_medida_agregar():
    """
    Agregar nuevo registro a 'unidades_medida'
    """
    form = SQLFORM(db.unidades_medida, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def generos():
    """
    Muestra las configuraciones para los generos
    """
    generos = db(db.generos).select()
    return dict(generos=generos)


@auth.requires(restricciones)
def generos_agregar():
    """
    Agregar nuevo registro a 'generos'
    """
    form = SQLFORM(db.generos, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def sub_generos():
    """
    Muestra las configuraciones para los sub-generos
    """
    subgeneros = db(db.sub_generos).select()
    return dict(subgeneros=subgeneros)


@auth.requires(restricciones)
def sub_generos_agregar():
    """
    Agregar nuevo registro a 'sub_generos'
    """
    form = SQLFORM(db.sub_generos, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def categorias():
    """
    Muestra las configuraciones para las categorias
    """
    categorias = db(db.categorias).select()
    return dict(categorias=categorias)


@auth.requires(restricciones)
def categorias_agregar():
    """
    Agregar nuevo registro a 'categorias'
    """
    form = SQLFORM(db.categorias, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def operaciones_logisticas():
    """
    Muestra las configuraciones para las operaciones logisticas
    """
    operaciones = db(db.operaciones_logisticas).select()
    return dict(operaciones=operaciones)


@auth.requires(restricciones)
def operaciones_logisticas_agregar():
    """
    Agregar nuevo registro a 'operaciones_logisticas'
    """
    form = SQLFORM(db.operaciones_logisticas, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)
