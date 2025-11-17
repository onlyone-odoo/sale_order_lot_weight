odoo.define('sale_order_lot_weight.custom_navigation', function (require) {
    "use strict";

    var ListRenderer = require('web.ListRenderer');

    ListRenderer.include({
        events: _.extend({}, ListRenderer.prototype.events, {
            'keydown .o_data_row td input': '_onKeydownInput',
        }),

        _onKeydownInput: function (ev) {
            this._super.apply(this, arguments);
            if (ev.key === 'Enter') {
                ev.stopPropagation();
                var $input = $(ev.target);
                var $td = $input.closest('td');
                var fieldName = $td.data('field-name') || $input.data('field-name');
                var $row = $input.closest('tr');

                if (fieldName === 'lot_name') {
                    // ENTER in lot_name -> focus weight in same row
                    var $weightInput = $row.find('input[name="weight"]');
                    if ($weightInput.length) {
                        $weightInput.focus();
                        $weightInput.select();
                    }
                } else if (fieldName === 'weight') {
                    // ENTER in weight -> focus lot_name of next row or add new
                    var $nextRow = $row.next('tr.o_data_row');
                    if ($nextRow.length) {
                        var $nextLotInput = $nextRow.find('input[name="lot_name"]');
                        if ($nextLotInput.length) {
                            $nextLotInput.focus();
                            $nextLotInput.select();
                        }
                    } else {
                        // Add new line
                        this.trigger_up('add_line');
                    }
                }
            }
        },
    });
});