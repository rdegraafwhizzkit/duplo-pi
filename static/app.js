function resize(e) {
    e.css({'height':e.width()+'px'});
    e.css({'top':((document.documentElement.clientHeight-e.width())/2)+'px'})
}

function sync(state) {
    for(var color in state) {
        if(state[color])
            $('#'+color).removeClass('black');
        else
            $('#'+color).addClass('black');
    }
}

$(function() {

    $('.color').click(function(){
        $.getJSON( "/"+$(this).attr('id'),function(state) {
            sync(state);
        })
    })

    $.getJSON("/sync",function(state) {
        sync(state);
    });

    $(window).resize(function() {
        resize($('#container'));
    });

    resize($('#container'));

})