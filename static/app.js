function resize(e) {
    e.css({'height':e.width()+'px'});
    e.css({'top':((window.innerHeight-e.width())/2)+'px'})
}

function sync(state) {
    $('.color').addClass('black');
    for(var color in state) {
        if(state[color])
            $('#'+color).removeClass('black');
        else
            $('#'+color).addClass('black');
    }
}

$(function() {

    namespace = '/test';
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
    $('.color').click(function(){
        socket.emit('sync_one', {data: $(this).attr('id')});
    });
    socket.on('sync_response', function(msg) {
        sync(msg.data);
    });
    socket.emit('sync_all');

    $(window).resize(function() {
        resize($('#container'));
    });

    resize($('#container'));

})