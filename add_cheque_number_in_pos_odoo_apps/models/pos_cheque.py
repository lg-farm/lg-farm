from odoo import api, fields, models


class PosPayment(models.Model):
    _inherit = "pos.payment"

    cheque_bank_id = fields.Many2one('res.bank', string="Bank")
    cheque_owner_name = fields.Char(string="Owner name")
    cheque_bank_acc_no = fields.Char(string="Bank Account", size=16)
    cheque_number = fields.Char(string="Cheque Number", digits=(16, 0))


class PosOrder(models.Model):
    _inherit = "pos.order"

    @api.model
    def _payment_fields(self, order, ui_paymentline):
        res = super(PosOrder, self)._payment_fields(order, ui_paymentline)
        res.update({
            'cheque_owner_name': ui_paymentline.get('cheque_owner_name', ""),
            'cheque_bank_id': ui_paymentline.get('cheque_bank_id', False),
            'cheque_bank_acc_no': ui_paymentline.get('cheque_bank_acc_no', ""),
            'cheque_number': ui_paymentline.get('cheque_number', ""),
        })
        return res


class ResBank(models.Model):
    _name = "res.bank"
    _inherit = ['res.bank', 'pos.load.mixin']

    @api.model
    def _load_pos_data_domain(self, data, config):
        return []

    @api.model
    def _load_pos_data_fields(self, config_id):
        return ['name', 'id']

    def _load_pos_data(self, data):
        fields = self._load_pos_data_fields(data['pos.config']['data'][0]['id'])
        banks = self.search_read([],fields)
        return {
            'data': banks,
            'fields': fields,
        }


class PosPaymentMethod(models.Model):
    _inherit = "pos.payment.method"

    cheque_information = fields.Boolean(string="Collects Cheque")

    @api.model
    def _load_pos_data_fields(self, config_id):
        rtn = super(PosPaymentMethod, self)._load_pos_data_fields(config_id)
        rtn.extend(['name', 'is_cash_count', 'use_payment_terminal', 'cheque_information'])
        return rtn


class PosSession(models.Model):
    _inherit = 'pos.session'

    @api.model
    def _load_pos_data_models(self, config_id):
        result = super(PosSession, self)._load_pos_data_models(config_id)
        result.append('res.bank')
        return result
