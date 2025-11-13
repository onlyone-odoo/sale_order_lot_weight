# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    total_weight = fields.Float(
        string="Total Weight (KG)",
        digits="Product Unit of Measure",
        compute="_compute_total_weight",
        store=True,
        help="Total weight in KG based on selected lots from sale order line.",
    )

    @api.depends("sale_line_ids.total_weight")
    def _compute_total_weight(self):
        """Compute total_weight from related sale_line_ids."""
        for line in self:
            line.total_weight = (
                sum(line.sale_line_ids.mapped("total_weight"))
                if line.sale_line_ids
                else 0.0
            )

    @api.model_create_multi
    def create(self, vals_list):
        """Adjust price_unit to average per box for multi-lot lines, keeping quantity=N boxes."""
        lines = super().create(vals_list)
        for line in lines.filtered("sale_line_ids"):
            total_weight = line.total_weight or sum(
                line.sale_line_ids.mapped("total_weight")
            )
            if total_weight > 0 and line.quantity > 0:
                original_price = line.price_unit
                average_price = original_price * (total_weight / line.quantity)
                line.with_context(skip_invoice_sync=True).write(
                    {"price_unit": average_price}
                )
        return lines
