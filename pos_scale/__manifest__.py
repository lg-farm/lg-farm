# -*- coding: utf-8 -*-

{
    'name': 'POS Scale Integration',
    'category': 'Point of Sale',
    'summary': """Electronic Scale Integration for Odoo POS without IoT Box
            keywords: scale integration | electronic scale | weight-based pricing | retail scale | POS scale integration | product weight capture | real-time weight | grocery scale integration | produce scale integration | IoT box alternative | weight measurement system
               """,
    'description': """
            POS Scale Integration
            =====================
            Connect electronic scales directly to your Odoo Point of Sale without the need for an IoT Box. This module enables seamless weight-based product pricing, streamlining your retail operations.

            Features:
            ---------
            * No IoT Box Required: Connect electronic scales directly to Odoo POS via jIotBox.
            * Real-Time Weight Reading: Automatically capture product weights for accurate pricing.
            * Wide Compatibility: Works with most electronic scales that support standard communication protocols.
            * Easy Configuration: Simple setup through POS configuration settings.

            This module is ideal for retail businesses dealing with weight-based products such as groceries, produce, meat, and bulk items.
    """,
    'author': 'Dustin Mimbela',
    'version': '1.0',
    'depends': ['point_of_sale'],
    'data': [
        'views/pos_config_view.xml',
        'views/res_config_settings_view.xml',
        'views/pos_printer_view.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_scale/static/src/js/pos_store.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'images':['static/description/banner.gif'],
    'price': 100.0,
    'currency': 'EUR'
}
