# -*- coding: utf-8 -*-
from odoo import fields, models


class StockLot(models.Model):
    _inherit = "stock.lot"

    weight = fields.Float(
        string="Weight (KG)",
        digits="Product Unit of Measure",
        help="The weight in kilograms of this lot (e.g., a box of meat).",
    )
