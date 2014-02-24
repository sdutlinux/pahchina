/**
 * Created by zhwei on 2/23/14.
 */

$( document ).ready(function() {
  // Handler for .ready() called.
    var p_list=location.search.substring(1).split("&");

    for (var i in p_list){
        var k = p_list[i].split('=')[0]
        var v = p_list[i].split('=')[1]
        document.getElementById('id_'+k).value=v;
    }
});