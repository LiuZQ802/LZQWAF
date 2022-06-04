$(document).ready(function () {
       getStatus();
    });

//获取防火墙状态
function getStatus(){
    $.ajax({
        type:'POST',
        url:'/init_status',
        dataType:'json',
        success:function(data){
            status=data['status'];
            if(status=='True'){
                init_switch(true);
            }else{
                init_switch(false);
            }
        }
    });
}
//开关按钮
function init_switch(status){
    $('#main_switch').bootstrapSwitch({
                            onText : "开启",      // 设置ON文本
                            offText : "关闭",    // 设置OFF文本
                            onColor : "success",// 设置ON文本颜色(info/success/warning/danger/primary)
                            offColor : "danger",  // 设置OFF文本颜色 (info/success/warning/danger/primary)
                            size : "large",    // 设置控件大小,从小到大  (mini/small/normal/large)
                            state:status,
                            labelText:'系统开关',

                            // 当开关状态改变时触发
                            onSwitchChange : function(event, state) {

                                if (state == true) {
                                    control_run(true);
                                } else {
                                    control_run(false);
                                }
                            }
                        });
}

//控制程序运行
function control_run(flag){
    $.ajax({
        type:'POST',
        url:'/run',
        dataType:'json',
        data:{
            'status':flag
        },
        success:function(data){
            status=data['flag'];
            console.log(status)
            console.log(flag)
            if(status){
                if(flag){
                    $('#status_success').remove();   //先移除这个id元素，不然后面会有冲突
                    a='<div class="alert alert-success" id="status_success" style="position:fixed;"><strong>成功!</strong>WAF系统已开启</div>';
                    $('#haha').append(a);
                    $('#status_success').fadeOut(2000);  //逐渐消失
                }else{
                    $('#status_danger').remove();   //先移除这个id元素，不然后面会有冲突
                    a='<div class="alert alert-success" id="status_danger" style="position:fixed;"><strong>成功!</strong>WAF系统已关闭</div>';
                    $('#haha').append(a);
                    $('#status_danger').fadeOut(2000);  //逐渐消失
                }
            }
        }
    })
}
 //清空日志的ajax请求
$(function(){
    $('#b1').click(function(){
        $.ajax({
        type:'POST',
        dataType:'json',
        url:'/rules_manage/delete',
        data:{'name':'logs_waf_pass'},
        success:function(data){
            flag=data['flag'];
            if(flag){
                    $('#rules_delete_pass_success').remove();   //先移除这个id元素，不然后面会有冲突
                    a='<div class="alert alert-success" id="rules_delete_pass_success" style="position:fixed;"><strong>成功!</strong>放行日志已清空</div>';
                    $('#haha').append(a);
                    $('#rules_delete_pass_success').fadeOut(2000);  //逐渐消失
            }else{
                $('#rules_delete_pass_error').remove();   //先移除这个id元素，不然后面会有冲突
                    a='<div class="alert alert-danger" id="rules_delete_pass_error" style="position:fixed;"><strong>失败!</strong>放行日志清空失败</div>';
                    $('#haha').append(a);
                    $('#rules_delete_pass_error').fadeOut(2000);  //逐渐消失
            }
        }
        });
    });

    $('#b2').click(function(){
        $.ajax({
        type:'POST',
        dataType:'json',
        url:'/rules_manage/delete',
        data:{'name':'logs_waf_block'},
        success:function(data){
            flag=data['flag'];
            if(flag){
                    $('#rules_delete_block_success').remove();   //先移除这个id元素，不然后面会有冲突
                    a='<div class="alert alert-success" id="rules_delete_block_success" style="position:fixed;"><strong>成功!</strong>拦截日志已清空</div>';
                    $('#haha').append(a);
                    $('#rules_delete_block_success').fadeOut(2000);  //逐渐消失
            }else{
                $('#rules_delete_block_error').remove();   //先移除这个id元素，不然后面会有冲突
                    a='<div class="alert alert-danger" id="rules_delete_block_error" style="position:fixed;"><strong>失败!</strong>拦截日志清空失败</div>';
                    $('#haha').append(a);
                    $('#rules_delete_block_error').fadeOut(2000);  //逐渐消失
            }
        }
        });
    });

    $('#b3').click(function(){
        $.ajax({
        type:'POST',
        dataType:'json',
        url:'/rules_manage/delete',
        data:{'name':'logs_waf_error'},
        success:function(data){
            flag=data['flag'];
            if(flag){
                    $('#rules_delete_error_success').remove();   //先移除这个id元素，不然后面会有冲突
                    a='<div class="alert alert-success" id="rules_delete_error_success" style="position:fixed;"><strong>成功!</strong>错误日志已清空</div>';
                    $('#haha').append(a);
                    $('#rules_delete_error_success').fadeOut(2000);  //逐渐消失
            }else{
                $('#rules_delete_error_error').remove();   //先移除这个id元素，不然后面会有冲突
                    a='<div class="alert alert-danger" id="rules_delete_error_error" style="position:fixed;"><strong>失败!</strong>错误日志清空失败</div>';
                    $('#haha').append(a);
                    $('#rules_delete_error_error').fadeOut(2000);  //逐渐消失
            }
        }
        });
    });
    $('#b4').click(function(){
        $.ajax({
        type:'POST',
        dataType:'json',
        url:'/rules_manage/delete',
        data:{'name':'logs_user_operate'},
        success:function(data){
            flag=data['flag'];
            if(flag){
                    $('#rules_delete_operate_success').remove();   //先移除这个id元素，不然后面会有冲突
                    a='<div class="alert alert-success" id="rules_delete_operate_success" style="position:fixed;"><strong>成功!</strong>用户操作日志已清空</div>';
                    $('#haha').append(a);
                    $('#rules_delete_operate_success').fadeOut(2000);  //逐渐消失
            }else{
                $('#rules_delete_operate_error').remove();   //先移除这个id元素，不然后面会有冲突
                    a='<div class="alert alert-danger" id="rules_delete_operate_error" style="position:fixed;"><strong>失败!</strong>用户操作日志清空失败</div>';
                    $('#haha').append(a);
                    $('#rules_delete_operate_error').fadeOut(2000);  //逐渐消失
            }
        }
        });
    });


})
