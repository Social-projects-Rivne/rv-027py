$( document ).ready(function() {
    $('#deletion').on('show.bs.modal', function(e) {
        var userId = $(e.relatedTarget).data('user-id');
        var userName = $(e.relatedTarget).data('user-name');
        $(".modal-title").text("Confirm deletion of " + userName);
        $("#delete-user").attr('href', '/deleteuser/' + userId);
    });
});