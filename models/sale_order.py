# -*- coding: utf-8 -*-
from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends(
        "order_line.price_subtotal", "order_line.price_tax", "order_line.price_total"
    )
    def _compute_amounts(self):
        """Override to ensure amounts recompute correctly with custom line subtotals."""
        for order in self:
            order_lines = order.order_line.filtered(lambda x: not x.display_type)
            order.amount_untaxed = sum(order_lines.mapped("price_subtotal"))
            order.amount_tax = sum(order_lines.mapped("price_tax"))
            order.amount_total = order.amount_untaxed + order.amount_tax

    def _action_confirm(self):
        """Split moves into one per lot with qty=1 and correct restrict_lot_id for proper reservation."""
        res = super()._action_confirm()
        for line in self.order_line.filtered("lot_ids"):
            if line.product_uom_qty != len(line.lot_ids):
                line.product_uom_qty = len(line.lot_ids)  # Force qty = number of lots
            move = line.move_ids[0] if line.move_ids else self.env["stock.move"]
            moves = self.env["stock.move"]
            for lot in line.lot_ids:
                if moves:
                    new_move = move.copy(
                        {
                            "product_uom_qty": 1.0,
                            "restrict_lot_id": lot.id,
                        }
                    )
                else:
                    move.write(
                        {
                            "product_uom_qty": 1.0,
                            "restrict_lot_id": lot.id,
                        }
                    )
                    moves |= move
                moves |= new_move if "new_move" in locals() else move
            # Unlink extra moves if any
            extra = line.move_ids - moves
            extra.unlink()
        return res
