
p_list = location.search.substring 1 .split "&"
for i in p_list
  k = i.split("=")[0]
  v = i.split("=")[1]
  if v not null
    document.getElementById('id_#{k}').value = v


username = $("#id_username").val()
$("#id_username").blur =->
  if @.val?
    $.getJSON(url="/accounts/register/username/#{username}/";)