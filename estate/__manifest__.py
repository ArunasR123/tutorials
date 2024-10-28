# -*- coding: utf-8 -*-
{
    'name': "Estate",
    'depends': ['base'],
    'application': True,
    'data': [
        'data/estate.property.type.csv',
        'data/estate_property_demo.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/property_users_view.xml',
        'views/estate_menus.xml',
    ],
    'category':'Real Estate/Brokerage'
}
