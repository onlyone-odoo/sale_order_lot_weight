# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    lot_ids = fields.Many2many(
        "stock.lot",
        string="Lots",
        domain="[('product_id', '=', product_id), ('product_qty', '>', 0), ('company_id', '=', parent.company_id)]",
    )

    total_weight = fields.Float(
        string="Total Weight (KG)",
        compute="_compute_total_weight",
        store=False,  # No warnings de precompute
        digits="Product Unit of Measure",
    )

    @api.depends("lot_ids.weight")
    def _compute_total_weight(self):
        for line in self:
            line.total_weight = sum(lot.weight for lot in line.lot_ids)

    @api.onchange("lot_ids")
    def _onchange_lot_ids(self):
        """Update quantity, recompute amounts and force order totals + tax_totals refresh in UI."""
        self.product_uom_qty = len(self.lot_ids)
        self._compute_total_weight()
        self._compute_amount()
        if self.order_id:
            self.order_id._compute_amounts()
            # Force UI refresh of tax_totals widget with fresh totals
            return {
                "value": {
                    "tax_totals": self.order_id.tax_totals,
                }
            }

    @api.depends("total_weight", "price_unit", "product_uom_qty", "discount", "tax_id")
    def _compute_amount(self):
        """Price based on total weight (per KG), handling price_include correctly."""
        super()._compute_amount()
        for line in self:
            if line.total_weight > 0:
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                taxes = line.tax_id.compute_all(
                    price,
                    line.order_id.currency_id,
                    line.total_weight,
                    product=line.product_id,
                    partner=line.order_id.partner_id,
                )
                line.price_subtotal = taxes["total_excluded"]
                line.price_total = taxes["total_included"]
                line.price_tax = taxes["total_included"] - taxes["total_excluded"]

    def _convert_to_tax_base_line_dict(self):
        """Use total_weight as quantity for tax base when available (for tax_totals and PDF)."""
        res = super()._convert_to_tax_base_line_dict()
        if self.total_weight > 0:
            res["quantity"] = self.total_weight  # Tax base uses real weight
        return res

    def _prepare_procurement_values(self, group_id=False):
        vals = super()._prepare_procurement_values(group_id=group_id)
        if self.lot_ids:
            vals["restrict_lot_ids"] = [(6, 0, self.lot_ids.ids)]
        return vals
