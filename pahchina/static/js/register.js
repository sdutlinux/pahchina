/**
 * Created by zhwei on 2/23/14.
 */

$(document).ready(function () {
    // Handler for .ready() called.
    var p_list = location.search.substring(1).split("&");
    for (var i in p_list) {
        var k = p_list[i].split('=')[0];
        var v = p_list[i].split('=')[1];
        if (v != null) {
            document.getElementById('id_' + k).value = v;
        }
    }
});
$(document).ready(function () {
    var username = $("#id_username");
    username.blur(function () {
        if ($(this).val() != undefined) {
            var url = "/accounts/register/username/" + $("#id_username").val() + "/";
            $.getJSON(url, function (data) {
                $.each(data, function (i, field) {
                    if (field == false) {
                        username.css("background-color", "rgb(255, 224, 219)");
                        username.after("&nbsp;<span id='alert_" + "username" + "' style='color: red;'>用户名已被占用！</span>")
                        $('input[type="submit"]').attr('disabled', 'disabled');
                    }
                    else {
                        username.css("background-color", "rgb(147, 236, 147)");
                        username.after("&nbsp;<span id='alert_" + "username" + "' style='color: green;'>用户名可以使用！</span>")
                        $('input[type="submit"]').removeAttr('disabled');
                    }
                });
            })
        }
    });
});
$(document).ready(function () {
    $("#id_username").focus(function () {
        $(this).css("background-color", "#fff");
        $("#alert_username").remove();
    })
});

$(document).ready(function () {
    $("#id_password2").blur(function () {
        if ($("#id_password1").val() != $(this).val()) {
            $(this).css("background-color", "rgb(255, 224, 219)");
            $(this).after("&nbsp;<span id='alert_password' style='color: red;'>两次输入的密码不相同！</span>")
            $('input[type="submit"]').attr('disabled', 'disabled');
        }
        else{
            $("input[id^='id_password']").css("background-color", "rgb(147, 236, 147)");
            $(this).after("&nbsp;<span id='alert_password' style='color: green;'>通过！</span>")
            $('input[type="submit"]').removeAttr('disabled');
        }
    })
    $("#id_password2").focus(function () {
        $(this).css("background-color", "#fff");
        $("#alert_password").remove();
    })
});