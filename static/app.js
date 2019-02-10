function resize(e) {
    e.css({'height':e.width()+'px'});
//    e.css({'top':((window.innerHeight-e.width())/2)+'px'})
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

    namespace = '/duplopi';
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
    $('.color').click(function(){
        socket.emit('sync_one', {data: $(this).attr('id')});
    });
    socket.on('sync_response', function(msg) {
        sync(msg.data);
    });

    $(window).resize(function() {
        resize($('#container_direct'));
    });
    resize($('#container_direct'));

    $('#start').click(function(){
        rows=[];
        $('.row').each(function(){
            colors=[];
            $(this).find('.check').each(function(){
                if(!$(this).hasClass('black')) {
                    colors.push($(this).data('color'));
                }
            })
            colors.push($(this).find("select").val());
            rows.push(colors.join(' '));
        })
        loop=rows.join(',');
        socket.emit('start', {data: loop});
    })

    $('#stop').click(function(){
        socket.emit('stop');
    })

    $('#toggle').click(function(){
        $('.toggle').toggle();
    })

    $(document).on('click', '.add', function(){
        $(this).parent().parent().parent().append($(this).parent().parent().clone(false));
        $('.remove').show();
    });

    $(document).on('click', '.remove', function(){
        if($('.row').length>1) {
            $(this).parent().parent().remove();
        }
        if($('.row').length==1) {
            $('.remove').hide();
        }
    })

    $(document).on('click', '.check', function(){
        $(this).toggleClass('black');
    })

    $('.remove').hide();

})

