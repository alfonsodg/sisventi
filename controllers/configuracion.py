# -*- coding: utf-8 -*-

restricciones = True


@auth.requires(restricciones)
def data():
    return dict(form=crud())


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
    grid = webgrid.WebGrid(crud)
    grid.datasource = db(db.tipos_cambio).select()
    grid.pagesize = 20
    #grid.fields = ['db.catmod.id', 'db.catmod.nombre', 'db.catmod.posicion']
    #grid.filters = ['db.catmod.catmod', 'db.catmod.nombre']
    return dict(grid=grid())


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
    grid = webgrid.WebGrid(crud)
    grid.datasource = db(db.directorio).select()
    grid.pagesize = 10
    grid.filter_query = lambda f,v: f==v
    return dict(grid=grid())
    #directorios = db(db.directorio).select()
    #return dict(directorios=directorios)


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
def formas_pago():
    """
    Muestra las configuraciones de las formas de pago
    """
    grid = webgrid.WebGrid(crud)
    grid.datasource = db(db.formas_pago).select()
    grid.pagesize = 20
    #grid.fields = ['db.catmod.id', 'db.catmod.nombre', 'db.catmod.posicion']
    #grid.filters = ['db.catmod.catmod', 'db.catmod.nombre']
    return dict(grid=grid())


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
def maestro():
    """
    Muestra las configuraciones de los productos
    """
    producto = request.vars.producto
    rows = []
    form = SQLFORM.factory(
        Field('producto', 'string', label='Producto', default=producto,widget = SQLFORM.widgets.autocomplete(
            request, db.maestro.alias, mode=1)),
        )
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page = 0
    if form.accepts(request.vars, session):
        session.prod_mae = form.vars.producto
        items_per_page=20
        limitby=(page*items_per_page,(page+1)*items_per_page+1)
        rows=db(db.maestro.alias.contains(producto)).select(db.maestro.ALL,limitby=limitby)
    return dict(form=form,rows=rows,page=page,items_per_page=items_per_page)


@auth.requires(restricciones)
def filtrar_productos():
    """
    Muestra las configuraciones de los productos
    """
    redirect(URL('data/search/maestro/'))
    #form = crud.search(db.maestro)
    #grid = webgrid.WebGrid(crud)
    #grid.datasource = db(db.maestro)
    #grid.pagesize = 20
    #grid.fields = ['db.catmod.id', 'db.catmod.nombre', 'db.catmod.posicion']
    #grid.filters = ['db.catmod.catmod', 'db.catmod.nombre']
    return dict()


