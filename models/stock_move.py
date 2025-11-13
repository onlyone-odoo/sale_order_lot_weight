# -*- coding: utf-8 -*-
from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _action_done(self, cancel_backorder=False):
        """Copy weight from move_line to newly created lots."""
        weight_by_lot_name = {}
        for move in self:
            for ml in move.move_line_ids.filtered(lambda l: l.lot_name and l.weight):
                weight_by_lot_name[ml.lot_name] = ml.weight

        res = super()._action_done(cancel_backorder=cancel_backorder)

        if weight_by_lot_name:
            lots = (
                self.env["stock.lot"]
                .sudo()
                .search(
                    [
                        ("name", "in", list(weight_by_lot_name.keys())),
                        ("product_id", "in", self.mapped("product_id").ids),
                    ]
                )
            )
            for lot in lots:
                if lot.name in weight_by_lot_name:
                    lot.write({"weight": weight_by_lot_name[lot.name]})

        return res
