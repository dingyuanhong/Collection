<script>
    import {HOST} from "./config.js"
    import {TimeZone} from "./apscheduler.js"
    import TaskCard from "./TaskCard.svelte"

    let params = [];
    function clearParams(){
        params = [{"id":Date.now().toString(36),"name":"","value":"",}];
    }
    function addParams(){
        params = params.concat({"id":Date.now().toString(36),"name":"","value":""});
    }
    function delParams(){
        if(params.length <= 1) return;
        var id = jQ(this).attr("data-id");
        var lst = [];
        for(var i in params){
            if(params[i]["id"] !== id){
                lst.push(params[i]);
            }
        }
        params = lst;
    }

    let todayChecked = true;
    let beginTime = "";
    let endTime = "";
    
    function initView(){
        clearParams();
        beginTime = moment().startOf('day').format('YYYY/MM/DD HH:mm:ss');
        endTime = moment().startOf('day').format('YYYY/MM/DD HH:mm:ss');
    }
    initView();
    function hideModel(){
        jQ('#addTaskModal').modal("hide");
        initView();
    }
    
    jQ(document).ready(function(){
        jQ('#addTask').click(function () {
            jQ('#addTaskModal').modal({
                "show":true,
            });
        });

        jQ('#time_interval').daterangepicker({
            locale: {
                format: 'YYYY/MM/DD HH:mm:ss'
            },
            timePicker:true,
            timePicker24Hour:true,
            timePickerSeconds:true,
            autoApply:true,

            startDate: beginTime,
            endDate: endTime,
        }, function(start, end, label) {
            beginTime = start.format('YYYY-MM-DD HH:mm:ss');
            endTime = end.format('YYYY-MM-DD HH:mm:ss');
        });

        jQ('.date_time').daterangepicker({
            singleDatePicker:true,
            minYear:1901,
            locale: {
                format: 'YYYY/MM/DD HH:mm:ss'
            },
            timePicker:true,
            timePicker24Hour:true,
            timePickerSeconds:true,
            autoApply:true,
            autoUpdateInput:false,
        },function(start, end, label){
            jQ(this.element).val(start.format('YYYY-MM-DD HH:mm:ss'));
        });

        jQ(document).ready(function(){
            jQ(".table").on("click",".collapse-click",function(){
                var target = jQ(this).attr("data-target")
                jQ(target).collapse("toggle")
            })
        });
    });
    let tasks = [];
    function getAllTasks(){
        jQ.ajax({
            type: "POST",
            url: HOST + "/api/task/all",
            dataType: "JSON",
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                console.log(data);
                tasks = data.data;
                console.log(tasks)
            },
        });
    };
    function delTask(){
        var data = {
            "id":jQ(this).attr("data-id")
        }
        jQ.ajax({
            type: "POST",
            url: HOST + "/api/task/del",
            data: JSON.stringify(data),
            dataType: "JSON",
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                console.log(data);
                getAllTasks();
            },
        });
    };
    function exectTask(){
        var data = {
            "id":jQ(this).attr("data-id")
        }
        jQ.ajax({
            type: "POST",
            url: HOST + "/api/exec/exec",
            data: JSON.stringify(data),
            dataType: "JSON",
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                console.log(data);
                if(data.success == 1){
                    alert("执行成功")
                }
            },
        });
    };
    // "once" "date" "interval" "cron"
    let timer_type = "once";
    function fixTimeTask(){
        function getTimer(){
            if(timer_type == "once"){
                return {
                    "type":timer_type,
                }
            }
            else if(timer_type == "date") {
                var ret = {};
                for(var it of jQ("#timer_date input")){
                    console.log(it)
                    var name = jQ(it).attr("name");
                    var val  = jQ(it).val();
                    if(val == "") continue;
                    ret[name] = val;
                }
                if(Object.keys(ret).length == 0){
                    return null;
                }
                ret["type"] = timer_type;
                return ret;
            }
            else if(timer_type == "interval") {
                var ret = {}
                for(var it of jQ("#timer_interval input")){
                    var name = jQ(it).attr("name");
                    var val  = jQ(it).val();
                    if(val == "") continue;
                    if (val == "0") continue;
                    ret[name] = val;
                }
                for(var it of jQ("#timer_interval select")){
                    var name = jQ(it).attr("name");
                    var val  = jQ(it).val();
                    if(val == "") continue;
                    if (val == "0") continue;
                    ret[name] = val;
                }
                if(!("start_date" in ret) && !("end_date" in ret)){
                    delete ret["timezone"]
                }

                if(Object.keys(ret).length == 0){
                    return null;
                }
                ret["type"] = timer_type;
                return ret;
            }
            else if(timer_type == "cron") {
                var ret = {}
                for(var it of jQ("#timer_cron input")){
                    var name = jQ(it).attr("name");
                    var val  = jQ(it).val();
                    if(val == "") continue;
                    ret[name] = val;
                }
                for(var it of jQ("#timer_cron select")){
                    var name = jQ(it).attr("name");
                    var val  = jQ(it).val();
                    if(val == "") continue;
                    ret[name] = val;
                }
                if(!("start_date" in ret) && !("end_date" in ret)){
                    delete ret["timezone"]
                }
                if(Object.keys(ret).length == 0){
                    return null;
                }
                ret["type"] = timer_type;
                return ret;
            }
        }
        var timing = getTimer();
        console.log(timing)
        if(!timing){
            alert("请填写好时间")
            return;
        }
        var data = {
            "id":jQ(this).attr("data-id"),
            "timing":timing,
        };
        jQ.ajax({
            type: "POST",
            url: HOST + "/api/exec/fixtime",
            data: JSON.stringify(data),
            dataType: "JSON",
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                if(data.success == 1){
                    jQ('#timerModol').modal("hide");
                }
            },
        });
    };
    function fixTimeModel(id){
        jQ('.date_time').val("");
        jQ("#timerModol .modal-footer .submit").attr("data-id",id);
        jQ('#timerModol').modal({
            "show":true,
        });
    }
    getAllTasks();
    function postTask(){
        var center_ = jQ("#center").val();
        var function_ = jQ("#function").val();
        var describe = jQ("#describe").val();
        // var date = {
        //     "begin":beginTime,
        //     "end":endTime
        // };
        // if(todayChecked){
        //     date = "today";
        // }
        var param = {};
        for(var i in params){
            var it = params[i];
            if(it["name"] !== ""){
                param[it["name"]] = it["value"];
            }
        }
        if(center_ === ""){
            alert("请输入功能所在域")
            return;
        }
        if(function_ === ""){
            alert("请输入功能名称")
            return;
        }

        var data = {
            "host":center_,
            "function":function_,
            "param":param,
            "describe":describe,
        };

        jQ.ajax({
            type: "POST",
            url: HOST + "/api/task/add",
            data: JSON.stringify(data),
            dataType: "JSON",
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                console.log(data)
                if (data.success == 1) {
                    hideModel();
                    getAllTasks();
                } else {
                    alert(data.error)
                }
            },
        });
    };
