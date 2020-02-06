function get_duration_select(duration) {
  var arr = [
    {val : 100, text: '0.1'},
    {val : 500, text: '0.5'},
    {val : 1000, text: '1'},
    {val : 2000, text: '2'},
    {val : 4000, text: '4'},
    {val : 8000, text: '8'}
  ];
  var sel = $('<select>');
  $(arr).each(function() {
    var option = $('<option>').attr('value',this.val).text(this.text);
    if(this.val == duration) {
      option.attr('selected','selected');
    }
    sel.append(option);
  });
  return sel;
}

function get_colors(colors) {
  var arr = ['blue', 'red', 'yellow', 'green'];
  var div = $('<div>', {class: 'left'});
  $(arr).each(function() {
    div.append($('<div>',{
        class:String(this) + ' check' + (colors.includes(String(this))?'':' black')
      }
    ).attr('data-color',String(this)));
  });
  return div;
}

function get_row(duration, colors, remove) {
  if(!duration) {
    var duration = 1000;
  }
  if(!colors) {
    var colors = [];
  }
  if(!remove) {
    var remove = false;
  }
  var left=$('<div>', {class:'left padded_left'});
  $('<div>', {class: 'button_small add',text:'+'}).appendTo(left);
  var remove_div=$('<div>', {class: 'button_small remove',text:'-'});
  if(remove) {
    remove_div.hide();
  }
  remove_div.appendTo(left);
  get_duration_select(duration).appendTo(left)
  var row = $('<div>', {class: 'row'});
  get_colors(colors).appendTo(row);
  left.appendTo(row)
  return row;
}