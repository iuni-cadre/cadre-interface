import Globals from "../../CadreGlobalsPlugin";
import axios from "axios";
import Vue from "vue";

import Datasets from "../../datasets";

export default {
    namespaced: true,
    state: {
        query_max_time: 30000,
        dataset: "wos",
        query: []
    },
    getters: {
        outputFields: function(state) {
            let fields = Datasets[state.dataset] && Datasets[state.dataset].fields.output;
            return fields;
        },
        inputFields: function(state) {
            let fields = Datasets[state.dataset] && Datasets[state.dataset].fields.input;
            return fields;
        },
        selectedDataset: function(state) {
            return state.dataset;
        },
        query: function(state) {
            return state.query;
        }
    },
    mutations: {
        setSelectedDataset: function(state, dataset_id) {
            state.dataset = dataset_id;
            //remove the operator from the last clause so that it doesn't confuse the data api
        },
        setQuery: function(state, query_clauses) {
            Vue.set(state, "query", query_clauses);
            state.query[state.query.length - 1].operator = "";
        },
        emptyQuery: function(state) {
            Vue.set(state, "query", []);
        }
    },
    actions: {
        sendQuery: function({ state }, payload) {
            let main_prom = new Promise(function(resolve, reject) {
                let query = state.query;
                let dataset = state.dataset;

                let async = payload.async || false;
                let fields = payload.output_fields;
                let field_string = fields.join(", ");

                let i = 0;

                let query_string = "";

                query_string = JSON.stringify(query);

                let request = {
                    query: `query {
    ${dataset}(q: "${query_string.replace(/"/g, '\\"')}")
    { ${field_string} }
}`
                };

                // console.debug(request);

                let url_piece = `/data/${dataset}-graphql/publication`;
                if (async) {
                    url_piece = `/data/${dataset}/publications-async`;
                    let query_array = [];

                    for (let clause of query) {
                        query_array.push({
                            field: clause.field,
                            value: clause.value,
                            operand: clause.operator || ""
                        });
                    }

                    request = {
                        q: query_array,
                        output_fields: fields,
                        data_set: dataset,
                        query_type: null
                    };
                }

                let canceled_timeout = setTimeout(() => {
                    reject({ code: 1000, message: "Query timed out" });
                }, state.query_max_time);

                let query_prom = Vue.$cadre.axios({
                    url: Vue.$cadreConfig.data_api_url + url_piece,
                    method: "POST",
                    data: request
                });

                query_prom.then(
                    response => {
                        if (canceled_timeout > 0) {
                            clearTimeout(canceled_timeout);
                            resolve(response.data);
                        }
                    },
                    error => {
                        if (canceled_timeout > 0) {
                            clearTimeout(canceled_timeout);
                            console.error(error);
                            reject(error);
                        }
                    }
                );
            });
            return main_prom;
        }
    }
};
