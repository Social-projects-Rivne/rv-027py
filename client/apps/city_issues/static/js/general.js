setTimeout(function ()
{
    $('.messages').fadeOut('slow');
}, 10000);

$('.del-msg').on('click', function (e)
{
    e.preventDefault();
    $('.del-msg').parent().hide();
});