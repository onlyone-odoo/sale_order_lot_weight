# -*- coding: utf-8 -*-
from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    weight = fields.Float(
        string="Weight (KG)",
        digits="Product Unit of Measure",
        help="Weight in KG for this lot (editable only for new lots).",
    )

    # Related para mostrar peso de lote existente, editable para nuevos (vista controla readonly)
    weight = fields.Float(related="lot_id.weight", readonly=False, store=True)
