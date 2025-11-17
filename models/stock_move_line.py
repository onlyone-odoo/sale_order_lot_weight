# -*- coding: utf-8 -*-
from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    weight = fields.Float(
        string="Weight (KG)",
        digits="Product Unit of Measure",
        related="lot_id.weight",  # Related para mostrar peso de lote existente
        readonly=False,  # Editable siempre (vista controla con readonly)
        store=True,  # Stored para búsquedas y compute
        help="Weight in KG for this lot (editable only for new lots).",
    )
