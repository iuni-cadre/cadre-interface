import Globals from "../../CadreGlobalsPlugin";
import axios from "axios";
import Vue from "vue";

export default {
    namespaced: true,
    state: {
        valid_fields: [
            "wos_id",
            "year",
            "number",
            "issue",
            "pages",
            "authors_full_name",
            "authors_id_orcid",
            "authors_id_dais",
            "authors_id_research",
            "authors_prefix",
            "authors_first_name",
            "authors_middle_name",
            "authors_last_name",
            "authors_suffix",
            "authors_initials",
            "authors_display_name",
            "authors_wos_name",
            "authors_id_lang",
            "authors_email",
            "references",
            "issn",
            "doi",
            "title",
            "journal_name",
            "journal_abbrev",
            "journal_iso",
            "abstract_paragraph",
        ]
    },
    getters: {
        validFields: function(state) {
            return state.valid_fields;
        }
    },
    mutations: {},
    actions: {
        sendQuery: function(state, payload) {
            let main_prom = new Promise(function(resolve, reject) {
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
                // $query;

                // for (let clause of query) {
                //                     // args_array.push(`${arg.argument}:${arg.value}`);
                //                     if (i > 0) {
                //                         clause.operator = clause.operator || "AND";
                //                     }

                //                     let clause_string = `
                // query QueryPart${i}
                // {
                //     ${dataset}(${clause.argument}:"${clause.value}", operator: "${clause.operator || ''}")
                //     {
                //         ${field_string}
                //     }
                // }
                // `;
                //                     query_array.push(clause_string);
                //                     i++;
                //                 }

                // let arg_string = args_array.join(",");

                //TODO: validate options before even constructing the request

                // let request = query_array.join("\n");

                let request = `query QueryA
{
    ${dataset}(q: '${query_string}')
    {
        ${field_string}
    }
}`;

                console.debug(request);

                let query_prom = Vue.$cadre.axios({
                    url: Vue.$cadreConfig.api_host + `/data/${dataset}-graphql/publication`,
                    method: "POST",
                    data: {
                        query: request
                    }
                });

                query_prom.then(
                    response => {
                        resolve(response.data);
                    },
                    error => {
                        console.error(error);
                        reject(error);
                    }
                );
            });
            return main_prom;
        }
    }
};
