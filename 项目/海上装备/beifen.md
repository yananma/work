
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
