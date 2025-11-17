# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    purchase_weight = fields.Float(
        string="Estimated Weight (KG)",
        digits="Product Unit of Measure",
        help="Estimated total weight in KG for this line (used for pricing per KG).",
    )

    @api.depends("purchase_weight", "price_unit", "product_qty", "discount", "taxes_id")
    def _compute_amount(self):
        """Override to compute price based on purchase_weight instead of quantity if applicable."""
        super()._compute_amount()
        for line in self:
            if line.purchase_weight > 0:
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                line.price_subtotal = price * line.purchase_weight
                taxes = line.taxes_id.compute_all(
                    price,
                    line.order_id.currency_id,
                    line.purchase_weight,
                    product=line.product_id,
                    partner=line.order_id.partner_id,
                )
                line.price_tax = sum(
                    t.get("amount", 0.0) for t in taxes.get("taxes", [])
                )
                line.price_total = line.price_subtotal + line.price_tax
            else:
                # Fall back to standard quantity-based calculation
                pass

    @api.onchange("purchase_weight")
    def _onchange_purchase_weight(self):
        """Trigger recompute of amounts on purchase_weight change."""
        self._compute_amount()
        if self.order_id:
            self.order_id._compute_amounts()
        return {}

    def _convert_to_tax_base_line_dict(self):
        """Use purchase_weight as quantity for tax base when available."""
        res = super()._convert_to_tax_base_line_dict()
        if self.purchase_weight > 0:
            res["quantity"] = self.purchase_weight  # Tax base uses estimated weight
        return res
