{
    'name': 'Custom Inventory & POS Reports',
    'version': '19.0.1.2.0',
    'category': 'Extra Tools',
    'summary': 'BIN Card & Day Sales Details Excel Reports',
    'description': """
        Generates comprehensive Excel reports:
        1. BIN CARD           - Full stock movement report
        2. BIN CARD Item Wise - Filtered stock movement per product
        3. Day Sales Details  - POS sales summary by outlet and payment type
    """,
    'author': 'VK DATA ApS',
    'website': 'https://vkdata.dk',
    'depends': ['stock', 'point_of_sale', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/bin_card_wizard_view.xml',
        'wizard/bin_card_item_wise_wizard_view.xml',
        'wizard/day_sales_details_wizard_view.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
