function resize(e) {
  e.css({
    'height': e.width() + 'px'
  });
}

function sync(state) {
  $('.color').addClass('black');
  for (var color in state) {
    if (state[color])
      $('#' + color).removeClass('black');
    else
      $('#' + color).addClass('black');
  }
}

function get_loop() {
  rows = [];
  $('.row').each(function() {
    ret = {}
    colors = [];
    $(this).find('.check').each(function() {
      if (!$(this).hasClass('black')) {
        colors.push($(this).data('color'));
      }
    })
    ret.colors = colors
    ret.duration = 1 * $(this).find("select").val()
    rows.push(ret)
  })
  return rows;
}

$(function() {

  namespace = '/duplopi';
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
  $('.color').click(function() {
    socket.emit('sync_one', {
      data: $(this).attr('id')
    });
  });

  socket.on('sync_patterns', function(msg) {
    $('#patterns').empty();
    localStorage.clear()
    for (i in msg.data) {
      localStorage.setItem(msg.data[i].name, JSON.stringify(msg.data[i].pattern));
      $('#patterns').append('<option value="' + msg.data[i].name + '">' + msg.data[i].name + '</option>');
    }
  });

  socket.on('loop_status', function(msg) {
    switch(String(msg.data)) {
      case 'stopped':
        $('#start').show();
        $('#stop').hide();
        break;
      case 'started':
        $('#start').hide();
        $('#stop').show();
        break;
    }
  });

  socket.on('sync_response', function(msg) {
    sync(msg.data);
  });

  $(window).resize(function() {
    resize($('#container_direct'));
  });
  resize($('#container_direct'));

  $('#start').click(function() {
    socket.emit('start', {
      data: get_loop()
    });
  })

  $('#load').click(function() {
    patterns=JSON.parse(localStorage.getItem($('#patterns').val()));
    $('#rows').empty();
    for(i in patterns) {
        get_row(patterns[i].duration, patterns[i].colors, patterns.length==1).appendTo('#rows');
    }
  })

  $('#save').click(function() {
    socket.emit('save', {
      name: $('#pattern').val(),
      pattern: get_loop()
    });
  })

  $('#stop').click(function() {
    socket.emit('stop');
  })

  $('#toggle').click(function() {
    $('.toggle').toggle();
  })

  $(document).on('click', '.add', function() {
    $(this).parent().parent().parent().append($(this).parent().parent().clone(false));
    $('.remove').show();
  });

  $(document).on('click', '.remove', function() {
    if ($('.row').length > 1) {
      $(this).parent().parent().remove();
    }
    if ($('.row').length == 1) {
      $('.remove').hide();
    }
  })

  $(document).on('click', '.check', function() {
    $(this).toggleClass('black');
  })

  get_row(1000,[],true).appendTo('#rows');
  $('#stop').hide();

})
