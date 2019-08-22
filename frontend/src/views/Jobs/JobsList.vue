<template>
    <div>
        <!-- <query-builder-header /> -->
        <section>
            <div class="container">
                <div class="m-3">
                    <router-link class="btn btn-primary"
                                 target="_blank"
                                 :to="{name: 'jupyter-hub'}">Go To Jupyter Notebook</router-link>


                    <button class="float-right btn btn-primary"
                                 @click.stop.prevent="getJobs"><fa icon="sync-alt" /> &nbsp;Refresh Status</button>
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
                        <tr v-for="job in jobs_sorted"
                            :class="{
                                'table-success': job.status == 'Completed',
                                'table-info': job.run_time <= (1000 * 60 * 10) && job.status == 'Running',
                                'table-danger': job.status == 'Failed',
                                'table-warning': (job.status == 'Running' || job.status == 'Submitted') && job.run_time > (1000 * 60 * 10),
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
    computed: {
        jobs_sorted: function() {
            let sorted = this.jobs.sort((job_a, job_b) => {
                if(job_a.update < job_b.update)
                {
                    return 1;
                }
                else
                {
                    return -1;
                }
            });

            return sorted;
        }
    },
    methods: {
        getRunTime: function(job) {
            let start_date = new Date(job[4]);
            let update_date = job[5] ? new Date(job[5]) : new Date();
            if (job[3] == "RUNNING" || job[3] == "SUBMITTED") {
                update_date = new Date();
            }

            // console.debug(start_date - update_date);

            let diff = update_date - start_date;
            // console.debug(start_date, update_date);
            // console.debug(diff);

            return diff; //> (10 * 60 * 1000);
        },
        getJobs: function() {
            // for (let job of sample_jobs) {
            //     // console.debug(job);
            //     this.jobs.push({
            //         job_id: job[0],
            //         status:
            //             job[3].substr(0, 1).toUpperCase() +
            //             job[3].substr(1).toLowerCase(),
            //         type:
            //             job[6].substr(0, 1).toUpperCase() +
            //             job[6].substr(1).toLowerCase(),
            //         start: new Date(job[4]),
            //         update: job[5] ? new Date(job[5]) : new Date(),
            //         run_time: this.getRunTime(job)
            //     });
            // }
            // return false;


            clearTimeout(this.refresh_timeout);
            this.refresh_timeout = 0;

            let prom = this.$cadre.qbAxios({
                url: "/user-jobs"
            });
            prom.then(
                response => {
                    this.$set(this, "jobs", []);

                    // this.jobs = response.data;
                    // console.debug(response.data);
                    for (let job of response.data) {
                        // console.debug(job);
                        this.jobs.push({
                            job_id: job[0],
                            status:
                                job[3].substr(0, 1).toUpperCase() +
                                job[3].substr(1).toLowerCase(),
                            type:
                                job[6].substr(0, 1).toUpperCase() +
                                job[6].substr(1).toLowerCase(),
                            start: new Date(job[4]),
                            update: job[5] ? new Date(job[5]) : new Date(),
                            run_time: this.getRunTime(job)
                        });
                    }

                    this.refresh_timeout = setTimeout(() => {
                        this.getJobs();
                    }, 10000);
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
    beforeDestroy: function() {
        clearTimeout(this.refresh_timeout);
        this.refresh_timeout = 0;
    },
    mounted: function() {
        this.getJobs();
    }
};

const sample_jobs = [
    [
        "de790e54-2160-44e3-b4f6-40e2cc02adcf",
        "9ab47f16-9737-424c-8c2d-009802a6795a",
        null,
        "COMPLETED",
        "Thu, 08 Aug 2019 20:26:34 GMT",
        "Thu, 08 Aug 2019 20:26:35 GMT",
        "PACKAGE",
        null
    ],
    [
        "a59d272d-542c-40fc-b845-120eef11e95a",
        "46ac77b3-3259-4eb3-8dfd-8a5dd6e674c0",
        null,
        "COMPLETED",
        "Fri, 09 Aug 2019 20:35:17 GMT",
        "Fri, 09 Aug 2019 20:35:17 GMT",
        "PACKAGE",
        null
    ],
    [
        "ebf363a1-ef95-4c00-b3d6-628f673e3336",
        "c15938cc-4ef0-4b24-8cb5-f1b10aeec437",
        null,
        "COMPLETED",
        "Mon, 12 Aug 2019 17:47:51 GMT",
        "Mon, 12 Aug 2019 17:47:52 GMT",
        "PACKAGE",
        null
    ],
    [
        "94cde50f-3a5f-4c38-bc9f-23ef5430bd7d",
        "f7ab2915-14ee-493f-a1d6-5b8d1d1b4f89",
        null,
        "COMPLETED",
        "Mon, 12 Aug 2019 19:39:09 GMT",
        "Mon, 12 Aug 2019 19:39:09 GMT",
        "PACKAGE",
        null
    ],
    [
        "1230c59b-1237-4bdd-bc46-428276dd34f1",
        "87e502d4-3237-4289-b420-a7db183cf656",
        null,
        "COMPLETED",
        "Wed, 14 Aug 2019 19:05:44 GMT",
        "Wed, 14 Aug 2019 19:10:12 GMT",
        "QUERY",
        null
    ],
    [
        "8de1303f-c8a8-4b84-aa4d-d8aa4869748e",
        "9cce9c87-a4a2-48b2-be82-e58175ec49ed",
        null,
        "COMPLETED",
        "Wed, 14 Aug 2019 19:15:03 GMT",
        "Wed, 14 Aug 2019 19:15:31 GMT",
        "QUERY",
        null
    ],
    [
        "38933c0b-6301-4a58-b883-84ffd2d38726",
        "ccd20f52-abb0-4f2b-a82f-b632305645b0",
        null,
        "COMPLETED",
        "Wed, 14 Aug 2019 19:16:14 GMT",
        "Wed, 14 Aug 2019 19:16:14 GMT",
        "QUERY",
        null
    ],
    [
        "e8ef14e7-6ed5-41a1-9568-b403757ef7cb",
        "92f5f800-c081-4733-b4d6-2c9486196c4b",
        null,
        "COMPLETED",
        "Wed, 14 Aug 2019 19:18:03 GMT",
        "Wed, 14 Aug 2019 19:18:03 GMT",
        "QUERY",
        null
    ],
    [
        "c40c19d8-7c96-4b71-97f5-ac4a61229831",
        "e8924bc3-0b9c-4902-abed-7276b6898fda",
        null,
        "COMPLETED",
        "Wed, 14 Aug 2019 19:20:59 GMT",
        "Wed, 14 Aug 2019 19:20:59 GMT",
        "QUERY",
        null
    ],
    [
        "c2c48705-2718-4375-b13c-324bfd7e344c",
        "b2555110-21b5-4cd4-8e6e-a4158b934a9f",
        null,
        "COMPLETED",
        "Wed, 14 Aug 2019 19:21:51 GMT",
        "Wed, 14 Aug 2019 19:21:52 GMT",
        "QUERY",
        null
    ],
    [
        "3f1f332b-006b-4c1c-967b-1d1a518a7553",
        "9956a5a7-dd29-4a8d-91f4-b8a08d2a3efa",
        null,
        "COMPLETED",
        "Wed, 14 Aug 2019 19:42:23 GMT",
        "Wed, 14 Aug 2019 19:42:23 GMT",
        "QUERY",
        null
    ],
    [
        "3f6e13a2-15b2-45d1-8d04-fef12393b0d3",
        "6eab86b8-bac5-4a0e-9485-1e3d27f58414",
        null,
        "COMPLETED",
        "Wed, 14 Aug 2019 19:56:05 GMT",
        "Wed, 14 Aug 2019 19:56:31 GMT",
        "QUERY",
        null
    ],
    [
        "bbc24970-5e05-41ef-9de5-b274eb7fca9e",
        "2d2718ca-0020-486c-8597-166e7fc79290",
        null,
        "COMPLETED",
        "Wed, 14 Aug 2019 21:18:00 GMT",
        "Wed, 14 Aug 2019 21:22:28 GMT",
        "QUERY",
        null
    ],
    [
        "fd938250-9b70-49f8-9acc-a41b5de2a58c",
        "36f7d256-6181-4773-be01-b7fa2a209e6b",
        null,
        "COMPLETED",
        "Wed, 14 Aug 2019 21:24:06 GMT",
        "Wed, 14 Aug 2019 21:31:22 GMT",
        "QUERY",
        null
    ],
    [
        "7ade28cb-7202-47be-a070-d9fe963e81cf",
        "9830aa80-6acc-4a80-85dc-a6a25bf400e4",
        null,
        "COMPLETED",
        "Wed, 14 Aug 2019 21:32:26 GMT",
        "Wed, 14 Aug 2019 21:45:29 GMT",
        "QUERY",
        null
    ],
    [
        "e236222c-7750-40f5-b1b9-cf95f0f1939a",
        "39968dd3-77c5-4d2b-bb58-6a0f0d167242",
        null,
        "COMPLETED",
        "Thu, 15 Aug 2019 21:57:23 GMT",
        "Thu, 15 Aug 2019 21:58:10 GMT",
        "QUERY",
        null
    ],
    [
        "61dd13b1-628c-4df5-865d-5edc9184fc30",
        "99529996-d6d2-4216-8b36-dd4347f7f9b5",
        null,
        "COMPLETED",
        "Thu, 15 Aug 2019 22:01:37 GMT",
        "Thu, 15 Aug 2019 22:06:25 GMT",
        "QUERY",
        null
    ],
    [
        "61f77f9a-2d8b-4829-97e1-b40f716931ec",
        "798b1738-f0c7-4e51-80c9-9d9ba8fc457f",
        null,
        "COMPLETED",
        "Fri, 16 Aug 2019 14:02:14 GMT",
        "Fri, 16 Aug 2019 14:03:19 GMT",
        "QUERY",
        null
    ],
    [
        "a5c377c9-9bab-4393-90db-8a77168b6cb1",
        "a2079714-d05f-425f-8f47-8774d5fc8691",
        null,
        "COMPLETED",
        "Fri, 16 Aug 2019 16:06:39 GMT",
        "Fri, 16 Aug 2019 16:06:39 GMT",
        "PACKAGE",
        null
    ],
    [
        "0e74c111-37fa-49b7-800e-46a787d6cbe0",
        "9593ca9d-c7b4-49d1-a804-c81ddbbe1849",
        null,
        "COMPLETED",
        "Fri, 16 Aug 2019 19:01:15 GMT",
        "Fri, 16 Aug 2019 19:02:16 GMT",
        "QUERY",
        null
    ],
    [
        "05233a8b-3c8d-4724-8dbd-5e0f8b118446",
        "1cd5027c-f9bb-4109-b137-6aef7eba48fa",
        null,
        "SUBMITTED",
        "Mon, 12 Aug 2019 14:59:14 GMT",
        null,
        "PACKAGE",
        null
    ]
];
</script>

<style>
</style>