@auth.requires(restricciones)
def productos_agregar():
    """
    Agregar nuevo registro a 'maestro'
    """
    form = SQLFORM(db.maestro, fields=['codbarras','genero','empaque',
        'catmod','precio','nombre','descripcion','alias','unidad_medida',
        'unidad_medida_valor', 'estado'], submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro Ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def productos_modificar_almacen():
    """
    Agregar nuevo registro a 'maestro'
    """
    producto = request.vars.producto
    form = SQLFORM.factory(
        Field('producto', 'integer', label='Producto', widget = SQLFORM.widgets.autocomplete(
     request, db.maestro.alias, id_field=db.maestro.id, mode=1,
     filterby=db.maestro.genero, filtervalue='1')),
        )
    form2 = SQLFORM(db.maestro, producto, fields=['codbarras','genero','empaque',
            'catmod','precio','nombre','descripcion','alias','unidad_medida',
            'unidad_medida_valor', 'estado'], submit_button='Modificar')
    if form.accepts(request.vars, session, formname='form_bas'):
        session.prod = form.vars.producto
        #record = db.maestro(session.prod)# or redirect(URL('index'))
    if form2.accepts(request.vars, session, formname='form_aux'):
            response.flash = 'Registro Modificado'
    return dict(form=form, form2=form2)


@auth.requires(restricciones)
def productos_modificar_ventas():
    """
    Agregar nuevo registro a 'maestro'
    """
    producto = request.vars.producto
    form = SQLFORM.factory(
        Field('producto', 'integer', label='Producto', widget = SQLFORM.widgets.autocomplete(
     request, db.maestro.alias, id_field=db.maestro.id, mode=1,
     filterby=db.maestro.genero, filtervalue='2')),
        )
    form2 = SQLFORM(db.maestro, producto, fields=['codbarras','genero','empaque',
            'catmod','precio','nombre','descripcion','alias','unidad_medida',
            'unidad_medida_valor', 'estado'], submit_button='Modificar')
    if form.accepts(request.vars, session, formname='form_bas'):
        session.prod = form.vars.producto
        #record = db.maestro(session.prod)# or redirect(URL('index'))
    if form2.accepts(request.vars, session, formname='form_aux'):
            response.flash = 'Registro Modificado'
    return dict(form=form, form2=form2)


@auth.requires(restricciones)
def creacion_recetas():
    """
    Agregar nueva receta
    """
    session.prod_vta = request.vars.prod_venta
    session.prod_alm = request.vars.prod_almacen
    form = SQLFORM.factory(
        Field('prod_venta', 'integer', requires=IS_NOT_EMPTY(), default=session.prod_vta,
            label='Producto Padre', widget = SQLFORM.widgets.autocomplete(
            request, db.maestro.alias, id_field=db.maestro.id, mode=1,
            filterby=db.maestro.genero, filtervalue='2')),
        Field('cantidad', 'double', requires=IS_NOT_EMPTY(), default=''),
        #Field('prod_almacen', 'integer', requires=IS_NOT_EMPTY(), default=session.prod_alm,
        #    label='Producto Hijo', widget = SQLFORM.widgets.autocomplete(
        #    request, db.maestro.alias, id_field=db.maestro.id, mode=1,
        #    filterby=db.maestro.genero, filtervalue='1'))
        )
    if form.accepts(request.vars, session):
        session.prod_vta = form.vars.prod_venta
        session.prod_alm = form.vars.prod_almacen
        session.cantidad = form.vars.cantidad
        #db.recetas.insert(codbarras_padre=session.prod_vta, codbarras_hijo=session.prod_alm,
        #    cantidad=session.cantidad)
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
    grid = webgrid.WebGrid(crud)
    grid.datasource = db(db.recetas).select()
    grid.pagesize = 20
    #grid.fields = ['db.catmod.id', 'db.catmod.nombre', 'db.catmod.posicion']
    #grid.filters = ['db.catmod.catmod', 'db.catmod.nombre']
    return dict(grid=grid())


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
    grid = webgrid.WebGrid(crud)
    grid.datasource = db(db.condiciones_comerciales).select()
    grid.pagesize = 10
    grid.filter_query = lambda f,v: f==v
    return dict(grid=grid())


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
def documentos_comerciales():
    """
    Muestra las configuraciones para los documentos comerciales
    """
    grid = webgrid.WebGrid(crud)
    grid.datasource = db(db.documentos_comerciales).select()
    grid.pagesize = 20
    grid.crud_function = 'data'
    grid.fields = ['documentos_comerciales.modo', 'documentos_comerciales.documento',
        'documentos_comerciales.nombre', 'documentos_comerciales.correlativo',
        'documentos_comerciales.port', 'documentos_comerciales.layout']
    #grid.fields = ['db.empaques.empaque', 'db.empaques.nombre', 'db.empaques.posicion']
    #grid.filters = ['db.catmod.catmod', 'db.catmod.nombre']
    return dict(grid=grid())


@auth.requires(restricciones)
def documentos_comerciales_agregar():
    """
    Agregar nuevo registro a Documentos Comerciales
    """
    form = SQLFORM(db.documentos_comerciales, submit_button='Aceptar')
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
    grid = webgrid.WebGrid(crud)
    grid.datasource = db(db.empaques).select()
    grid.pagesize = 20
    grid.crud_function = 'data'
    #grid.fields = ['db.empaques.empaque', 'db.empaques.nombre', 'db.empaques.posicion']
    #grid.filters = ['db.catmod.catmod', 'db.catmod.nombre']
    return dict(grid=grid())


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
    grid = webgrid.WebGrid(crud)
    grid.datasource = db(db.unidades_medida).select()
    grid.pagesize = 20
    #grid.fields = ['db.catmod.id', 'db.catmod.nombre', 'db.catmod.posicion']
    #grid.filters = ['db.catmod.catmod', 'db.catmod.nombre']
    return dict(grid=grid())


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
    grid = webgrid.WebGrid(crud)
    grid.datasource = db(db.generos).select()
    grid.pagesize = 20
    #grid.fields = ['db.catmod.id', 'db.catmod.nombre', 'db.catmod.posicion']
    #grid.filters = ['db.catmod.catmod', 'db.catmod.nombre']
    return dict(grid=grid())
    #generos = db(db.generos).select()
    #return dict(generos=generos)


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
    grid = webgrid.WebGrid(crud)
    grid.datasource = db(db.operaciones_logisticas).select()
    grid.pagesize = 20
    #grid.fields = ['db.catmod.id', 'db.catmod.nombre', 'db.catmod.posicion']
    #grid.filters = ['db.catmod.catmod', 'db.catmod.nombre']
    return dict(grid=grid())


@auth.requires(restricciones)
def operaciones_logisticas_agregar():
    """
    Agregar nuevo registro a 'operaciones_logisticas'
    """
    form = SQLFORM(db.operaciones_logisticas, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def catmod():
    """
    Muestra las configuraciones para categoria modo
    """
    grid = webgrid.WebGrid(crud)
    grid.datasource = db(db.catmod).select()
    grid.pagesize = 20
    #grid.fields = ['db.catmod.id', 'db.catmod.nombre', 'db.catmod.posicion']
    #grid.filters = ['db.catmod.catmod', 'db.catmod.nombre']
    return dict(grid=grid())


@auth.requires(restricciones)
def catmod_agregar():
    """
    Agregar nuevo registro a 'catmod'
    """
    form = SQLFORM(db.catmod, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def areas():
    """
    Muestra las configuraciones para las areas
    """
    areas = db(db.areas).select()
    return dict(areas=areas)


@auth.requires(restricciones)
def areas_agregar():
    """
    Agregar nuevo registro a 'areas'
    """
    form = SQLFORM(db.areas, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def backup():
    """
    Muestra las configuraciones para los backups
    """
    backups = db(db.backup).select()
    return dict(backups=backups)


@auth.requires(restricciones)
def backup_agregar():
    """
    Agregar nuevo registro a 'backups'
    """
    form = SQLFORM(db.backup, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def bancos():
    """
    Muestra las configuraciones para los bancos
    """
    bancos = db(db.bancos).select()
    return dict(bancos=bancos)


@auth.requires(restricciones)
def bancos_agregar():
    """
    Agregar nuevo registro a 'bancos'
    """
    form = SQLFORM(db.bancos, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)


@auth.requires(restricciones)
def clientes_preferentes():
    """
    Muestra las configuraciones para los clientes preferentes
    """
    clientes = db(db.clientes_preferentes).select()
    return dict(clientes=clientes)


@auth.requires(restricciones)
def clientes_preferentes_agregar():
    """
    Agregar nuevo registro a 'clientes_preferentes'
    """
    form = SQLFORM(db.clientes_preferentes, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)

@auth.requires(restricciones)
def productos_almacen():
    """
    Agregar nuevo registro a 'clientes_preferentes'
    """
    form = SQLFORM(db.clientes_preferentes, submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'Registro ingresado'
    return dict(form=form)
    
