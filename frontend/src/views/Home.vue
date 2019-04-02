<template>
    <div>
        <h1>Query Builder</h1>
        <form @submit.stop.prevent="sendQuery()">

            <h2 class="mt-5">Filters</h2>
            <div class="card container py-3 mb-3">
                <template v-for="(clause, index) in queries">
                    <div :key="`clause_${index}`">

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

                        <div v-if="index != queries.length - 1">
                            <div class="form-group">

                                <!-- <label>Operator</label> -->
                                <select class="form-control"
                                        style="width: auto"
                                        v-model="queries[index].operator">
                                    <option disabled
                                            selected
                                            :value="''">Choose an operand</option>
                                    <option v-for="operator in operator_types"
                                            :key="`${operator}_${index}`"
                                            :value="operator"
                                            v-text="operator"></option>
                                </select>
                            </div>
                        </div>
                    </div>
                </template>
                <div>
                    <button class="btn btn-primary"
                            @click.stop.prevent="addQueryClause()">Add Another Filter</button>
                </div>
            </div>


            <h2 class="mt-5">Output Fields</h2>
            <div>
                <label class="btn btn-sm mr-5"
                       :class="{
                            'btn-outline-primary': fields_view != 'selected',
                            'btn-primary': fields_view == 'selected'
                        }"><input type="radio"
                           v-model="fields_view"
                           value="selected" />Show Selected Only</label>
                <label class="btn btn-sm"
                       :class="{
                            'btn-outline-primary': fields_view != 'all',
                            'btn-primary': fields_view == 'all'
                        }"><input type="radio"
                           v-model="fields_view"
                           value="all" />Show All Available Fields</label>
            </div>
            <div class="card container">
                <div class="row ">
                    <template v-for="field in fields">
                        <div class="col-3 d-flex align-items-center p-1"
                             :key="`${field}_field`"
                             v-if="fields_view=='all' || selected_fields.indexOf(field) >= 0">
                            <label class="btn"
                                   :class="{
                            'btn-outline-primary': selected_fields.indexOf(field) == -1,
                            'btn-primary': selected_fields.indexOf(field) >= 0,
                        }">
                                <input type="checkbox"
                                       class="mr-2"
                                       :id="`${field}_field`"
                                       v-model="selected_fields"
                                       :value="field" />

                                <span :for="`${field}_field`"
                                      v-text="field"></span>
                            </label>
                        </div>
                    </template>
                </div>
            </div>

            <!-- <p>OR</p>
        <div class="form-group">
            <label>WoS ID</label>
            <input class="form-control"
                   v-model="wos_id">
        </div> -->
            <div class="form-group mt-5">
                <button class="btn btn-primary btn-lg"
                        type="submit">Preview Query</button>
            </div>

            <div class="form-group mt-5">
                <button @click.stop.prevent="sendQuery(true)" class="btn btn-primary btn-lg"
                        type="submit">Submit Query</button>
            </div>
        </form>

        <div>
            <label>Output</label>
            <pre class="pre"
                 v-text="result"></pre>
        </div>
        <!-- <div>
            <label>Database Status</label>
            <pre v-text="database_status"></pre>
        </div> -->
        <div>
            <label>API Status</label>
            <pre v-text="status"></pre>
        </div>
    </div>
</template>
<script>
let field_options = [
    { value: "wosId", label: "WoS ID" },
    { value: "year", label: "Year" },
    { value: "authorsFullName", label: "Author" },
    { value: "journalsName", label: "Journal Name" },
    { value: "abstractText", label: "Abstract" }
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
                "wosId",
                "year",
                "authorsFullName",
                "journalsName",
            ],
            queries: [
                {
                    field: "",
                    value: "",
                    join: ""
                }
            ],
            fields_view: "selected"
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
        sendQuery: function(async) {
            async = async || false;
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
                async: async,
                query: query,
                output_fields: [...this.selected_fields],
                dataset: "wos"
            };

            let query_prom = this.$store.dispatch("query/sendQuery", payload);
            this.result = "Sending Query...";
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

