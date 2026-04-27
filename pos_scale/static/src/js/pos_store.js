/** @odoo-module */

import { PosConfig } from "@point_of_sale/app/models/pos_config";
import { patch } from "@web/core/utils/patch";

patch(PosConfig.prototype, {
    get useProxy() {
        const result = (
            (this.is_posbox || this.is_jposbox) &&
            (this.iface_electronic_scale ||
                this.iface_print_via_proxy ||
                this.iface_scan_via_proxy ||
                this.iface_customer_facing_display_via_proxy)
        );

        return result;
    }
});
