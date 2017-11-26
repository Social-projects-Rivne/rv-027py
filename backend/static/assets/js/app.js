$( document ).ready(function() {
    $('#deletion').on('show.bs.modal', function(e) {
        var elemId = $(e.relatedTarget).data('elem-id');
        var elemName = $(e.relatedTarget).data('elem-name');
        var funcName = $(e.relatedTarget).data('func-name');
        $(".modal-title").text("Confirm deletion of " + elemName);
        $("#delete-user").attr('action', '/'+funcName+'/' + elemId);
    });
});
