function Users()
{
    $(".action").click($.proxy(this.onActionClick, this));
}

Users.prototype.onActionClick = function (event)
{
    event.preventDefault();

    var target = $(event.target);
    var url = target.attr('data-url');
    var id = target.parent('td').attr('data-user-id');
    var $this = this;

    bootbox.confirm("Are you sure?", function (confirmed) {
        if (confirmed) {
           $this.AJAXSetup(url, id);
        }});

};

Users.prototype.AJAXSetup = function (url, id) {

    var csrftoken = $('meta[name=csrf-token]').attr('content');

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        }
    });

    $.ajax({
        type: "POST",
        url: url,
        data: {id: id},
        success: function (response) {
            bootbox.alert({
                message: response,
                size: 'small'
            });
            setTimeout(function () {
                location.reload(true);
            }, 1000);

        },
        error: function (response) {
            bootbox.alert({
                message: response,
                size: 'small'
            });
        }
    });

};

$(function()
{
    if($('#users-table').length > 0)
    {
        new Users();
    }
});
