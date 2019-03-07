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
        validFields: function(state){
            return state.valid_fields;
        }
    },
    mutations: {},
    actions: {
        sendQuery: function(state, payload) {
            let main_prom = new Promise(function(resolve, reject) {

                let query = payload.query;
                let args_array = [];
                for (let arg of query) {
                    args_array.push(`${arg.argument}:${arg.value}`);
                }
                let arg_string = args_array.join(",");
                let dataset = payload.dataset;

                let fields = payload.output_fields;
                let field_string = fields.join(", ");

                //TODO: validate options before even constructing the request

                let request = `
                    {
                        ${dataset}(${arg_string})
                        {
                            ${field_string}
                        }
                    }
                `;

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