</script>

<style>
    .w2 {
        width:20%;
    }
    .w5 {
        width:50%;
    }
    .tasklist {
        padding-top:20px;
        padding-bottom:20px;
    }
</style>

<div class="tasklist">
    <div class="btn-toolbar" role="toolbar" aria-label="Toolbar with button groups">
        <div class="btn-group mr-2" role="group" aria-label="First group">
            <button type="button" class="btn btn-primary" on:click="{getAllTasks}">刷新</button>
            <span class="btn px-0 m-0 h-100" style="width:1px;"></span>
            <button type="button" class="btn btn-primary" id="addTask">添加任务</button>
        </div>
    </div>
    <table class="table table-bordered">
        <thead class="thead-light">
            <tr>
            <th scope="col" class="w2">任务ID</th>
            <th scope="col" class="w5">内容</th>
            <th scope="col">操作</th>
            </tr>
        </thead>
        <tbody>
{#each tasks as data, i}
            <tr>
            <td class="align-middle font-weight-bold">{data["id"]}</td>
            <td>
                <TaskCard data="{data}"  type="exec"/>
            </td>
            <td class="align-middle font-weight-bold">
            <button type="button"  on:click="{exectTask}" data-id="{data["id"]}">执行</button>
            <button type="button"  on:click="{fixTimeModel(data["id"])}" data-id="{data["id"]}">定时执行</button>
            <button type="button" class="btn-danger" on:click="{delTask}" data-id="{data["id"]}">删除</button>
            </td>
            </tr>
{/each}
        </tbody>
    </table>
</div>

<div id="addTaskModal" class="modal" tabindex="-1" role="dialog">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
        <form >
            <div class="modal-header">
                <h5 class="modal-title">添加任务</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
                </button>
            </div>
            
            <div class="modal-body">
                <div class="form-row">
                    <div class="col">
                        <span class="col-ms-3">域:</span>
                        <input type="text" class="form-control" placeholder="请输入功能所在域" id="center">
                    </div>
                    <div class="col">
                        <span for="function" class="col-ms-3">功能:</span>
                        <input type="text" class="form-control" id="function" placeholder="请输入功能名称">
                    </div>
                </div>
                <!-- <div class="form-row">
                时段:
                </div>
                <div class="form-row">
                    <div class="col" style="display:{!todayChecked?'block':'none'};">
                        <input type="text" class="form-control" id="time_interval">
                    </div>
                    <div class="col-form-label">
                        <div class="form-check">
                            <label class="form-check-label" for="today">
                            <input class="form-check-input" type="checkbox" id="today" bind:checked={todayChecked}/>
                            当天</label>
                        </div>
                    </div>
                </div> -->
                <div class="form-row">
                参数:
                </div>
                <div class="form-row" id="params">
        {#each params as data, i}
        {#if data}
                    <div class="form-row m-0">
                        <div class="col">
                            <input type="text" class="form-control" bind:value="{data['name']}" placeholder="请输入参数">
                        </div>
                        <div class="col">
                            <input type="text" class="form-control" bind:value="{data['value']}" placeholder="请输入数值">
                        </div>
                        <div class="col" style="padding-top:3px;">
                            <button type="button" class="btn btn-primary btn-sm add" on:click="{addParams}">添加</button>
                            <button type="button" class="btn btn-danger btn-sm del" on:click="{delParams}" data-id="{data['id']}">删除</button>
                        </div>
                    </div>
        {/if}
        {/each}
                </div>
                <div class="form-row">
                描述:
                </div>
                <div class="form-row">
                    <div class="col">
                        <textarea id="describe" class="form-control"></textarea>
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                <button type="button" class="btn btn-primary" on:click="{()=>{postTask();return false;}}">提交</button>
            </div>
        </form>
        </div>
    </div>
</div>

<div id="timerModol" class="modal" tabindex="-1" role="dialog">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <form >
                <div class="modal-header">
                    <h5 class="modal-title">定时任务</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                    </button>
                </div>

                <div class="modal-body">
                <form>
                    <div class="form-row">
                        <select class="btn border mb-2" bind:value={timer_type}>
                            <option value="once">立即执行</option>
                            <option value="date">时间点执行</option>
                            <option value="interval">间隔执行</option>
                            <option value="cron">定时执行</option>
                        </select>
                    </div>

                    <div id="timer_date" class="form-row {(timer_type == 'date')?'':'d-none'}">
                        <div class="input-group">
                            <div>
                                <select class="input-group-text" placeholder="请选择时区" name="timezone">
{#each TimeZone as timezone}
                                    <option value="{timezone[0]}">{timezone[1]}</option>
{/each}
                                </select>
                            </div>
                            <div class="form-control border-0 my-0 py-0">
                                <input class="form-control date_time" type="text" name="run_date" placeholder="请选择时间"/>
                            </div>
                        </div>
                    </div>

                    <div id="timer_interval" class="{(timer_type == 'interval')?'':'d-none'}">
                        <div class="form-row ">
                            <div class="col-md-4">
                                <div class="input-group mb-3">
                                    <input class="form-control" type="number" min=0 name="weeks" placeholder="间隔周"/>
                                    <div class="input-group-append">
                                        <span class="input-group-text">周</span>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="input-group mb-3">
                                    <input class="form-control" type="number" min=0 name="days" placeholder="间隔日"/>
                                    <div class="input-group-append">
                                        <span class="input-group-text">日</span>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="input-group mb-3">
                                    <input class="form-control" type="number" min=0 name="hours" placeholder="间隔小时"/>
                                    <div class="input-group-append">
                                        <span class="input-group-text">小时</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="form-row ">
                            <div class="col-md-4">
                                <div class="input-group mb-3">
                                    <input class="form-control" type="number" min=0 name="minutes" placeholder="间隔分钟"/>
                                    <div class="input-group-append">
                                        <span class="input-group-text">分钟</span>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="input-group mb-3">
                                    <input class="form-control" type="number" min=0 name="seconds" placeholder="间隔秒"/>
                                    <div class="input-group-append">
                                        <span class="input-group-text">秒</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="form-row" >
                            <div class="input-group">
                                <div>
                                    <select class="input-group-text" placeholder="请选择时区" name="timezone">
{#each TimeZone as timezone}
                                    <option value="{timezone[0]}">{timezone[1]}</option>
{/each}
                                    </select>
                                </div>
                                <div class="form-control border-0 my-0 py-0 h-auto">
                                    <input class="form-control date_time" type="text" name="start_date" placeholder="请选择开始时间"/>
                                    <input class="form-control date_time" type="text" name="end_date" placeholder="请选择结束时间"/>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div id="timer_cron" class="{(timer_type == 'cron')?'':'d-none'}">
                        <div class="form-row ">
                            <div class="col-md-4">
                                <div class="input-group mb-3">
                                    <input class="form-control" type="text" name="year" placeholder="1990"/>
                                    <div class="input-group-append">
                                        <span class="input-group-text">年</span>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="input-group mb-3">
                                    <input class="form-control" type="text" name="month" placeholder="1-12"/>
                                    <div class="input-group-append">
                                        <span class="input-group-text">月</span>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="input-group mb-3">
                                    <input class="form-control" type="text" name="day" placeholder="1-31"/>
                                    <div class="input-group-append">
                                        <span class="input-group-text">日</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="form-row ">
                            <div class="col-md-4">
                                <div class="input-group mb-3">
                                    <input class="form-control" type="number" name="hour" placeholder="0-23"/>
                                    <div class="input-group-append">
                                        <span class="input-group-text">时</span>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="input-group mb-3">
                                    <input class="form-control" type="text" name="minute" placeholder="0-59"/>
                                    <div class="input-group-append">
                                        <span class="input-group-text">分</span>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="input-group mb-3">
                                    <input class="form-control" type="text" name="second" placeholder="0-59"/>
                                    <div class="input-group-append">
                                        <span class="input-group-text">秒</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="form-row" >
                            <div class="col-md-4">
                                <div class="input-group mb-3">
                                    <input class="form-control" type="text" name="week" placeholder="1-53"/>
                                    <div class="input-group-append">
                                        <span class="input-group-text">周</span>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="input-group mb-3">
                                    <div class="input-group-append">
                                        <span class="input-group-text">星期</span>
                                    </div>
                                    <input class="form-control" type="text" name="day_of_week" placeholder="0-6"/>
                                    
                                </div>
                            </div>
                        </div>

                        <div class="form-row" >
                            <div class="input-group">
                                <div>
                                    <select class="input-group-text" placeholder="请选择时区" name="timezone">
{#each TimeZone as timezone}
                                    <option value="{timezone[0]}">{timezone[1]}</option>
{/each}
                                    </select>
                                </div>
                                <div class="form-control border-0 my-0 py-0 h-auto">
                                    <input class="form-control date_time" type="text" name="start_date" placeholder="请选择开始时间"/>
                                    <input class="form-control date_time" type="text" name="end_date" placeholder="请选择结束时间"/>
                                </div>
                            </div>
                        </div>
                    </div>

                </form>
                 </div>

                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary submit" on:click="{fixTimeTask}" data-id="">提交</button>
                </div>
            </form>
        </div>
    </div>
</div>