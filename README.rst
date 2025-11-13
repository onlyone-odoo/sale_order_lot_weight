===========
Sale Order Multi Lot Weight
===========
.. |badge1| image:: https://img.shields.io/badge/maturity-Stable-brightgreen
    :target: https://odoo-community.org/page/development-status
    :alt: Stable
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://onlyone.odoo.com/web/image/website/1/logo/OnlyOne%20Soft?unique=dccda5b
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
|badge1| |badge2| |badge3|
This module enables multi-lot selection per sale order line and computes pricing based on the total weight of selected lots in KG. It supports variable-weight products like meat boxes, with automatic stock picking splitting by lot for traceability and accurate invoicing.

**Table of contents**
.. contents::
   :local:

Configuration
=============
To configure this module, you need to:

1. For products (e.g., meat boxes), enable lot tracking on the product form (Inventory tab > Tracking > By Lots).
2. Set the Unit of Measure to 'Units' or 'Boxes', and define the price unit as per KG in pricelists or product forms.
3. Ensure stock locations have lot tracking enabled for accurate availability filtering in lot selection.

Usage
=====
1. Receive stock: Create a purchase order for boxes, receive in picking, and annotate exact weight in KG for each new lot in detailed operations.
2. Sell multiple boxes: Create a sale order, add a line for the product, select multiple lots via the 'Lots' widget (only free lots with stock >0 are available).
3. Automatic calculation: The line quantity updates to the number of lots, total weight sums the KG of selected lots, and subtotal adjusts to total_weight * price_unit (per KG).
4. Confirm order: The system splits stock moves into one per lot (qty=1, restricted to the specific lot) for precise reservation and traceability.
5. Picking and delivery: Validate the delivery order; each lot is assigned to its move line.
6. Invoice: Create invoice from the order; invoice lines show quantity = number of boxes, adjusted price_unit (average per box), and subtotal based on total weight for accurate billing.

Known issues / Roadmap
======================
* No known issues at this time.
* Roadmap: Wizard for bulk lot selection, multi-company lot filtering, and integration with advanced pricing rules for weight tiers.

Bug Tracker
===========
Bugs are tracked on `GitHub Issues <https://github.com/onlyone/sale_order_lot_weight/issues>`_. In case of trouble, please check there if your issue has already been reported. If you spotted it first, help us smash it by providing a detailed and welcomed feedback.

Credits
=======
Authors
~~~~~~~
* Be OnlyOne

Contributors
~~~~~~~~~~~~
* `Be OnlyOne. <https://onlyone.odoo.com/>`_

  * Matías Bressanello

Maintainers
~~~~~~~~~~~
This module is maintained by Be OnlyOne.