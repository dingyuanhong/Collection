<script>
    // https://svelte.dev/examples#group-inputs

    // https://v4.bootcss.com/docs/components/navs/
    // https://www.runoob.com/bootstrap/bootstrap-typography.html
    import TaskList from './components/TaskList.svelte';
    import TimerList from './components/TimerList.svelte';
    import ExectorList from './components/ExectorList.svelte';

    jQ(document).ready(function(){
        jQ("#myNav").on("click",".nav-link",function(e){
            e.preventDefault();

            var last = jQ("#myNav").find(".active");
            jQ(last).removeClass("active");
            var last_page = jQ(last).attr("href");
            var page = jQ(this).attr("href");
            jQ(last_page).hide();
            jQ(page).show();
            jQ(page).addClass("active");
        })
    });
</script>

<style>
    .border-gray {
        border-color: #dee2e6!important;
    }
    .mh-100 {
        height:100%;
    }
</style>

<main>
    <div class="container">
        <ul class="nav nav-tabs" role="tablist" id="myNav">
            <li class="nav-item">
                <a class="nav-link active" id="home-tab" 
                    data-toggle="tab" href="#home" role="tab" 
                    aria-controls="home" aria-selected="true">任务模版</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" id="profile-tab" 
                    data-toggle="tab" href="#profile" role="tab" 
                    aria-controls="profile" aria-selected="false">定时列表</a>
            </li>
            <li class="nav-item">
                <a class="nav-link " id="profile-tab" 
                    data-toggle="tab" href="#contact" role="tab" 
                    aria-controls="contact" aria-selected="false">执行列表</a>
            </li>
        </ul>
        <div class="tab-content border border-top-0 border-gray rounded-bottom mh-100" 
            style="padding-left:10px;padding-right:10px;min-height:500px;">
            <div class="tab-pane fade show active" id="home" role="tabpanel" aria-labelledby="home-tab">
                <TaskList></TaskList>
            </div>
            <div class="tab-pane fade" id="profile" role="tabpanel" aria-labelledby="profile-tab">
                <TimerList></TimerList>
            </div>
            <div class="tab-pane fade " id="contact" role="tabpanel" aria-labelledby="contact-tab">
                <ExectorList></ExectorList>
            </div>
        </div>
    </div>
</main>
