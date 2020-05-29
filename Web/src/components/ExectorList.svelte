<script>
    import {HOST} from "./config.js"
    import TaskCardFull from "./TaskCardFull.svelte"
    import TimerCard from "./TimerCard.svelte"
    let jobs = [];
    let job_id = "";
    let task_id = "";
    let beginTime = "";
    let endTime = "";
    let status = "";
    function getExector(){
        var data = {
            "job_id":job_id,
            "task_id":task_id,
            "begin_time":beginTime,
            "end_time":endTime,
            "status":status,
        };
        jQ.ajax({
            type: "POST",
            url: HOST + "/api/exec/gets",
            dataType: "JSON",
            data:JSON.stringify(data),
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                jobs = data;
            },
        });
    };
    function delExector(){
        var data = {
            "id":jQ(this).attr("data-id")
        }
        jQ.ajax({
            type: "POST",
            url: HOST + "/api/exec/del",
            data: JSON.stringify(data),
            dataType: "JSON",
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                console.log(data);
                getExector();
            },
        });
    };

    jQ(document).ready(function(){
        console.log("document ready");

        jQ("#input_time_begin").daterangepicker({
            singleDatePicker: true,//设置为单个的datepicker，而不是有区间的datepicker 默认false
            showDropdowns: true,//当设置值为true的时候，允许年份和月份通过下拉框的形式选择 默认false
            autoUpdateInput: false,//1.当设置为false的时候,不给与默认值(当前时间)2.选择时间时,失去鼠标焦点,不会给与默认值 默认true
            timePicker24Hour : true,//设置小时为24小时制 默认false
            // timePickerIncrement: 1,
            timePicker : true,//可选中时分 默认false
            locale: {
                format: "YYYY-MM-DD HH:mm:SS",
                cancelLabel: 'Clear',
                separator: " - ",
                daysOfWeek: ["日","一","二","三","四","五","六"],
                monthNames: ["一月","二月","三月","四月","五月","六月","七月","八月","九月","十月","十一月","十二月"]
            }
        }).on('cancel.daterangepicker', function(ev, picker) {
            beginTime = "";
        }).on('apply.daterangepicker', function(ev, picker) {
            beginTime = picker.startDate.format('YYYY-MM-DD HH:mm:SS')
        });

        jQ("#input_time_end").daterangepicker({
            singleDatePicker: true,//设置为单个的datepicker，而不是有区间的datepicker 默认false
            showDropdowns: true,//当设置值为true的时候，允许年份和月份通过下拉框的形式选择 默认false
            autoUpdateInput: false,//1.当设置为false的时候,不给与默认值(当前时间)2.选择时间时,失去鼠标焦点,不会给与默认值 默认true
            timePicker24Hour : true,//设置小时为24小时制 默认false
            timePicker : true,//可选中时分 默认false
            locale: {
                format: "YYYY-MM-DD HH:mm:SS",
                cancelLabel: 'Clear',
                separator: " - ",
                daysOfWeek: ["日","一","二","三","四","五","六"],
                monthNames: ["一月","二月","三月","四月","五月","六月","七月","八月","九月","十月","十一月","十二月"]
            }
        }).on('cancel.daterangepicker', function(ev, picker) {
            endTime = "";
        }).on('apply.daterangepicker', function(ev, picker) {
            endTime = picker.startDate.format('YYYY-MM-DD HH:mm:SS')
        });
    })
</script>

<style>
</style>

<div class="timerlist">
    <div class="btn-toolbar" >
        <div class="m-2 w-100">
            <div class="row my-2">
                <div  class="col">
                    <input type="text" class="form-control " bind:value="{job_id}" placeholder="定时器ID"/>
                </div>
                <div class="col">
                    <input type="text" class="form-control " bind:value="{task_id}" placeholder="任务ID"/>
                </div>
            </div>

            <div class="row my-2">
                <div class="col">
                    <input type="text " id="input_time_begin" class="form-control " bind:value="{beginTime}" placeholder="开始时间"/>
                </div>
                <div class="col">
                    <input type="text " id="input_time_end" class="form-control" bind:value="{endTime}" placeholder="结束时间"/>
                </div>
            </div>

            <div class="row my-2">
                <div class="col">
                    <select type="text"  class="form-control" bind:value="{status}"  placeholder="状态">
                        <option value="">所有</option>
                        <option value="success">成功</option>
                        <option value="active">活动</option>
                        <option value="failed">失败</option>
                    </select>
                </div>

                <div class="col">
                     <button type="button" class="btn btn-primary btn-group-lg" on:click="{getExector}">确认</button>
                </div>
            </div>
        </div>
    </div>
    <table class="table table-bordered">
        <thead class="thead-light">
            <tr>
            <th scope="col" class="w2">执行ID</th>
            <th scope="col" class="w2">定时器ID</th>
            <th scope="col" class="w5">任务ID</th>
            <th scope="col" class="w5">时间</th>
            <th scope="col" class="w5">状态</th>
            <th scope="col" class="w5">消息</th>
            <th scope="col">操作</th>
            </tr>
        </thead>
        <tbody>
{#each jobs as data, i}
            <tr>
            <td class="align-middle font-weight-bold">
                {data["id"]}
            </td>
            <td class="align-middle font-weight-bold">
                {data.hasOwnProperty('job_id')?data['job_id']:''}
{#if data.hasOwnProperty('job_id')}
                <a class="collapse-click border-0 w-100 text-left cursor-pointer" 
                    data-toggle="collapse" data-target="#{'exec_job_'+data['id']}"
                    role="button">
                    <h6 class="border-bottom">{data["job_id"]}</h6>
                </a>
                <TimerCard data="{data['timer']}" id="{data['id']}" type="exec_job_"></TimerCard>
{/if}
            </td>
            <td class="align-middle font-weight-bold">
                <div class="border-0">
                    <a class="collapse-click border-0 w-100 text-left cursor-pointer" 
                        data-toggle="collapse" data-target="#{'exec_task_'+data['id']}"
                        role="button">
                        <h6 class="border-bottom">{data["task_id"]}</h6>
                    </a>
                    <TaskCardFull data="{data['task']}" id="{data['id']}" type="exec_task_"></TaskCardFull>
                </div>
            </td>
            <td>
                {data['create_time']}
            </td>
            <td>
                {data['status']}
            </td>
            <td>
                {data['message']}
            </td>
            <td class="align-middle font-weight-bold">
            <button type="button" class="btn-danger" on:click="{delExector}" data-id="{data["id"]}">删除</button>
            </td>
            </tr>
{/each}
        </tbody>
    </table>
</div>