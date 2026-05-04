/** @odoo-module */

import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { PosPayment } from "@point_of_sale/app/models/pos_payment";
import { patch } from "@web/core/utils/patch";

patch(PosOrder.prototype, {
    setup(options) {
        super.setup(...arguments);
    },

    get_total_qty(){
        var lines = this.payment_ids;
        var cheques = [];
        lines.map(function(line){
            if(line.cheque_number){
                cheques.push(line.cheque_number);
            }
        });
        let text = cheques.toString();
        return cheques;
    }
});

patch(PosPayment.prototype, {

    setup(options) {
        super.setup(...arguments);
        this.cheque_bank_id = options.cheque_bank_id || false;
        this.cheque_owner_name = options.cheque_owner_name || false;
        this.cheque_bank_acc_no = options.cheque_bank_acc_no || false;
        this.cheque_number = options.cheque_number || false;
    },

    export_for_printing() {
        const json = super.export_for_printing(...arguments);
        json.cheque_bank_id = this.cheque_bank_id;
        json.cheque_owner_name = this.cheque_owner_name;
        json.cheque_bank_acc_no = this.cheque_bank_acc_no;
        json.cheque_number = this.cheque_number;
        return json;
    },

    set_cheque_bank_id(cheque_bank_id) {
        this.cheque_bank_id = cheque_bank_id;
    },

    get_cheque_bank_id() {
        return this.cheque_bank_id
    },

    set_cheque_owner_name(cheque_owner_name) {
        this.cheque_owner_name = cheque_owner_name
    },

    get_cheque_owner_name() {
        return this.cheque_owner_name
    },

    set_cheque_bank_acc_no(cheque_bank_acc_no) {
        this.cheque_bank_acc_no = cheque_bank_acc_no
    },

    get_cheque_bank_acc_no() {
        return this.cheque_bank_acc_no
    },

    set_cheque_number(cheque_number) {
        this.cheque_number = cheque_number
    },

    get_cheque_number() {
        return this.cheque_number
    },

});
