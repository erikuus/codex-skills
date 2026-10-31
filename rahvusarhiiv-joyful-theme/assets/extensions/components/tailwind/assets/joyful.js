/* Joyful Yii adapters. Requires the application's Yii-managed jQuery. */
(function ($) {
    'use strict';
    function scope(id) { return $(document.getElementById(id)); }
    function eventName(prefix, id) { return prefix + '.joyful' + id.replace(/[^a-zA-Z0-9]/g, '_'); }
    window.joyfulDropdown = function (options) {
        var form = scope(options.form), input = document.getElementById(options.input);
        var event = eventName('change', options.input);
        function update() {
            var selected = $(input).val();
            form.find('div').filter(function () { return this.classList.contains(options.area); }).each(function () {
                var area = $(this), active = this.classList.contains('selected_' + selected);
                area.toggle(active);
                area.find(':input').each(function () {
                    var field = $(this);
                    if (!active) {
                        if (field.data('joyfulDisabled') === undefined) field.data('joyfulDisabled', this.disabled);
                        this.disabled = true;
                    } else if (field.data('joyfulDisabled') !== undefined) {
                        this.disabled = field.data('joyfulDisabled');
                        field.removeData('joyfulDisabled');
                    }
                });
            });
        }
        form.off(event).on(event, function (e) { if (e.target.id === options.input) { input = e.target; update(); } });
        update();
    };
    window.joyfulToggle = function (options) {
        var form = scope(options.form), event = eventName('change', options.form + options.type);
        function update() {
            form.find('input').filter(function () { return this.type === options.type; }).each(function () {
                var input = this;
                $(this).siblings().filter(function () { return this.classList.contains(options.content); }).each(function () {
                    this.style.display = input.checked ? (this.classList.contains(options.inline) ? 'inline' : 'block') : 'none';
                });
            });
        }
        form.off(event).on(event, 'input', update);
        update();
    };
    window.joyfulGridAction = function (options) {
        var event = eventName('click', options.grid + '_' + options.column);
        var selector = 'a[data-joyful-column]';
        $(document).off(event, selector).on(event, selector, function (e) {
            var grid = document.getElementById(options.grid);
            if (!grid || $(this).attr('data-joyful-column') !== options.column || !$.contains(grid, this)) return;
            e.preventDefault();
            var link = $(this);
            if (link.data('joyfulBusy')) return;
            link.data('joyfulBusy', true).attr('aria-busy', 'true');
            $.ajax({type: 'POST', url: this.href, data: options.data, dataType: options.dataType || undefined})
                .done(function () { $.fn.yiiGridView.update(options.grid); })
                .fail(function (xhr) {
                    scope(options.grid).trigger('joyful:action-error', [xhr]);
                    window.alert(options.errorMessage);
                })
                .always(function () { link.removeData('joyfulBusy').removeAttr('aria-busy'); });
        });
    };
})(jQuery);
