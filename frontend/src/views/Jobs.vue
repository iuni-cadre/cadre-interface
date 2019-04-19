<template>
    <div>
        <h1>Query Status</h1>
        <nav>
            <router-link :to="{name: 'home'}">Back To Query Builder</router-link>
        </nav>

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
import axios from "axios";
export default {
    data: function() {
        return {
            jobs: []
        };
    },
    methods: {
        getJobs: function() {
            let prom = axios({
                url:
                    this.$cadreConfig.localhost +
                    process.env.BASE_URL +
                    "api/user-jobs",
                headers: {
                    "auth-token": this.$store.getters["user/authToken"],
                    "auth-username": this.$store.getters["user/username"]
                }
            });
            prom.then(
                response => {
                    // console.debug(response.data);
                    this.jobs = response.data;
                },
                error => {
                    console.error(error);
                }
            );
        }
    },
    mounted: function() {
        this.getJobs();
    }
};
</script>

<style>
</style>
