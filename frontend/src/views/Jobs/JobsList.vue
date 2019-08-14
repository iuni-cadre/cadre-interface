<template>
    <div>
        <!-- <query-builder-header /> -->
        <section>
            <div class="container">
                <div class="m-3">
                    <router-link class="btn btn-primary"
                                 target="_blank"
                                 :to="{name: 'jupyter-hub'}">Go To Jupyter Notebook</router-link>
                </div>

                <div class="card">
                    <h4>Jobs</h4>
                    <table class="table mt-3">
                        <tr>
                            <th>Job ID</th>
                            <th>Status</th>
                            <th>Type</th>
                            <th>Started</th>
                            <th>Run Time</th>
                            <!-- <th>S3 Bucket</th> -->
                        </tr>
                        <tr v-for="job in jobs"
                            :class="{
                                'table-success': job.status == 'Completed',
                                'table-info': job.run_time <= (1000 * 60 * 10) && job.status == 'Running',
                                'table-danger': job.status == 'Failed',
                                'table-warning': job.run_time > (1000 * 60 * 10),
                                }"
                            :key="job.job_id">

                            <td v-text="job.job_id">Job Id</td>
                            <td v-text="job.status">Status</td>
                            <td v-text="job.type">Type</td>
                            <td v-text="job.start.toLocaleString()">Started</td>
                            <td v-text="(job.run_time/1000) + ' second' + ((job.run_time/100) !== 1?'s':'')"></td>
                            <!-- <td><a :href="job[2]"
                       v-text="job[2]"></a></td> -->
                        </tr>
                        <tr v-if="jobs.length === 0">
                            <td colspan="3">No jobs could be found</td>
                        </tr>
                    </table>
                </div>
            </div>
        </section>
    </div>
</template>

<script>
// import QueryBuilderHeader from "./QueryInterfaceHeader";

import axios from "axios";
export default {
    data: function() {
        return {
            jobs: [],
            refresh_timeout: 0
        };
    },
    methods: {
        getRunTime: function(job){
            let start_date = new Date(job[4]);
            let update_date = job[5] ? new Date(job[5]) : new Date();
            if(job[3] == "RUNNING" || job[3] == "SUBMITTED")
            {
                update_date = new Date();
            }

            // console.debug(start_date - update_date);

            let diff = update_date - start_date;
            // console.debug(start_date, update_date);
            // console.debug(diff);

            return diff; //> (10 * 60 * 1000);
        },
        getJobs: function() {
            let prom = this.$cadre.qbAxios({
                url: "/user-jobs"
            });
            prom.then(
                response => {
                    this.$set(this, "jobs", []);

                    // this.jobs = response.data;
                    // console.debug(response.data);
                    for(let job of response.data)
                    {
                        // console.debug(job);
                        this.jobs.push({
                            job_id: job[0],
                            status: job[3].substr(0, 1).toUpperCase() + job[3].substr(1).toLowerCase(),
                            type: job[6].substr(0, 1).toUpperCase() + job[6].substr(1).toLowerCase(),
                            start: new Date(job[4]),
                            update: job[5]?new Date(job[5]):new Date(),
                            run_time: this.getRunTime(job)
                        });

                    }

                    this.refresh_timeout = setTimeout(()=>{ this.getJobs(); }, 15000);
                },
                error => {
                    console.error(error);
                }
            );
        }
    },
    components: {
        // QueryBuilderHeader
    },
    beforeDestroy: function(){
        clearTimeout(this.refresh_timeout);
        this.refresh_timeout = 0;
    },
    mounted: function() {
        this.getJobs();
    }
};
</script>

<style>
</style>
