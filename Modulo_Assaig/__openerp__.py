{
	'name' : "L'ASSAIG",
	'icon' : "/modulo_assaig/static/src/img/lassaig_logo_modulo.jpg",
	'image-icon' : "/modulo_assaig/static/src/img/icon.jpg",
	'version' : "05.15b",
	'author' : "Carlos Huelmo Vaquero",
	'website' : "https://moodle.cipfpbatoi.es",
	'category' : "Hosteleria",
	'summary' : "Proyecto de un módulo de hostelería.",
	'description' : """

Creación de un módulo en Odoo para gestionar las mesas
y permitir realizar reservas...		

DAM 2014-2015
=============

Creación de un website en odoo 8 para gestionar las mesas
y permitir realizar reservas...	

otras cosas
___________	

A tener en cuenta:
------------------
* Leer bootstrap: http://getbootstrap.com/css/
* Ver qweb en https://doc.openerp.com/trunk/web/qweb especialmente las directivas de q-web en https://doc.openerp.com/trunk/web/qweb/#defining-templates
* Probar css http://jsfiddle.net/h8SBh/1/

* Los reportes constan basicamente de:
    * Un registro en la clase de reportes (ir.actions.report.xml) que se puede crear con el atajo "<report". Se suelen crear todos los reportes de un modulo en el archivo "[nombre_de_modulo]_report.xml"
    * Cada reporte qweb tiene además vistas definidas, dichas vistas se suelen guardar en la carpeta views. Se crea un archivo para cada reporte
    * Si se requieren funcionalidades avanzadas, se pueden crear archivos .py que modifican el funcionamiento por defecto de los reportes, eso suele ir en la carpeta "reports" (solo archivos .py). En dicha carpeta se suelen almacenar también los cubos (su corresndiente .py y .xml)
    * Si se requiere de un wizard, tanto el .py como el .xml irían en la carpeta "wizard"

		""",
	'depends' : ['base'],
	'init_xml' : [],
	'demo_xml' : [],
	'update_xml' : [],
	'data' : [
		'security/model_data.xml',
		'security/assaig_security.xml',
		'security/ir.model.access.csv',
		'views/assaig_view.xml',
	],
	#'css': [
	#	'static/src/css/kanban_view.css',
	#],
	'installable' : True,
	'application' : True,
	'auto_install' : False,
}