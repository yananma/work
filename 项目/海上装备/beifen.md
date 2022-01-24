
```js
function admin_user_login() {
  $.ajax({
    type: "POST",
    url: "/account/login/",
    async: false,
    dataType:'json',
    contentType: 'application/json',
    // headers: {'token': localStorage.getItem("Authorization")},
    data: JSON.stringify({
      'name': 'wangyanpeng',
      'password': '123456',
    }),
    success: function (res) {
      // localStorage.removeItem("Authorization");
      localStorage.setItem("Authorization", res.token)
      console.log(res)
    },
    error: function (e) {
      console.log(e)
    }
  })
}

function normal_user_login() {
  $.ajax({
    type: "POST",
    url: "/account/login/",
    async: false,
    dataType:'json',
    contentType: 'application/json',
    // headers: {'token': localStorage.getItem("Authorization")},
    data: JSON.stringify({
      'name': 'zhengchang',
      'password': '654321',
    }),
    success: function (res) {
      localStorage.setItem("Authorization", res.token)
      console.log(res)
    },
    error: function (e) {
      console.log(e)
    }
  })
}
```



```js 
// 表格展开
$(function () {
  $("#collapse-cell td").click(function () {
    console.log($(this).css("background"))
    if ($(this).css("background") === "rgb(144, 238, 144) none repeat scroll 0% 0% / auto padding-box border-box"){
      $(this).css({"background": ""})
    }else {
      $(this).css({"background": "lightgreen"})
      $("#collapse-cell + tr td p").html($(this).text())
    }
  })
})
```


