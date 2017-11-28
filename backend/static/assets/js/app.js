$( document ).ready(function() {
    $('#deletion').on('show.bs.modal', function(e) {
        var elemId = $(e.relatedTarget).data('elem-id');
        var elemName = $(e.relatedTarget).data('elem-name');
        var funcName = $(e.relatedTarget).data('func-name');
        if (funcName == 'deleteissue'){
            buttonText ='Delete';
            bodyText = "Please click "+buttonText+" button if you want to delete data.";
        }
        else {
            buttonText ='Restore';
            bodyText = "Please click "+buttonText+" button if you want to restore data.";
        }
        $(".modal-title").text("Confirm operation of " + elemName);
        $(".button-confirm").text(buttonText);
        $(".modal-body").text(bodyText);
        $("#delete-user").attr('action', '/'+funcName+'/' + elemId);
    });

    $('.table-row').click(function() {
        window.document.location = $(this).data('href');
    });
});
