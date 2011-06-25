#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SISVENTI - POS module
"""

#####
#Call external functions.
#####

import curses  # manages the windows
import time  # manages the time
import os  # manages the os
import MySQLdb  # manages the MySQL DB
import sys
import crypt
import re
import types
import signal
import fpformat
#import locale
import thread
import smtplib
import md5
import logging
#import tempfile
import pdb
from curses import panel
#from curses import textpad
#from types import *
#####

#####
signal.signal(signal.SIGINT,  signal.SIG_IGN)
signal.signal(signal.SIGTSTP,  signal.SIG_IGN)
signal.signal(signal.SIGABRT,  signal.SIG_IGN)
#####

logging.basicConfig(filename='sisventi.log', level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s')

#####
#Read the db.cfg file (variables for assign the POS and MySQL DB values)
#####
try:
    in_file = open("data.cfg", "r")  # Opens the file
    params = in_file.read().splitlines()
    pos_num = params[0]  # When a value is assigned,
            #is added the '\n' (non-visible character),  then we omit it
    caja_num = params[1]
    print_port = params[2]
    host = params[3]
    database = params[4]
    user = params[5]
    pswd = params[6]
    n_serie = params[7]
    debug_mode = params[8]
    in_file.close()  #Close the file
except IOError:
    msg = "Error al abrir el archivo de configuracion!!!!"
    logging.debug("Main: %s" % msg)
    sys.exit()
#####

#####
#Initialize Variables and Functions
#####
try:
    CONDB = MySQLdb.connect(db=database, host=host,
        user=user, passwd=pswd)  #Starts the MySQL DB connection
except Exception, error:
    msg = "Error al conectarse con la base de datos"
    logging.debug("Database: %s" % msg)
    sys.exit()
##DB Conex (cursor)
curs = CONDB.cursor()
##Start with curses
stdscr = curses.initscr()  # Initialize the call to the curses function
curses.start_color()  # Initialize the color access
curses.init_pair(1,  curses.COLOR_BLACK,  curses.COLOR_WHITE)
# Assigns the color to the screen
curses.noecho()  # No returns a  character after a keypress
stdscr.leaveok(0)  # Reduces cursor movement
maxy, maxx = stdscr.getmaxyx()  # Obtains the screen dimensions
#curses.cbreak() Read a character one by one
#stdscr.keypad(1) Recognition of all the keys
#curses.curs_set(0)Assigns an invisible cursor (values goes from 0 to 2)
#curses.mousemask(curses.ALL_MOUSE_EVENTS) Calls to the detection
# of mouse events (moves and clicks)
##Setting locale
#loc = locale.setlocale(locale.LC_ALL, '')

#####
#py = 0
#cantidad = 0
#total = 0.0
#a = 0
nodoc = 0
posy = 1
cnt = 0
#valtot = 0.00
#y = ''
modo_imp = ''
impuestos = {}
modmon = ''
moneda = ''
tipo_cambio = ''
gaveta = ''
empresa = ''
tipo_servicio = ''
servidor_smtp = ''
from_smtp = ''
to_smtp = ''
consumo_alerta = ''
dia_alerta = ''
hora_max = ''
datos_modo = ''
stock_alerta = ''
pos_modo = ''
modo_decimal = ''
modo_control = ''
modo_almacen = ''
genero_producto = ''
almacen_key = ''
almacen = ''
moneda_aux = ''
nombre_usuario = 'I'
doc_cabecera = ''
doc_pie = ''
ctrlprods = {}


#####
#Checks the proper resolution.  We need al least,
#80 characters for 24 lines
#####
if maxy < 24 or maxx < 80:
    curses.echo()
    curses.endwin()
    print "Error!....."
    print "Resolution Error"
    print "Needed at least:"
    print "80 chars x 24 lines"
    sys.exit()
#####


def configuration():
    """
    Configuration load
    """
    global doc_cabecera, doc_pie, modo_imp, impuestos, modmon, moneda
    global tipo_cambio, gaveta, empresa, tipo_servicio, servidor_smtp
    global from_smtp, to_smtp, consumo_alerta, dia_alerta, hora_max
    global datos_modo, stock_alerta, pos_modo, modo_decimal
    global modo_control, modo_almacen, genero_producto, almacen_key
    global almacen, moneda_ux
    fecha_act = time.strftime("%Y-%m-%d")
    sql = """select '', '', modo_impuesto, impuestos,
        modo_moneda, moneda, money_drawer, empresa, tipo_servicio,
        servidor_smtp, from_smtp, to_smtp, consumo_alerta, dia_alerta,
        hora_max, datos_modo, stock_alerta, pos_modo, modo_decimal,
        modo_control, modo_almacen, genero_producto, almacen_key,
        almacen, moneda_aux from pos_configuracion where codigo = '%s'
        and caja = %s""" % (pos_num, caja_num)
    cnt, rso = query(sql, 0)
    if cnt == 0:
        curses.echo()
        curses.endwin()
        msg = "DB Error!..... Parametros de POS errados o inexistentes"
        logging.debug("Database: %s" % msg)
        sys.exit()
    doc_cabecera = ""
    doc_pie = ""
    modo_imp = rso[2]
    impuestos = dict([(imp.split(":")[1], float(imp.split(":")[0])) 
        for imp in rso[3].split(",")])
#    for parte in rso[3].split(','):
#        temp = parte.split(':')
#        impuestos[temp[1]] = temp[0]
    modmon = rso[4]
    moneda = rso[5]
    gaveta = rso[6]
    empresa = rso[7]
    tipo_servicio = str(rso[8])
    servidor_smtp = str(rso[9])
    from_smtp = str(rso[10])
    to_smtp = str(rso[11])
    consumo_alerta = str(rso[12])
    dia_alerta = str(rso[13])
    hora_max = str(rso[14])
    datos_modo = str(rso[15])
    stock_alerta = str(rso[16])
    pos_modo = str(rso[17])
    modo_decimal = str(rso[18])
    modo_control = str(rso[19])
    modo_almacen = str(rso[20])
    genero_producto = str(rso[21])
    almacen_key = str(rso[22])
    almacen = str(rso[23])
    moneda_aux = str(rso[24])
    sql = """select valor from tipos_cambio where fecha = '%s'
        or fecha = '0000-00-00' order by fecha
        desc limit 1""" % (fecha_act)
    cnt_1, rso_1 = query(sql, 0)
    if cnt_1 == 0:
        msg = """Advertencia: No existe Tipo de Cambio Definido"""
        dicotomic_question(msg)
        logging.debug("Database: %s" % msg)
        tipo_cambio = 1
    else:
        tipo_cambio = rso_1[0]
#        if rso_1[1] is None:
#            fecha_cambio='0000-00-00'
#        else:
#            fecha_cambio=rso_1[1]
    return


def point_programs(fecha, n_doc_base, total):
    """
    Points program
    """
    cty = 3
    ctx = 40
    cpy = (maxy - cty) / 2
    cpx = (maxx - ctx) / 2
    paning = make_panel(curses.COLOR_WHITE, cty, ctx, cpy, cpx)
    modo = ''
    try:
        sql = """select codigo, nombre from programas_configuracion
            order by posicion"""
        cnt, rso = query(sql)
        if cnt > 0:
            programa, nombre = list_selection(rso, 'Programa')
            nombre = ''
            if programa == 'Anular':
                return ''
            else:
                sql = """select equivalencia, mensaje, modo, longitud
                    from programas_configuracion where
                    codigo = '%s'""" % (programa)
                cnt, rso = query(sql, 0)
                if cnt > 0:
                    equivalencia = float(rso[0])
                    mensaje = str(rso[1])
                    modo = int(rso[2])
                    longitud = int(rso[3])
                else:
                    return ''
                while 1:
                    data_num = data_input('Tarjeta', paning, 20)
                    if data_num == 'Anular':
                        resp = dicotomic_question('Esta seguro?')
                        if resp == 'si':
                            return ''
                    else:
                        if len(data_num) == longitud or longitud == 0:
                            linea = "No de Tarjeta es %s ?" % (data_num)
                            resp = dicotomic_question(linea)
                            if resp == 'si':
                                break
                        else:
                            pass
                if modo == 0:
                    puntos = round(total / equivalencia, 0)
                elif modo == 1:
                    puntos = round(total / equivalencia, 1)
                elif modo == 2:
                    puntos = round(total / equivalencia, 2)
                else:
                    return ''
                mensaje = "%s:%s" % (mensaje, puntos)
                tiempo = time.strftime("%Y-%m-%d %H:%M:%S")
                sql = """insert into programas_registros (tiempo, 
                    fecha, programa, n_doc_base, codigo,
                    total_asignado, total_bruto) values ('%s', '%s',
                    '%s', '%s', '%s', '%s', '%s')""" % (tiempo, fecha,
                    programa, n_doc_base, data_num, puntos, total)
                curs.execute(sql)
                return mensaje
        else:
            return ''
    except Exception, error:
        logging.debug("PointProgram:%s" % error)
        return ''


def keyboard_definition(atajo=''):
    """
    Keyboard definition
    """
    if atajo == '':
        return 'Anular'
    codigo = ''
#    descripcion = ''
    sub_codigo = ''
#    sub_descripcion = ''
#    valor = []
    temporal = {}
    producto = {}
    codigo = {}
    sql = """select pos.denominacion_padre from maestro_pos pos
        where pos.atajo = '%s' order by pos.denominacion_padre
        desc limit 1""" % (atajo)
    cuenta, resultado = query(sql, 0)
    if cuenta > 0:
        titulo = resultado[0]
    else:
        return 'Anular'
    sql = """select distinct(pos.codbarras_padre),
        if(pos.alias_padre = '', concat(upper(mae.nombre), ' ',
        upper(mae.descripcion)), pos.alias_padre) as padre
        from maestro_pos pos left join maestro mae on
        mae.codbarras = pos.codbarras_padre where pos.atajo = '%s'
        order by pos.posicion_padre, padre""" % (atajo) 
    cuenta, resultado = query(sql)
    if cuenta > 0:
        codigos = opciones_cnt(resultado, 0, titulo)
        if codigos == 'Anular':
            return codigos
    sub_factor = 0
    for codigo in codigos:
        sql = """select distinct(pos.nivel_hijo), pos.denominacion_hijo,
            mae.aux_num_data, pos.modo_hijo from maestro_pos pos
            left join maestro mae on mae.codbarras = pos.codbarras_padre
            where pos.atajo = '%s' and pos.codbarras_padre = '%s'
            and pos.denominacion_hijo != '' order by pos.nivel_hijo,
            pos.denominacion_hijo desc""" % (atajo, codigo)
        cuenta, resultado = query(sql)
        if cuenta > 0:
            temporal = {}
            for parte in resultado:
                valor_sf = round(float(parte[2]) * float(parte[3]), 2)
                if valor_sf == 0:
                    valor_sf = 1
                sub_factor = round(float(codigos[codigo][1]) * 
                    valor_sf, 2)
                sub_nivel = parte[0]
                sub_titulo = "%s:%s" % (parte[1], sub_factor)
                sql = """select pos.codbarras_hijo, 
                    if(pos.alias_hijo = '', concat(upper(ma2.nombre), 
                    ' ', upper(ma2.descripcion)), pos.alias_hijo)
                    as hijo from maestro_pos pos left join maestro ma2
                    on ma2.codbarras = pos.codbarras_hijo where
                    pos.atajo = '%s' and pos.codbarras_padre = '%s' and
                    pos.nivel_hijo = '%s' and pos.codbarras_hijo != ''
                    order by pos.codbarras_hijo, pos.posicion_hijo, 
                    hijo""" % (atajo, codigo, sub_nivel)
                cuenta_1, resultado_1 = query(sql)
                if cuenta_1 > 1:
                    while 1:
                        cnt_sub = 0
                        sub_codigos = opciones_cnt(resultado_1, 0,
                            sub_titulo)
                        if sub_codigos == 'Anular':
                            return sub_codigos
                        for sub_codigo in sub_codigos:
                            temporal[sub_nivel] = {}
                            temporal[sub_nivel] = sub_codigos
                            cnt_sub += sub_codigos[sub_codigo][1]
                        if cnt_sub == sub_factor:
                            break
                elif cuenta_1 == 1:
                    temporal[sub_nivel] = {}
                    temporal[sub_nivel][resultado_1[0][0]
                                    ] = resultado_1[0][1], sub_factor
        producto[codigo] = {}
        producto[codigo]['nam'] = codigos[codigo][0]
        producto[codigo]['cnt'] = codigos[codigo][1]
        producto[codigo]['sub'] = temporal
    return producto


def make_panel(color, rows, cols, tly, tlx):
    """
    Panel creation
    """
    if tly + rows > maxy:
        tly = 0
    if tlx + cols > maxx:
        tly = 0
    win = curses.newwin(rows, cols, tly, tlx)
    pan = panel.new_panel(win)
    if curses.has_colors():
        if color == curses.COLOR_BLUE:
            fg = curses.COLOR_WHITE
        else:
#            fg = curses.COLOR_BLACK
#            bg = color
            curses.init_pair(color,  color,  curses.COLOR_BLACK)
            win.bkgdset(ord(' '),  curses.color_pair(color))
    else:
        win.bkgdset(ord(' '),  curses.A_BOLD)
    return pan


def authorization():
    """
    Authorization scheme
    """
    curses.curs_set(1)
    update_panels()
    pan = make_panel(curses.COLOR_WHITE, maxy, maxx, 0, 0)
    win = define_window(pan, borde=1)
    msg = "Modulo: Caja"
    posx = center_text(maxx, msg)
    win.addstr(1, posx, msg)
    win.addstr(maxy / 2 - 2, maxx / 2 - 10, "Usuario: ")
    curses.echo()
    while 1:
        update_panels()
        user_ing = win.getstr(maxy / 2 - 2, maxx / 2, 15)
        if user_ing != "":
            break
    win.addstr(maxy / 2 - 1, maxx / 2 - 10, "Password: ")
    curses.noecho()
    while 1:
        pwd_ing = win.getstr(maxy / 2 - 1, maxx / 2, 15)
        if pwd_ing != "":
            break
    pwd_ing = md5.new(pwd_ing).hexdigest()
    sql = """select user.first_name,user.last_name,level.group_id
        from auth_user user, auth_membership level where
        user.id=level.user_id and user.username='%s' and
        user.password='%s'""" % (user_ing, pwd_ing)
    cnt, rso = query(sql, 0)
    if cnt > 0:
        nombre = "%s %s" % (rso[0], rso[1])
        nombre = nombre[:20]
        nivel_usuario = rso[2]
        curses.curs_set(0)
        update_panels()
        return user_ing, nombre, nivel_usuario
    else:
        curses.curs_set(0)
        update_panels()
        return 0, 'I', 0


def pos_status():
    """
    POS status
    """
    pan = make_panel(curses.COLOR_WHITE, maxy, maxx, 0, 0)
    win = define_window(pan, 0, 1)
    sql = """select apertura, cierre from pos_administracion 
        where pv='%s' and caja=%s and estado=1
        order by id desc""" % (pos_num, caja_num)
    cuenta, resultado = query(sql, 0)
    if cuenta == 0:
        msg003 = 'La Caja NO se encuentra APERTURADA'
        win.addstr(10, 10, msg003)
        win.getch()
        win.erase()
        update_panels()
        return 'bad'
    else:
        win.erase()
        update_panels()
        return 'ok'


def pos_time(modo=1):
    """
    POS time status
    """
    sql = """select apertura, cierre, 
        adddate(apertura,  interval 1 day) as tiempo_max from
        pos_administracion where pv='%s' and caja=%s
        and estado=1""" % (pos_num, caja_num)
    cuenta, resultado = query(sql, 0)
    if cuenta == 0:
        apertura = 'Error'
        cierre = 'Error'
        tiempo_max = 'Error'
    else:
        apertura = resultado[0]
        cierre = resultado[1]
        tiempo_max = resultado[2]
        if cierre == '0000-00-00 00:00:00' or cierre is None:
            cierre = '2999-12-30 23:59:59'
    if modo == 1:
        return str(apertura), str(cierre)
    else:
        return str(apertura), str(cierre), str(tiempo_max)


def right_text(x, texto):
    """
    Right Text
    """
    texto = str(texto)
    posx = (x - len(texto)) - 1
    return posx


def center_text(x, texto):
    """
    Center Text
    """
    posx = (x / 2) - (len(texto) / 2)
    return posx


def define_window(pan, optam=1, opbox=1, opcaja=0, borde=0):
    """
    Define Windows
    """
    win = pan.window()
    if borde == 1:
        win.erase()
        win.border()
        return win
    if opbox == 1:
        win.erase()
        win.box()
    if opcaja == 1:
        win.box()
    update_panels()
    if optam == 1:
        tamy, tamx = win.getmaxyx()
        return win, tamy, tamx
    else:
        return win


def main_header(pan, nombre):
    """
    Window Header
    """
    pan.show()
    curses.curs_set(0)
    win, y, x = define_window(pan)
    pos_y = 0
    pos_x = center_text(x, empresa)
    win.addstr(2, pos_x, empresa)
    msg_tienda = 'Tienda: '
    msg_caja = 'Caja: '
    msg_cajero = 'Cajero: '
    linea = ("%s%s" % (msg_tienda, pos_num)).ljust(15) + ("%s%s" % 
        (msg_caja, caja_num)).ljust(10) + ("%s%s" % 
        (msg_cajero, nombre)).ljust(30) + ("%s" % (texto_dm)).ljust(20)
    win.addstr(5, 1, linea)
    update_panels()
    return


def window_body(*paneles):
    """
    Panels
    """
    for panel in paneles:
        curses.curs_set(0)
        panel.show()
        win, y, x = define_window(panel)
        update_panels()


def obch(pan, pcy=0, pcx=0, estado='n', tipo=0):
    """
    Get Character
    """
    win = pan.window()
    win.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    update_panels()
    while 1:
        if estado == 'v':
            curses.echo()
            curses.curs_set(1)
            update_panels()
        c = win.getch(pcy, pcx)
        curses.noecho()
        curses.curs_set(0)
        update_panels()
        if c == curses.KEY_F2:
            return 'f2'
        if c == curses.KEY_F10:
            return 'f10'
        if c == curses.KEY_F11:
            return 'f11'
        if c == curses.KEY_F12:
            return 'f12'
        if c == curses.KEY_UP and tipo == 0:
            return 'arriba'
        if c == curses.KEY_DOWN and tipo == 0:
            return 'abajo'
        if c == curses.KEY_LEFT  and tipo == 0:
            return 'izquierda'
        if c == curses.KEY_RIGHT  and tipo == 0:
            return 'derecha'
        if c == curses.KEY_BACKSPACE or c == 127:
            return 'backspace'
        if c == curses.KEY_IC  and tipo == 0:
            return 'insert'
        if c == curses.KEY_DC  and tipo == 0:
            return 'borrar'
        if c == curses.KEY_NPAGE  and tipo == 0:
            return 'spag'
        if c == curses.KEY_PPAGE  and tipo == 0:
            return 'ppag'
        if c == curses.KEY_END:
            return 'finp'
        if c == curses.KEY_HOME:
            return 'inicio'
        if c == 27:
            return 'escape'
        if c == 10:
            return 'enter'
        if ((c > 47 and c < 58) or (c > 64 and c < 91) or (c > 96 and
            c < 123) or c == 32 or c == 46 or c == 45 or 
            c == 209 or c == 241):
            return chr(c)
        # retorna numero o letra en mayusculas o minusculas


def producto_data(codbarras):
    """
    Product information
    """
    sql = """select if(length(mae.alias)>0, mae.alias,
        concat(mae.nombre, ' ', mae.descripcion)),
        round(mae.precio, 2) from maestro mae
        where mae.codbarras = '%s'""" % (codbarras)
    cnt, rso = query(sql, 0)
    nombre = rso[0]
    precio = round(rso[1], 2)
    return nombre, precio


def opciones_cnt(data, code=1, titulo='', modo=''):
    """
    Select Products
    """
    if modo == '':
        modo = modo_decimal
    if len(data) <= 0:
        return 'Anular'
    lineas = []
    temporal = []
    selec = {}
    for parte in data:
        datos = []
        datos.append(parte[0])
        datos.append(parte[1])
        if code == 1:
            texto = "%s->%s" % (parte[0], parte[1])
        else:
            texto = str(parte[1])
        tamano_x = len(texto) + 11
        temporal.append(tamano_x)
        lineas.append(datos)
    cuenta = len(lineas)
    sizex = max(temporal) + 2
    if sizex > maxx:
        sizex = maxx
    if cuenta >= (maxy - 2):
        sizey = maxy
        inic_y = 0
        term_y = maxy - 2
    else:
        sizey = cuenta + 2
        inic_y = 0  #Inicio de Array
        term_y = cuenta  #Termino de Array
    posy = screen_position(sizey, maxy)
    posx = screen_position(sizex, maxx)
    panel = make_panel(curses.COLOR_WHITE, sizey, sizex, posy, posx)
    win = define_window(panel, 0, 1)
    win.addstr(0, 1, titulo, curses.A_BOLD)
    sely = 1
    while 1:
        py = 0
        for cnt in range(inic_y, term_y):
            codigo = lineas[cnt][0]
            if code == 1:
                texto = "%s->%s" % (lineas[cnt][0], lineas[cnt][1])
            else:
                texto = str(lineas[cnt][1])
            contenido = texto
            py += 1
            condicion = curses.A_NORMAL
            win.addstr(py, 1, ' ' * (sizex - 2), condicion)
            if py == sely:
                condicion = curses.A_REVERSE
                valor1 = lineas[cnt][0]
                valor2 = lineas[cnt][1]
            cont_cnt = ''
            if codigo in selec:
                condicion = curses.A_REVERSE
                cont_cnt = "[%s]" % (selec[codigo][1])
            win.addstr(py, 1, contenido, condicion)
            px = right_text(sizex, cont_cnt)
            win.addstr(py, px, cont_cnt, condicion)
            update_panels()
        opcion = obch(panel)
        if opcion == 'arriba':
            if sely > 1:
                sely -= 1
            else:
                if inic_y > 0:
                    sely = 1
                    inic_y -= 1
                    term_y -= 1
        elif opcion == 'abajo':
            if sely < sizey - 2:
                sely += 1
            else:
                if term_y < cuenta:
                    sely = sizey - 1
                    inic_y += 1
                    term_y += 1
        elif opcion == 'escape':
            selec = 'Anular'
            break
        elif opcion == 'enter':
            if len(selec) == 0:
                selec[valor1] = valor2, ''
            break
        elif opcion == ' ':
            if valor1 in selec:
                del selec[valor1]
            else:
                selec[valor1] = valor2, ''
        elif (opcion >= '0' and opcion <= '9') or (
            opcion == '.' and modo == '1'):
            cantidad = opcion
            if valor1 in selec:
                cantidad = str(selec[valor1][1])
                cantidad += opcion
                if len(cantidad) >= 8:
                    cantidad = ''
            selec[valor1] = valor2, cantidad
        elif opcion == 'backspace':
            if valor1 in selec:
                cantidad = str(selec[valor1][1])
                cantidad = cantidad[:-1]
                selec[valor1] = valor2, cantidad
    if selec == 'Anular':
        opciones = selec
    else:
        opciones = {}
        for codigo in selec:
            if selec[codigo][1] == '':
                opciones[codigo] = selec[codigo][0], 1.0
            else:
                opciones[codigo] = selec[codigo][0], float(
                    selec[codigo][1])
    return opciones


def white_spaces(x):
    """
    Blank Spaces
    """
    x -= 2
    espac = ' ' * x
    return espac


def clear_screen(modo=1, *paneles):
    """
    Clear Window
    """
    for panel in paneles:
        win = define_window(panel, borde=1)
        win.erase()
        if modo == 1:
            panel.hide()
        update_panels()
    return


def windows_printing(pan2, pan3, pan6, pan4, pan5, pan8, pan7,
    var_y=0):
    """
    Windows Printing
    """
    data = ctrlprods
    win2, y2, x2 = define_window(pan2)
    win3, y3, x3 = define_window(pan3)
    win6, y6, x6 = define_window(pan6)
    win4, y4, x4 = define_window(pan4)
    win5, y5, x5 = define_window(pan5)
    win8, y8, x8 = define_window(pan8)
    win7, y7, x7 = define_window(pan7)
    for z in range(1, y2 - 1):
        win2.addstr(z, 1, str(white_spaces(x2)))
        win3.addstr(z, 1, str(white_spaces(x3)))
        win4.addstr(z, 1, str(white_spaces(x4)))
        win6.addstr(z, 1, str(white_spaces(x6)))
        win5.addstr(1, 1, str(white_spaces(x5)))
        win8.addstr(1, 1, str(white_spaces(x8)))
        win7.addstr(1, 1, str(white_spaces(x7)))
    update_panels()
    posicion = {}
    for codigo in data:
        pos_y = int(data[codigo]['pos'])
        posicion[pos_y] = codigo
    elementos = posicion.keys()
    elementos.sort()
    pos_y = 0
    elem_y_min = 1 + var_y
    elem_y_max = elem_y_min + 11
    cnt_y = 0
    for dato in elementos:
        codigo = posicion[dato]
        cantidad = float(data[codigo]['cnt'])
        precio = float(data[codigo]['prc'])
        descuento = float(data[codigo]['dsc'])
        producto = str(data[codigo]['nam'])
        producto = producto[:38]
        sub_productos = data[codigo]['sub']
        cnt_y += 1
        if cnt_y >= elem_y_min and cnt_y <= elem_y_max:
            pos_y += 1
            sub_total = float(cantidad * precio)
            item_precio = round(sub_total - ((sub_total * descuento) /
                100), 2)
            px4 = right_text(x4, item_precio)
            px2 = right_text(x2, cantidad)
            px6 = right_text(x6, precio)
            px7 = right_text(x7, descuento)
            win2.addstr(pos_y, px2, str(cantidad))
            win3.addstr(pos_y, 1, str(producto))
            win6.addstr(pos_y, px6, str(precio))
            win7.addstr(pos_y, px7, str(descuento))
            win4.addstr(pos_y, px4, str(item_precio))
            if len(sub_productos) > 0:
                sub_datos = sub_productos
                sub_orden = sub_datos.keys()
                sub_orden.sort()
                for sub_dato in sub_orden:
                    for sub_valor in sub_datos[sub_dato]:
                        producto = sub_datos[sub_dato][sub_valor][0]
                        producto = producto[:38]
                        cantidad = sub_datos[sub_dato][sub_valor][1]
                        cnt_y += 1
                        if cnt_y >= elem_y_min and cnt_y <= elem_y_max:
                            pos_y += 1
                            px2 = right_text(x2, cantidad)
                            win2.addstr(pos_y, px2, str(cantidad))
                            win3.addstr(pos_y, 1, "** %s" % (producto))
    if cnt_y > elem_y_max:
        win3.addstr(elem_y_max + 1, 0, "(>)")
    for cupon in cupones:
        pos_y += 1
        if pos_y >= 17:
            break
        dsc_cupon = "%s-%s" % (cupon, cupones[cupon]['nam'])
        valor = cupones[cupon]['cnt'] * cupones[cupon]['mnt']
        cantidad = cupones[cupon]['cnt']
        monto = cupones[cupon]['mnt']
        referencia = cupones[cupon]['ref']
        px2 = right_text(x2, cantidad)
        win2.addstr(pos_y, px2, str(cantidad))
        px4 = right_text(x4, "-%s" % (valor))
        win3.addstr(pos_y, 1, "-->%s" % (dsc_cupon))
        win4.addstr(pos_y, px4, "-%s" % (valor))
        px6 = right_text(x6, "-%s" % (monto))
        win6.addstr(pos_y, px6, "-%s" % (monto))
        pos_y += 1
        win3.addstr(pos_y, 1, "   *%s" % (referencia))
    update_panels()
    px5 = right_text(x5, float_chars(total))
    if modmon == 3:
        cambio = round(total / tipo_cambio, 2)
        px8 = right_text(x8, float_chars(cambio))
        win5.addstr(1, px5-5, moneda)
        win5.addstr(1, px5-1, float_chars(total))
        win8.addstr(1, px8-5, "$")
        win8.addstr(1, px8-1, float_chars(cambio))
    else:
        win5.addstr(1, px5-5, "$")
        win5.addstr(1, px5-1, float_chars(total))
    update_panels()
    return


def query(sql, ndat=1):
    """
    Database Query
    """
    if ndat == 5:
        try:
            curs.execute("START TRANSACTION")
            for query in sql:
                curs.execute(query)
            curs.execute("COMMIT")
            return 1
        except MySQLdb.Error,  error:
            curs.execute("ROLLBACK")
            dicotomic_question("""ERROR. INFORMACION NO 
                REGISTRADA.""")
            logging.debug("Query: %s" % error)
            return -1
    else:
        try:
            curs.execute(sql)
            cnt = curs.rowcount
            if ndat == 0:
                rso = curs.fetchone()
            else:
                rso = curs.fetchall()
            return cnt, rso
        except MySQLdb.Error,  error:
            logging.debug("Query: %s" % error)
            return -1, error.args[1]
        except Exception, error:
            logging.debug("Query: %s" % error)
            return -1, sql


def payment_process():
    """
    Payment Process
    """
    ty = 14
    tx = 70
    py = screen_position(ty, maxy)
    px = screen_position(tx, maxx)
    pan7 = make_panel(curses.COLOR_WHITE, ty, tx, py, px)
    win7, y7, x7 = define_window(pan7)
    msg007 = 'Forma de Pago'
    posx = center_text(x7, msg007)
    win7.addstr(1, posx, msg007, curses.A_BOLD)
    update_panels()
    medios_pago, vuelsol, vueldol = document_process()
    if medios_pago == 'Anular':
        return ('Anular', '', '', '', '', '')
    lineas = []
    mntsol = 0.0
    mntdol = 0.0
    for pago in medios_pago:
        cadena = """%s->%s/%s **""" % (
            medios_pago[pago][0], medios_pago[pago][1],
            medios_pago[pago][2])
        #str(medios_pago[pago][0])+"->"+
        #str(medios_pago[pago][1])+"/"+str(medios_pago[pago][2])+" **"
        lineas.append(cadena)
        mntsol += float(medios_pago[pago][1])
        mntdol += float(medios_pago[pago][2])
    cnt = 1
    cuenta_mp = len(medios_pago)
    elementos = []
    if cuenta_mp <= 2:
        parte = lineas[:2]
        elementos.append(' '.join(parte))
    elif cuenta_mp >= 3 and cuenta_mp <= 4:
        parte = lineas[:2]
        elementos.append(' '.join(parte))
        parte = lineas[2:4]
        elementos.append(' '.join(parte))
    elif cuenta_mp >= 5 and cuenta_mp <= 6:
        parte = lineas[:2]
        elementos.append(' '.join(parte))
        parte = lineas[2:4]
        elementos.append(' '.join(parte))
        parte = lineas[4:6]
        elementos.append(' '.join(parte))
    for linea in elementos:
        cnt += 1
        posx = center_text(x7, str(linea))
        win7.addstr(cnt, posx, str(linea))
    if ventaext == 1:
        tmp_compn = ndocext_detalle
        comprobante_id = doc_man
    else:
        comprobante_id, compr = document_selection(0)
        #pdb.set_trace()
        if comprobante_id != 'Anular':
            (t_pre, t_nod, t_pos, t_copia, t_compn, t_port,
                t_layout) = get_correlative(0, comprobante_id, 0, 1)
            if t_pre == 'Anular':
                return ('Anular', '', '', '', '', '')
        else:
            return ('Anular', '', '', '', '', '')
        msg008 = 'Documento de Venta'
        posx = center_text(x7, msg008)
        win7.addstr(5, posx, msg008, curses.A_BOLD)
        posx = center_text(x7, str(compr))
        win7.addstr(6, posx, str(compr))
        update_panels()
    nombre = ''
    docnum = ''    
    if t_compn == '1':
        ty = 3
        tx = 20
        py = screen_position(ty, maxy)
        px = screen_position(tx, maxx)
        pancl = make_panel(curses.COLOR_WHITE, ty, tx, py, px)
        msg009 = 'Cliente'
        posx = center_text(x7, msg009)
        win7.addstr(7, posx, msg009, curses.A_BOLD)
        update_panels()
        cli, tipdat = get_value_type(pancl)
        pancl.hide()
        if tipdat == 'entero':
            modo_cli = 0
            condicion = "doc_id like '%s%%'" % (cli)
        else:
            modo_cli = 1
            condicion = "nombre_corto like '%%%s%%'" % (cli.upper())
        sql = """select doc_id, nombre_corto from directorio where %s
            order by doc_id""" % (condicion)
        cnt, rso = query(sql)
        if cnt > 0:
            docnum, nombre = list_selection(rso)
            if docnum == 'insertar':
                nombre, docnum = costumer_process(nombre)
            elif docnum == 'agregar':
                nombre, docnum = costumer_process(cli, modo_cli)
            elif docnum == 'Anular':
                return ('Anular', '', '', '', '', '')
        else:
            nombre, docnum = costumer_process(cli, modo_cli)
        if nombre == 'Anular':
            return ('Anular', '', '', '', '', '')
        posx = center_text(x7, nombre)
        win7.addstr(8, posx, nombre)
        posx = center_text(x7, docnum)
        win7.addstr(9, posx, docnum)
        update_panels()
    msg010 = 'Operacion'
    posx = center_text(x7, msg010)
    win7.addstr(10, posx, msg010, curses.A_BOLD)
    update_panels()
    if len(medios_pago) <= 0:
        mntsol = total
        mntdol = 0.00
        vuelsol = 0.00
        vueldol = 0.00
    msg011 = 'Total '
    texto = """%s%s: %s  |  %s$: %s""" % (msg011, moneda, 
        float_chars(mntsol), msg011, float_chars(mntdol))
    posx = center_text(x7, texto)
    win7.addstr(11, posx, texto)
    msg012 = 'Vuelto '
    texto = """%s%s: %s  |  %s$: %s""" % (msg012, moneda,
        float_chars(vuelsol), msg012, float_chars(vueldol))
    posx = center_text(x7, texto)
    win7.addstr(12, posx, texto)
    update_panels()
    while 1:
        opcion = get_control_char(pan7)
        if opcion == 'escape':
            return ('Anular', '', '', '', '', '')
        else:
            return (medios_pago, comprobante_id, nombre, docnum,
                vuelsol, vueldol)


def float_chars(dato):
    """
    Float Chars
    """
    if type(dato) is types.FloatType:
        dato = round(dato, 2)
        dato = fpformat.fix(dato, 2)
        return str(dato)
    else:
        return str(dato)


def document_process():
    """
    Payment Options
    """
    #Variables
    divx = int(maxx)/3
    tot_loc = total
    tot_dol = round(total/tipo_cambio, 2)
    mnt_loc = total
    mnt_dol = round(total/tipo_cambio, 2)
    valor_tmp = ("%s" % (mnt_dol)).split('.')
    mnt_ful = float(valor_tmp[0])
    mnt_dif = (float(valor_tmp[1])*tipo_cambio)/100
    divx_1 = divx/2
    divx_2 = (divx/2)+divx
    tam_x = divx/2
    vlt_loc = 0.00
    vlt_dol = 0.00
    rec_loc = ''
    rec_dol = ''
    #Ventanas
    panel_1 = make_panel(curses.COLOR_WHITE, 10, divx, 1, divx_1)
    panel_2 = make_panel(curses.COLOR_WHITE, 4, divx, 5, divx_2)
    panel_3 = make_panel(curses.COLOR_WHITE, 4, divx, 1, divx_2)
    win_1 = define_window(panel_1, borde=1)
    win_2 = define_window(panel_2, borde=1)
    win_3 = define_window(panel_3, borde=1)
    #Ventana 1
    texto = ('Total %s :' % (moneda)).ljust(tam_x)+("%s" %
        float_chars(mnt_loc)).rjust(tam_x-2)
    win_1.addstr(1, 1, texto)
    texto = 'Total $ :'.ljust(tam_x)+("%s" %
        float_chars(mnt_dol)).rjust(tam_x-2)
    win_1.addstr(2, 1, texto)
    texto = 'Tipo Cambio :'.ljust(tam_x)+("%s" %
        float_chars(tipo_cambio)).rjust(tam_x-2)
    win_1.addstr(6, 1, texto)
    texto = '$ Completos :'.ljust(tam_x)+("%s" %
        float_chars(mnt_ful)).rjust(tam_x-2)
    win_1.addstr(7, 1, texto)
    texto = ('%s Diferencia :' % (moneda)).ljust(tam_x+2)+("%s" %
        float_chars(mnt_dif)).rjust(tam_x-5)
    win_1.addstr(8, 1, texto)
    update_panels()
    sql = """select forma_pago, nombre from formas_pago
        order by posicion, forma_pago"""
    cuenta, resultado = query(sql)
    metodos = opciones_cnt(resultado, 1, 'Forma de Pago', '1')
    if metodos == 'Anular':
        return 'Anular', '', ''
    mnt_sld = 0
    modo_fp = {}
    sql = """select forma_pago, modo, nombre from formas_pago
        order by posicion, forma_pago"""
    cuenta, resultado = query(sql)
    if cuenta > 0:
        for linea in resultado:
            modo_fp[linea[0]] = str(linea[1]), linea[2]
    for dato in metodos:
        if modo_fp[dato][0] != '1':
            mnt_sld += metodos[dato][1]
    if len(metodos) == 1:
        for dato in metodos:
            if modo_fp[dato][0] == '1':
                pass
            elif modo_fp[dato][0] == '2':
                pass
            else:
                metodos[dato] = modo_fp[dato][1], tot_loc, 0.0
                mnt_sld = tot_loc
    diferencia = 0
    mnt_sld = round(mnt_sld, 2)
    diferencia_mnt = tot_loc-mnt_sld
    if diferencia_mnt > 0:
        diferencia = 1
        saldo_dif = tot_loc-mnt_sld
        tot_loc = saldo_dif
        texto = "Cancelado".ljust(tam_x)+("%s" % float_chars(mnt_sld)
            ).rjust(tam_x-2)
        win_1.addstr(3, 1, texto)
        texto = "Pendiente".ljust(tam_x)+("%s" % float_chars(saldo_dif)
            ).rjust(tam_x-2)
        win_1.addstr(4, 1, texto)
        while 1:
            texto = "%s Recibido" % (moneda)
            rec_loc = linea_dato(texto, win_3, panel_3, rec_loc)
            if rec_loc == '':
                mnt_loc = tot_loc
                mnt_dol = 0.00
                break
            elif rec_loc == 'Anular':
                return 'Anular', '', ''
            try:
                rec_loc = float(rec_loc)
                if rec_loc >= tot_loc:
                    mnt_loc = rec_loc
                    mnt_dol = 0.00
                    rec_dol = 0.00
                    break
                else:
                    #Ventana 1
                    if rec_dol == '':
                        dol_tmp = 0
                    else:
                        dol_tmp = rec_dol
                    dif_1 = tot_loc-((dol_tmp*tipo_cambio)+rec_loc)
                    texto = ("Dif. %s :" % (moneda)).ljust(tam_x)+("%s"%
                        (float_chars(dif_1))).rjust(tam_x-2)
                    win_2.addstr(1, 1, texto)
                    update_panels()
                    msg = '$ Recibido '
                    rec_dol = linea_dato(msg, win_3, panel_3, 
                        rec_dol, 2)
                    if rec_dol == 'Anular':
                        return 'Anular', '', ''
                    try:
                        rec_dol = float(rec_dol)
                        operacion = (rec_dol*tipo_cambio)+rec_loc
                        if operacion >= tot_loc:
                            mnt_loc = rec_loc
                            mnt_dol = rec_dol
                            break
                        if rec_dol >= tot_dol:
                            mnt_loc = 0.00
                            mnt_dol = rec_dol
                            break
                        elif rec_dol < 1:
                            rec_loc = mnt_loc
                            rec_dol = 0.00
                        else:
                            rec_loc = round((tot_loc - (rec_dol *
                                tipo_cambio)) + ((rec_dol % 1) *
                                tipo_cambio), 2)
                            rec_dol = round(rec_dol-(rec_dol%1), 2)
                        dif_1 = tot_loc-((rec_dol*tipo_cambio)+rec_loc)
                        dif_2 = round((rec_dol*tipo_cambio), 2)
                        texto = ("Dif. %s :"%moneda).ljust(tam_x)+("%s"%
                            (float_chars(dif_1))).rjust(tam_x-2)
                        win_2.addstr(1, 1, texto)
                        texto = "Equiv. $ :".ljust(tam_x)+("%s"%
                            (float_chars(dif_2))).rjust(tam_x-2)
                        win_2.addstr(2, 1, texto)
                        update_panels()
                        win_3.addstr(2, len(msg)+3, ' '*10)
                        win_3.addstr(2, len(msg)+3, str(rec_dol))
                    except Exception, error:
                        rec_dol = 0.00
                        vlt_dol = 0.00
                        logging.debug("DocumentProcess: %s" % error)
            except Exception, error:
                rec_loc = mnt_loc
                vlt_loc = 0.00
                logging.debug("DocumentProcess: %s" % error)
    elif diferencia_mnt == 0:
        if tot_loc == 0:
            diferencia = 1
    else:
        alerta_modo = 1
        for dato in metodos:
            if modo_fp[dato][0] == '2':
                alerta_modo = 0
        if alerta_modo == 1:
            texto = "ALERTA: MONTO A COBRAR EXCEDENTE EN: " % (
                abs(diferencia_mnt))
            dicotomic_question(texto)
                #mnt_sld += metodos[dato][1]
    vlt_loc = 0.0
    vlt_dol = 0.0
    for dato in modo_fp:
        if modo_fp[dato][0] == '1':
            if diferencia == 1:
                vlt_loc = abs((mnt_loc+(mnt_dol*tipo_cambio))-tot_loc)
                vlt_dol = 0.00
                metodos[dato] = modo_fp[dato][1], mnt_loc, mnt_dol
        else:
            if dato in metodos:
                metodos[dato] = modo_fp[dato][1], metodos[dato][1], 0.0
    return metodos, vlt_loc, vlt_dol


def get_value_expresion(dato):
    """
    Data Type Conditionals
    """
    dato = str(dato)
    decimal = re.search('^\d+\.\d+$', dato)
    entero = re.search('^\d+$', dato)
    alfanumerico = re.search('^[a-zA-Z0-9]+$', dato)
    caracter = re.search('^\D+$', dato)
    if decimal:
        dato = float(decimal.group(0))
        dato = round(dato, 2)
        return dato, 'decimal'
    if entero:
        dato = entero.group(0)
        return dato, 'entero'
    if alfanumerico:
        dato = alfanumerico.group(0)
        return dato, 'alfanumerico'
    if caracter:
        dato = caracter.group(0)
        return dato, 'caracter'
    return 'nulo', 'nulo'


def get_control_char(pan, opciones={}):
    """
    Gets Key
    """
    control = {259: 'arriba', 258: 'abajo', 331: 'insert', 10: 'enter',
        27: 'escape'}
    for llave in control:
        if llave not in opciones:
            opciones[llave] = control[llave]
    win = pan.window()
    curses.noecho()
    win.keypad(1)
    while 1:
        c = win.getch()
        if c in opciones:
            return opciones[c]


def get_value_type(pan):
    """
    Get Object From List
    """
    win, y, x = define_window(pan)
    curses.curs_set(1)
    curses.echo()
    update_panels()
    while 1:
        linea = win.getstr(1, 1)
        valor, tipdat = get_value_expresion(linea)
        if tipdat == 'entero' and len(linea) > 4:
            curses.noecho()
            curses.curs_set(0)
            win.erase()
            update_panels()
            return linea, tipdat
        elif tipdat == 'alfanumerico' and len(linea) > 2:
            curses.noecho()
            curses.curs_set(0)
            win.erase()
            update_panels()
            return linea, tipdat


def list_selection(data, titulo='', key_val=0, dsc_val=1):
    """
    Select Element from a List
    """
    if len(data) <= 0:
        return 'Anular', 'Anular'
    lineas = []
    temporal = []
    for parte in data:
        datos = []
        datos.append(str(parte[key_val]))
        datos.append(str(parte[dsc_val]))
        #texto = "%s->%s" % (len(str(parte[key_val])), parte[dsc_val])
        texto = "%s::%s" % (parte[key_val], parte[dsc_val])
        temporal.append(texto)
        lineas.append(datos)
    cuenta = len(lineas)
    sizex = len(max(temporal)) + 2
    if sizex > maxx:
        sizex = maxx
    temporal = []
    if cuenta >= (maxy-2):
        sizey = maxy
        inic_y = 0
        term_y = maxy-2
    else:
        sizey = cuenta+2
        inic_y = 0  #Inicio de Array
        term_y = cuenta  #Termino de Array
    posy = screen_position(sizey, maxy)
    posx = screen_position(sizex, maxx)
    panel = make_panel(curses.COLOR_WHITE, sizey, sizex, posy, posx)
    win = define_window(panel, 0, 1)
    win.addstr(0, 1, titulo, curses.A_BOLD)
    sely = 1
    while 1:
        py = 0
        for cnt in range(inic_y, term_y):
            contenido = "%s::%s" % (lineas[cnt][0], lineas[cnt][1])
            py += 1
            condicion = curses.A_NORMAL
            win.addstr(py, 1, ' '*(sizex-2), condicion)
            if py == sely:
                condicion = curses.A_REVERSE
                valor1 = lineas[cnt][0]
                valor2 = lineas[cnt][1]
            win.addstr(py, 1, str(contenido), condicion)
            update_panels()
        opcion = obch(panel)
        if opcion == 'arriba':
            if sely > 1:
                sely -= 1
            else:
                if inic_y > 0:
                    sely = 1
                    inic_y -= 1
                    term_y -= 1
        elif opcion == 'abajo':
            if sely < sizey-2:
                sely += 1
            else:
                if term_y < cuenta:
                    sely = sizey-1
                    inic_y += 1
                    term_y += 1
        elif opcion == 'escape':
            valor1, valor2 = 'Anular', 'Anular'
            break
        elif opcion == 'enter':
            break
        elif opcion == 'insert':
            valor_tmp = valor1
            valor1, valor2 = 'insertar', valor_tmp
            break
        elif opcion == 'n':
            valor_tmp = valor1
            valor1, valor2 = 'agregar', valor_tmp
            break
    return valor1, valor2


def update_panels():
    """
    Update Panels
    """
    panel.update_panels()
    curses.doupdate()
    return


def screen_position(tam_win, tam_scr):
    """
    Windows Position
    """
    dato_scr = (tam_scr-tam_win) / 2
    return dato_scr


def costumer_process(cliente, modo=0):
    """
    Costumer Processing
    """
    sql = """select nombre_corto, tipo_doc, doc_id, ubigeo, direccion
        from directorio where doc_id = '%s' 
        order by doc_id""" % (cliente)
    cuenta, resultado = query(sql, 0)
    if cuenta > 0:
        nombre = resultado[0]
        tipo_doc = resultado[1]
        documento = resultado[2]
        distrito = resultado[3]
        direccion = resultado[4]
        modo_sql = 1
    else:
        if modo == 1:
            nombre = cliente
        else:
            nombre = ''
        tipo_doc = ''
        if modo == 1:
            documento = ''
        else:
            documento = cliente
        distrito = ''
        direccion = ''
        modo_sql = 0
    vacio = 1
    msg020 = 'Nombre: '
    msg021 = 'Tipo Doc.: '
    msg022 = 'Documento: '
    msg023 = 'Distrito: '
    msg024 = 'Direccion: '
    ty = 7
    tx = 70
    py = screen_position(ty, maxy)
    px = screen_position(tx, maxx)
    panel = make_panel(curses.COLOR_WHITE, ty, tx, py, px)
    win = define_window(panel, borde=1)
    while 1:
        nombre = linea_dato(msg020, win, panel, nombre, 1)
        if nombre == 'Anular':
            vacio = 0
            break
        if tipo_doc == '':
            sql = """select id, nombre, longitud from
                documentos_identidad"""
            cuenta, resultado = query(sql)
            if cuenta > 0:
                tipo_doc, tipo_doc_dscp = list_selection(resultado)
                if tipo_doc == 'Anular':
                    vacio = 0
                    break
        sql = """select longitud from documentos_identidad
            where id = '%s'""" % (tipo_doc)
        cuenta2, resultado2 = query(sql, 0)
        tipo_doc_long = int(resultado2[0])
        msg = "%s %s " % (msg021, tipo_doc)
        win.addstr(2, 1, msg)
        documento = linea_dato(msg022, win, panel, documento, 3)
        if documento == 'Anular':
            vacio = 0
            break
        distrito = linea_dato(msg023, win, panel, distrito, 4)
        if distrito == 'Anular':
            vacio = 0
            break
        direccion = linea_dato(msg024, win, panel, direccion, 5)
        if direccion == 'Anular':
            vacio = 0
            break
        if len(documento) == tipo_doc_long and len(nombre) > 4:
            resp = dicotomic_question('Guardar,  Esta Seguro?')
            if resp == 'si':
                break
    if vacio == 1:
        if modo_sql == 0:
            sql = """insert into directorio (nombre_corto, tipo_doc,
            doc_id, direccion) values ('%s', '%s', '%s', '%s')""" % (
            nombre, tipo_doc, documento, direccion)
        else:
            sql = """update directorio set nombre_corto = '%s',
            tipo_doc = '%s', direccion = '%s'  where
            doc_id = '%s'""" % (nombre, tipo_doc, direccion, documento)
        exe = curs.execute(sql)
        return nombre, documento
    else:
        return 'Anular', ''


def machine_id():
    """
    Hardware Identification
    """
    if n_serie == '':
        comando = os.popen('cat /proc/cpuinfo')
        ident = comando.read()
        comando.close()
        ident = "%s%s%s" % (pos_num, caja_num, ident)
        ident = crypt.crypt(ident, '0-9')
    else:
        ident = n_serie
    return ident


def final_process(vuelsol, vueldol, doccli, nomcli, dircli, refcli,
        telcli, texto1, texto2, texto3, norden, timeord):
    """
    Closes Sales Process / Prints Invoice
    """
    #Variables
    apertura, cierre = pos_time(1)
    if apertura == 'Error':
        return 'Anular'
    mntsol = 0.0
    mntdol = 0.0
    mensaje_programas = ''
    device_port = print_port
    cnt = 0
    sub_codex = {}
    doc_layout = ''
    fecha = time.strftime("%Y-%m-%d")
    fecha_hora = time.strftime("%Y-%m-%d %H:%M:%S")
    tx = 50  #Tamano de Preview
    px = (maxx-tx)/2
    ident = machine_id()  #No. Serie
    det_pagos = "|".join(["%s:%s" % (elem, medios_pago[elem][1]) 
        for elem in medios_pago])
    ##Vales y Cupones
    vales = "|".join(cupones.keys())
    temp = []
    for cupon in cupones:
        temp.append("|".join(cupones[cupon]['ref']))
    sellos = "|".join(temp) 
    ##Operaciones
    for pago in medios_pago:
        mntsol += float(medios_pago[pago][1])
        mntdol += float(medios_pago[pago][2])
    ##Correlativo de Documentos
    if ventaext != 1:
        (nodoc_prefijo, nodoc, nodoc_sufijo, doc_copia,
            doc_detalle, doc_port, doc_layout) = get_correlative(0,
            comprobante_id, 1, 1)
        if nodoc_prefijo == 'Anular':
            return 'Anular'
        device_port = doc_port
    elif ventaext == 1:
        nodoc = ndocext
        nodoc_prefijo = ndocext_pre
        nodoc_sufijo = ndocext_pos
        doc_copia = ndocext_copia
        doc_detalle = ndocext_detalle
        doc_layout = ndocext_layout
        device_port = ndocext_port
    ##Define plantilla de impresion
    if doc_layout == '':
        doc_layout = "default.txt"
    ##Apertura de gaveta
    if ventaext != 1:
        if gaveta == '':
            os.system("cat apertura | escpos > %s" % device_port)
        else:
            os.system("ls > /dev/%s" % gaveta)
    ##Programa de puntos
    mensaje_programas = point_programs(fecha, nodoc, total)
    ##Archivo Temporal
    nomarch = str(nodoc)+str(time.time())
    archivo = open(nomarch, 'w')
    plantilla = open(doc_layout).read()
    ##Funciones de Pantalla
    pan = make_panel(curses.COLOR_WHITE, maxy, tx, 0, px)
    #pan.top()
    win = define_window(pan, 0, 1)
    curses.curs_set(0)
    update_panels()
    dvar = {"ST":pos_num, "PB":caja_num, "DT":fecha_hora,
        "DA":fecha, "DF":"%s-%s-%s" % (nodoc_prefijo, nodoc,
        nodoc_sufijo), "DI":nodoc, "UI":codigo_usuario,
        "UN":nombre_usuario, "PI":",".join(medios_pago.keys()),
        "PM":",".join([elem[0] for elem in medios_pago.values()]),
        "PQ":[], "PN":[], "PA":[], "CI":nombre_cliente, "CN":id_cliente,
        "ST":total_neto, "FT":total, "MO":moneda, "M1R":mntsol,
        "M1B":vuelsol, "M2R":mntdol, "M2B":vueldol, "MA":moneda_aux,
        "SN":ident, "DT":msg_dist, "PP":mensaje_programas, "D1":norden,
        "D2":nomcli, "D3":dircli, "D4":refcli, "D5":telcli,
        "DX":comprobante_id}
    sql_layout = """insert into docventa (pv, caja, n_doc_prefijo,
        n_doc_base, n_doc_sufijo, estado, comprobante, cliente,
        cv_ing, codigo, precio, cantidad, sub_total_bruto,
        sub_total_impto, sub_total_neto, total, detalle_impto,
        total_neto, mntsol, mntdol, tiempo, vales, sello, data_1, imod,
        fecha_vta, medios_pago, sub_codbarras)
        values (%s)""" % (",".join(["'%s'" for ele in range(0,28)]))
    curses.echo()
    curses.endwin()
    for linea in format_list:
        sql = sql_layout % (pos_num, caja_num, nodoc_prefijo, nodoc,
            nodoc_sufijo, '1', comprobante_id, id_cliente,
            codigo_usuario, linea[1], linea[2], linea[3], linea[4],
            linea[5], linea[6], total, det_impto, total_neto, mntsol,
            mntdol, fecha_hora, vales, sellos, distribucion, ventaext,
            apertura[:10], det_pagos, '')
        print sql
    #print cupones
    #print medios_pago
    #print ctrlprods
    sys.exit()
    ##Impresion
    if ventaext == 0 and (debug_mode == '0' or debug_mode == ''):
        estad = os.system("cat %s > %s" % (nomarch, device_port))
        estad = os.system("cat corte | escpos > %s" % device_port)
        if doc_copia == '1':
            if device_port[5:9] == 'ttyS':
                time.sleep(6)
            estad = os.system("cat %s > %s" % (nomarch, device_port))
            estad = os.system("cat corte | escpos > %s" % device_port)
        if extra_print == '1':
            if device_port[5:9] == 'ttyS':
                time.sleep(6)
            estad = os.system("cat %s > %s" % (nomarch, device_port))
            estad = os.system("cat corte | escpos > %s" % device_port)
    else:
        estad = 1
    ##Archivo Temporal
    if debug_mode == '0' or debug_mode == '':
        os.remove(nomarch)
        #archivo.close()
            #if len(sub_productos) > 0:
                #for elemento in sub_productos:
                    #elementos = sub_productos[elemento]
                    #for sub_producto in elementos:
                        #sql = ''
                        #sql = "insert into operaciones_vta_aux(pv, caja, fecha_vta, n_doc_prefijo, n_doc_base, n_doc_sufijo, codbarras_padre, codbarras_auxiliar, cantidad_auxiliar) values "
                        #sql += "('"+str(pos_num)+"', '"+str(caja_num)+"', '"+str(apertura[:10])+"', '"+str(nodoc_prefijo)+"', '"+str(nodoc)+"', '"+str(nodoc_sufijo)+"', '"+str(x)+"', '"+str(sub_producto)+"', '"+str(elementos[sub_producto][1])+"');"
                        #b = curs.execute(sql)
            #if ventaext == 1:
                #modo_com = '5'
            #else:
                #modo_com = '0'
            #sql = "update documentos_comerciales set correlativo = '"+str(nodoc)+"', prefijo = '"+str(nodoc_prefijo)+"', sufijo = '"+str(nodoc_sufijo)+"' where modo = '"+str(modo_com)+"' and documento = '"+str(comprobante_id)+"' and caja = "+str(caja_num)+" and pv = "+str(pos_num)+""
            #b = curs.execute(sql)
    if doccli != '':
        sql = "insert into delivery (tiempo, pv, numero, cliente, docnum, carac1, carac2, carac3) values ('"+str(timeord)+"', '"+str(pos_num)+"', '"+str(norden)+"', '"+str(doccli)+"', '"+str(nodoc)+"', '"+str(texto1.upper)+"', '"+str(texto2.upper)+"', '"+str(texto3.upper)+"')"
        curs.execute(sql)
    win.getch()
    return


def linea_dato(msg, win, pan, texto="", pos_y=1):
    """
    Gets Lists
    """
    texto = str(texto)
    size_y, size_x = win.getmaxyx()
    ubic_x = len(msg)+3
    tam_real_x = size_x-2
    txt_pre = 0
    if len(texto) > 0:
        dato = texto
        txt_pre = 1
    else:
        dato = ''
    win.addstr(pos_y, 1, msg)
    while 1:
        if ubic_x >= tam_real_x:
            ubic_x = len(msg)+3
        if txt_pre == 1:
            win.addstr(pos_y, ubic_x, dato)
            ubic_x += len(dato)
            txt_pre = 0
        update_panels()
        caracter = obch(pan, pos_y, ubic_x, 'v', 0)
        if caracter == 'enter':
            return dato
        elif caracter == 'escape':
            return 'Anular'
        elif (caracter == 'arriba' or caracter == 'abajo' or
            caracter == 'insert' or caracter == 'spag' or
            caracter == 'ppag' or caracter == 'derecha' or
            caracter == 'izquierda'):
            pass
        elif caracter == 'backspace':
            ubic_x -= 1
            if ubic_x <= len(msg)+3:
                ubic_x = len(msg)+3
            dato = dato[:-1]
            win.addstr(pos_y, ubic_x, '   ')
            caracter = ''
        elif (caracter >= '0' and caracter <= '9') or (caracter >= 'a' 
            and caracter <= 'z') or (caracter >= 'A' 
            and caracter <= 'Z') or (caracter == '-') or (
            caracter == '.') or (caracter == ' ') or (caracter == '&'):
            ubic_x += 1
            dato += str(caracter)
            if ubic_x >= (tam_real_x):
                ubic_x = tam_real_x
                dato = dato[:tam_real_x]


def data_input(msg, pan, tamx=20, texto="", tipo=0, clr=0):
    """
    Gets Data
    """
    ubicx = len(msg)+3
    tmax = tamx+ubicx
    txtp = 0
    if len(texto) > 0:
        codobt = texto
        txtp = 1
    else:
        codobt = ''
    win = define_window(pan, borde=1)
    tmy, tmx = win.getmaxyx()
    win.addstr(1, 1, msg+': ')
    while 1:
        if ubicx >= tmx:
            ubicx = len(msg)+3
        update_panels()
        if txtp == 1:
            win.addstr(1, ubicx, codobt)
            ubicx = ubicx+len(codobt)
            txtp = 0
        caracter = obch(pan, 1, ubicx, 'v', tipo)
        if caracter == 'enter':
            if clr == 1:
                win.erase()
            return codobt
        elif caracter == 'escape':
            return 'Anular'
        elif caracter == 'arriba' and tipo == 0:
            return 'arriba'
        elif caracter == 'abajo' and tipo == 0:
            return 'abajo'
        elif caracter == 'insert' and tipo == 0:
            return 'insert'
        elif caracter == 'spag' and tipo == 0:
            return 'spag'
        elif caracter == 'ppag' and tipo == 0:
            return 'ppag'
        if caracter == 'backspace':
            ubicx -= 1
            if ubicx <= len(msg)+3:
                ubicx = len(msg)+3
            codobt = codobt[:-1]
            win.addstr(1, ubicx, '   ')
            caracter = ''
        if (caracter >= '0' and caracter <= '9') or (caracter >= 'a' 
            and caracter <= 'z') or (caracter >= 'A' 
            and caracter <= 'Z') or (caracter == '-') or (
            caracter == '.'):
            ubicx += 1
            codobt += str(caracter)
            if ubicx >= (tmax):
                ubicx = tmax
                codobt = codobt[:tamx]


def dicotomic_question(msg, modo=0):
    """
    Y/N Query
    """
    curses.curs_set(1)
    update_panels()
    ty = 3
    tx = len(msg)+3
    py = screen_position(ty, maxy)
    px = screen_position(tx, maxx)
    pan = make_panel(curses.COLOR_WHITE, ty, tx, py, px)
    pan.show()
    win = define_window(pan, 0, 1)
    win.addstr(1, 1, msg)
    while 1:
        resp = win.getch()
        if resp == ord('s'):
            win.erase()
            curses.curs_set(0)
            update_panels()
            return 'si'
        elif resp == ord('n'):
            win.erase()
            curses.curs_set(0)
            update_panels()
            return 'no'
        else:
            win.erase()
            curses.curs_set(0)
            update_panels()
            if modo == 0:
                return 'no'
            else:
                return 'nulo'


def message_alert(pan, texto="", posx=1):
    """
    Shows Message
    """
    pan.show()
    win, tpx, tpy = define_window(pan, 1, 0, 1)
    win.addstr(1, posx, texto)
    return


def contador_pantalla(cantidad):
    """
    Screen Counter
    """
    posx = right_text(maxx-10, str(cantidad))
    win = define_window(p1, 0, 0)
    espacios = ' '
    for cnt in range(0, 10):
        espacios += espacios
    win.addstr(5, maxx-20, '          ')
    win.addstr(5, posx, str(cantidad))
    update_panels()
    return


def time_printing(pan):
    """
    Prints Time
    """
    win = define_window(pan, 0, 0)
    while 1:
        time.sleep(1)
        impres = time.strftime("%A,  %d-%B(%m)-%Y %H:%M:%S")
        posx = center_text(maxx, impres)
        win.addstr(0, posx, impres)
        update_panels()


def sales_report(modo=0):
    """
    Full SUM
    """
    total_full = 0
    tot_cupones = 0
    tot_porc_imp = 100
    total_impuestos = 0
    sub_total = 0
    dsc_global = 0
    format_list = []
    if len(ctrlprods) == 0:
        return 0, 0, 0
    for codigo in cupones:
        if cupones[codigo]['mod'] == 1:
            tot_cupones += (cupones[codigo]['mnt']
                *cupones[codigo]['cnt'])
    for codigo in ctrlprods:
        cantidad = ctrlprods[codigo]['cnt']
        precio = ctrlprods[codigo]['prc']
        descuento = ctrlprods[codigo]['dsc']
        limite = ctrlprods[codigo]['lmt']
        if limite >= cantidad:
            sub_total = (cantidad*precio)-(
                ((cantidad*precio)*descuento)/100)
        else:
            sub_total = (cantidad*precio)-(
                ((limite*precio)*descuento)/100)
        sub_total = round(sub_total, 2)
        total_full += sub_total
    total_full = round(total_full, 2)
    tot_cupones = round(tot_cupones, 2)
    dsc_global = round((tot_cupones * 100) / total_full,2)
    total = total_full - tot_cupones
    if total < 0:
        total = 0.0
    ##Procesamiento de Impuestos
    tot_porc_imp += sum(impuestos.values())
    imp_glob = dict([(val,round((impuestos[val]*total)/tot_porc_imp,2)) 
        for val in impuestos])
    total_impuestos = sum(imp_glob.values())
    ##Impuestos
    det_impto = " ".join(["%s:%s" % (elem[0], elem[1]) 
        for elem in imp_glob.items()])
    total_neto = round(total - total_impuestos, 2)
    if modo == 0:
        return total, total_neto, total_impuestos
    elif modo == 1:
        for codigo in ctrlprods:
            nombre = ctrlprods[codigo]['nam']
            precio = ctrlprods[codigo]['prc']
            cantidad = ctrlprods[codigo]['cnt']
            descuento = ctrlprods[codigo]['dsc'] + dsc_global
            limite = ctrlprods[codigo]['lmt']
            sub_productos = ctrlprods[codigo]['sub']
            if limite >= cantidad:
                sub_total_bruto = (cantidad*precio)-(
                    ((cantidad*precio)*descuento)/100)
            else:
                sub_total_bruto = (cantidad*precio)-(
                    ((limite*precio)*descuento)/100)
            sub_total_bruto = round(sub_total_bruto, 2)
            sub_total_neto = round((sub_total_bruto*100)/tot_porc_imp, 2)
            sub_imp = dict([(val,round((impuestos[val]*sub_total_bruto)/
                tot_porc_imp,2)) for val in impuestos])
            sub_det = " ".join(["%s:%s" % (elem[0], elem[1]) 
                for elem in sub_imp.items()])
            format_list.append([nombre, codigo, fpformat.fix(precio, 2),
                fpformat.fix(cantidad, 2),
                fpformat.fix(sub_total_bruto, 2),
                fpformat.fix(sub_det, 2),
                fpformat.fix(sub_total_neto, 2)])
            #total_full += sub_total_bruto
        return total, total_neto, det_impto, format_list


def windows_header(texto, pan, borde=1):
    """
    Windows Header
    """
    window = define_window(pan, borde)
    maxx, maxy = window.getmaxyx()
    pos_x = center_text(maxx, texto)
    window.addstr(1, pos_x, texto)
    update_panels()
    return


def boolean(mensaje, opcion1, opcion2):
    """
    Single Option from Selection
    """
    dato = ''
    while dato == '':
        resp = dicotomic_question(mensaje, 1)
        if resp == 'si':
            dato = '1'
            msg_resp = opcion1
            return dato, msg_resp
        elif resp == 'no':
            dato = '0'
            msg_resp = opcion2
            return dato, msg_resp


def delivery_process():
    """
    Delivery Functions
    """
    #impresion = 'n'
    tiempo = time.strftime("%Y-%m-%d %H:%M:%S")
    sql = "select max(numero)+1 from delivery"
    cnt, rso = query(sql, 0)
    if rso[0] is None:
        n_orden = 1
    else:
        n_orden = rso[0]
    ty = 16
    tx = 70
    n_fld = 0
    valor = 1
    telefono = ''
    doc_num = ''
    nombre = ''
    direccion = ''
    referencia = ''
    py = screen_position(ty, maxy)
    px = screen_position(tx, maxx)
    panel = make_panel(curses.COLOR_WHITE, ty, tx, py, px)
    win = define_window(panel, borde=1)
    texto = """DELIVERY  === No. ORDEN: %s -- 
        FECHA/HORA: %s""" % (n_orden, tiempo)
    windows_header(texto, panel)
    while 1:
        telefono = linea_dato('Telefono', win, panel, telefono, 3)
        if telefono == 'Anular':
            valor = 0
            break
        sql = """select a.doc_id, a.nombre_corto from directorio a 
            left join directorio_auxiliar b on a.doc_id = b.doc_id 
            where b.telefono like '%s%%' order 
            by a.nombre_corto""" % (telefono)
        cnt, rso = query(sql)
        if cnt > 0:
            doc_num, nombre = list_selection(rso, 'Identificacion')
            if doc_num == 'Anular':
                valor = 0
                break
            elif doc_num != 'agregar' and doc_num != 'insertar':
                n_fld = 1
                sql = """select a.direccion, a.referencia from
                    directorio a where a.doc_id = '%s'""" % (doc_num)
                cnt, rso = query(sql, 0)
                if cnt > 0:
                    direccion = rso[0]
                    referencia = rso[1]
            else:
                doc_num = ''
                nombre = ''
        nombre = linea_dato('Nombre', win, panel, nombre, 4)
        if nombre == 'Anular':
            valor = 0
            break
        direccion = linea_dato('Direccion', win, panel, direccion, 5)
        if direccion == 'Anular':
            valor = 0
            break
        referencia = linea_dato('Referencia', win, panel, referencia, 6)
        if referencia == 'Anular':
            valor = 0
            break
        while 1:
            if doc_num == '':
                doc_num = linea_dato('ID', win, panel, '', 7)
                if doc_num == 'Anular':
                    valor = 0
                    break
                sql = """select a.direccion, a.referencia from 
                    directorio a where a.doc_id = '%s'""" % (docnum)
                cnt, rso = query(sql)
                if cnt == 0:
                    break
                else:
                    doc_num = ''
            else:
                break
        if valor == 0:
            break
        texto1_l1 = linea_dato('C1-L1:', win, panel, '', 9)
        if texto1_l1 == 'Anular':
            valor = 0
            break
        texto1_l2 = linea_dato('C1-L2:', win, panel, '', 10)
        if texto1_l2 == 'Anular':
            valor = 0
            break
        texto2_l1 = linea_dato('C2-L1:', win, panel, '', 11)
        if texto2_l1 == 'Anular':
            valor = 0
            break
        texto2_l2 = linea_dato('C2-L2:', win, panel, '', 12)
        if texto2_l2 == 'Anular':
            valor = 0
            break
        texto3_l1 = linea_dato('C3-L1:', win, panel, '', 13)
        if texto3_l1 == 'Anular':
            valor = 0
            break
        texto3_l2 = linea_dato('C3-L2:', win, panel, '', 14)
        if texto3_l2 == 'Anular':
            valor = 0
            break
        resp = dicotomic_question('Guardar?')
        if resp == 'si':
            valor = 1
            break
    if valor == 0:
        return ('Anular', '', '', '', '', '', '', '', '', '')
    else:
        if n_fld == 0:
            sql = """insert into directorio (tipo_doc, doc_id,
                nombre_corto, direccion, referencia) values ('1', '%s',
                '%s', '%s', '%s')""" % (doc_num, nombre.upper(),
                direccion.upper(), referencia.upper())
            curs.execute(sql)
            sql = """insert into directorio_auxiliar (doc_id, telefono)
                values ('%s', '%s')""" % (doc_num, telefono)
            curs.execute(sql)
        else:
            sql = """update directorio set nombre_corto='%s',
                direccion='%s', referencia='%s' where
                doc_id= '%s'""" % (nombre.upper(), direccion.upper(),
                referencia.upper(), doc_num)
            curs.execute(sql)
        return (doc_num, nombre.upper(), direccion.upper(), 
            referencia.upper(), telefono, 
            ("%s%s" % (texto1_l1+texto1_l2)).upper(), 
            ("%s%s" % (texto2_l1+texto2_l2)).upper(), 
            ("%s%s" % (texto3_l1+texto3_l2)).upper(), n_orden, time)


def document_selection(modo):
    """
    Document Selection
    """
    sql = """select documento, nombre from documentos_comerciales 
        where modo = '%s' and pv = '%s' and caja = %s 
        order by documento""" % (modo, pos_num, caja_num)
    cuenta, resultado = query(sql)
    if cuenta > 0:
        doc_tipo, doc_tipo_dscp = list_selection(resultado, 'Documento')
        if doc_tipo == 'Anular':
            return 'Anular', 'Anular'
        else:
            return doc_tipo, doc_tipo_dscp
    else:
        return 'Anular', 'Anular'


def get_correlative(modo, documento, extra=0, edit=0, panel=''):
    """
    Obtains Documents Correlative
    """
    prefijo = 'Anular'
    correlativo = ''
    sufijo = ''
    copia_doc = ''
    detalle_doc = ''
    doc_port = ''
    doc_layout = ''
    sql = """select prefijo, correlativo, sufijo, copia, detalle, port,
        layout from documentos_comerciales where documento = '%s' and
        modo = '%s' and pv = '%s' and caja = %s""" % (documento, 
        modo, pos_num, caja_num)
    cuenta, resultado = query(sql, 0)
    if cuenta > 0:
        prefijo = resultado[0]
        correlativo = int(resultado[1])+1
        sufijo = resultado[2]
        copia_doc = resultado[3]
        detalle_doc = resultado[4]
        doc_port = resultado[5]
        doc_layout = resultado[6]
        if extra == 1:
            sql2 = """select id from docventa where n_doc_base = '%s' 
                and n_doc_prefijo = '%s'""" % (correlativo, prefijo)
            cuenta2, resultado2 = query(sql2, 0)
            if cuenta2 > 0:
                dicotomic_question("""Inconsistencia en Correlativos!!!
                    Corrigiendo....""")
                sql3 = "select max(n_doc_base) from docventa"
                cuenta3, resultado3 = query(sql3, 0)
                if cuenta3 > 0:
                    correlativo = int(resultado3[0])+1
    if panel == 'new':
        cty = 3
        ctx = 40
        cpy = (maxy-cty)/2
        cpx = (maxx-ctx)/2
        panel = make_panel(curses.COLOR_WHITE, cty, ctx, cpy, cpx)
    if edit == 0:
        alerta_flag = 1
        if len(str(sufijo)) > 0:
            sufijo = "-" % (sufijo)
        old_prefijo = prefijo
        old_correlativo = correlativo
        dato = "%s-%s%s" % (prefijo, correlativo, sufijo)
        while 1:
            try:
                ingdat = data_input('Documento', panel, 30, dato, 0, 0)
                if ingdat == 'Anular':
                    return 'Anular', '', '', '', ''
                elif ingdat == dato:
                    alerta_flag = 0
                    break
                partes = "-".split(ingdat)
                elem = len(partes)
                if elem == 1:
                    correlativo = int(partes[0])
                elif elem == 2:
                    prefijo = str(partes[0])
                    correlativo = int(partes[1])
                elif elem == 3:
                    prefijo = str(partes[0])
                    correlativo = int(partes[1])
                    sufijo = str(partes[2])
                if correlativo >= old_correlativo:
                    break
            except Exception, error:
                logging.debug("GetCorrelative: %s" % error)
        if alerta_flag == 1:
            dato = "%s-%s%s " % (prefijo, correlativo, sufijo)
            mensaje = """Documento %s Original:%s-%s Cambiado 
                a:%s""" % (documento, old_prefijo, old_correlativo,
                dato)
            mail_warning(mensaje, 'ALERTA DE DOCUMENTOS MANUALES')
    return (str(prefijo), str(correlativo), str(sufijo),
        str(copia_doc), str(detalle_doc), str(doc_port),
        str(doc_layout))


def mail_warning(mensaje, subject='ALERTA'):
    """
    Warning Window
    """
    if from_smtp == '':
        return
    message = "From: %s\r\nTo:%s\r\nSubject:%s\r\n%s" % (from_smtp,
        to_smtp, subject, mensaje)
    try:
        server = smtplib.SMTP(servidor_smtp)
        server.sendmail(from_smtp, to_smtp, message)
        server.quit()
    except Exception, error:
        logging.debug("MailWarning: %s" % error)


def check_time(alerta_max='1', hora_limite='00:00:00'):
    """
    Checks POS Time
    """
    apertura, cierre, tiempo_max = pos_time()
    tiempo_actual = time.strftime("%Y-%m-%d %H:%M:%S")
    tiempo_cierre = apertura[:10]+" "+hora_limite
    if apertura == 'Error':
        dicotomic_question("""ERROR: LA CAJA NO SE ENCUENTRA
            APERTURADA""")
        return 'Error'
    if apertura > tiempo_actual:
        dicotomic_question("""ERROR: INCONGRUENCIA EN LA APERTURA""")
        return 'Error'
    if tiempo_actual >= tiempo_cierre and (hora_limite != '0:00:00' and
        hora_limite != '00:00:00' and hora_limite != '00:00:00.00'):
        dicotomic_question("""ERROR: CIERRE LA CAJA,  
            HORA MAXIMA EXCEDIDA""")
        return 'Error'
    elif revisa_tiempo > tiempo_max:
        if alerta_max == '1':
            dicotomic_question("""ADVERTENCIA: LA CAJA LLEVA MAS DE 
                1 DIA APERTURADA""")
        return 'Warning'
    return 'Ok'


def product_list(py=1):
    """
    Products List
    """
    global ctrlprods
    for cupon in cupones:
        modo = cupones[cupon]['mod']
        codigos = cupones[cupon]['prd']
        if modo == 0:
            #cnt = 0
            for codigo in codigos:
                if codigo in ctrlprods:
                    ctrlprods[codigo]['dsc'] = (
                        cupones[cupon]['dsc'])
                    ctrlprods[codigo]['lmt'] = (
                        cupones[cupon]['lmt'])
                    ctrlprods[codigo]['val'].append(cupon)
                #cnt += 1
        elif modo == 1:
            pass
        elif modo == 2:
            #cnt = 0
            for codigo in codigos:
                if codigo not in ctrlprods:
                    py += 1
                    ctrlprods[codigo] = {}
                    ctrlprods[codigo]['nam'] = (
                        cupones[cupon]['id'])
                    ctrlprods[codigo]['cnt'] = (
                        cupones[cupon]['cnt'])
                    ctrlprods[codigo]['prc'] = (
                        cupones[cupon]['prc'])
                    ctrlprods[codigo]['dsc'] = (
                        cupones[cupon]['dsc'])
                    ctrlprods[codigo]['lmt'] = (
                        cupones[cupon]['lmt'])
                    ctrlprods[codigo]['pos'] = py
                    ctrlprods[codigo]['val'] = []
                    ctrlprods[codigo]['sub'] = []
        elif modo == 3:
            for codigo in ctrlprods:
                ctrlprods[codigo]['dsc'] = cupones[cupon]['dsc']
                ctrlprods[codigo]['lmt'] = cupones[cupon]['lmt']
                ctrlprods[codigo]['val'].append(cupon)
    return py


def product_finder(titulo, num_char, valid_data_types, sql_cond=''):
    """
    Searchs any product with some conditions
    """
    cond_types = valid_data_types.split(',')
    size_y = 3
    size_x = 12 + num_char
    pos_y = (maxy - size_y) / 2
    pos_x = (maxx - size_x) / 2
    while 1:
        paning = make_panel(curses.COLOR_WHITE, size_y, size_x, pos_y,
            pos_x)
        data_ing = data_input('Producto', paning, num_char)
        if data_ing == 'Anular':
            return data_ing, 0
        tipo_dato = get_value_expresion(data_ing)[1]
        if tipo_dato in cond_types:
            sql = """select codbarras,concat(nombre,' ',descripcion,
                '==',round(precio,2)) from maestro where 
                (nombre like '%%%s%%' or descripcion like '%%%s%%'
                or nombre like '%%%s%%' or descripcion like '%%%s%%'
                or alias like '%%%s%%' or alias like '%%%s%%')
                and (%s) order by codbarras asc""" % (data_ing, 
                data_ing, data_ing.upper(), data_ing.upper(),
                data_ing, data_ing.upper(), sql_cond)
            cuenta, resultado = query(sql, 1)
            data_ing, nombre = list_selection(resultado, "Productos")
            return data_ing, nombre

#sql="select val.tipo,if(tip.valor is NULL,val.precio,(val.precio*tip.valor)) as 
#precio from maestro_valores val left join tipos_cambio tip on tip.moneda=val.moneda 
#where val.codbarras='%s' and tip.fecha='%s' and (val.pv='' or val.pv=0 or val.pv=%s) 
#order by val.posicion"%(codigo,fecha_cambio,pos_num)


def product_processing(datos):
    """
    Products processing
    """
    global ctrlprods
    global cnt_prod
    global py
    for dato in datos:
        #autoriz = 1
        py += 1
        nombre, precio = producto_data(dato)
        datos[dato]['pos'] = py
        datos[dato]['prc'] = precio
        if cnt_prod > 0:
            if datos[dato]['cnt'] == 1:
                datos[dato]['cnt'] = float(cnt_prod)
        #Descuentos
        sql = """select modo, descuento, limite, data
            from  pos_descuentos where (pv = %s or 
            pv = 0 or pv = '') and (caja = %s or 
            caja = 0) and codbarras = '%s' and 
            estado = 1""" % (pos_num, caja_num, dato)
        cuenta, resultado = query(sql)
        if cuenta > 0:
            check_cnt = 0
            for parte in resultado:
                desc_modo = int(parte[0])
                desc_porc = float(parte[1])
                desc_limit = float(parte[2])
                desc_valor = str(parte[3])
                desc_valor_tmp = "|".split(desc_valor)
                if desc_modo == 0:
                    #Descuento General
                    check_cnt += 1
                elif desc_modo == 1:
                    #Descuento por Montos
                    if total >= float(desc_valor):
                        check_cnt += 1
                elif desc_modo == 2:
                    #Descuento por Nivel
                    if nivel_usuario <= int(desc_valor):
                        check_cnt += 1
                elif desc_modo == 3:
                    #Descuento por Fecha
                    if (apertura[:10] >= desc_valor_tmp[0] and 
                        apertura[:10] <= desc_valor_tmp[1]):
                        check_cnt += 1
                elif desc_modo == 4:
                    #Descuento por Hora
                    if (apertura[11:] >= desc_valor_tmp[0] and
                        apertura[11:] <= desc_valor_tmp[1]):
                        check_cnt += 1
                elif desc_modo == 5:
                    if desc_valor_tmp.count(codigo_usuario) > 0:
                        check_cnt += 1
            if check_cnt >= cuenta:
                datos[dato]['dsc'] = desc_porc
                datos[dato]['lmt'] = desc_limit
            else:
                datos[dato]['dsc'] = 0
                datos[dato]['lmt'] = 10000
        else:
            datos[dato]['dsc'] = 0
            datos[dato]['lmt'] = 10000
        #Dependencias
        sql = """select modo, data from 
            maestro_dependencias where (pv = %s or 
            pv = 0) and codbarras = '%s' and 
            estado = 1""" % (pos_num, dato)
        cuenta, resultado = query(sql)
        extracto = 0
        check_cnt = 0
        if cuenta > 0:
            for parte in resultado:
                extracto = 0
                modo = int(parte[0])
                data = parte[1]
                data_tmp = "|".split(data)
                if modo == 0:
                    #Dependencia por Nivel
                    if nivel_usuario <= int(data):
                        check_cnt += 1
                elif modo == 1:
                    #Dependencia por Usuarios
                    if data_tmp.count(codigo_usuario) > 0:
                        check_cnt += 1
                elif modo == 2:
                    #Dependencia por Montos
                    if total >= float(data):
                        check_cnt += 1
                elif modo == 3:
                    #Dependencia por Productos
                    for part in data_tmp:
                        if part in ctrlprods:
                            extracto += 1
                    if extracto > 0:
                        check_cnt += 1
                elif modo == 4:
                    #Dependencia por Horas
                    hora_dependencia = time.strftime(
                        '%H:%M:%S')
                    if (hora_dependencia >= data_tmp[0] 
                        and hora_dependencia 
                        <= data_tmp[1]):
                        check_cnt += 1
                elif modo == 5:
                    #Dependencia por Fechas
                    fecha_dependencia = time.strftime(
                        '%Y-%m-%d')
                    if (fecha_dependencia >= data_tmp[0]
                        and fecha_dependencia 
                        <= data_tmp[1]):
                        check_cnt += 1
        if dato not in ctrlprods:
            if check_cnt >= cuenta:
                ctrlprods[dato] = datos[dato]
                ctrlprods[dato]['val'] = []
        else:
            if check_cnt >= cuenta:
                ctrlprods[dato]['cnt'] = (
                    ctrlprods[dato]['cnt'] + 
                    datos[dato]['cnt'])
                sub_dato_new = datos[dato]['sub']
                sub_dato_ori = ctrlprods[dato]['sub']
                for elem in sub_dato_new:
                    if elem in sub_dato_ori:
                        for parte in sub_dato_new[elem]:
                            if parte in sub_dato_ori[elem]:
                                ctrlprods[dato]['sub'][elem][parte] = sub_dato_new[elem][parte][0], (ctrlprods[dato]['sub'][elem][parte][1]+sub_dato_new[elem][parte][1])
                            else:
                                ctrlprods[dato]['sub'][elem][parte] = sub_dato_new[elem][parte][0], sub_dato_new[elem][parte][1]
                    else:
                        ctrlprods[dato]['sub'][elem] = sub_dato_new[elem]
    cnt_prod = 0


def coupon_process():
    global cupones
    cty = 3
    ctx = 20
    cpy = (maxy-cty)/2
    cpx = (maxx-ctx)/2
    sql = """select prom.modo, prom.producto, prom.cantidad,
        prom.porcentaje, prom.limite, prom.valor, prom.nombre,
        prom.impresion, if(length(mae.alias)>0, mae.alias,
        concat(mae.nombre, ' ', mae.descripcion)) as prod,
        mae.precio from promociones prom left join maestro mae on
        mae.codbarras = prom.producto where prom.codigo='%s' and
        prom.estado='A' and (prom.pv = '0' or prom.pv = %s) and
        (prom.cond_hora_term >= '%s' and prom.cond_hora_inic <= '%s')
        and prom.cond_valor <= '%s'"""
    paning = make_panel(curses.COLOR_WHITE, cty, ctx, cpy, cpx)
    codigo = data_input('Vale', paning, 10)
    if codigo != 'Anular':
        codvale = data_input('No.', paning, 10)
        if codvale != 'Anular':
            prom_fecha = time.strftime("%Y-%m-%d")
            prom_hora = time.strftime("%H:%M:%S")
            sql = sql % (codigo, pos_num, prom_hora, prom_hora, total)
            cuenta, resultado = query(sql, 1)
            if cuenta > 0:
                if codigo in cupones:
                    if cupones[codigo]['mod'] == 1:
                        #temp = cupones[codigo]['cnt'][0] + 1
                        #cupones[codigo]['cnt'] = []
                        cupones[codigo]['cnt'] +=1
                        cupones[codigo]['ref'].append(codvale)
                else:
                    cupones[codigo] = {}
                    cupones[codigo]['prd'] = []
                    cupones[codigo]['cnt'] = 0
                    cupones[codigo]['dsc'] = 0
                    cupones[codigo]['lmt'] = 0
                    cupones[codigo]['id'] = []
                    cupones[codigo]['prc'] = 0
                    cupones[codigo]['ref'] = []
                    for linea in resultado:
                        ## Modo del Cupon
                        cupones[codigo]['mod'] = int(linea[0])
                        ## Productos afectado
                        cupones[codigo]['prd'].append(linea[1])
                        ## Cantidad de prods afectados
                        cupones[codigo]['cnt'] = float(linea[2])
                        ## Porcentaje descuento afectado
                        cupones[codigo]['dsc'] = float(linea[3])
                        ## Limite de productos afectados
                        lmt = float(linea[4])
                        if lmt == 0:
                            lmt = 10000
                        cupones[codigo]['lmt'] = lmt
                        ## Valor del cupon
                        cupones[codigo]['mnt'] = float(linea[5])
                        ## Nombre del cupon
                        cupones[codigo]['nam'] = linea[6]
                        
                        cupones[codigo]['ext'] = str(linea[7])
                        cupones[codigo]['id'].append(str(linea[8]))
                        ## Precio a aplicar
                        if linea[9] >= 0:
                            precio = linea[9]
                        else:
                            precio = 0
                        cupones[codigo]['prc'] = float(precio)
                    cupones[codigo]['ref'].append(codvale)
    return
#    paning.hide()
#    update_panels()


def product_delete():
    global ctrlprods
    impres = 'ELIM'
    posx = right_text(maxx, impres)
    win = define_window(p1, 0, 0)
    win.addstr(5, posx, impres)
#    update_panels()
    objeto = obch(p1)
    if objeto == "borrar":
        msg = 'Desea borrar todos los productos?'
        resp = dicotomic_question(msg)
        if resp == 'si':
            ctrlprods = {}
            return
    else:
        lista_prod = []
        for codigo in ctrlprods:
            temporal = []
            temporal.append(codigo)
            temporal.append(ctrlprods[codigo]['nam'])
            lista_prod.append(temporal)
        eliminados = opciones_cnt(lista_prod, 0, 'ELIMINAR')
        for codigo in eliminados:
            if codigo in ctrlprods:
                cnt_key = eliminados[codigo][1]
                if float(cnt_key) >= float(
                    ctrlprods[codigo]['cnt']):
                    del ctrlprods[codigo]
                else:
                    ctrlprods[codigo]['cnt'] = float(
                        ctrlprods[codigo]['cnt'])-float(cnt_key)
                    sub_productos = ctrlprods[codigo]['sub']
                    lista_prod = []
                    if len(sub_productos) > 0:
                        sub_datos = sub_productos
                        sub_orden = sub_datos.keys()
                        sub_orden.sort()
                        for sub_dato in sub_orden:
                            for sub_valor in sub_datos[sub_dato]:
                                temporal = []
                                producto = (sub_datos[sub_dato]
                                    [sub_valor][0])
                                producto = producto[:38]
                                cantidad = (sub_datos[sub_dato]
                                    [sub_valor][1])
                                temporal.append(sub_valor)
                                temporal.append(producto)
                                lista_prod.append(temporal)
                        eliminados_sub = opciones_cnt(
                            lista_prod, 0, 'ELIMINAR SUB')
                        tmp_cnt = 0
                        for aux_codigo in eliminados_sub:
                            tmp_cnt += 1
                            for sub_dato in sub_orden:
                                if float(eliminados_sub[aux_codigo][1]) >= float(ctrlprods[codigo]['sub'][sub_dato][aux_codigo][1]):
                                    del ctrlprods[codigo]['sub'][sub_dato][aux_codigo]
                                else:
                                    temp = ctrlprods[codigo]['sub'][sub_dato][aux_codigo]
                                    del ctrlprods[codigo]['sub'][sub_dato][aux_codigo]
                                    ctrlprods[codigo]['sub'][sub_dato][aux_codigo] = [temp[0], float(temp[1])-float(eliminados_sub[aux_codigo][1])]


####
tty = maxy-10
x_p2 = int((maxx*12.5)/100)
x_p3 = int((maxx*50)/100)
x_p7 = int((maxx*7.5)/100)
x_p6 = int((maxx*12)/100)
x_p5 = int((maxx*25)/100)
x_p9 = int((maxx*40)/100)
x_px = int((maxx*10)/100)
x_p4 = maxx-(x_p3+x_p2+x_p6+x_p7)
x_p8 = maxx-(x_p9+x_px+x_p5)
p1 = make_panel(curses.COLOR_WHITE, 7, maxx, 0, 0)
p2 = make_panel(curses.COLOR_WHITE, tty, x_p2, 7, 0)
p3 = make_panel(curses.COLOR_WHITE, tty, x_p3, 7, x_p2)
p6 = make_panel(curses.COLOR_WHITE, tty, x_p6, 7, x_p3+x_p2)
p7 = make_panel(curses.COLOR_WHITE, tty, x_p7, 7, x_p3+x_p2+x_p6)
p4 = make_panel(curses.COLOR_WHITE, tty, x_p4, 7, x_p3+x_p2+x_p6+x_p7)
p5 = make_panel(curses.COLOR_WHITE, 3, x_p5, maxy-3, x_p9+x_px)
p8 = make_panel(curses.COLOR_WHITE, 3, x_p8, maxy-3, x_p9+x_px+x_p5)
p9 = make_panel(curses.COLOR_WHITE, 3, x_p9, maxy-3, 0)
panel_text_5 = make_panel(curses.COLOR_WHITE, 3, 20, 6, 0)
hora = make_panel(curses.COLOR_WHITE, 1, maxx-2, 4, 1)
thread.start_new_thread(time_printing, (hora, ))


while 1:
    while nombre_usuario == 'I':
        codigo_usuario, nombre_usuario, nivel_usuario = authorization()
        dataz = pos_status()
        if dataz == 'bad':
            nombre_usuario = 'I'
    configuration()
    (doccli, nomcli, dircli, refcli, telcli, texto1, texto2, texto3, 
        norden, timeord) = ('', '', '', '', '', '', '', '', '', '')
    nombre_cliente = ''
    id_cliente = ''
    medios_pago = {}
    ventaext = 0
    ndocext_pre = ''
    ndocext = ''
    texto_dm = ''
    extra_print = '0'
    msg_dist = ''
    global_y = 0
    py = 0
    total = 0.0
    total_neto = 0.0
    total_impuestos = 0.0
    det_impto = ''
    format_list = []
    cnt_prod = 0
    total_cupones = 0
    dsc_global = 0
    ctrlprods = {}
    distribucion = '0'
    cupones = {}
    main_header(p1, nombre_usuario[:20])
    window_body(p2, p3, p6, p4, p5, p8, p7)
    message_alert(p9, " "*33)
    update_panels()
    while 1:
        #apertura, cierre = pos_time(1)
        revisar_time = check_time(dia_alerta,hora_max)
        if revisar_time == 'Error':
            nombre_usuario = "I"
            break
        hora.show()
        # Define some variables
        total = 0.00
        impres = 'AGRG'
        posx = right_text(maxx, impres)
        # Defines the Window and prints part of the header
        win = define_window(p1, 0, 0)
        win.addstr(5, posx, impres)
        # Gets a char or key
        car = obch(p1)
        if car == 'ppag':  #Delivery
            distribucion = '1'
            (doccli, nomcli, dircli, refcli, telcli, texto1, texto2, 
                texto3, norden, timeord) = delivery_process()
            if doccli == 'Anular':
                (doccli, nomcli, dircli, refcli, telcli, texto1, texto2,
                    texto3, norden, timeord) = ('', '', '', '', '', '',
                     '', '', '', '')
            else:
                message_alert(p9, "DELIVERY:"%(norden))
        elif car == ' ':
            codigo_producto, nombre_producto = product_finder("Codigo",
                20, "caracter,alfanumerico", "genero='0003'")
            if codigo_producto != 'Anular':
                if cnt_prod == 0:
                    cnt_prod = 1
                nombre_producto, precio_producto = producto_data(
                    codigo_producto)
                datos = {codigo_producto: {'cnt': cnt_prod,
                    'sub': {}, 'nam': nombre_producto}}
                product_processing(datos)
                cnt_prod = 0
        elif car == 'finp':  #Lugar Consumo
            if distribucion == '0':
                distribucion = '1'
                msg_dist = 'LLEVAR'
            else:
                distribucion = '0'
                msg_dist = '-MESA-'
            message_alert(p9, "TIPO:"%(msg_dist), 20)
        elif car == 'inicio':  #Sale de Sesion
            msg = 'Desea cambiar de Operador?'
            resp = dicotomic_question(msg)
            if resp == 'si':
                nombre_usuario = 'I'
                break
            else:
                cnt_prod = 0
        elif car == 'borrar':  #Elimina Productos
            product_delete()
        elif (car >= '0' and car <= '9') or car == '.':
            #Cantidad de Producto
            cnt_prod = "%s%s" % (cnt_prod, car)
            if modo_decimal == '0':
                cnt_prod = int(cnt_prod)
            else:
                cnt_prod = round(float(cnt_prod),2)
        elif car == 'spag':  #Vales
            coupon_process()
        elif car == 'f11' and nivel_usuario < 10:
            #Salida del SuperUsuario
            msg = "Desea Salir del Programa?"
            resp = dicotomic_question(msg)
            if resp == 'si':
                curses.echo()
                curses.endwin()
                sys.exit()
        elif car == 'f12':
            #Ingreso de Documentos Manuales
            doc_man, doc_man_dscp = document_selection(5)
            if doc_man != 'Anular':
                (ndocext_pre, ndocext, ndocext_pos, ndocext_copia,
                    ndocext_detalle, ndocext_port, ndocext_layout
                    ) = get_correlative(5, doc_man, 0, 0, 'new')
                if ndocext_pre != 'Anular':
                    texto_dm = "D.M.: %s-%s-%s" % (ndocext_pre, 
                        ndocext, ndocext_pos)
                    main_header(p1, nombre_usuario[:20])
                    ventaext = 1
        elif car == 'enter':
            #Procesa Datos
            total, total_neto, det_impto, format_list = sales_report(1)
            if tipo_servicio == '1' and ventaext != 1:
                mensaje = 'Pedido para Llevar?'
                opcion1 = 'LLEVAR'
                opcion2 = '-MESA-'
                distribucion, msg_dist = boolean(mensaje, opcion1, opcion2)
                message_alert(p9, 'TIPO: %s' % msg_dist, 20)
            else:
                distribucion = str(tipo_servicio)
            if len(ctrlprods.keys()) > 0:
                (medios_pago, comprobante_id, nombre_cliente, id_cliente, vuelsol,
                    vueldol) = payment_process()
#                print medios_pago, comprobante_id, nombre_cliente, id_cliente, vuelsol, vueldol
#                sys.exit()
                if medios_pago != 'Anular':
                    clear_screen(1, p1, p2, p3, p4, p5, p6, p7, p8, p9)
                    estado_doc = final_process(vuelsol, vueldol, doccli, nomcli,
                        dircli, refcli, telcli, texto1, texto2, texto3,
                        norden, timeord)
                    if estado_doc == 'Anular':
                        break
                    if modo_control == '1':
                        nombre_usuario = 'I'
                    break
        elif car == 'arriba':
            global_y -= 1
            if global_y <= 0:
                global_y = 0
        elif car == 'abajo':
            global_y += 1
        else:
            try:
                datos = keyboard_definition(car)
                if datos != 'Anular':
                    product_processing(datos)
            except Exception, error:
                logging.debug("Main: %s" % error)
        py = product_list(py)
        total, total_neto, total_impuestos = sales_report()
        windows_printing(p2, p3, p6, p4, p5, p8, p7, global_y)
        contador_pantalla(cnt_prod)
curses.endwin()
