# -*- coding: utf-8 -*-

@auth.requires(auth.has_membership('root') or auth.has_membership('administrador'))
def index():
    """
    Muestra usuarios registrados
    """
    users = db(db.auth_user).select()
    return dict(users=users)


def add():
    """
    Agregar un usuario al sistema
    """
    group = request.vars.group
    group_id = db(db.auth_group.role == group).select().first().id
    form = SQLFORM(db.auth_user, submit_button=T('Submit'))
    form[0].insert(-1, TR(LABEL('Verificar contraseña:'),
                          INPUT(_name='password2',
                                _type='password',
                                requires=[
                                    IS_NOT_EMPTY(error_message='Campo obligatorio'),
                                    CRYPT()]
                            )))

    if form.accepts(request.vars, session, dbio=False):
        if form.vars.password != form.vars.password2:
            response.flash = 'Las contraseñas no coinciden'
        else:
            db.auth_user.insert(
                    username=form.vars.username,
                    first_name=form.vars.first_name,
                    last_name=form.vars.last_name,
                    email=form.vars.email,
                    password=form.vars.password)
            last_user = db(db.auth_user.username == form.vars.username).select().first()
            auth.add_membership(group_id, last_user.id)
            session.flash = 'Nuevo usuario creado'
            redirect(URL('users', 'index'))
        
    return dict(form=form)
    
