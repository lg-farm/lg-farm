# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models

class PosConfig(models.Model):
    """
    Inherits the 'pos.config' model to extend Point of Sale configuration
    with additional pricelist-related fields.
    """
    _inherit = 'pos.config'

    sh_pricelist_for_code = fields.Many2one(
        'product.pricelist',
        string="Code for the selected pricelist",
        help="Pricelist used as a code for identifying the selected pricelist."
    )
    sh_min_pricelist_value = fields.Many2one(
        'product.pricelist',
        string="Minimum value for pricelist",
        help="Minimum acceptable value defined by a pricelist."
    )
