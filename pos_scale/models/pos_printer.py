# -*- coding: utf-8 -*-
from odoo import fields, models

class PosPrinter(models.Model):
    _inherit = 'pos.printer'

    printer_type = fields.Selection(
        selection_add=[('jiot', 'Use a printer connected to the jIoT Box')],
        ondelete={'jiot': 'cascade'}
    )
