# -*- coding: utf-8 -*-

db = DAL('mysql://root:root@localhost/sisventi_old')

db.define_table('almacenes',  
    Field('registro',  'datetime'),  
    Field('id',  'integer'),  
    Field('modo',  'integer'),  
    Field('pv',  'string'),  
    Field('tiempo',  'datetime'),  
    Field('estado',  'integer'),  
    Field('user_ing',  'string'),  
    Field('operacion_logistica',  'string'),  
    Field('compra_n_doc_prefijo',  'string'),  
    Field('compra_n_doc_base',  'integer'),  
    Field('compra_n_doc_sufijo',  'string'),  
    Field('proveedor_n_doc',  'string'),  
    Field('modo_doc',  'integer'),  
    Field('tipo_doc',  'integer'),  
    Field('fecha_doc',  'date'),  
    Field('n_doc_prefijo',  'string'),  
    Field('n_doc_base',  'integer'),  
    Field('n_doc_sufijo',  'string'),  
    Field('proveedor',  'string'),  
    Field('proveedor_tipo_doc',  'string'),  
    Field('proveedor_condicion',  'integer'),  
    Field('proveedor_fecha_doc',  'date'), 
    Field('proveedor_moneda_doc', 'integer'), 
    Field('proveedor_total_doc', 'double'), 
    Field('almacen_origen', 'string'), 
    Field('almacen_destino', 'string'), 
    Field('articulo', 'string'), 
    Field('codbarras_padre', 'string'), 
    Field('codbarras', 'string'), 
    Field('pedido', 'integer'), 
    Field('cantidad_exp', 'double'), 
    Field('cantidad_ing', 'double'), 
    Field('peso_exp', 'double'), 
    Field('peso_ing', 'double'), 
    Field('tipo', 'string'), 
    Field('precio', 'double'), 
    Field('fecha_prod', 'date'), 
    Field('fecha_venc', 'date'), 
    Field('extra_data', 'string'), 
    Field('transportista', 'string'), 
    Field('vehiculo', 'string'), 
    Field('grupo', 'integer'), 
    Field('turno', 'string'), 
    Field('masa', 'string'), 
    Field('temperatura', 'double'), 
    Field('peso', 'double'), 
    Field('hora_inicial', 'time'), 
    Field('hora_final', 'time'), 
    Field('n_serie', 'string'), 
    Field('n_prefijo_relacion', 'string'), 
    Field('n_doc_relacion', 'integer'), 
    Field('observaciones', 'string'), 
    migrate=False)

