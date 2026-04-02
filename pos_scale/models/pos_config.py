# -*- coding: utf-8 -*-
from odoo import api, fields, models

class PosConfig(models.Model):
    _inherit = 'pos.config'

    is_jposbox = fields.Boolean(string='jIoT Box', help='Connect devices using a jIoT Box')

    @api.model
    def _load_pos_data_read(self, records, config):
        read_records = super()._load_pos_data_read(records, config)
        # is_jposbox is already included in the read because super() reads all fields
        # No additional processing needed
        return read_records

    @api.onchange('is_jposbox')
    def _onchange_is_jposbox(self):
        if self.is_jposbox:
            self.is_posbox = False

    @api.onchange('is_posbox')
    def _onchange_is_posbox(self):
        if self.is_posbox:
            self.is_jposbox = False
