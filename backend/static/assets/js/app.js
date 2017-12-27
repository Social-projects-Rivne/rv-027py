$( document ).ready(function() {
    $('#deletion').on('show.bs.modal', function(e) {
        var elemId = $(e.relatedTarget).data('elem-id');
        var name = $(e.relatedTarget).data('name');
        var funcName = $(e.relatedTarget).data('func-name');
        var elemName = $(e.relatedTarget).data('elem-name');
        if (funcName == 'delete'){
            buttonText ='Delete';
            bodyText = "Please click "+buttonText+" button if you want to delete data.";
        }
        else {
            buttonText ='Restore';
            bodyText = "Please click "+buttonText+" button if you want to restore data.";
        }
        $(".modal-title").text("Confirm operation of \"" + name+"\"");
        $(".button-confirm").text(buttonText);
        $(".modal-body").text(bodyText);
        $("#delete-elem").attr('action', '/'+funcName+elemName+'/' + elemId);
    });

    $('#deleteModal').on('show.bs.modal', function(e) {
        var imageID =  $(e.relatedTarget).data('attach-id');
        $('input[name=attachment-id]').val(imageID);
    });
});
