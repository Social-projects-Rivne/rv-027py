$( document ).ready(function() {
    $('#deletion').on('show.bs.modal', function(e) {
        var issueId = $(e.relatedTarget).data('issue-id');
        var name = $(e.relatedTarget).data('name');
        var funcName = $(e.relatedTarget).data('func-name');
        var elemName = $(e.relatedTarget).data('elem-name');
        if (elemName === 'delete'){
            buttonText ='Delete';
            bodyText = "Please click "+buttonText+" button if you want to delete data.";
        }
        else {
            buttonText ='Restore';
            bodyText = "Please click "+buttonText+" button if you want to restore data.";
        }
        $(".modal-title").text("Confirm operation \"" + name+"\"");
        $(".button-confirm").text(buttonText);
        $(".modal-body").text(bodyText);
        $("#delete-issue").attr('action', '/'+funcName+'/'+ issueId +'/'+ elemName +'/');
    });
});