#--------
db.define_table('almacenes_lista', 
    Field('almacen', 'string'), 
    Field('registro', 'datetime'), 
    Field('descripcion', 'string'), 
    Field('area', 'string'), 
    Field('pv', 'string'), 
    Field('usuario', 'string'), 
    Field('ubigeo', 'string'), 
    Field('direccion', 'string'), 
    Field('tipo_doc', 'integer'), 
    Field('doc_id', 'string'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('almacenes_ubicacion', 
    Field('registro', 'datetime'), 
    Field('id', 'integer'), 
    Field('almacen', 'string'), 
    Field('codbarras', 'string'), 
    Field('ubicacion', 'string'), 
    migrate=False)

#--------
db.define_table('areas', 
    Field('registro', 'datetime'), 
    Field('area', 'string'), 
    Field('nombre', 'string'), 
    Field('descripcion', 'string'), 
    Field('posicion', 'integer'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('articulos', 
    Field('registro', 'datetime'), 
    Field('articulo', 'string'), 
    Field('nombre', 'string'), 
    Field('posicion', 'integer'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('backup', 
    Field('registro', 'datetime'), 
    Field('tiempo', 'datetime'), 
    Field('log', 'string'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('bancos', 
    Field('registro', 'datetime'), 
    Field('id', 'integer'), 
    Field('pv', 'integer'), 
    Field('fechav', 'date'), 
    Field('fechad', 'date'), 
    Field('banco', 'string'), 
    Field('monto', 'double'), 
    Field('cambio', 'double'), 
    Field('glosa1', 'string'), 
    Field('glosa2', 'string'), 
    Field('agencia', 'string'), 
    migrate=False)

#--------
db.define_table('casas', 
    Field('registro', 'datetime'), 
    Field('casa', 'string'), 
    Field('nombre', 'string'), 
    Field('posicion', 'integer'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('categorias', 
    Field('registro', 'datetime'), 
    Field('categoria', 'string'), 
    Field('nombre', 'string'), 
    Field('posicion', 'integer'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('catmod', 
    Field('registro', 'datetime'), 
    Field('catmod', 'string'), 
    Field('nombre', 'string'), 
    Field('posicion', 'integer'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('clientes_preferentes', 
    Field('id', 'integer'), 
    Field('registro', 'datetime'), 
    Field('doc_id', 'string'), 
    Field('tiempo', 'datetime'), 
    Field('promocion', 'string'), 
    Field('tarjeta', 'string'), 
    Field('user_ing', 'integer'), 
    migrate=False)

#--------
db.define_table('compras_ordenes', 
    Field('id', 'integer'), 
    Field('registro', 'datetime'), 
    Field('tiempo', 'datetime'), 
    Field('n_doc_prefijo', 'string'), 
    Field('n_doc_base', 'integer'), 
    Field('n_doc_sufijo', 'string'), 
    Field('estado', 'integer'), 
    Field('area', 'string'), 
    Field('forma_pago', 'string'), 
    Field('codbarras', 'string'), 
    Field('cantidad', 'double'), 
    Field('cantidad_proveedor', 'double'), 
    Field('moneda', 'string'), 
    Field('precio_neto', 'double'), 
    Field('precio_imp', 'double'), 
    Field('precio_bruto', 'double'), 
    Field('sub_total_neto', 'double'), 
    Field('sub_total_imp', 'double'), 
    Field('sub_total_bruto', 'double'), 
    Field('proveedor', 'string'), 
    Field('total_neto', 'double'), 
    Field('total_imp', 'double'), 
    Field('total_bruto', 'double'), 
    Field('total_texto', 'string'), 
    Field('fecha_entrega', 'date'), 
    Field('lugar_entrega', 'string'), 
    Field('user_req', 'string'), 
    Field('user_ing', 'string'), 
    Field('user_aut1', 'string'), 
    Field('user_aut2', 'string'), 
    Field('user_anul', 'string'), 
    Field('tiempo_anul', 'datetime'), 
    Field('observaciones', 'string'), 
    migrate=False)

#--------
db.define_table('condiciones_comerciales', 
    Field('condicion', 'string'), 
    Field('registro', 'datetime'), 
    Field('modo', 'integer'), 
    Field('descripcion', 'string'), 
    Field('codigo', 'integer'), 
    Field('dias', 'integer'), 
    Field('posicion', 'integer'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('control_insumos', 
    Field('id', 'integer'), 
    Field('codbarras_padre', 'string'), 
    Field('codbarras_hijo', 'string'), 
    Field('gramos', 'double'), 
    Field('adicional', 'double'), 
    Field('estado', 'integer'), 
    Field('truco', 'integer'), 
    Field('orden', 'integer'), 
    Field('modo', 'integer'), 
    migrate=False)

#--------
db.define_table('control_produccion', 
    Field('id', 'integer'), 
    Field('fecha', 'date'), 
    Field('turno', 'string'), 
    Field('producto', 'string'), 
    Field('producto_derivado', 'string'), 
    migrate=False)

#--------
db.define_table('criterio', 
    Field('cp', 'string'), 
    Field('grupo_distribucion', 'string'), 
    Field('turno', 'string'), 
    Field('porcentaje', 'double'), 
    Field('codbarras', 'string'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('criterio2', 
    Field('turno', 'string'), 
    Field('cp', 'string'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('delivery', 
    Field('registro', 'datetime'), 
    Field('pv', 'integer'), 
    Field('tiempo', 'datetime'), 
    Field('numero', 'integer'), 
    Field('cliente', 'string'), 
    Field('docnum', 'integer'), 
    Field('carac1', 'string'), 
    Field('carac2', 'string'), 
    Field('carac3', 'string'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('directorio', 
    Field('registro', 'datetime'), 
    Field('modo', 'integer'), 
    Field('nombre_corto', 'string'), 
    Field('razon_social', 'string'), 
    Field('rubro', 'integer'), 
    Field('nombres', 'string'), 
    Field('apellidos', 'string'), 
    Field('tipo_doc', 'string'), 
    Field('doc_id', 'string'), 
    Field('doc_id_aux', 'string'), 
    Field('ubigeo', 'string'), 
    Field('direccion', 'string'), 
    Field('codigo_postal', 'string'), 
    Field('pais', 'string'), 
    Field('referencia', 'string'), 
    Field('condicion', 'string'), 
    Field('tiempo_cred', 'integer'), 
    Field('linea_credito', 'double'), 
    Field('representante_legal', 'string'), 
    Field('cargo', 'string'), 
    Field('fecha', 'date'), 
    Field('sexo', 'integer'), 
    Field('preferente', 'integer'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('directorio_auxiliar', 
    Field('id', 'integer'), 
    Field('registro', 'datetime'), 
    Field('doc_id', 'string'), 
    Field('telefono', 'string'), 
    Field('tel_prio', 'integer'), 
    Field('fax', 'string'), 
    Field('fax_prio', 'integer'), 
    Field('email', 'string'), 
    Field('ema_prio', 'integer'), 
    Field('web', 'string'), 
    Field('web_prio', 'integer'), 
    Field('contacto', 'string'), 
    Field('con_prio', 'integer'), 
    Field('telefono_c', 'string'), 
    Field('tec_prio', 'integer'), 
    Field('email_c', 'string'), 
    Field('emc_prio', 'integer'), 
    migrate=False)

#--------
db.define_table('documentos_comerciales', 
    Field('id', 'integer'), 
    Field('registro', 'datetime'), 
    Field('modo', 'integer'), 
    Field('documento', 'integer'), 
    Field('doc_reg', 'string'), 
    Field('nombre', 'string'), 
    Field('pv', 'string'), 
    Field('caja', 'integer'), 
    Field('prefijo', 'string'), 
    Field('correlativo', 'integer'), 
    Field('sufijo', 'string'), 
    Field('copia', 'integer'), 
    Field('detalle', 'integer'), 
    Field('limite', 'integer'), 
    Field('impresion', 'integer'), 
    Field('impuestos', 'string'), 
    migrate=False)

#--------
db.define_table('documentos_identidad', 
    Field('id', 'string'), 
    Field('registro', 'datetime'), 
    Field('nombre', 'string'), 
    migrate=False)

#--------
db.define_table('docventa', 
    Field('registro', 'datetime'), 
    Field('id', 'integer'), 
    Field('pv', 'integer'), 
    Field('caja', 'integer'), 
    Field('fecha_vta', 'date'), 
    Field('tiempo', 'datetime'), 
    Field('n_doc_base', 'integer'), 
    Field('estado', 'string'), 
    Field('comprobante', 'integer'), 
    Field('cliente', 'string'), 
    Field('cv_ing', 'integer'), 
    Field('fp', 'integer'), 
    Field('vales', 'string'), 
    Field('sello', 'string'), 
    Field('codigo', 'string'), 
    Field('detalle', 'string'), 
    Field('precio', 'double'), 
    Field('cantidad', 'integer'), 
    Field('sub_total_bruto', 'double'), 
    Field('sub_total_impto', 'string'), 
    Field('sub_total_neto', 'double'), 
    Field('total', 'double'), 
    Field('detalle_impto', 'string'), 
    Field('total_neto', 'double'), 
    Field('mntsol', 'double'), 
    Field('mntdol', 'double'), 
    Field('cv_anul', 'integer'), 
    Field('imod', 'integer'), 
    Field('n_doc_sufijo', 'string'), 
    Field('n_doc_prefijo', 'string'), 
    Field('data_1', 'string'), 
    Field('fecha_vto', 'date'), 
    Field('condicion_comercial', 'integer'), 
    migrate=False)

#--------
db.define_table('empaques', 
    Field('registro', 'datetime'), 
    Field('empaque', 'string'), 
    Field('nombre', 'string'), 
    Field('posicion', 'integer'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('factores_merma', 
    Field('id', 'integer'), 
    Field('fecha', 'date'), 
    Field('cp', 'string'), 
    Field('codbarras', 'string'), 
    Field('valor', 'double'), 
    Field('modo', 'integer'), 
    migrate=False)

#--------
db.define_table('formas_pago', 
    Field('forma_pago', 'string'), 
    Field('registro', 'datetime'), 
    Field('nombre', 'string'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('generos', 
    Field('genero', 'string'), 
    Field('registro', 'datetime'), 
    Field('nombre', 'string'), 
    Field('posicion', 'integer'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('grupo_distribucion', 
    Field('grupo_distribucion', 'string'), 
    Field('registro', 'datetime'), 
    Field('turno', 'string'), 
    Field('descripcion', 'string'), 
    Field('prioridad', 'integer'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('impuestos', 
    Field('registro', 'datetime'), 
    Field('codigo', 'string'), 
    Field('abreviatura', 'string'), 
    Field('nombre', 'string'), 
    Field('valor', 'double'), 
    Field('modo', 'integer'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('maestro', 
    Field('codbarras', 'string'), 
    Field('registro', 'datetime'), 
    Field('pv', 'string'), 
    Field('grupo_venta', 'string'), 
    Field('articulo', 'string'), 
    Field('casa', 'string'), 
    Field('sub_casa', 'string'), 
    Field('genero', 'string'), 
    Field('sub_genero', 'string'), 
    Field('empaque', 'string'), 
    Field('sello', 'string'), 
    Field('sub_sello', 'string'), 
    Field('tipo', 'string'), 
    Field('catmod', 'string'), 
    Field('categoria', 'string'), 
    Field('status', 'string'), 
    Field('proveedor', 'string'), 
    Field('moneda', 'string'), 
    Field('precio', 'double'), 
    Field('modo_impuesto', 'integer'), 
    Field('impuesto', 'string'), 
    Field('nombre', 'string'), 
    Field('descripcion', 'string'), 
    Field('alias', 'string'), 
    Field('descuento', 'integer'), 
    Field('dependencia', 'integer'), 
    Field('unidad_medida_valor', 'double'), 
    Field('aux_num_data', 'integer'), 
    Field('stock_min', 'double'), 
    Field('stock_max', 'double'), 
    Field('reposicion', 'integer'), 
    Field('ventas_key', 'integer'), 
    Field('fecha', 'date'), 
    Field('unidad_medida', 'string'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('maestro_auxiliar', 
    Field('id', 'integer'), 
    Field('registro', 'datetime'), 
    Field('codbarras', 'string'), 
    Field('nombre', 'string'), 
    Field('valor', 'string'), 
    Field('prioridad', 'integer'), 
    migrate=False)

#--------
db.define_table('maestro_dependencias', 
    Field('id', 'integer'), 
    Field('registro', 'datetime'), 
    Field('pv', 'string'), 
    Field('modo', 'integer'), 
    Field('codbarras', 'string'), 
    Field('data', 'string'), 
    Field('estado', 'integer'), 
    Field('user_ing', 'integer'), 
    migrate=False)

#--------
db.define_table('maestro_descuentos', 
    Field('id', 'integer'), 
    Field('registro', 'datetime'), 
    Field('tiempo', 'datetime'), 
    Field('pv', 'string'), 
    Field('modo', 'integer'), 
    Field('codbarras', 'string'), 
    Field('descuento', 'double'), 
    Field('monto_req', 'double'), 
    Field('user_nivel', 'integer'), 
    Field('fecha_inicio', 'date'), 
    Field('hora_inicio', 'time'), 
    Field('fecha_fin', 'date'), 
    Field('hora_fin', 'time'), 
    Field('estado', 'integer'), 
    Field('user_ing', 'integer'), 
    migrate=False)

#--------
db.define_table('maestro_posiciones', 
    Field('registro', 'datetime'), 
    Field('modo', 'integer'), 
    Field('codbarras', 'string'), 
    Field('posicion', 'integer'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('maestro_proveedores', 
    Field('id', 'integer'), 
    Field('registro', 'datetime'), 
    Field('codbarras', 'string'), 
    Field('proveedor', 'string'), 
    Field('unidad_medida', 'string'), 
    migrate=False)

#--------
db.define_table('maestro_valores', 
    Field('id', 'integer'), 
    Field('registro', 'datetime'), 
    Field('tiempo', 'datetime'), 
    Field('pv', 'string'), 
    Field('codbarras', 'string'), 
    Field('precio', 'double'), 
    Field('user_ing', 'integer'), 
    migrate=False)

#--------
db.define_table('modos_logisticos', 
    Field('id', 'integer'), 
    Field('registro', 'datetime'), 
    Field('modo_logistico', 'string'), 
    Field('descripcion', 'string'), 
    migrate=False)

#--------
db.define_table('modos_pvr', 
    Field('id', 'integer'), 
    Field('tabla', 'string'), 
    Field('modo', 'integer'), 
    Field('descripcion', 'string'), 
    Field('modo_tabla', 'integer'), 
    migrate=False)

#--------
db.define_table('monedas', 
    Field('registro', 'datetime'), 
    Field('modo', 'integer'), 
    Field('codigo', 'string'), 
    Field('nombre', 'string'), 
    Field('simbolo', 'string'), 
    Field('orden', 'integer'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('operaciones_logisticas', 
    Field('operacion', 'string'), 
    Field('registro', 'datetime'), 
    Field('modo', 'integer'), 
    Field('descripcion', 'string'), 
    Field('operacion_relac', 'string'), 
    Field('almacen_relac', 'string'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('pedidos', 
    Field('id', 'integer'), 
    Field('registro', 'datetime'), 
    Field('fecha', 'date'), 
    Field('pv', 'string'), 
    Field('turno', 'string'), 
    Field('grupo_distribucion', 'string'), 
    Field('area', 'string'), 
    Field('genero', 'string'), 
    Field('tipo', 'integer'), 
    Field('user_req', 'string'), 
    Field('n_doc_prefijo', 'string'), 
    Field('n_doc_base', 'integer'), 
    Field('n_doc_sufijo', 'string'), 
    Field('codbarras_padre', 'string'), 
    Field('codbarras', 'string'), 
    Field('cantidad', 'double'), 
    Field('peso', 'double'), 
    Field('detalle', 'string'), 
    Field('modo', 'integer'), 
    Field('estado', 'integer'), 
    Field('user_ing', 'string'), 
    migrate=False)

#--------
db.define_table('pedidos_emergencia_produccion', 
    Field('id', 'integer'), 
    Field('registro', 'datetime'), 
    Field('fecha', 'date'), 
    Field('pv', 'string'), 
    Field('turno', 'string'), 
    Field('codbarras', 'string'), 
    Field('cantidad', 'double'), 
    Field('modo', 'integer'), 
    migrate=False)

#--------
db.define_table('pesos_operaciones', 
    Field('codbarras', 'string'), 
    Field('registro', 'datetime'), 
    Field('peso_neto', 'double'), 
    Field('peso_tara', 'double'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('pos_administracion', 
    Field('id', 'integer'), 
    Field('registro', 'datetime'), 
    Field('pv', 'string'), 
    Field('caja', 'integer'), 
    Field('user_ing', 'string'), 
    Field('user_out', 'string'), 
    Field('apertura', 'datetime'), 
    Field('cierre', 'datetime'), 
    migrate=False)

#--------
db.define_table('produccion_datos', 
    Field('id', 'integer'), 
    Field('fecha', 'date'), 
    Field('turno', 'string'), 
    Field('grupo_distribucion', 'string'), 
    Field('pv', 'string'), 
    Field('codbarras', 'string'), 
    Field('codbarras_hijo', 'string'), 
    Field('cantidad', 'double'), 
    Field('modo', 'integer'), 
    migrate=False)

#--------
db.define_table('produccion_derivados', 
    Field('id', 'integer'), 
    Field('registro', 'datetime'), 
    Field('modo', 'integer'), 
    Field('turno', 'string'), 
    Field('tipo', 'integer'), 
    Field('cp_base', 'string'), 
    Field('cp_aux', 'string'), 
    Field('user_ing', 'string'), 
    Field('fecha', 'date'), 
    Field('n_doc_prefijo', 'string'), 
    Field('n_doc_base', 'string'), 
    Field('n_doc_sufijo', 'string'), 
    Field('codbarras', 'string'), 
    Field('ing_produccion', 'double'), 
    Field('ing_traslado', 'double'), 
    Field('ing_varios', 'double'), 
    Field('sal_ventas', 'double'), 
    Field('sal_merma', 'double'), 
    Field('sal_consumo_int', 'double'), 
    Field('sal_traslado', 'double'), 
    Field('sal_varios', 'double'), 
    migrate=False)

#--------
db.define_table('produccion_estadistica', 
    Field('id', 'integer'), 
    Field('fecha', 'date'), 
    Field('turno', 'string'), 
    Field('pv', 'string'), 
    Field('codbarras_abuelo', 'string'), 
    Field('codbarras_padre', 'string'), 
    Field('codbarras_hijo', 'string'), 
    Field('cantidad_abuelo', 'double'), 
    Field('cantidad_padre', 'double'), 
    Field('porcentaje_padre', 'double'), 
    Field('cantidad_hijo', 'double'), 
    Field('porcentaje_hijo', 'double'), 
    Field('modo', 'integer'), 
    Field('porcentaje_general', 'double'), 
    migrate=False)

#--------
db.define_table('produccion_pedidos', 
    Field('id', 'integer'), 
    Field('registro', 'datetime'), 
    Field('fecha', 'date'), 
    Field('pv', 'string'), 
    Field('turno', 'string'), 
    Field('modo', 'integer'), 
    Field('codbarras', 'string'), 
    Field('cantidad', 'double'), 
    migrate=False)

#--------
db.define_table('produccion_planeamiento', 
    Field('id', 'integer'), 
    Field('registro', 'datetime'), 
    Field('fecha', 'date'), 
    Field('codbarras_padre', 'string'), 
    Field('codbarras', 'string'), 
    Field('codbarras_hijo', 'string'), 
    Field('cantidad_prod', 'double'), 
    Field('condicion_pedido', 'string'), 
    Field('grupo_distribucion', 'string'), 
    Field('cp', 'string'), 
    Field('turno', 'string'), 
    migrate=False)

#--------
db.define_table('produccion_planeamiento_aux', 
    Field('id', 'integer'), 
    Field('registro', 'datetime'), 
    Field('fecha', 'date'), 
    Field('codbarras', 'string'), 
    Field('cantidad_prod', 'double'), 
    Field('condicion_pedido', 'string'), 
    Field('grupo_distribucion', 'string'), 
    Field('cp', 'string'), 
    Field('turno', 'string'), 
    migrate=False)

#--------
db.define_table('produccion_rendimiento', 
    Field('id', 'integer'), 
    Field('registro', 'datetime'), 
    Field('fecha', 'date'), 
    Field('turno', 'string'), 
    Field('modo', 'integer'), 
    Field('tipo', 'integer'), 
    Field('codbarras', 'string'), 
    Field('cantidad', 'double'), 
    Field('masa', 'string'), 
    Field('peso', 'double'), 
    Field('temperatura', 'double'), 
    Field('hora_inicial', 'time'), 
    Field('hora_final', 'time'), 
    migrate=False)

#--------
db.define_table('promociones', 
    Field('id', 'integer'), 
    Field('registro', 'datetime'), 
    Field('pv', 'integer'), 
    Field('codigo', 'string'), 
    Field('nombre', 'string'), 
    Field('porcentaje', 'double'), 
    Field('valor', 'double'), 
    Field('modo', 'integer'), 
    Field('codbarras', 'string'), 
    Field('cantidad', 'integer'), 
    Field('limite', 'integer'), 
    Field('cond_modo', 'integer'), 
    Field('cond_valor', 'integer'), 
    Field('cond_fecha_inic', 'date'), 
    Field('cond_hora_inic', 'time'), 
    Field('cond_fecha_term', 'date'), 
    Field('cond_hora_term', 'time'), 
    Field('estado', 'integer'), 
    migrate=False)

#--------
db.define_table('puntos_venta', 
    Field('codigo', 'string'), 
    Field('registro', 'datetime'), 
    Field('nombre', 'string'), 
    Field('distrito', 'string'), 
    Field('direccion', 'string'), 
    Field('posicion', 'integer'), 
    Field('posicion2', 'integer'), 
    Field('alias', 'string'), 
    Field('cab1', 'string'), 
    Field('cab2', 'string'), 
    Field('cab3', 'string'), 
    Field('cab4', 'string'), 
    Field('impt', 'string'), 
    Field('modimp', 'integer'), 
    Field('modmon', 'integer'), 
    Field('moneda', 'string'), 
    Field('wincha', 'string'), 
    Field('money_drawer', 'string'), 
    Field('area', 'integer'), 
    Field('replic_srv', 'string'), 
    Field('replic_db', 'string'), 
    Field('replic_user', 'string'), 
    Field('replic_passwd', 'string'), 
    Field('prodimp', 'string'), 
    Field('prodkey', 'string'), 
    Field('facmerma', 'double'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('puntos_venta_grupos', 
    Field('id', 'integer'), 
    Field('cp', 'string'), 
    Field('grupo_distribucion', 'string'), 
    Field('turno', 'string'), 
    Field('porcentaje', 'double'), 
    Field('codbarras', 'string'), 
    Field('modo', 'integer'), 
    migrate=False)

#--------
db.define_table('puntos_venta_relaciones', 
    Field('id', 'integer'), 
    Field('registro', 'datetime'), 
    Field('pv_padre', 'string'), 
    Field('pv_hijo', 'string'), 
    Field('modo', 'integer'), 
    migrate=False)

#--------
db.define_table('puntos_venta_satelites', 
    Field('registro', 'datetime'), 
    Field('pv_padre', 'string'), 
    Field('pv_hijo', 'string'), 
    Field('modo', 'integer'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('recetas', 
    Field('id', 'integer'), 
    Field('registro', 'datetime'), 
    Field('codbarras_padre', 'string'), 
    Field('cantidad', 'double'), 
    Field('codbarras_hijo', 'string'), 
    Field('modo', 'integer'), 
    Field('estado', 'integer'), 
    Field('orden', 'integer'), 
    migrate=False)

#--------
db.define_table('relaciones', 
    Field('id', 'integer'), 
    Field('registro', 'datetime'), 
    Field('codbarras_padre', 'string'), 
    Field('codbarras_hijo', 'string'), 
    Field('modo', 'integer'), 
    Field('orden', 'integer'), 
    migrate=False)

#--------
db.define_table('rendimientos_sintesis', 
    Field('id', 'integer'), 
    Field('fecha', 'date'), 
    Field('turno', 'string'), 
    Field('tipo', 'integer'), 
    Field('cantidad', 'double'), 
    Field('peso', 'double'), 
    Field('merma', 'double'), 
    Field('rendimiento', 'double'), 
    migrate=False)

#--------
db.define_table('reportes_configuracion', 
    Field('id', 'integer'), 
    Field('codigo_reporte', 'string'), 
    Field('detalle_reporte', 'string'), 
    Field('turno', 'string'), 
    Field('pv', 'string'), 
    Field('grupo_distribucion', 'string'), 
    Field('modo', 'integer'), 
    Field('codigo_dato', 'string'), 
    Field('array', 'string'), 
    Field('codbarras_abuelo', 'string'), 
    Field('codbarras_padre', 'string'), 
    Field('codbarras_hijo', 'string'), 
    Field('descripcion', 'string'), 
    Field('posicion', 'integer'), 
    migrate=False)

#--------
db.define_table('rubros', 
    Field('rubro', 'string'), 
    Field('registro', 'datetime'), 
    Field('nombre', 'string'), 
    Field('descripcion', 'string'), 
    Field('posicion', 'integer'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('sellos', 
    Field('registro', 'datetime'), 
    Field('sello', 'string'), 
    Field('nombre', 'string'), 
    Field('posicion', 'integer'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('status', 
    Field('registro', 'datetime'), 
    Field('status', 'string'), 
    Field('nombre', 'string'), 
    Field('posicion', 'integer'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('sub_casas', 
    Field('registro', 'datetime'), 
    Field('sub_casa', 'string'), 
    Field('nombre', 'string'), 
    Field('posicion', 'integer'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('sub_generos', 
    Field('sub_genero', 'string'), 
    Field('genero', 'string'), 
    Field('registro', 'datetime'), 
    Field('nombre', 'string'), 
    Field('posicion', 'integer'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('sub_sellos', 
    Field('registro', 'datetime'), 
    Field('sub_sello', 'string'), 
    Field('nombre', 'string'), 
    Field('posicion', 'integer'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('tablas_modos', 
    Field('id', 'integer'), 
    Field('tabla', 'string'), 
    Field('modo', 'string'), 
    Field('descripcion', 'string'), 
    migrate=False)

#--------
db.define_table('tipos', 
    Field('registro', 'datetime'), 
    Field('tipo', 'string'), 
    Field('nombre', 'string'), 
    Field('posicion', 'integer'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('tipos_cambio', 
    Field('id', 'integer'), 
    Field('registro', 'datetime'), 
    Field('moneda', 'string'), 
    Field('area', 'string'), 
    Field('modo', 'integer'), 
    Field('fecha', 'date'), 
    Field('hora', 'time'), 
    Field('valor', 'double'), 
    Field('user_ing', 'string'), 
    migrate=False)

#--------
db.define_table('transferencias_produccion', 
    Field('id', 'integer'), 
    Field('codbarras', 'string'), 
    Field('descripcion', 'string'), 
    Field('total', 'integer'), 
    Field('transferencia', 'integer'), 
    Field('produccion', 'integer'), 
    Field('turno', 'string'), 
    Field('fecha', 'date'), 
    migrate=False)

#--------
db.define_table('transportistas', 
    Field('codigo', 'string'), 
    Field('emp_doc_id', 'string'), 
    Field('doc_id', 'string'), 
    Field('nombres', 'string'), 
    Field('apellidos', 'string'), 
    Field('ubigeo', 'string'), 
    Field('direccion', 'string'), 
    Field('posicion', 'integer'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('turnos', 
    Field('turno', 'string'), 
    Field('registro', 'datetime'), 
    Field('descripcion', 'string'), 
    Field('hora_inicio', 'time'), 
    Field('hora_fin', 'time'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('ubigeo_departamentos', 
    Field('departamento', 'string'), 
    Field('descripcion', 'string'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('ubigeo_detalle', 
    Field('departamento', 'string'), 
    Field('provincia', 'string'), 
    Field('ubigeo', 'string'), 
    Field('descripcion', 'string'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('ubigeo_provincias', 
    Field('departamento', 'string'), 
    Field('provincia', 'string'), 
    Field('descripcion', 'string'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('unidades_medida', 
    Field('codigo', 'string'), 
    Field('descripcion', 'string'), 
    Field('modo', 'integer'), 
    Field('abreviatura_origen', 'string'), 
    Field('abreviatura_destino', 'string'), 
    Field('factor', 'double'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('usuarios', 
    Field('cv', 'string'), 
    Field('registro', 'datetime'), 
    Field('usuario', 'string'), 
    Field('password', 'string'), 
    Field('apellidos', 'string'), 
    Field('doc_id', 'string'), 
    Field('nombres', 'string'), 
    Field('cargo', 'string'), 
    Field('nivel', 'integer'), 
    Field('autorizacion', 'string'), 
    Field('almacen', 'string'), 
    Field('area', 'string'), 
    Field('articulo', 'string'), 
    Field('backup', 'string'), 
    Field('casa', 'string'), 
    Field('categoria', 'string'), 
    Field('comprobante', 'string'), 
    Field('condicion', 'string'), 
    Field('corden', 'string'), 
    Field('cuenta', 'string'), 
    Field('delivery', 'string'), 
    Field('directorio', 'string'), 
    Field('docventa', 'string'), 
    Field('fpago', 'string'), 
    Field('genero', 'string'), 
    Field('gventa', 'string'), 
    Field('indentificacion', 'string'), 
    Field('lista', 'string'), 
    Field('ologistica', 'string'), 
    Field('pedido', 'string'), 
    Field('produccion_derivados', 'string'), 
    Field('pventa', 'string'), 
    Field('ralmacen', 'string'), 
    Field('receta', 'string'), 
    Field('relacion', 'string'), 
    Field('rubro', 'string'), 
    Field('sellos', 'string'), 
    Field('status', 'string'), 
    Field('subgenero', 'string'), 
    Field('tcambio', 'string'), 
    Field('usuarios', 'string'), 
    Field('valor', 'string'), 
    Field('varauxiliar', 'string'), 
    Field('vardependencia', 'string'), 
    Field('vardescuentos', 'string'), 
    Field('varvalores', 'string'), 
    Field('variable', 'string'), 
    Field('valores', 'string'), 
    Field('iproducto', 'string'), 
    Field('cliente', 'string'), 
    Field('promocion', 'string'), 
    Field('clientes_preferentes', 'string'), 
    Field('unidadmedida', 'string'), 
    Field('produccion_wong', 'string'), 
    Field('produccion_dunkin', 'string'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('variaciones_derivados', 
    Field('id', 'integer'), 
    Field('registro', 'datetime'), 
    Field('codbarras', 'string'), 
    Field('tiempo_ini', 'datetime'), 
    Field('tiempo_fin', 'datetime'), 
    Field('porcentaje', 'double'), 
    Field('cp', 'string'), 
    Field('turno', 'string'), 
    Field('modo', 'string'), 
    migrate=False)

#--------
db.define_table('vehiculos', 
    Field('codigo', 'string'), 
    Field('doc_id', 'string'), 
    Field('registro', 'string'), 
    Field('marca', 'string'), 
    Field('modelo', 'string'), 
    Field('tipo', 'string'), 
    Field('caracteristicas', 'string'), 
    Field('posicion', 'integer'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('ventas_bancos_cuentas', 
    Field('registro', 'datetime'), 
    Field('codigo', 'string'), 
    Field('entidad', 'string'), 
    Field('moneda', 'string'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('ventas_bancos_operaciones', 
    Field('id', 'integer'), 
    Field('registro', 'datetime'), 
    Field('pv', 'integer'), 
    Field('fechav', 'date'), 
    Field('fechad', 'date'), 
    Field('banco', 'string'), 
    Field('monto', 'double'), 
    Field('cambio', 'double'), 
    Field('glosa1', 'string'), 
    Field('glosa2', 'string'), 
    Field('agencia', 'string'), 
    migrate=False)

#--------
db.define_table('ventas_grupos', 
    Field('codigo', 'string'), 
    Field('registro', 'datetime'), 
    Field('nombre', 'string'), 
    Field('atajo', 'string'), 
    Field('articulo', 'string'), 
    Field('casa', 'string'), 
    Field('sello', 'string'), 
    Field('genero', 'string'), 
    Field('subgenero', 'string'), 
    Field('categoria', 'string'), 
    Field('aux_data', 'integer'), 
    Field('id', 'integer'), 
    migrate=False)

#--------
db.define_table('ventas_operaciones', 
    Field('id', 'integer'), 
    Field('registro', 'datetime'), 
    Field('pv', 'string'), 
    Field('caja', 'integer'), 
    Field('tiempo', 'datetime'), 
    Field('n_doc_prefijo', 'string'), 
    Field('n_doc_base', 'string'), 
    Field('n_doc_sufijo', 'string'), 
    Field('estado', 'integer'), 
    Field('documento', 'integer'), 
    Field('cliente', 'string'), 
    Field('user_ing', 'integer'), 
    Field('user_null', 'integer'), 
    Field('forma_pago', 'string'), 
    Field('vales', 'string'), 
    Field('sello', 'string'), 
    Field('codbarras', 'string'), 
    Field('precio', 'double'), 
    Field('cantidad', 'integer'), 
    Field('total', 'double'), 
    Field('monto_local', 'double'), 
    Field('monto_dolar', 'double'), 
    Field('data_1', 'string'), 
    Field('data_2', 'string'), 
    Field('imod', 'integer'), 
    migrate=False)

#--------
db.define_table('ventas_resumen', 
    Field('registro', 'datetime'), 
    Field('id', 'integer'), 
    Field('pv', 'string'), 
    Field('fecha', 'date'), 
    Field('cnt_doc', 'integer'), 
    Field('total_neto', 'double'), 
    Field('total_igv', 'double'), 
    Field('total_srv', 'double'), 
    Field('total_bruto', 'double'), 
    Field('status', 'integer'), 
    Field('condicion_comercial', 'integer'), 
    migrate=False)


