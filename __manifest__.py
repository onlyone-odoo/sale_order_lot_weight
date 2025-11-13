{
    "name": "Sale Order Lot Weight",
    "summary": "Multi-lot selection per sale order line with weight-based pricing",
    "description": """
        Allows selecting multiple lots per sale order line, computes total weight
        as the sum of selected lots, and prices based on total weight (per KG).
        Ideal for variable-weight products like meat boxes, with full traceability in picking and accurate invoicing.
    """,
    "author": "Be OnlyOne",
    "maintainers": ["onlyone-odoo"],
    "website": "https://onlyone.odoo.com/",
    "category": "Sales",
    "version": "17.0.1.2.1",
    "depends": ["stock", "sale", "account"],
    "data": [
        "views/stock_lot_views.xml",
        "views/sale_order_views.xml",
        "views/stock_picking_views.xml",
        "views/account_invoice_views.xml",
        "views/sale_order_report_inherit.xml",
        "views/account_invoice_report_inherit.xml",
    ],
    "application": False,
    "installable": True,
}
