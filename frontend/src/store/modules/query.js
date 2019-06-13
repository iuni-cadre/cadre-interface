import Globals from "../../CadreGlobalsPlugin";
import axios from "axios";
import Vue from "vue";

import Datasets from "../../datasets";

export default {
    namespaced: true,
    state: {
        query_max_time: 30000,
        dataset: "wos",
    },
    getters: {
        validFields: function(state) {
            let fields = Datasets[state.dataset] && Datasets[state.dataset].fields;
            return fields;
        },
        selectedDataset: function(state){
            return state.dataset;
        }
    },
    mutations: {
        setSelectedDataset: function(state, dataset_id)
        {
            state.dataset = dataset_id;
        }
    },
    actions: {
        sendQuery: function({state}, payload) {
            let main_prom = new Promise(function(resolve, reject) {
                let async = payload.async || false;
                let query = payload.query;
                let dataset = payload.dataset;
                // let args_array = [];
                let fields = payload.output_fields;
                let field_string = fields.join(", ");
                let query_array = [];

                let i = 0;

                let query_string = "";
                for (let clause of query) {
                    query_array.push({
                        field: clause.argument,
                        value: clause.value,
                        operand: clause.operator || ""
                    });
                }

                query_string = JSON.stringify(query_array);

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
                    request = { q: query_array };
                }

                let canceled_timeout = setTimeout(
                    ()=>{
                        reject({code: 1000, message: "Query timed out"});
                    }, state.query_max_time
                );



                let query_prom = Vue.$cadre.axios({
                    url: Vue.$cadreConfig.data_api_url + url_piece,
                    method: "POST",
                    data: request
                });

                query_prom.then(
                    response => {
                        if(canceled_timeout > 0)
                        {
                            clearTimeout(canceled_timeout);
                            resolve(response.data);
                        }
                    },
                    error => {
                        if(canceled_timeout > 0)
                        {
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
