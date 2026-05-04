/** @odoo-module */

import { PaymentScreenPaymentLines } from "@point_of_sale/app/screens/payment_screen/payment_lines/payment_lines";
import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { _t } from "@web/core/l10n/translation";
import { ChequeInfoPopup } from "@add_cheque_number_in_pos_odoo_apps/js/ChequePopUp";


patch(PaymentScreenPaymentLines.prototype, {

    setup() {
        super.setup();
        this.pos = usePos();
    },

    get paymentLines() {
        return this.pos.getOrder().payment_ids;
    },

    async chequeBank(event) {
        this.dialog.add(ChequeInfoPopup, {
            list: this.pos.models["res.bank"].readAll(),
            title: _t("Cheque Information"),
        });
    },
});
