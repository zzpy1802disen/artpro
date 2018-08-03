// 抢读的函数
function advanceArt(artId) {
    $.getJSON('/art/advance/' + artId + "/", function (data) {
        alert(data.msg);
        if (data.status == 201) {
            queryAdvanceArt(artId);
        }else if (data.status == 101){
            // 打开登录页面
            window.open('/user/login/', target='_self');
        }
    })
}

//定时查询抢读的结果
function queryAdvanceArt(artId) {
    tid = setInterval(function () {
        $.getJSON('/art/qAdvance/' + artId + "/", function (data) {
            // alert(data.msg);
            $('#advanceBtn').text(data.msg);
            if (data.status != 202) {
                //抢读成功
                clearInterval(tid); //停止定时刷新
            }
        })
    }, 2000)
}