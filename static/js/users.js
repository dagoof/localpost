var active=false, name=null;

function sethooks(){
    $('#username').keyup(function(){
        name=$(this).val();
        if(active){
            clearTimeout(active);
        }
        active=setTimeout(ajaxreq, 400);
    });
}

function ajaxreq(){
    $.ajax({
        url:['/gen_users/',name].join(''),
        success:function(response){
            $('.content_post[id!=form_container]').remove();
            var res=jQuery.parseJSON(response);
            for(var elem in res){
                elem=res[elem];
                for(var item in elem){
                    $('<div></div>').addClass('content_post').html(item+"<div class='post_sig'><a href='/toggle_follow/"+item+"'>follow</a></div>").insertAfter($('#form_container'));
                }
            }
        },
    });
    active=false;
}
        

$(function(){
        sethooks();
        });
