$( document ).ready(function() {
    $('#deletion').on('show.bs.modal', function(e) {
        var elemId = $(e.relatedTarget).data('elem-id');
        var issueId = $(e.relatedTarget).data('issue-id');
        var funcName = $(e.relatedTarget).data('func-name');
        var elemName = $(e.relatedTarget).data('elem-name');
        if (funcName == 'delete'){
            buttonText ='Delete';
            bodyText = "Please click "+buttonText+" button if you want to delete data.";
            $(".button-confirm").addClass('btn-danger');
        }
        else {
            buttonText ='Restore';
            bodyText = "Please click "+buttonText+" button if you want to restore data.";
            $(".button-confirm").addClass('btn-success');

        }
        $(".modal-title").text("Confirm operation");
        $(".button-confirm").text(buttonText);
        $(".modal-body").text(bodyText);
        $("#delete-comment").attr('action', '/'+funcName+elemName+'/'+ issueId +'/'+ elemId+'/');
    });
});
