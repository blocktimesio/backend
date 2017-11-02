(function($) {
  'use strict';
  $(document).ready(function() {
    $('#id_lock_btn').on('click', function(e) {
      $.get('lock/', function (e) {
        if ($(this).text().trim() === 'Lock') {
          $(this).text('Unlock');
        }
        else {
          $(this).text('Lock');
        }
      });
    });
  });
})(django.jQuery);