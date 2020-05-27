<script>
    import {HOST} from "./config.js"
    import TaskCardFull from "./TaskCardFull.svelte"
    import TimerCard from "./TimerCard.svelte"

    let jobs = [];
    function getAllJobs(){
        jQ.ajax({
            type: "POST",
            url: HOST + "/api/job/all",
            dataType: "JSON",
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                console.log(data);
                jobs = data["data"];
            },
        });
    };
    function exectJob(){
        var data = {
            "id":jQ(this).attr("data-id")
        }
        jQ.ajax({
            type: "POST",
            url: HOST + "/api/exec/restart",
            data: JSON.stringify(data),
            dataType: "JSON",
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                console.log(data);
                getAllJobs();
            },
        });
    };
    function stopJob(){
        var data = {
            "id":jQ(this).attr("data-id")
        }
        jQ.ajax({
            type: "POST",
            url: HOST + "/api/exec/stop",
            data: JSON.stringify(data),
            dataType: "JSON",
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                console.log(data);
                getAllJobs();
            },
        });
    };
    function delJob(){
        var data = {
            "id":jQ(this).attr("data-id")
        }
        jQ.ajax({
            type: "POST",
            url: HOST + "/api/job/del",
            data: JSON.stringify(data),
            dataType: "JSON",
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                console.log(data);
                getAllJobs();
            },
        });
    };
    getAllJobs();
</script>

<style>
</style>

<div class="timerlist">
    <div class="btn-toolbar" role="toolbar" aria-label="Toolbar with button groups">
        <div class="btn-group mr-2" role="group" aria-label="First group">
            <button type="button" class="btn btn-primary" on:click="{getAllJobs}">刷新</button>
            <span class="btn px-0 m-0 h-100" style="width:1px;"></span>
        </div>
    </div>
    <table class="table table-bordered">
        <thead class="thead-light">
            <tr>
            <th scope="col" class="w2">定时器ID</th>
            <th scope="col" class="w5">任务ID</th>
            <th scope="col" class="w5">状态</th>
            <th scope="col">操作</th>
            </tr>
        </thead>
        <tbody>
{#each jobs as data, i}
            <tr>
            <td class="align-middle font-weight-bold">
                <div class="border-0">
                    <a class="collapse-click border-0 w-100 text-left cursor-pointer" 
                        data-toggle="collapse" data-target="#{'timer'+data['id']}"
                        role="button">
                        <h6 class="border-bottom">{data["id"]}</h6>
                    </a>
                    <TimerCard data="{data['timer']}" id="{data['id']}" type="timer"></TimerCard>
                </div>
            </td>
            <td class="align-middle font-weight-bold">
                <div class="border-0">
                    <a class="collapse-click border-0 w-100 text-left cursor-pointer" 
                        data-toggle="collapse" data-target="#{'timer_task_'+data['task_id']}"
                        role="button">
                        <h6 class="border-bottom">{data["task_id"]}</h6>
                    </a>
                    <TaskCardFull data="{data['task']}" id="{data['task_id']}" type="timer_task_"></TaskCardFull>
                </div>
            </td>
            <td class="align-middle">
                {data['status']}
            </td>
            <td class="align-middle font-weight-bold">
            <button type="button"  on:click="{exectJob}" data-id="{data["id"]}">重新执行</button>
            <button type="button" class="btn-danger" on:click="{stopJob}" data-id="{data["id"]}">停止</button>
            <button type="button" class="btn-danger" on:click="{delJob}" data-id="{data["id"]}">删除</button>
            </td>
            </tr>
{/each}
        </tbody>
    </table>
</div>