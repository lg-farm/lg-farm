# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_is_jposbox = fields.Boolean(
        related='pos_config_id.is_jposbox',
        readonly=False,
        string='jIoT Box'
    )
    
    @api.depends('pos_is_posbox', 'pos_is_jposbox', 'pos_config_id')
    def _compute_pos_iface_print_via_proxy(self):
        """Override to support jIoT Box"""
        for res_config in self:
            if not res_config.pos_is_posbox and not res_config.pos_is_jposbox:
                res_config.pos_iface_print_via_proxy = False
            else:
                res_config.pos_iface_print_via_proxy = res_config.pos_config_id.iface_print_via_proxy

    @api.depends('pos_is_posbox', 'pos_is_jposbox', 'pos_config_id')
    def _compute_pos_iface_scan_via_proxy(self):
        """Override to support jIoT Box"""
        for res_config in self:
            if not res_config.pos_is_posbox and not res_config.pos_is_jposbox:
                res_config.pos_iface_scan_via_proxy = False
            else:
                res_config.pos_iface_scan_via_proxy = res_config.pos_config_id.iface_scan_via_proxy

    @api.depends('pos_is_posbox', 'pos_is_jposbox', 'pos_config_id')
    def _compute_pos_iface_electronic_scale(self):
        """Override to support jIoT Box"""
        for res_config in self:
            if not res_config.pos_is_posbox and not res_config.pos_is_jposbox:
                res_config.pos_iface_electronic_scale = False
            else:
                res_config.pos_iface_electronic_scale = res_config.pos_config_id.iface_electronic_scale

    @api.depends('pos_iface_print_via_proxy', 'pos_config_id', 'pos_epson_printer_ip', 'pos_other_devices')
    def _compute_pos_iface_cashdrawer(self):
        """Override to support jIoT Box"""
        for res_config in self:
            if self._is_cashdrawer_displayed(res_config):
                res_config.pos_iface_cashdrawer = res_config.pos_config_id.iface_cashdrawer
            else:
                res_config.pos_iface_cashdrawer = False
