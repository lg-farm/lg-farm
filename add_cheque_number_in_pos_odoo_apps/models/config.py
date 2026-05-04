from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    cheque_information = fields.Boolean(string="Collects Cheque Information?")
    cheque_bank_id = fields.Many2one('res.bank')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    cheque_information = fields.Boolean(related='pos_config_id.cheque_information', readonly=False)
