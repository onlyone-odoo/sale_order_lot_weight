# -*- coding: utf-8 -*-
from odoo import api, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.depends(
        "order_line.price_subtotal", "order_line.price_tax", "order_line.price_total"
    )
    def _compute_amounts(self):
        """Override to ensure amounts recompute correctly with custom line subtotals."""
        for order in self:
            order = order.with_company(order.company_id)
            order_lines = order.order_line.filtered(lambda x: not x.display_type)
            order.amount_untaxed = sum(order_lines.mapped("price_subtotal"))
            order.amount_tax = sum(order_lines.mapped("price_tax"))
            order.amount_total = order.amount_untaxed + order.amount_tax
