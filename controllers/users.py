# coding: utf8
# try something like
def index(): return dict(message="hello from users.py")

# -*- coding: utf-8 -*-
@auth.requires(auth.has_membership('root') or auth.has_membership('administrador'))
def index():
    users = db(db.auth_user).select()
    return dict(users=users)

    
    
