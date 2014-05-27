
$(document).ready ->

  form_alert = (loc, name, content) ->
    loc.css("background-color", "rgb(255, 224, 219)")
    loc.after("&nbsp;<span id='alert_#{name}' style='color: red;'>#{content}</span>")
    $('input[type="submit"]').attr('disabled', 'disabled')

  form_success = (loc, name, content) ->
    loc.css("background-color", "rgb(147, 236, 147)")
    loc.after("&nbsp;<span id='alert_#{name}' style='color: green;'>#{content}</span>")
    $('input[type="submit"]').removeAttr('disabled')

#  target = $(".not_blank")
#  target.blur ->
#    if target.val() is "" then form_alert $(@), 'not_blank', "该项不能为空！"
#
  $(".not_blank").focus ->
    $(@).css "background-color", "#fff"
    $("#alert_not_blank").remove()

  $('input[type="submit"]').click ->
    if $(".not_blank").val() is ""
      form_alert $(@), 'not_blank', "该项不能为空！"

  $(".not_blank").blur ->
      if $(@).val() is ""
        form_alert $(@), 'not_blank', "该项不能为空！"


$(document).ready ->

