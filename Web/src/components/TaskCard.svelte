<script>
    export let data;
    export let type;
    // console.log(data)
</script>

<style>
</style>

<div class="border-0">
        <a class="collapse-click border-0 w-100 text-left cursor-pointer" 
            data-toggle="collapse" data-target="#{type+data["id"]}"
            role="button">
            <h1 class="border-bottom">{data["function"]}</h1>
        </a>
        <h6>{data["describe"]}</h6>
        <div class="collapse row" id="{type+data["id"]}">
            <div class="col">
                <h6><span class="d-inline font-weight-bold">所在域:</span>{data["host"]}</h6>
<!-- {#if data["date"] == "today"}
                <h6><span class="d-inline font-weight-bold">时间:</span>当日</h6>
{:else}
                <h6><span class="d-inline font-weight-bold">时间:</span></h6>
                <h6>{data["date"]["begin"]}</h6>
                <h6>{data["date"]["end"]}</h6>
{/if} -->
            </div>
{#if Object.keys(data["param"]).length > 0}
            <div class="col">
                <h6 class="font-weight-bold">参数:</h6>
                <div>
{#each Object.keys(data["param"]) as name,i}
                    <h6>
                    {name}
                    <span class="font-weight-bold" style="margin-left:4px;margin-right:4px;">:</span>
                    {data["param"][name]}
                    </h6>
{/each}
                </div>
            </div>
{/if}
        </div>
</div>