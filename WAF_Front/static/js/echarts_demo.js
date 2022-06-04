var chartDom = document.getElementById('main');
var chartDom2=document.getElementById('main2');
var myChart = echarts.init(chartDom);
var myChart2=echarts.init(chartDom2);
var option,option2;

 $(document).ready(function () {
       getData();
       getIP_static()
    });
function getData(){
    $.ajax({
        type:'POST',
        dataType:'json',
        data:{},
        url:'/static/type',
        success:function(data){
            sql_count=0;
            xss_count=0;
            file_count=0;
            command_count=0;
            dir_count=0;
            file_bh_count=0
            cc_cout=0
            for(item in data){
               if(data[item]['type']=='sql注入'){
                sql_count=data[item]['count'];
               }else if(data[item]['type']=='xss'){
                xss_count=data[item]['count'];
               }else if(data[item]['type']=='文件上传'){
                file_count=data[item]['count'];
               }else if(data[item]['type']=='命令执行'){
                command_count=data[item]['count'];
               }else if(data[item]['type']=='敏感目录文件'){
                dir_count=data[item]['count'];
               }else if(data[item]['type']=='文件包含'){
                file_bh_count=data[item]['count'];
               }else if(data[item]['type']=='CC'){
                cc_cout=data[item]['count'];
               }
            }
            option = {
                title: {
                    text: '攻击统计',
                    subtext: '统计各种攻击方式次数'
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                    type: 'shadow'
                    }
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis: [
                 {
                    type: 'category',
                    data: ['SQL注入', 'XSS','命令执行', '恶意文件上传','恶意文件包含',  '敏感目录文件','CC'],
                    axisTick: {
                        alignWithLabel: true
                    }
                    }
                ],
                yAxis: [
                    {
                    type: 'value'
                    }
                ],
                series: [
                    {
                    name: '次数',
                     type: 'bar',
                    barWidth: '60%',
                    data: [sql_count, xss_count, command_count ,file_count,file_bh_count ,dir_count,cc_cout]
                    }
                ]
                };
              myChart.setOption(option);
        }
    })
}
function getIP_static(){
    $.ajax({
        type:'POST',
        dataType:'json',
        data:{},
        url:'/IP/power',
        success:function(data){
            date=data['date'];
            pass_num=data['pass_num'];
            block_num=data['block_num'];
            option2= {
                title: {
                        text: '一周IP访问趋势（次）'
                },
                tooltip: {
                    trigger: 'axis'
                },
                legend: {},
                toolbox: {
                    show: true,
                    feature: {
                    dataZoom: {
                        yAxisIndex: 'none'
                        },
                        dataView: { readOnly: false },
                    magicType: { type: ['line', 'bar'] },
                    restore: {},
                    saveAsImage: {}
                    }
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: false,
                    data: [date[0], date[1], date[2], date[3], date[4], date[5], date[6]]
                },
                yAxis: {
                    type: 'value',
                    axisLabel: {
                    formatter: '{value}'
                    }
                },
                series: [
                    {
                        name: '正常访问',
                        type: 'line',
                        data: [pass_num[date[0]],pass_num[date[1]],pass_num[date[2]],pass_num[date[3]],pass_num[date[4]],pass_num[date[5]],pass_num[date[6]]],
                        markPoint: {
                            data: [
                                { type: 'max', name: 'Max' },
                                { type: 'min', name: 'Min' }
                            ]
                            },
                                markLine: {
                                data: [{ type: 'average', name: 'Avg' }]
                               }
                     },
                        {
                        name: '恶意访问',
                        type: 'line',
                        data: [block_num[date[0]],block_num[date[1]],block_num[date[2]],block_num[date[3]],block_num[date[4]],block_num[date[5]],block_num[date[6]]],
                        markPoint: {
                        data: [
                                { type: 'max', name: 'Max' },
                                { type: 'min', name: 'Min' }
                              ]
                        },
                        markLine: {
                            data: [
                            { type: 'average', name: 'Avg' },
                            [
                                {
                                symbol: 'none',
                                x: '90%',
                                yAxis: 'max'
                             },
                                {
                            symbol: 'circle',
                            label: {
                            position: 'start',
                            formatter: 'Max'
                            },
                        type: 'max',
                        name: '最高点'
                            }
                        ]
                        ]
                    }
                    }
                ]
       };
       myChart2.setOption(option2);
       }
   });
}