import Globals from "../../CadreGlobalsPlugin";
import axios from "axios";
import Vue from "vue";

import Datasets from "../../datasets";

export default {
    namespaced: true,
    state: {
        query_max_time: 30000,
        dataset: "",
        query: []
    },
    getters: {
        outputFields: function(state) {
            let fields = Datasets[state.dataset] && Datasets[state.dataset].fields.output || [];
            return fields;
        },
        inputFields: function(state) {
            let fields = Datasets[state.dataset] && Datasets[state.dataset].fields.input || [];
            return fields;
        },
        defaultFields: function(state) {
            let fields = Datasets[state.dataset] && Datasets[state.dataset].fields.default || [];
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
                let async = payload.async || false;


                let endpoint = '';

                if(async)
                {

                    endpoint = '/publications-async'; //preview query
                }
                else
                {
                    endpoint = '/publications-sync'; //full query
                }



                let query = state.query;
                let dataset = state.dataset;
                let fields = payload.output_fields;

                let request = {};
                let query_array = [];

                for (let clause of query) {
                    query_array.push({
                        field: clause.field,
                        value: clause.value,
                        operation: clause.operator || ""
                    });
                }

                request = {
                    job_name: payload.job_name,
                    filters: query_array,
                    output: fields,
                    dataset: dataset
                };

                if(Datasets[dataset].database_type == "janus")
                {
                    request = convertQueryDataToJanus(request);
                }

                let canceled_timeout = setTimeout(() => {
                    reject({ code: 1000, message: "Query timed out" });
                }, state.query_max_time);

                let query_prom = Vue.$cadre.axios({
                    url: Vue.$cadreConfig.data_api_url + endpoint,
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

export function convertQueryDataToJanus({job_name = "", filters = [], output = [], dataset = ""})
{
    let result = {
        job_name: job_name,
        graph: [],
        csv_output: [],
        dataset: dataset
    };
    //get the maps so we can map the old filters to the new
    const janus_map = Datasets[dataset].fields.janus_map;
    const input_map = janus_map.input_field_map;
    const network_map = janus_map.network_map;
    const output_map = janus_map.output_field_map;

    let graph = [];
    let types_with_filters = {}
    let csv_output = [];

    //pull out all the filters and group by vertex
    for(let {field, value, operation} of filters)
    {
        let {vertex, field: new_field} = input_map[field];
        if(!types_with_filters[vertex])
        {
            types_with_filters[vertex] = [];
        }
        types_with_filters[vertex].push({
            "field": new_field,
            "filterType": "is",
            "value": value,
            "operator": operation
        });
    }

    //build the actual graph
    for(let vertex in types_with_filters)
    {
        let node = {"vertexType": vertex, "filters": []}
        const filters = types_with_filters[vertex];
        for(let filter of filters)
        {
            node.filters.push(filter);
        }
        graph.push(node);
    }

    for(let {field, type, degree = 0} of output)
    {
        //if a network output field was checked, match it to proper
        //  vertex type and push an empty vertex on the graph
        if(type == "network")
        {
            let {vertex} = network_map[field];
            graph.push({
                vertexType: vertex,
                filters: []
            });
        }
        else if(type == "single")
        {
            csv_output.push(output_map[field]);
        }
    }
    
    result.csv_output = csv_output;
    result.graph = graph;
    return result;
}
// export convertQueryDataToJanus as convertQueryDataToJanus;
