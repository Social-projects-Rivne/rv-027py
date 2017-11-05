function Users()
{
    $(".remove").click($.proxy(this.onRemoveClick, this));
}

Users.prototype.onRemoveClick = function (event)
{
    event.preventDefault();

    var target = $(event.target);
    var id = target.attr('data-user-id');
    var $this = this;

    bootbox.confirm("Are you sure?", function (confirmed) {
        if (confirmed) {
           $this.AJAXSetup(id);
        }});

};

Users.prototype.AJAXSetup = function (id) {

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
        url: '/deleteuser',
        data: {id: id},
        success: function (response) {
            bootbox.alert({
                message: response.message,
                size: 'small'
            });
            setTimeout(function () {
                location.reload(true);
            }, 1000);

        },
        error: function (response) {
            bootbox.alert({
                message: response.message,
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
