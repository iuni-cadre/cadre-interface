<template>
    <div>
        <h1>Cadre Test Form</h1>
        <form @submit.stop.prevent="sendQuery()">
            <template v-for="(clause, index) in queries">
                <div :key="`clause_${index}`">
                    <div v-if="index > 0">
                        <div class="form-group">

                            <!-- <label>Operator</label> -->
                            <select class="form-control"
                                    style="width: auto"
                                    v-model="queries[index].operator">
                                <option disabled
                                        selected
                                        :value="''">Choose an operator</option>
                                <option v-for="operator in operator_types"
                                        :key="`${operator}_${index}`"
                                        :value="operator"
                                        v-text="operator"></option>
                            </select>
                        </div>
                    </div>
                    <div class=" d-flex justify-content-between align-items-end">
                        <div class="form-group">

                            <label>Field</label>
                            <select class="form-control"
                                    v-model="queries[index].field">
                                <option disabled
                                        selected
                                        :value="''">Choose a search field</option>
                                <option v-for="field in field_options"
                                        :key="`${field.value}_${index}`"
                                        :value="field.value"
                                        v-text="field.label"></option>
                            </select>
                        </div>
                        <div class="form-group col">

                            <label>Value</label>
                            <input class="form-control"
                                   type="text"
                                   v-model="queries[index].value" />
                        </div>
                        <div class="form-group">
                            <button class="btn btn-danger"
                                    @click.stop.prevent="removeQueryClause(index)">X</button>
                        </div>
                    </div>
                </div>
            </template>

            <div>
                <button class="btn btn-primary"
                        @click.stop.prevent="addQueryClause()">Add Search Clause</button>
            </div>
            <!-- <pre>{{queries}}</pre> -->

            <div class="row my-5">
                <div class="col">
                    Output Fields
                </div>
            </div>
            <div class="row">

                <div class="col-3 d-flex align-items-center"
                     v-for="field in fields"
                     :key="`${field}_field`">

                    <input type="checkbox"
                           :id="`${field}_field`"
                           v-model="selected_fields"
                           :value="field" />

                    <label :for="`${field}_field`"
                           v-text="field"></label>
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
let field_options = [
    { value: "year", label: "Year" },
    { value: "author", label: "Author" },
    { value: "wos_id", label: "WoS ID" },
    { value: "journal", label: "Journal Title" },
    { value: "abstract", label: "Abstract" }
];
let operator_types = [
    "OR",
    "AND"
    // "NOT"
];

export default {
    data: function() {
        return {
            result: {},
            year: "1912",
            wos_id: "",
            database_status: {},
            status: {},
            selected_fields: [
                "PubType",
                "PubYear",
                "PubMonth",
                "CoverDate",
                "City",
                "AddressCount"
            ],
            queries: [
                {
                    field: "",
                    value: "",
                    join: ""
                }
            ]
        };
    },
    computed: {
        fields: function() {
            return this.$store.getters["query/validFields"];
        },
        field_options: function() {
            return field_options;
        },
        operator_types: function() {
            return operator_types;
        }
    },
    methods: {
        addQueryClause: function(clause) {
            this.queries.push({
                field: "",
                value: "",
                operator: ""
            });
        },
        removeQueryClause: function(index) {
            this.queries.splice(index, 1);
        },
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
            // if (isNaN(Number(this.year))) {
            //     console.debug("Not a year");
            //     this.year = "";
            //     return false;
            // }

            let query = [];
            for (let clause of this.queries) {
                if (clause.field && clause.value) {
                    query.push({
                        argument: clause.field,
                        value: clause.value,
                        operator: clause.operator
                    });
                }
            }

            if (query.length === 0) {
                console.error("Empty Query", this.queries);
                return false;
            }

            let payload = {
                query: query,
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

