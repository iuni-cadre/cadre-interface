<script>
import QueryBuilderHeader from "./QueryInterfaceHeader";
import OutputFields from "@/components/QueryBuilder/QueryBuilderOutputFields";
import Datasets from "../../datasets";
import QueryBuilderFilter from "../../components/QueryBuilder/QueryBuilderFilter";

// let operator_types = [
//     "AND",
//     "OR"
//     // "NOT"
// ];

export default {
    data: function () {
        return {
            result: null,
            database_status: {},
            status: {},
            job_name: "",
            selected_fields: [
                // "wosId",
                // "year",
                // "authorsFullName",
                // "journalName"
            ],
            network_field_degrees: {},
            network_field_selected: false,

            queries: [
                {
                    field: "",
                    value: [],
                },
            ],
            preview_result: null,
            fields_view: "selected",
            error_message: "",
            query_results: {
                job_id: "",
                message_id: "",
                s3_location: "",
            },
            query_modal_open: false,
            query_errors: {},
        };
    },
    computed: {
        allow_overload: function () {
            return this.$cadreConfig.allow_overload || false;
        },
        dataset_name: function () {
            try {
                return Datasets[this.$store.getters["query/selectedDataset"]]
                    .name;
            } catch (err) {
                return "";
            }
        },
        database_type: function () {
            try {
                return Datasets[this.$store.getters["query/selectedDataset"]]
                    .database_type;
            } catch (err) {
                return "";
            }
        },
        is_loading: function () {
            return this.isLoading;
        },

        all_fields: function () {
            let fields = this.$store.getters["query/outputFields"];
            let fields_obj = {};

            for (let field of fields) {
                fields_obj[field.field] = field;
            }
            return fields_obj;
        },
        fields: function () {
            // return this.$store.getters["query/validFields"];
            let fields = this.$store.getters["query/outputFields"];
            let fields_obj = {};

            for (let field of fields) {
                // console.debug(field.type);
                if (field.type == "single") {
                    fields_obj[field.field] = field;
                }
            }
            return fields_obj;
        },
        network_fields: function () {
            let fields = this.$store.getters["query/outputFields"];
            let fields_obj = {};

            for (let field of fields) {
                // console.debug(field.type);
                if (field.type == "network") {
                    fields_obj[field.field] = field;
                }
            }
            return fields_obj;
        },
        default_fields: function () {
            return this.$cadre.cloneObject(
                this.$store.getters["query/defaultFields"]
            );
        },
        field_options: function () {
            // return field_options;
            let field_array = [];
            let fields = this.$store.getters["query/inputFields"];
            for (let field in fields) {
                field_array.push({value: field, label: fields[field]});
            }

            const exclusive_fields =
                (Datasets[this.$store.getters["query/selectedDataset"]] &&
                    Datasets[this.$store.getters["query/selectedDataset"]]
                        .fields.exclusive_input_fields) ||
                [];

            let exclusive_selected = this.queries
                .filter((item) => exclusive_fields.includes(item.field))
                .map((item) => item.field);

            return function (current_value) {
                // console.debug(exclusive_selected, current_value)
                if (exclusive_selected.length > 0) {
                    let filtered = field_array.filter(
                        (item) =>
                            item.value == current_value ||
                            !exclusive_selected.includes(item.value)
                    );
                    return filtered;
                }

                return field_array;
            };
        },
        selected_network_outputs: function () {
            let fields = this.network_fields;
            let outputs = [];

            for (let field_name in fields) {
                let field = fields[field_name];
                if (
                    field.type == "network" &&
                    this.selected_fields.indexOf(field.field) >= 0
                ) {
                    outputs.push(field);
                }
            }

            return outputs;
            // return this.fields.filter(field => {
            //     if (
            //         field.type == "network" &&
            //         this.selected_fields.indexOf(field.field) >= 0
            //     ) {
            //         return field;
            //     }
            // });
        },
        // queries: function() {
        //     return this.$store.getters["query/queryClauses"];
        // },
        operator_types: function () {
            let types = [];
            types.push("AND");
            if (this.database_type != "janus") {
                types.push("OR");
            }
            return types;
        },
        preview_data: function () {
            // let tmp =
            //     (this.result && this.result.data && this.result.data.wos) ||
            //     null;
            // if (tmp) {
            //     tmp.splice(9);
            // }
            return this.result || null;
        },
    },
    methods: {
        overloadDatabase: function () {
            if (!this.allow_overload) {
                console.error(
                    "What in the everloving hell do you think you're doing!?"
                );
                return false;
            } else {
                console.error(
                    "You're about to cause major havok and overload CADRE."
                );
            }

            let confirmed = confirm(
                "Are you absolutely sure you want to set CADRE on fire?"
            );

            if (confirmed) {
                confirmed = confirm("Last chance to cancel... ");
            }

            if (confirmed) {
                console.error("Here we go...");

                //find year
                var year_index = -1;
                for (var i in this.queries) {
                    if (this.queries[i].field == "year") {
                        year_index = i;
                    }
                }

                for (let i = 0; i < 80; i++) {
                    console.warn("Sending query " + i);

                    //change year
                    if (year_index >= 0) {
                        this.queries[year_index].value--;
                    }

                    this.sendQuery(true);
                }
                console.error("You monster...");
            }

            return false;
        },
        getStoreQuery: function () {
            if (this.$store.getters["query/query"].length > 0) {
                this.$set(this, "queries", this.$store.getters["query/query"]);
            } else {
                this.$set(this, "queries", [
                    {
                        field: "",
                        value: [
                            {
                                value: "",
                                operator: "",
                            },
                        ],
                        operator: "",
                    },
                ]);
            }
        },
        setStoreQuery: function () {
            this.$store.commit("query/setQuery", this.queries);
        },

        addQueryClause: function (clause) {
            let len = this.queries.length;

            //when adding a new clause, set the operator of the previous clause
            // if (len) {
            //     this.queries[len - 1].operator = this.operator_types[0];
            // }

            this.queries.push({
                field: "",
                value: [
                    {
                        value: "",
                        operator: "",
                    },
                ],
                operator: "",
            });

            this.setStoreQuery();
        },
        removeQueryClause: function (index) {
            this.queries.splice(index, 1);
            this.setStoreQuery();
        },
        sendQuery: async function (async) {

            await this.startCluster();
            //async is false for preve, true for full query
            async = async || false;
            let query = [];

            //clear any errors
            this.$set(this, "query_errors", {});

            //detect any new errors
            for (let index in this.queries) {
                if (!this.queries[index].field || !this.queries[index].value) {
                    this.query_errors[index] = "Filter is empty";
                }
                // this.queries[index].value = this.queries[index].value + "";
            }

            //error message and exit if errors
            if (Object.keys(this.query_errors).length > 0) {
                this.error_message = "One or more of your filters is invalid.";
                return false;
            }
            if (this.queries.length === 0) {
                this.error_message = "You must provide at least one filter.";
                console.error("Empty Query", this.queries);
                return false;
            }


            //save the query
            this.setStoreQuery();
            //start loading
            if (!async) {
                this.$store.commit("loading/addKey", {
                    message: "Fetching Preview...",
                    key: "query",
                });
            } else {
                this.$store.commit("loading/addKey", {
                    message: "Sending Query...",
                    key: "query",
                });
            }
            //build up the output fields
            let output_fields = [];
            for (let selected_field of this.selected_fields) {
                let field = this.all_fields[selected_field];
                let field_to_add = {
                    field: field.field,
                    type: field.type,
                };
                //if the output is a network type, there should be a degree associated with it.
                if (field.type == "network") {
                    field_to_add.degree = 1;
                    // this.network_field_degrees[field.field] || 1;
                }
                output_fields.push(field_to_add);
            }

            //create payload
            let payload = {
                job_name: this.job_name,
                async: async,
                output_fields: output_fields,
            };
            //launch query
            this.result = null;

            // let query_prom = this.$store.dispatch("query/sendQuery", payload);
            // let query_prom = Promise.reject(); //just for testing

            try {
                let result = await this.$store.dispatch(
                    "query/sendQuery",
                    payload
                );

                console.debug(result);
                if (!async) {
                    if (result.errors) {
                        console.error("GraphQL Error: ", result.errors);
                        this.error_message = "";
                        for (let error of result.errors) {
                            this.error_message += error.message + " ";
                        }
                        this.result = null;
                    } else {
                        this.result = result;
                    }
                } else {
                    if (result[0] && result[1] === 200) {
                        this.query_results.job_id = result[0].job_id;
                        this.query_results.message_id = result[0].message_id;
                        this.query_results.s3_location = result[0].s3_location;
                        this.query_modal_open = true;
                    }
                }
            } catch (error) {
                // console.error(error);
                if (error.code === 1000) {
                    if (async) {
                        this.error_message =
                            "Your query timed out.  Please try again in a moment.";
                    } else {
                        this.error_message =
                            "Your preview query timed out.  Please try again in a moment.";
                    }
                } else if (error.response) {
                    // console.debug(error.response.data.error);
                    if (error.response.status == 401) {
                        this.error_message =
                            "You do not have access to this dataset.";
                    } else if (error.response.data.error) {
                        this.error_message =
                            error.response.data.error.toString();
                    } else {
                        // console.error(error)
                        this.error_message =
                            "Unknown error: " + error.response.status;
                    }
                } else {
                    console.debug(error);
                    this.error_message = error.toString();
                }
            }
            this.$store.commit("loading/removeKey", {key: "query"});
        },
        async startCluster() {
            try {
                this.$cadre
                    .axios({
                        url: `${this.$cadreConfig.query_builder_api_prefix}/start_cluster`,
                        method: "POST",
                        data: {dataset: this.dataset_name},
                    })
                    .then(
                        (resp) => {
                            console.info(
                                "Start cluster signal sent successfully."
                            );
                        },
                        (err) => {
                            console.error("Couldn't start cluster: ", err);
                        }
                    );
            } catch (e) {
                console.error("Couldn't start cluster: ", e);
            }
        },
        clickNetworkField(field_name) {
            for (let field in this.network_fields) {
                let index = this.selected_fields.indexOf(field);
                // console.log(index);
                if (index > -1) {
                    this.selected_fields.splice(index, 1);
                }
            }

            if (this.network_field_selected == field_name) {
                this.network_field_selected = null;
            } else {
                this.network_field_selected = field_name;
                this.selected_fields.push(field_name);
            }
        },
        filterFieldChanged({index, field}) {
            // console.debug(index, field);
            this.queries[index].field = field;
        },
        filterValueChanged({index, value}) {
            // console.debug(index, value);
            this.queries[index].value = value;
        },
        filterRemoveClickHandler({index}) {
            // console.debug(index);
            this.removeQueryClause(index);
        },
    },
    props: {
        isLoading: Boolean,
    },
    components: {
        QueryBuilderHeader,
        OutputFields,
        QueryBuilderFilter,
    },
    watch: {
        default_fields: function (o, n) {
            this.$set(this, "selected_fields", this.default_fields);
        },
        selected_fields: function () {
            for (let field in this.network_field_degrees) {
                if (this.selected_fields.indexOf(field) < 0) {
                    this.$delete(this.network_field_degrees, field);
                }
            }
        },
        selected_network_outputs: function () {
            for (let field of this.selected_network_outputs) {
                if (!this.network_field_degrees[field.field]) {
                    this.$set(this.network_field_degrees, field.field, 1);
                }
            }
        },
    },
    mounted: async function () {
        if (!this.$store.getters["query/selectedDataset"]) {
            this.$router.push({name: "query-builder"});
            return false;
        } else {
            try {
                this.$cadre
                    .axios({
                        url: `${this.$cadreConfig.query_builder_api_prefix}/start_cluster`,
                        method: "POST",
                        data: {dataset: this.dataset_name},
                    })
                    .then(
                        (resp) => {
                            console.info(
                                "Start cluster signal sent successfully."
                            );
                        },
                        (err) => {
                            console.error("Couldn't start cluster: ", err);
                        }
                    );
            } catch (e) {
                console.error("Couldn't start cluster: ", e);
            }

            this.$set(this, "selected_fields", this.default_fields);
            this.getStoreQuery();
        }
    },
};
</script>

