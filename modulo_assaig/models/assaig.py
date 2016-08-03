# -*- coding: utf-8 -*-

from openerp.osv import osv, fields, orm
from datetime import date
from dateutil import relativedelta
import time
from dateutil import parser
from types import *
# Para mensajes de log
import logging
_logger = logging.getLogger(__name__)
# Precisión para la entrega
#import openerp.addons.decimal_precision as dp
from openerp.exceptions import ValidationError
#from openerp import models, fields, api, exceptions


class cliente(osv.osv):

	def _nom_apell_fnc(self, cr, uid, ids, fields, args, context):
		res = {}
		for r in self.browse(cr, uid, ids, context=context):
		#	res[r.id] = "%s, %s" % (r.apellidos, r.nombre)
			res[r.id] = "%s %s" % (r.nombre, r.apellidos)
		return res

	_name = "assaig.cliente"
	_rec_name = "name"
	_description = "Tabla Mod. de clientes"

	_columns = {
		'nombre' : fields.char('Nombre',size=20, help="Nombre del cliente." ,required=True),
		'apellidos' : fields.char('Apellidos', size=35, help="Apellidos del cliente.", required=True),
		'telefono' : fields.integer('Teléfono', size=9, 
			help="Ejemplo >>> Teléfono 999999999", required=True),
		'movil' : fields.integer('Móvil', size=9, help="Ejemplo >>> Móvil 999999999", required=True),
		'fecha_alta' : fields.date('Alta'),
		'observaciones' : fields.text('Observaciones', size_row=4, size_column=100, help="Anotaciones sobre el cliente"),
		'cliente_reserva_id' : fields.one2many('assaig.reserva','cliente_id', 'Reserva cliente'),
		'name' : fields.function(_nom_apell_fnc, type="char", size=140, string="Nombre y Apellidos", readonly=True),
		'situacion' : fields.selection([('activo','Activo'),('baja','Baja'),
			('moroso','Moroso')], string="Situación del cliente"),
	}

	_defaults = {
		'fecha_alta' : lambda *a : time.strftime("%Y-%m-%d"),
		'situacion' : 'activo',
	}

	_sql_constraints = [
		('nombre_unique','UNIQUE(nombre,apellidos)','El cliente ya existe'),
	]

	_order = "apellidos, nombre"


class mesa(osv.osv):

	def _codigo_plazas_fnc(self, cr, uid, ids, fields, args, context):
		res = {}
		for r in self.browse(cr, uid, ids, context=context):
			res[r.id] = "%s %sp" % (r.codigo, r.comensales)
		return res	

	_name = "assaig.mesa"
	_rec_name = "name"
	_description = "Tabla Mod. de mesas"

	_columns = {
		'codigo' : fields.char('Código', size=7, help="Ejemplo >>> MESA-XX", required=True),
		'ubicacion' : fields.selection([
			('comedor','Comedor'),('terraza','Terraza')], 'Ubicación', required=True),
		'foto_mesa' : fields.binary('Foto', help="Añadir imagen según comensales.",required=False),
		'comensales' : fields.integer('Comensales',size=2, help="Numero de comensales\nMínimo 1 persona.", required=True),
		'estado': fields.selection([('disponible','Disponible'),('no_disponible','No disponible')],'Estado', required=True),
		'observaciones' : fields.text('Observaciones', size_row=2, size_colum=50),
		'mesa_reserva_id' : fields.one2many('assaig.reserva','mesa_id','Reserva mesa'),
		'name' : fields.function(_codigo_plazas_fnc,type="char", size=11, string="Referencia", readonly=True),
	}

	_defaults = {
		'codigo' : 'MESA-0',
		'comensales' : 4,
	}

	_sql_constraints = {
		('codigo_unique','UNIQUE(codigo)','La mesa ya existe.'),
	}

class reserva(osv.osv):

	def anula_reserva_f(self, cr, uid, ids, context=None):
		cambiar_valor = 'anulada'
		reserva_id = self.pool('assaig.reserva').search(cr,uid,[('state','=','pendiente')])
		self.write(cr,uid,reserva_id[0],{'state': cambiar_valor}, context = context)
		return True

	def activa_reserva_f(self, cr, uid, ids, context=None):
		cambiar_valor = 'pendiente'
		reserva_id = self.pool('assaig.reserva').search(cr,uid,[('state','=','anulada')])
		self.write(cr,uid,reserva_id[0],{'state': cambiar_valor}, context = context)
		return True

	def servir_reserva_f(self, cr, uid, ids, context=None):
		cambiar_valor = 'servida'
		reserva_id = self.pool('assaig.reserva').search(cr,uid,[('state','=','pendiente')])
		self.write(cr,uid,reserva_id[0],{'state': cambiar_valor}, context = context)
		return True

	def cambia_reserva_f(self, cr, uid, ids, context=None):
		cambiar_valor = 'pendiente'
		reserva_id = self.pool('assaig.reserva').search(cr,uid,[('state','=','servida')])
		self.write(cr,uid,reserva_id[0],{'state': cambiar_valor}, context = context)
		return True

	_name = "assaig.reserva"
	_rec_name = "mesa_id"
	_description = "Tabla Mod. de reservas"

	_columns = {
		'tipo_reserva' : fields.selection([
			('en persona','En persona'),
			('movil','Móvil'),
			('telefono','Teléfono'),
			('email','Email')],
			'Tipo de Reserva' ,required=True),
		'entrega' : fields.float('Entrega',digits=(6,2), help="Euros entregados por el cliente."),
		#'entrega' : fields.float('Entrega',digits_compute=dp.get_precision('Entrega'), help="Euros entregados por el cliente."),
		'comensales' : fields.integer('Comensales',digits=(2), help="Numero de comensales.\nMínimo 2.", required=True),
		'fecha_todo' : fields.datetime('Fecha reserva', required=True),
		'observaciones' : fields.text('Observaciones', size_row=5, size_column=100),	
		'cliente_id' : fields.many2one('assaig.cliente','Cliente', select=True, required=True, domain="['&',('situacion','!=','moroso'),('situacion','=','activo')]"),
		'mesa_id' : fields.many2one('assaig.mesa','Mesa', select=True, required=True, domain="[('estado','=','disponible')]"),
		'state' : fields.selection([('pendiente','Pendiente'),
			('servida','Servida'),('anulada','Anulada')],'Estado',required=True),
	}	

	_defaults = {
		'comensales' : 2,
		'state' : 'pendiente',
	}

	_sql_constraints = {
		('cliente_id_unique','UNIQUE(cliente_id,mesa_id,fecha_todo)','La reserva ya existe.\nFecha idéntica'),
	}

	_order = "fecha_todo desc"	
	
class configuracion(osv.osv):

	def _total_comensales(self, cr, uid, ids, fields, args, context):
		res = {}
		for r in self.browse(cr, uid, ids, context=context):
			res[r.id] = "%s" % (r.superficie*4)
		return res

	_name = "assaig.configuracion"
	_rec_name = "name"
	_description = "Tabla Mod. de la configuracion"

	_columns = {
		'name' : fields.char('Nombre', size=50, required=True),
		'superficie' : fields.integer('Capacidad en mesas',	help="Mesa-base = 4 comensales"),
		'total_comensales' : fields.function(_total_comensales, string='Max. Comensales',type="integer", readonly=True), 
		'estado' : fields.boolean('Activo'),
	}

	_defaults = {
		'name' : 'Default',
		'superficie' : 06,
		'estado' : True,
	}

	_sql_constraints = {
		('name_unique','UNIQUE(name)','Esa configuración ya existe.')
	}

	
cliente()
mesa()
reserva()
configuracion()
	
