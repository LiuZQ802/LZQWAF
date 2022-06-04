             var all_data   //后端提交的数据
             $('#mytab').bootstrapTable({
                        //全部参数
                        url:"/post_data",                     //从后台获取数据时，可以是json数组，也可以是json对象
                        dataType: "json",
                        method: 'post',                      //请求方式（*）
                        toolbar: '#toolbar',                //工具按钮用哪个容器
                        striped: true,                      //是否显示行间隔色
                        cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
                        pagination: true,                   //是否显示分页（*）
                        sortable: true,                     //是否启用排序
                        sortOrder: "asc",                   //排序方式
                        //queryParams: oTableInit.queryParams,//传递参数（*）
                        pageNumber: 1,                       //初始化加载第一页，默认第一页
                        pageSize: 10,                       //每页的记录行数（*）
                        pageList: [5,10,25],        //可供选择的每页的行数（*）
                        strictSearch: true,
                        //showColumns: true,                  //是否显示所有的列
                        showRefresh: true,                  //是否显示刷新按钮
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
                                field: 'regular',  //返回数据rows数组中的每个字典的键名与此处的field值要保持一致
                                title: '正则表达式',
                                align: 'center',
                                valign: 'middle',
                            },
                            {
                                field: 'type',
                                title: '攻击类型',
                                align:'center',   //居中
                                valign: 'middle',
                            },
                            {
                                field: 'description',
                                title: '描述',
                                align:'center',   //居中
                                valign: 'middle',
                            },
                            {
                                field: 'status',
                                title: '状态',
                                formatter: project_status,
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
                        onLoadSuccess: function(value){
                        //    初始化switch开关按钮
                           all_data=value
                            for(var i=0;i<all_data.length;i++){
                                status=all_data[i]['status']
                                index=all_data[i]['id']
                                if(status=='on'){
                                    initSwitch(true,index)
                                }else{
                                    initSwitch(false,index)
                                }
                            }
                        },
                        onPageChange:function(value,data){   //改变页
                           for(var i=0;i<all_data.length;i++){
                                status=all_data[i]['status']
                                index=all_data[i]['id']
                                if(status=='on'){
                                    initSwitch(true,index)
                                }else{
                                    initSwitch(false,index)
                                }
                            }
                        },
                        onRefresh:function(value){   //刷新
                            for(var i=0;i<all_data.length;i++){
                                status=all_data[i]['status']
                                index=all_data[i]['id']
                                if(status=='on'){
                                    initSwitch(true,index)
                                }else{
                                    initSwitch(false,index)
                                }
                            }
                        }
                    });

                    function initSwitch(value,index){
                    id='#project_status_switch'+index
                    $(id).bootstrapSwitch({
                            onText : "启用",      // 设置ON文本
                            offText : "禁用",    // 设置OFF文本
                            onColor : "success",// 设置ON文本颜色(info/success/warning/danger/primary)
                            offColor : "danger",  // 设置OFF文本颜色 (info/success/warning/danger/primary)
                            size : "small",    // 设置控件大小,从小到大  (mini/small/normal/large)
                            state:value,

                            // 当开关状态改变时触发
                            onSwitchChange : function(event, state) {
                                var id=this.value   //获得正则id

                                if (state == true) {
                                    change_status(index,'on')

                                } else {
                                    change_status(index,'off')
                                }
                            }
                        });
                    }
                    //修改规则的状态，传给服务端
                    function change_status(index,status){
                        $.ajax({
                            type:'post',
                            dataType:'json',
                            url:"/post_rules_manage/change_status_post",
                            data:{
                                id:index,
                                status:status
                            },
                            success:function(data){
                                var flag=data['flag']   //是否修改成功
                                var status=data['status'];
                                var id=data['id'];
                                var mess;
                                if(flag){
                                    if(status=='on'){
                                        mess='已开启'+id+'号规则状态！';
                                    }else{
                                        mess='已关闭'+id+'号规则状态！';
                                    }
                                    $('#alert_success').remove();   //先移除这个id元素，不然后面会有冲突
                                    a='<div class="alert alert-success"id="alert_success" ><strong>成功!</strong> '+mess+'</div>';
                                    $('#haha').append(a);
                                    $('#alert_success').fadeOut(2000);  //逐渐消失
                                }else{
                                    if(status=='on'){
                                        mess=id+'号规则开启失败!!!';
                                    }else{
                                        mess=id+'号规则关闭失败!!!';
                                    }
                                    $('#alert_error').remove();   //先移除这个id元素，不然后面会有冲突
                                    a='<div class="alert alert-danger" id="alert_error"><strong>失败!</strong> '+mess+'</div>';
                                    $('#haha').append(a);
                                    $('#alert_error').fadeOut(2000);  //逐渐消失
                                }


                            },
                            error:function(data){
                            }
                        })
                    }
                    //{#状态栏格式化#}
                    function project_status(value, row, index) {
                        index=row['id']        //表示该条数据的id
                        id='project_status_switch'+index
                        a="<input type='checkbox' checked id="+id+" name='mycheck' value="+index+">";
                        return a
                    }



                //操作栏的格式化
                function actionFormatter(value) {
                    //console.log(value)
                    var result = "<button type='button' class='btn btn-danger' style='width:90px' onclick=remove_rules("+value+")>删除</button>";
                    return result;

                }
                //删除规则
                function remove_rules(id){
                    $.ajax({
                        type:'post',
                        dataType:'json',
                        url:"/post_rules_manage/remove_rules_post",
                        data:{
                            id:id
                            },
                        success:function(data){
                            $('#mytab').bootstrapTable(('refresh')); //刷新表格
                            flag=data['flag'];
                            id=data['id'];
                            if(flag){
                                mess=id+'号规则删除成功!!!';
                                $('#delete_success').remove();
                                a='<div class="alert alert-success" id="delete_success"><strong>成功!</strong> '+mess+'</div>';
                                $('#haha').append(a);
                                $('#delete_success').fadeOut(2000);  //逐渐消失
                            }else{
                                mess=id+'号规则删除失败!!!';
                                $('#delete_error').remove();
                                a='<div class="alert alert-danger" id="delete_error"><strong>失败!</strong> '+mess+'</div>';
                                $('#haha').append(a);
                                $('#delete_error').fadeOut(2000);  //逐渐消失
                            }
                        }

                    })
                }

                // 搜索查询按钮触发事件
                $(function() {
                    $("#search-button").click(function () {
                        $('#mytab').bootstrapTable(('refresh')); // 很重要的一步，刷新url！
                        a=$('#search-keyword').val()
                    })
                })

             //重置搜索条件
                function clean(){
                    //先清空
                    $('#search-keyword').val('');
                    //清空后查询条件为空了，再次刷新页面，就是全部数据了
                    $('#mytab').bootstrapTable(('refresh')); // 很重要的一步，刷新url！
                }

                //添加规则，利用ajax
                $('#add_rules_form').submit(function(e){
                    e.preventDefault();  //禁止form表单的action自动提交
                    $.ajax({
                        url:'/post_rules_manage/add_rules_post',
                        type:'POST',
                        data:$(this).serialize(),
                        success:function(data){
                            flag=data['flag'];
                            $('#close_add_form').click();  //将添加规则的表格给关闭
                            $('#mytab').bootstrapTable(('refresh')); //刷新表格
                            if(flag){
                                mess='规则添加成功!!!';
                                $('#add_success').remove();
                                a='<div class="alert alert-success" id="add_success"><strong>成功!</strong> '+mess+'</div>';
                                $('#haha').append(a);
                                $('#add_success').fadeOut(2000);  //逐渐消失
                            }else{
                                mess='规则添加失败!!!';
                                $('#add_error').remove();
                                a='<div class="alert alert-danger" id="add_error"><strong>失败!</strong> '+mess+'</div>';
                                $('#haha').append(a);
                                $('#add_error').fadeOut(2000);  //逐渐消失
                            }
                        }
                    })
                });
