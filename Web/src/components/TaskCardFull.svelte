<script>
    export let data;
    export let id;
    export let type;
    console.log(data);
</script>

<style>
</style>

        
        <div class="collapse row" id="{type+id}">
            <div class="col">
                <h6 class="border-bottom">{data["function"]}</h6>
                <h6><span class="d-inline font-weight-bold">所在域:</span>{data["host"]}</h6>
                <h6>{data["describe"]}</h6>
            </div>
            <!-- <div class="col"> -->
                
<!-- {#if data["date"] == "today"}
                <h6><span class="d-inline font-weight-bold">时间:</span>当日</h6>
{:else}
                <h6><span class="d-inline font-weight-bold">时间:</span></h6>
                <h6>{data["date"]["begin"]}</h6>
                <h6>{data["date"]["end"]}</h6>
{/if} -->
            <!-- </div> -->
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
            
        </div>