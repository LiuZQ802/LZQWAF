             var all_data   //后端提交的数据
             $('#mytab').bootstrapTable({
                        //全部参数
                        url:"/illegal_ask_data",                     //从后台获取数据时，可以是json数组，也可以是json对象
                        dataType: "json",
                        method: 'post',                      //请求方式（*）
                        toolbar: '#toolbar',                //工具按钮用哪个容器
                        striped: false,                      //是否显示行间隔色
                        cache: true,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
                        pagination: true,                   //是否显示分页（*）
                        sortable: true,                     //是否启用排序
                        sortOrder: "asc",                   //排序方式
                        //queryParams: oTableInit.queryParams,//传递参数（*）
                        pageNumber: 1,                       //初始化加载第一页，默认第一页
                        pageSize: 10,                       //每页的记录行数（*）
                        pageList: [5,10,25],        //可供选择的每页的行数（*）
                        strictSearch: true,
                        //showColumns: true,                  //是否显示所有的列
                        showRefresh: false,                  //是否显示刷新按钮
                        minimumCountColumns: 2,             //最少允许的列数
                        clickToSelect: true,                //是否启用点击选中行
                        uniqueId: "ID",                     //每一行的唯一标识，一般为主键列
                        showToggle: false,                    //是否显示详细视图和列表视图的切换按钮
                        cardView: false,                    //是否显示详细视图
                        detailView: false,                   //是否显示父子表

                        //得到查询的参数
                        queryParams: function (params) {
                            //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
                            var query_params = {
                                rows: params.limit,                         //页面大小
                                page: (params.offset / params.limit) + 1,   //页码
                                sort: params.sort,      //排序列名
                                sortOrder: params.order, //排位命令（desc，asc）

                                //查询框中的参数传递给后台
                                search_kw: $('#search-keyword').val(), // 请求时向服务端传递的参数
                            };
                            return query_params;
                        },



                        columns: [
                            {
                                field: 'id',  //返回数据rows数组中的每个字典的键名与此处的field值要保持一致
                                title: '序号',
                                align:'center',   //居中
                                valign: 'middle',
                            },
                            {
                                field: 'minutes',  //返回数据rows数组中的每个字典的键名与此处的field值要保持一致
                                title: '判断时间范围(分钟)',
                                align: 'center',
                                valign: 'middle',
                            },
                            {
                                field: 'times',
                                title: '最大请求次数',
                                align:'center',   //居中
                                valign: 'middle',
                            },
                            {
                                field: 'id',
                                title: '操作',
                                width: 120,
                                align: 'center',
                                valign: 'middle',
                                formatter: actionFormatter,
                             },

                        ],
                    });


               //操作栏的格式化
                function actionFormatter(value) {
                    //console.log(value)
                    var result = "<button type='button' class='btn btn-success' style='width:90px' data-toggle='modal' data-target='#myModal'>编辑</button>";
                    return result;
                }

                //添加规则，利用ajax
                $('#add_rules_form').submit(function(e){
                    e.preventDefault();  //禁止form表单的action自动提交
                    $.ajax({
                        url:'/set_illegal_ask_data',
                        type:'POST',
                        data:$(this).serialize(),
                        success:function(data){
                            flag=data['flag'];
                            $('#close_add_form').click();  //将添加规则的表格给关闭
                            $('#mytab').bootstrapTable(('refresh')); //刷新表格
                            if(flag){
                                mess='CC参数修改成功!!!';
                                $('#add_success').remove();
                                a='<div class="alert alert-success" id="add_success"><strong>成功!</strong> '+mess+'</div>';
                                $('#haha').append(a);
                                $('#add_success').fadeOut(2000);  //逐渐消失
                            }else{
                                mess='CC参数修改失败!!!';
                                $('#add_error').remove();
                                a='<div class="alert alert-danger" id="add_error"><strong>失败!</strong> '+mess+'</div>';
                                $('#haha').append(a);
                                $('#add_error').fadeOut(2000);  //逐渐消失
                            }
                        }
                    })
                });
