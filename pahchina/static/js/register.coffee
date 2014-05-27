$(document).ready ->
  p_list = location.search.substring(1).split "&"
  for i in p_list
    k = i.split("=")[0]
    v = i.split("=")[1]
    document.getElementById("id_#{k}").value = v if v? and k?


form_alert = (loc, name, content) ->
  loc.css("background-color", "rgb(255, 224, 219)")
  loc.after("&nbsp;<span id='alert_#{name}' style='color: red;'>#{content}</span>")
  $('input[type="submit"]').attr('disabled', 'disabled')

form_success = (loc, name, content) ->
  loc.css("background-color", "rgb(147, 236, 147)")
  loc.after("&nbsp;<span id='alert_#{name}' style='color: green;'>#{content}</span>")
  $('input[type="submit"]').removeAttr('disabled')

$(document).ready ->
  username = $("#id_username")
  username.blur ->
    if username.val()?
        $.getJSON "/accounts/register/username/#{username.val()}/", (data)->
          $.each data, (i, field)->
            if field is false then form_alert username, 'username', "用户名已被占用！"
            else form_success username, 'username', '用户名可以使用'

  $("#id_username").focus ->
    $(@).css "background-color", "#fff"
    $("#alert_username").remove()

  email = $("#id_email")
  email.blur ->
    if email.val()?
      reg =  /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,4}$/;
      if reg.test(email.val()) is false
        form_alert email, 'email', "邮箱格式错误！"
      else
        $.post "/accounts/register/email/", {"email": email.val()}, (data) ->
          $.each data, (i, field) ->
              if field is false then form_alert email, 'email', "该邮箱已被注册！"
              else form_success email, 'email', '该邮箱可以注册！'
  $('#id_email').focus ->
    $(@).css "background-color", "#fff"
    $("#alert_email").remove()

  $('#id_password2').blur ->
    if $("#id_password1").val() isnt $(@).val()
      form_alert $(@), "password2", "两次输入的密码不相同！"
    else form_success $(@), "password2", "通过！"

  $('#id_password2').focus ->
    $(@).css "background-color", "#fff"
    $("#alert_password2").remove()