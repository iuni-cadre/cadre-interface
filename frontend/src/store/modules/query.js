import Globals from "../../CadreGlobalsPlugin";
import axios from "axios";
import Vue from "vue";

export default {
    namespaced: true,
    state: {
        valid_fields: [
            "FileNumber",
            "CollID",
            "PubYear",
            "Season",
            "PubMonth",
            "PubDay",
            "CoverDate",
            "EDate",
            "Vol",
            "Issue",
            "VolIss",
            "Supplement",
            "SpecialIssue",
            "PartNo",
            "PubType",
            "Medium",
            "Model",
            "Indicator",
            "Inpi",
            "IsArchive",
            "City",
            "Country",
            "HasAbstract",
            "SortDate",
            "TitleCount",
            "NameCount",
            "DocTypeCount",
            "ConferenceCount",
            "LanguageCount",
            "NormalizedLanguageCount",
            "NormalizedDocTypeCount",
            "DescriptiveRefCount",
            "ReferenceCount",
            "AddressCount",
            "HeadingsCount",
            "SubHeadingsCount",
            "SubjectsCount",
            "FundAck",
            "GrantsCount",
            "GrantsComplete",
            "KeywordCount",
            "AbstractCount",
            "ItemCollId",
            "ItemIds",
            "ItemIdsAvail",
            "BibId",
            "BibPageCount",
            "BibPageCountType",
            "ReviewedLanguageCount",
            "ReviewedAuthorCount",
            "ReviewedYear",
            "KeywordsPlusCount",
            "BookChapters",
            "BookPages",
            "BookNotesCount",
            "ChapterListCount",
            "ContributorCount"
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
                for (let clause of query) {
                    // args_array.push(`${arg.argument}:${arg.value}`);
                    if (i > 0) {
                        clause.operator = clause.operator || "AND";
                    }

                    let clause_string = `
query QueryPart${i}
{
    ${dataset}(${clause.argument}:"${clause.value}", operator: "${clause.operator || ''}")
    {
        ${field_string}
    }
}
`;
                    query_array.push(clause_string);
                    i++;
                }
                // let arg_string = args_array.join(",");

                //TODO: validate options before even constructing the request

                let request = query_array.join("\n");

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
