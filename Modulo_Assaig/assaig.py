# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from datetime import date
from dateutil import relativedelta
import time
from dateutil import parser
from types import *


class cliente(osv.osv):
	_name = "assaig.cliente"

	_description = "Tabla de clientes"

	_columns = {
		'name' : fields.char('DNI', size=12, help="Introducir DNI >>> 99.999.999-X", required=True),
		'nombre' : fields.char('Nombre',size=40, help="Nombre del cliente." ,required=True),
		'apellidos' : fields.char('Apellidos', size=100, help="Apellidos del cliente.", required=True),
		'telefono' : fields.char('Telefono',size=20, required=True),
		#'entrega' : fields.float('Entrega',size=6, help="Euros entregados por el cliente."),
		'entrega' : fields.float('Entrega',digits=(6,2), help="Euros entregados por el cliente."),
		'fecha_alta' : fields.date('Alta'),
		'observaciones' : fields.text('Observaciones', size_row=5, size_column=100),
		'cliente_reserva_id' : fields.one2many('assaig.reserva','cliente_id', 'Reserva cliente'),
		
	}

	_defaults = {
		'fecha_alta' : lambda *a : time.strftime("%Y-%m-%d"),
		'observaciones' : 'Escriba lo que proceda...',
		
	}

	_sql_constraints =[
			('name_unique','unique(name)','El DNI debe ser único'),
	]

	_order = "apellidos"
	
class mesa(osv.osv):
	_name ="assaig.mesa"

	_description ="Tabla de mesas"

	_columns = {
		'name' : fields.char('Codigo', size=7, help="Por ejemplo: MESA-XX", required=True),
		'plazas' : fields.integer('Plazas',size=2, help="Numero de comensales.", required=True),
		'disponible': fields.selection([('si','Si'),('no','No')],'Disponible', required=False),
		'disponible2' : fields.boolean('Disponible'),
		'mesa_reserva_id' : fields.one2many('assaig.reserva','mesa_id','Reserva mesa'),
	}

	_defaults = {
		'name' : 'MESA-0',
	}

	_sql_constraints = {
		('name_unique','unique(name)','El código de la mesa debe ser único.'),
	}

class reserva(osv.osv):
	def mostrar_nombre_apellidos( self, cr, uid, ids, fields, arg, context):
		resultado = cr.execute('SELECT DISTINCT nombre, apellidos '\
                    'FROM assaig_cliente '\
                    'WHERE name LIKE \'21672532T\'')	
		return resultado


	_name="assaig.reserva"

	_description="Tabla de reservas"

	_columns ={

		'fecha_alta' : fields.date('Alta', required=True),
		'fecha_todo' : fields.datetime('Todo'),	
		'cliente_id' : fields.many2one('assaig.cliente','Cliente Seleccionado', select=True, required=True),
		'mesa_id' : fields.many2one('assaig.mesa','Mesa Seleccionada', select=True, required=True),
		
	}	

	_sql_constraints = {
		('fecha_alta_unique','unique(fecha_lata','Una mesa no puede ser reservada el mismo día.'),
	}	

	
cliente()
mesa()
reserva()
	
