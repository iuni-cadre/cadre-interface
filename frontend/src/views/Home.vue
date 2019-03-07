<template>
    <div>
        <h1>Cadre Test Form</h1>
        <form @submit.stop.prevent="sendQuery()">
            <div class="form-group">
                <label>Year</label>
                <input class="form-control"
                       v-model="year">
            </div>
            <div class="d-flex flex-wrap">
                <div class="btn" v-for="field in fields"
                     :key="`${field}_field`">
                    <input type="checkbox"
                           :id="`${field}_field`"
                           v-model="selected_fields"
                           :value="field" />
                    <label :for="`${field}_field`"
                           v-text="field" ></label>
                </div>
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
            year: "1912",
            wos_id: "",
            database_status: {},
            status: {},
            selected_fields: []
        };
    },
    computed: {
        fields: function() {
            return this.$store.getters["query/validFields"];
        }
    },
    methods: {
        getStatus: function() {
            let status_prom = this.$cadre.axios({
                url: "/data/status"
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
                url: "/data/wos/status"
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
            // let database_prom = this.$cadre.axios({
            //     url: "/data/wos/publications/" + this.year
            // });
            // database_prom.then(
            //     result => {
            //         this.result = result.data;
            //     },
            //     err => {
            //         this.result = "Could not get data\n" + err;
            //     }
            // );
            if (isNaN(Number(this.year))) {
                console.debug("Not a year");
                this.year = "";
                return false;
            }

            let payload = {
                query: [
                    {
                        argument: "year",
                        value: Math.floor(Number(this.year))
                    }
                ],
                output_fields: ["ID", ...this.selected_fields],
                dataset: "wos"
            };

            let query_prom = this.$store.dispatch("query/sendQuery", payload);
            query_prom.then(
                result => {
                    this.result = result;
                },
                error => {
                    console.error(error);
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

