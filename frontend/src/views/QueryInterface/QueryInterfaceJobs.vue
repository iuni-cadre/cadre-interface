<template>
    <div>
        <query-builder-header />

        <div class="mt-5">
            <router-link class="btn btn-primary" target="_blank" :to="{name: 'jupyter-hub'}">Go To Jupyter Notebook</router-link>
        </div>

        <table class="table mt-5">
            <tr>
                <th>Job ID</th>
                <th>Status</th>
                <th>Last Updated</th>
                <!-- <th>S3 Bucket</th> -->
            </tr>
            <tr v-for="job in jobs"
                :key="job[0]">

                <td v-text="job[0]">Job Id</td>
                <td v-text="job[3]">Status</td>
                <td v-text="job[5]">Status</td>
                <!-- <td><a :href="job[2]"
                       v-text="job[2]"></a></td> -->
            </tr>
            <tr v-if="jobs.length === 0">
                <td colspan="3">No jobs could be found</td>
            </tr>
        </table>
    </div>
</template>

<script>
import QueryBuilderHeader from "./QueryInterfaceHeader";

import axios from "axios";
export default {
    data: function() {
        return {
            jobs: []
        };
    },
    methods: {
        getJobs: function() {
            let prom = this.$cadre.qbAxios({
                url: "/user-jobs"
            });
            prom.then(
                response => {
                    this.jobs = response.data;
                },
                error => {
                    console.error(error);
                }
            );
        }
    },
    components: {
        QueryBuilderHeader
    },
    mounted: function() {
        this.getJobs();
    }
};
</script>

<style>
</style>