<template>
    <!--
######## ######## ##     ## ########  ##          ###    ######## ########
   ##    ##       ###   ### ##     ## ##         ## ##      ##    ##
   ##    ##       #### #### ##     ## ##        ##   ##     ##    ##
   ##    ######   ## ### ## ########  ##       ##     ##    ##    ######
   ##    ##       ##     ## ##        ##       #########    ##    ##
   ##    ##       ##     ## ##        ##       ##     ##    ##    ##
   ##    ######## ##     ## ##        ######## ##     ##    ##    ########
    -->
    <div>
        <query-builder-header/>
        <section>
            <div class="container">
                <h3 class>
                    Query the
                    <u>{{ dataset_name }}</u> dataset
                </h3>
                <form @submit.stop.prevent="sendQuery()">
                    <div class="card container mb-3">
                        <h4>Filters</h4>

                        <template v-for="(clause, index) in queries">
                            <div :key="`clause_${index}`">
                                <query-builder-filter
                                    :index="index"
                                    :query_errors="query_errors"
                                    :queries="queries"
                                    :operator_types="operator_types"
                                    :value="queries[index]"
                                    @fieldChanged="filterFieldChanged"
                                    @valueChanged="filterValueChanged"
                                    @removeFilter="filterRemoveClickHandler"
                                />
                            </div>
                        </template>

                        <div class="alert">
                            <button
                                class="btn btn-outline-primary"
                                type="button"
                                @click.stop.prevent="addQueryClause()"
                            >
                                + Add Additional Filter
                            </button>
                        </div>
                    </div>

                    <div class="card mb-3">
                        <h4 class>Output Fields</h4>
                        <!-- <div>Help Text</div> -->
                        <div class="alert">
                            <output-fields
                                v-model="selected_fields"
                            ></output-fields>
                        </div>
                    </div>
                    <div
                        v-if="Object.keys(network_fields).length > 0"
                        class="card mb-3"
                    >
                        <h4>Network Queries</h4>
                        <!-- <div>Help Text</div> -->
                        <div>
                            <p>
                                CADRE supports the generation of citations and
                                references graphs. The user specifies a set of
                                filtering criteria to generate a list of query
                                papers or patents that fit the criteria. A
                                citations graph consists of the query results
                                and any papers or patents the query results
                                cite, with edges representing citations by the
                                query result. A references graph consists of the
                                query results and any papers or patents
                                referencing the query results, with edges
                                representing references made to the query
                                results.
                            </p>
                            <p>
                                When requesting a citations or references graph,
                                the user should pose narrow queries so as not to
                                exceed processing capacity. To constrain the
                                graph generation within processing capacity, a
                                limit of 100000 papers or patents has been placed
                                on the number of query results that the graph
                                generation supports. Any generated citations or
                                references graph with 100000 or more items
                                included should be considered an incomplete
                                graph and it is recommended that the user should
                                resubmit their query more narrow search
                                criteria.
                            </p>
                        </div>
                        <div
                            v-for="(field, field_name) in network_fields"
                            class="
                                d-flex
                                justify-content-start
                                align-items-center
                            "
                            :key="`network_field_${field_name}`"
                        >
                            <label
                                class="btn mb-3"
                                :class="{
                                    'btn-outline-primary':
                                        network_field_selected != field.field,
                                    'btn-primary':
                                        network_field_selected == field.field,
                                }"
                                :for="`${field.field}_field`"
                            >
                                <input
                                    type="radio"
                                    class="mr-2"
                                    :id="`${field.field}_field`"
                                    :checked="
                                        network_field_selected == field.field
                                    "
                                    :value="field.field"
                                    @click="clickNetworkField(field.field)"
                                    name="network_field"
                                />
                                Include
                                <strong
                                    :for="`${field.field}_field`"
                                    v-text="field.label"
                                ></strong>
                            </label>
                            <!-- <div
                                class="ml-3 d-flex align-items-center network-query-degrees"
                                :class="{
                                        'text-muted disabled': selected_fields.indexOf(field.field) == -1,
                                        }"
                            > -->
                            <!-- <span>Degrees:</span>
                                <span
                                    v-for="degree in [1, 2]"
                                    :key="`${field.field}_degree_${degree}`"
                                >
                                    <label
                                        class="btn ml-3 mb-0"
                                        :title=" degree > 1 ? 'Coming Soon...': ''"
                                        :class="{
                                                    'disabled': selected_fields.indexOf(field.field) == -1 || degree > 1,
                                                    'btn-outline-primary': network_field_degrees[field.field] != degree,
                                                    'btn-primary': network_field_degrees[field.field] == degree,
                                                    }"
                                    >
                                        <input
                                            type="radio"
                                            :disabled="selected_fields.indexOf(field.field) == -1 || degree > 1"
                                            class="mr-2"
                                            :id="`${field.field}_field_degree`"
                                            v-model="network_field_degrees[field.field]"
                                            :value="degree"
                                        />
                                        <span v-text="degree"></span>
                                    </label> -->
                            <!-- <label class="btn ml-3 mb-0"
                                           :class="{
                                                    'disabled': selected_fields.indexOf(field.field) == -1,
                                                    'btn-outline-primary': network_field_degrees[field.field] != degree,
                                                    'btn-primary': network_field_degrees[field.field] == degree,
                                                    }">
                                        <input type="radio"
                                               :disabled='selected_fields.indexOf(field.field) == -1'
                                               class="mr-2"
                                               :id="`${field.field}_field_degree`"
                                               v-model="network_field_degrees[field.field]"
                                               :value="degree" />
                                        <span v-text="degree"></span>
                                    </label>-->
                            <!-- </span> -->
                            <!-- </div> -->
                        </div>
                    </div>

                    <div class="card mb-3">
                        <div class="form-group">
                            <h4 class>
                                <label for="job_name"
                                >Job Name
                                    <small class="text-muted"
                                    >(Optional)</small
                                    ></label
                                >
                            </h4>

                            <p>
                                To make it easier to identify the status of a
                                specific query, you may enter an optional job
                                name.
                            </p>
                            <p></p>
                            <div class="form-group col">
                                <input
                                    id="job_name"
                                    class="form-control"
                                    type="text"
                                    v-model="job_name"
                                    maxlength="255"
                                    placeholder="Some Name"
                                />
                            </div>
                        </div>
                    </div>

                    <div v-if="database_type != 'janus'" class="card mb-3">
                        <div class="form-group">
                            <button
                                v-if="selected_fields.length == 0"
                                class="btn btn-primary btn-lg disabled"
                                disabled
                            >
                                Preview Query
                            </button>
                            <button
                                v-else
                                class="btn btn-primary btn-lg"
                                type="submit"
                            >
                                Get Preview
                            </button>
                        </div>
                        <div v-if="preview_data">
                            <h4 class="mt-5">Preview Results</h4>
                            <table class="table">
                                <tr>
                                    <th
                                        v-for="(
                                            data, field_name
                                        ) in preview_data[0]"
                                        v-text="field_name"
                                        :key="`preview_header_${field_name}`"
                                    ></th>
                                </tr>
                                <template v-for="(row, index) in preview_data">
                                    <tr :key="`preview_row_${index}`">
                                        <td
                                            v-for="(value, field_name) in row"
                                            v-text="
                                                (value !== undefined &&
                                                    value !== null &&
                                                    String(value)
                                                        .split('|')
                                                        .join(', ')) ||
                                                ''
                                            "
                                            :key="`preview_row_${index}_${field_name}`"
                                        ></td>
                                    </tr>
                                </template>
                                <tr v-if="preview_data.length == 0">
                                    <td :colspan="selected_fields.length">
                                        No results were found. Please modify
                                        your query and try again.
                                    </td>
                                </tr>
                            </table>
                        </div>
                        <!-- <div v-else>There are currently no preview results. Please run a query.</div> -->
                        <!-- <pre class="pre"
                        v-text="result"></pre>-->
                    </div>

                    <div class="card mb-3">
                        <div class="form-group">
                            <!-- <button v-if="selected_fields.length == 0 || !preview_data"
                        class="btn btn-primary btn-lg disabled"
                        disabled
                        @click.stop.prevent>Submit Query</button>
                <button v-else
                        @click.stop.prevent="sendQuery(true)"
                        class="btn btn-primary btn-lg"
                            type="submit">Submit Query</button>-->

                            <button
                                v-if="selected_fields.length == 0"
                                class="btn btn-primary btn-lg disabled"
                                disabled
                            >
                                Submit Query
                            </button>
                            <button
                                v-else
                                @click.stop.prevent="sendQuery(true)"
                                class="btn btn-primary btn-lg"
                                type="submit"
                            >
                                Submit Query
                            </button>

                            <button
                                v-if="allow_overload"
                                @click.stop.prevent="overloadDatabase(true)"
                                class="btn btn-danger btn-lg float-right"
                                type="button"
                            >
                                &#x1F47F; Overload CADRE &#x1F47F;
                            </button>
                        </div>
                    </div>
                </form>

                <template v-if="error_message">
                    <div
                        class="modal show"
                        style="display: block"
                        tabindex="-1"
                        role="dialog"
                    >
                        <div class="modal-dialog" role="document">
                            <div class="modal-content">
                                <div class="alert alert-danger mb-0">
                                    <div class="modal-header">
                                        <h5 class="modal-title">
                                            There was a problem with your query
                                        </h5>
                                        <button
                                            type="button"
                                            class="close"
                                            @click="error_message = ''"
                                            aria-label="Close"
                                        >
                                            <span aria-hidden="true"
                                            >&times;</span
                                            >
                                        </button>
                                    </div>
                                    <div class="modal-body">
                                        <p v-text="error_message"></p>
                                    </div>
                                    <div class="modal-footer">
                                        <button
                                            type="button"
                                            class="btn btn-secondary"
                                            @click="error_message = ''"
                                        >
                                            OK
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div
                        class="modal-backdrop fade show"
                        @click="error_message = ''"
                    ></div>
                </template>

                <template v-if="query_modal_open && !is_loading">
                    <div
                        class="modal show"
                        style="display: block"
                        tabindex="-1"
                        role="dialog"
                    >
                        <div class="modal-dialog" role="document">
                            <div class="modal-content">
                                <div class="alert alert-success mb-0">
                                    <div class="modal-header">
                                        <h5 class="modal-title">
                                            Query Is Running
                                        </h5>
                                        <button
                                            type="button"
                                            class="close"
                                            @click="query_modal_open = false"
                                            aria-label="Close"
                                        >
                                            <span aria-hidden="true"
                                            >&times;</span
                                            >
                                        </button>
                                    </div>
                                    <div class="modal-body">
                                        <div v-if="job_name">
                                            Job Name:
                                            <b v-text="job_name"></b>
                                        </div>
                                        <div>
                                            Job ID:
                                            <b
                                                v-text="query_results.job_id"
                                            ></b>
                                        </div>
                                        <button
                                            @click.prevent.stop="
                                                $router.push({
                                                    name: 'jobs-list-id',
                                                    params: {
                                                        job_id: query_results.job_id,
                                                    },
                                                })
                                            "
                                            class="btn btn-primary"
                                        >
                                            Check Job Statuses
                                        </button>
                                    </div>
                                    <div class="modal-footer">
                                        <button
                                            type="button"
                                            class="btn btn-secondary"
                                            @click="query_modal_open = false"
                                        >
                                            OK
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div
                        class="modal-backdrop fade show"
                        @click="query_modal_open = false"
                    ></div>
                </template>
            </div>
        </section>
    </div>
</template>

<style lang="scss">
.network-query-degrees.disabled {
    &,
    label,
    input {
        cursor: no-drop;
    }
}
</style>

