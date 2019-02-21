<template>
    <div>
        <h1>Cadre Test Form</h1>
        <form @submit.stop.prevent="sendQuery()">
            <div class="form-group">
                <label>Year</label>
                <input class="form-control"
                       v-model="year">
            </div>
            <!-- <p>OR</p>
        <div class="form-group">
            <label>WoS ID</label>
            <input class="form-control"
                   v-model="wos_id">
        </div> -->
            <div class="form-group">
                <button class="btn btn-primary"
                        type="submit">Submit Query</button>
            </div>
            <div>
                <label>Output</label>
                <pre class="pre"
                     v-text="result"></pre>
            </div>
        </form>

        <div>
            <label>Database Status</label>
            <pre v-text="database_status"></pre>
        </div>
        <div>
            <label>API Status</label>
            <pre v-text="status"></pre>
        </div>
    </div>
</template>
<script>
export default {
    data: function() {
        return {
            result: {},
            year: "",
            wos_id: "",
            database_status: {},
            status: {}
        };
    },
    methods: {
        getStatus: function() {
            let status_prom = this.$cadre.axios({
                url: "/status"
            });
            status_prom.then(
                result => {
                    this.status = result.data;
                },
                err => {
                    this.status = "Could not get status\n" + err;
                }
            );
            let database_prom = this.$cadre.axios({
                url: "/database"
            });
            database_prom.then(
                result => {
                    this.database_status = result.data;
                },
                err => {
                    this.database_status = "Could not get status\n" + err;
                }
            );
        },
        sendQuery: function() {
            let database_prom = this.$cadre.axios({
                url: "/database/" + this.year
            });
            database_prom.then(
                result => {
                    this.result = result.data;
                },
                err => {
                    this.result = "Could not get data\n" + err;
                }
            );
        }
    },
    mounted: function() {
        this.getStatus();
    }
};
</script>
<style lang="scss">
</style>

