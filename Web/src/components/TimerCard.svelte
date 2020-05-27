<script>
    import {HOST} from "./config.js";
    export let data;
    export let id;
    export let type;
</script>

<style>
</style>


{#if data != null}
        <div class="collapse row" id="{type+id}">
            <div class="col">
{#if data["type"] == "once"}
                <h6><span class="d-inline font-weight-bold">执行一次</span></h6>
{:else if data["type"] == "date"}
                <h6><span class="d-inline font-weight-bold">时间:</span></h6>
            {#if "timezone" in data["param"]}
                <h6>{data["param"]["timezone"]}</h6>
            {/if}
                <h6>{data["param"]["run_date"]}</h6>
{:else if data["type"] == "interval"}
                <h6><span class="d-inline font-weight-bold">间隔执行:</span></h6>
                {#if data["param"]["weeks"]}
                <span>{data["param"]["weeks"]}周</span>
                {/if}
                {#if data["param"]["days"]}
                <span>{data["param"]["days"]}日</span>
                {/if}
                {#if data["param"]["hours"]}
                <span>{data["param"]["hours"]}时</span>
                {/if}
                {#if data["param"]["minutes"]}
                <span>{data["param"]["minutes"]}分</span>
                {/if}
                {#if data["param"]["seconds"]}
                <span>{data["param"]["seconds"]}秒</span>
                {/if}
                {#if "timezone" in data["param"]}
                <h6>时区:{data["param"]["timezone"]}</h6>
                {/if}
                {#if data["param"]["start_date"]}
                <span>开始时间:{data["param"]["start_date"]}</span>
                {/if}
                {#if data["param"]["end_date"]}
                <span>结束时间:{data["param"]["end_date"]}</span>
                {/if}
{:else if data["type"] == "cron"}
                <h6><span class="d-inline font-weight-bold">Cron执行:</span></h6>
                {#if data["param"]["year"]}
                <span>{data["param"]["year"]}年</span>
                {/if}
                {#if data["param"]["month"]}
                <span>{data["param"]["month"]}月</span>
                {/if}
                {#if data["param"]["day"]}
                <span>{data["param"]["day"]}天</span>
                {/if}
                {#if data["param"]["hour"]}
                <span>{data["param"]["hour"]}时</span>
                {/if}
                {#if data["param"]["minute"]}
                <span>{data["param"]["minute"]}分</span>
                {/if}
                {#if data["param"]["second"]}
                <h6>{data["param"]["second"]}秒</h6>
                {/if}
                {#if data["param"]["week"]}
                <span>{data["param"]["week"]}周</span>
                {/if}
                {#if data["param"]["day_of_week"]}
                <span>星期{parseInt(data["param"]["day_of_week"])+1}</span>
                {/if}
{/if}
            </div>
        </div>
{/if}
