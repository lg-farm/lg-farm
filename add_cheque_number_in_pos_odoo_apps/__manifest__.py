{
    'name': 'Add Cheque Number In POS | Payment Register Through Cheque',
    'license': 'OPL-1',
    "author": "Fusion Matesolutions Odoo Apps",
    "description": """Register cheque information in pos, point of sale cheque payment, payment in cheque, pos cheque,
point of sale cheque book,pos check pos cheque information on pos,cheque information on point of sale,payment detail filled with cheque number,pos cheque number print,pos order report with cheque number,print order with check number,add bank detail in point of sale,pos bank detail with cheque number,cheque details point of sale,check print,cheque information on the receipt in pos print cheque number on pos receipt check info pos receipt cheque info pos payment with cheque info, display cheque in pos display cheque number in pos,pos cheque number: a unique identification code assigned to a point-of-sale (pos) transaction involving a cheque payment check information.this number helps track and verify the transaction, ensuring accuracy and transparency in financial records. cheque pos point of sale cheque cheque point of sale,pos check order,pos check info, pos check information on post cheque information on point of sale cheque details point of sale check print cheque information on the receipt in pos print cheque number on pos receipt check info pos receipt cheque info pos payment with cheque info. cheque configuration in pos,cheque collection in pos,pos cheque collection,order cheque collection,cheque collection,POS bank cheque payment Collect cheque details POS Cheque payment processing Bank cheque information entry Cheque payment options,Pos check information on pos cheque info on point of sale cheque details point of sales check information on receipt in pos cheque number on pos receipt check info pos order receipt cheque info pos payment cheque info point of sales cheque,pos cheque register,sale register cheque,pos register cheque,order register cheque,bank cheque detail,invoice bank cheque,customer bank cheque,bank cheque,invoice cheque,chequebook""",
    'summary': """Register cheque information in pos, point of sale cheque payment, payment in cheque, pos cheque,
               point of sale cheque book,pos check pos cheque information on pos,cheque information on point of sale,payment detail filled with cheque number,pos cheque number print,pos order report with cheque number,print order with check number,add bank detail in point of sale,pos bank detail with cheque number,cheque details point of sale,check print,cheque information on the receipt in pos print cheque number on pos receipt check info pos receipt cheque info pos payment with cheque info, display cheque in pos display cheque number in pos,pos cheque number: a unique identification code assigned to a point-of-sale (pos) transaction involving a cheque payment check information.this number helps track and verify the transaction, ensuring accuracy and transparency in financial records. cheque pos point of sale cheque cheque point of sale,pos check order,pos check info, pos check information on post cheque information on point of sale cheque details point of sale check print cheque information on the receipt in pos print cheque number on pos receipt check info pos receipt cheque info pos payment with cheque info. cheque configuration in pos,cheque collection in pos,pos cheque collection,order cheque collection,cheque collection,POS bank cheque payment Collect cheque details POS Cheque payment processing Bank cheque information entry Cheque payment options,Pos check information on pos cheque info on point of sale cheque details point of sales check information on receipt in pos cheque number on pos receipt check info pos order receipt cheque info pos payment cheque info point of sales cheque,pos cheque register,sale register cheque,pos register cheque,order register cheque,bank cheque detail,invoice bank cheque,customer bank cheque,bank cheque,invoice cheque,chequebook""",
    "website": "mailto:fusionmatesolutionsodooapps@gmail.com",
    "support": "mailto:fusionmatesolutionsodooapps@gmail.com",
    "depends": ["point_of_sale"],
    "data": ["views/config.xml",
             "views/pos_cheque.xml",
             ],
    'assets': {
        'point_of_sale._assets_pos': [
            'add_cheque_number_in_pos_odoo_apps/static/src/**/*.js',
            'add_cheque_number_in_pos_odoo_apps/static/src/**/*.xml'
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 11,
    'currency': 'USD',
    'images': ['static/description/banner.gif']
}