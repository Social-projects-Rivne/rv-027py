function InternalComments(userId)
{
    this.currentUserId = userId;
    this.form =  $('#comment-form');
    this.getUrl = '';
    this.storeUrl = '';
    this.commentInput = $('input[name=comment]');

    $('button.comments').on('click', $.proxy(this.onCommentsClick, this));
    this.form.submit($.proxy(this.sendComment, this))
}

InternalComments.prototype.onCommentsClick = function (e)
{
    this.getUrl = $(e.target).attr('data-url');
    this.storeUrl = $(e.target).attr('data-store-url');

    this.form.attr('action', this.storeUrl);

    this.getComments();
    this.clearErrors();

};

InternalComments.prototype.getComments = function ()
{
    var $this = this;

     $.get($this.getUrl, function (answer)
    {
        $('#internal-comments').show();
        var comments = $();

        answer['comments'].forEach(function (item)
        {
            var isMessageRight = $this.currentUserId == (item.user_id) ? 'right': '';
            var date  = new Date(item.date_public);
            var formattedDate = date.getHours() + ":" + date.getMinutes() + '/' + date.getDay() + '/' + date.getMonth() + '/' + date.getFullYear();
            comments = comments.add(
                            "<div class=\" "+ isMessageRight +  " direct-chat-msg \">\n" +
                               "<div class=\"direct-chat-info clearfix\">\n" +
                                 "<span class=\"direct-chat-name pull-left user-name\">" + item.user__alias + "</span>\n" +
                                 "<span class=\"direct-chat-timestamp pull-right time\">" + formattedDate + "</span>\n" +
                               "</div>\n" +
                               "<img class=\"direct-chat-img\" src=\"/static/images/avatar.png\" alt=\"Message User Image\">\n" +
                               "<div class=\"direct-chat-text message-text\">" + item.comment + "</div>\n" +
                            "</div>");
        });


       $(".direct-chat-messages").html(comments);
       $this.clearErrors();
    })
    .fail(function ()
    {
        $(".direct-chat-messages").html($('h2').text('Error loading comments'));
    });
};

InternalComments.prototype.sendComment = function (e)
{
    e.preventDefault();
    var $this = this;

    $.post(this.form.attr('action'), this.form.serialize(), function(answer)
        {
            $this.getComments();
            var messageContainer = $('.direct-chat-messages');
            messageContainer.animate({ scrollTop: messageContainer[0].scrollHeight}, 1000);

            $this.commentInput.val('');
        }
    )
     .fail(function (answer)
    {
       var errorText = JSON.parse(answer.responseJSON).comment[0].message;

       $this.commentInput.addClass('error');
       $('span.error').text(errorText);

    });
};


InternalComments.prototype.clearErrors = function()
{
    this.commentInput.removeClass('error');
    $('span.error').text('');
};
