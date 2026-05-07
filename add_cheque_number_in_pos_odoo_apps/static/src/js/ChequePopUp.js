/** @odoo-module */

import { _t } from "@web/core/l10n/translation";
import { Component, useRef } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { Dialog } from "@web/core/dialog/dialog";
import { useService } from "@web/core/utils/hooks";

export class ChequeInfoPopup extends Component {
    static template = "add_cheque_number_in_pos_odoo_apps.ChequeInfoPopup";
    static components = { Dialog };
    static components = {
        Dialog,
    };

    static props = {
        title: { type: String, optional: true },
        body: { type: String, optional: true },
        startingValue: { type: String, optional: true },
        list: { type: Array, optional: true },
        close: Function,
    };

    static defaultProps = {
        cancelText: _t("Cancel"),
        confirmText: _t("Ok-G"),
        title: '',
        body: '',
        list: [],
        startingValue: '',
    };

    setup() {
        super.setup();
        this.pos = usePos();
        this.ui = useService("ui");
        this.setChequeBankID = useRef('input-set_cheque_bank_id');
        this.setChequeOwnerName = useRef('input-set_cheque_owner_name');
        this.setChequeBankAccountNumber = useRef('input-set_cheque_bank_acc_no');
        this.setChequeNumber = useRef('input-set_cheque_number');
    }

    getValue() {
        var order = this.pos.getOrder();
        let selected_line = order.getSelectedPaymentline();
        var selectedBank = this.setChequeBankID.el.value || "";
        var bankObj = this.pos.models["res.bank"].getBy("id", parseInt(selectedBank));
        selected_line.set_cheque_bank_id(bankObj);
        selected_line.set_cheque_owner_name(this.setChequeOwnerName.el.value);
        selected_line.set_cheque_bank_acc_no(this.setChequeBankAccountNumber.el.value);
        selected_line.set_cheque_number(this.setChequeNumber.el.value);
        this.props.close();
    }
}