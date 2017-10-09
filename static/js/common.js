/**
 * Created by zhangjinsi on 2017/9/14.
 */


function init_chart(chartlist){


    chartlist.forEach(function(value, index, array){

       var elem = value['elemid'];
        echarts.init(document.getElementById(elem));
    });
}


function init_date(chartlist){

    $("#sdate").jeDate({
            format:"YYYY-MM-DD",
            isTime:false,
            isinitVal : true,
            minDate:"2014-09-19",
            choosefun:function(elem, val, date) {

                var sdate = $("#sdate").val();
                var edate = $("#edate").val();

                //刷新表格数据
                chartlist.forEach(function(value, index, array){

                    var elemid = value["elemid"];
                    var dims = value["dims"];
                    flushchart(sdate, edate, elemid, dims);
                });

            }
        });

    $("#edate").jeDate({
            format:"YYYY-MM-DD",
            isTime:false,
            isinitVal : true,
            minDate:"2014-09-19",
            choosefun:function(elem, val, date) {

                var sdate = $("#sdate").val();
                var edate = $("#edate").val();

                //刷新表格数据
                chartlist.forEach(function(value, index, array){

                    var elemid = value["elemid"];
                    var dims = value["dims"];
                    flushchart(sdate, edate, elemid, dims);
                });
            }
        });
}


function flushchart(sdate,edate, elem, dims){
    var url = "/data/get_data";
    var params = {
        "sdate":sdate,
        "edate":edate,
        "dims":dims
    };
    $.get(url,params,function(json_data){
        //设置表格
        if(json_data.code == 0){
            setChartData(elem, json_data.data);
        }
    });
}

function setChartData(elem, data){

    var title = data["title"];
    var xAxis = data["xAxis"];
    var series = data["series"];

    var names = [];

    series.forEach(function(value,index, array){

        names.push(value["name"]);
    });

    var option = {
            title: {
                text: title
            },
            tooltip: {},
            legend: {
                data: names
            },
            xAxis: {
                data: xAxis
            },
            yAxis: {},

            series: series
        };

        // 使用刚指定的配置项和数据显示图表。
    var chart = echarts.getInstanceByDom(document.getElementById(elem));

    chart.setOption(option);  //设置数据
}



function login(){


    $("#btn").click(function(){

        var elem = $(this);

        if (elem.text() == "登录"){
            //发送登录请求
            var url = "/user/login";
            var param = {
                "fworkid" : $("#account").val(),
                "fpassword" : $("#password").val()
            };

            $.post(url, param, function(json_data){

                console.log(json_data);
                if (0 == json_data.code){
                    elem.text("注销");
                }else{
                    alert(json_data.msg);
                }
            });
        }else{
            //发送注销请求
            var url = "/user/logout";
            $.post(url, {}, function(json_data){

                if (0 == json_data.code){
                    elem.text("登录");
                }else{
                    alert(json_data.msg);
                }
            });
        }
    })

}