# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    "name": "Point Of Sale Cart Line Pricelist",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Point Of Sale",
    "license": "OPL-1",
    "summary": "POS Line Pricelist, point of sale line pricelist, pos pricelist, point of sale pricelist,point of sale product pricelist, pos product pricelist, pos cart line pricelist, point of sale order pricelist, pos order pricelist,pos different pricelist odoo",
    "description": """Using this module you can set the different pricelist for the pos order line. If you change the pricelist then the order line price will be changed according to the selected pricelist. Sometimes Required to hide price (minimum price or negotiable price) in the POS screen in case the customer is also in front of the pos screen. so we provide a code pricelist feature that displays the price in the encoded format in the pricelist popup. You can also set a minimum pricelist for the order line.""",
    "version": "0.0.1",
    "depends": ["base", "web", "point_of_sale"],
    "application": True,
    "data": ['views/res_config_settings.xml', ],
    'assets': {'point_of_sale._assets_pos': [
        "sh_pos_line_pricelist/static/src/scss/pos.scss",
        'sh_pos_line_pricelist/static/src/overrides/components/Orderline/orderline.xml',
        'sh_pos_line_pricelist/static/src/overrides/models/model.js',
        'sh_pos_line_pricelist/static/src/overrides/models/pos_store.js',
        'sh_pos_line_pricelist/static/src/overrides/components/Orderline/orderline.js',
        'sh_pos_line_pricelist/static/src/apps/pricelist_popup/pricelist_popup.js',
        'sh_pos_line_pricelist/static/src/apps/pricelist_popup/pricelist_popup.xml',
    ],
    },
    "images": ["static/description/background.png", ],

    "auto_install": False,
    "installable": True,
    "price": 59,
    "currency": "EUR"
}
