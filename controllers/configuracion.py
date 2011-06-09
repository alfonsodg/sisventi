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
    return dict(form=form)
