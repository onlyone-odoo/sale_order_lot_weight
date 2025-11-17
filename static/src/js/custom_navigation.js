

import { ListRenderer } from "@web/views/list/list_renderer";

ListRenderer.include({
    events: _.extend({}, ListRenderer.prototype.events, {
        'keydown .o_data_row td input': '_onKeydownInput',
    }),

    _onKeydownInput: function (ev) {
        this._super.apply(this, arguments);
        if (ev.key === 'Enter') {
            ev.stopPropagation();
            const $input = $(ev.target);
            const $td = $input.closest('td');
            const fieldName = $td.data('field-name') || $input.data('field-name');

            if (fieldName === 'lot_name') {
                // ENTER in lot_name -> focus weight in same row
                const $row = $input.closest('tr');
                const $weightInput = $row.find('input[name="weight"]');
                if ($weightInput.length) {
                    $weightInput.focus();
                    $weightInput.select();
                }
            } else if (fieldName === 'weight') {
                // ENTER in weight -> focus lot_name of next row or add new
                const $row = $input.closest('tr');
                const $nextRow = $row.next('tr.o_data_row');
                if ($nextRow.length) {
                    const $nextLotInput = $nextRow.find('input[name="lot_name"]');
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