var zebra=function(){
    $('.content_post:odd').addClass('odd');
}

var boldItems=function(){
    $('.content_post').each(function(){
        var current=$(this);
        var link=$('.post_sig a', this).attr('href');
        current.html(current.html().replace(/(^\w+)/,'<a href="'+link+'">$1</a>'));
    });
}

$(function(){
        zebra();
        boldItems();
});
