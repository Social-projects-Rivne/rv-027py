$( document ).ready(function() {
    $('.get-request').on('click', function(e) {
      e.preventDefault();

      var search = $('#search-filter').data('search');
      var order_by = $(this).data('order-by');
      var reverse = $(this).data('reverse');
      var page = $(this).data('page');

      if (order_by === undefined){
        order_by = $('#search-filter').data('order');
      }
      if (reverse === undefined){
        reverse = $('#search-filter').data('reverse');
      }

      $("#id_search").val(search);
      $("#id_order_by").val(order_by);
      $("#id_reverse").val(reverse);
      $("#id_page").val(page);

      $('#search-filter').data('order',order_by);
      $('#submit-btn').click();
    });

    $('#search-filter').on('submit', function(e){
      order_by = $('#search-filter').data('order');
      $("#id_order_by").val(order_by);
    });
});