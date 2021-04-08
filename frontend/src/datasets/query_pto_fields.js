export default {
    output: [
        {
            field: "patent_type",
            type: "single",
            label: "Patent Type"
        },
        {
            field: "patent_number",
            type: "single",
            label: "Patent Number"
        },
        {
            field: "patent_date",
            type: "single",
            label: "Patent Date"
        },
        {
            field: "patent_year",
            type: "single",
            label: "Patent Year"
        },
        {
            field: "patent_abstract",
            type: "single",
            label: "Patent Abstract"
        },
        {
            field: "patent_title",
            type: "single",
            label: "Patent Title"
        },
        {
            field: "inventor_name_first",
            type: "single",
            label: "Inventor First Name"
        },
        {
            field: "inventor_name_last",
            type: "single",
            label: "Inventor Last Name"
        },
        {
            field: "inventor_location_city",
            type: "single",
            label: "Inventor City"
        },
        {
            field: "inventor_location_state",
            type: "single",
            label: "Inventor State"
        },
        {
            field: "inventor_location_country",
            type: "single",
            label: "Inventor Country"
        },
        {
            field: "inventor_location_state_fips",
            type: "single",
            label: "Inventor State FIPS"
        },
        {
            field: "inventor_location_country_fip",
            type: "single",
            label: "Inventor State"
        },
        {
            field: "inventor_location_longitude",
            type: "single",
            label: "Inventor Longitude"
        },
        {
            field: "inventor_location_latitude",
            type: "single",
            label: "Inventor Latitude"
        },

        
        {
            field: "assignee_location_city",
            type: "single",
            label: "Assignee City"
        },
        {
            field: "assignee_location_state",
            type: "single",
            label: "Assignee State"
        },
        {
            field: "assignee_location_country",
            type: "single",
            label: "Assignee Country"
        },
        {
            field: "assignee_location_state_fips",
            type: "single",
            label: "Assignee State FIPS"
        },
        {
            field: "assignee_location_country_fip",
            type: "single",
            label: "Assignee State"
        },
        {
            field: "assignee_location_longitude",
            type: "single",
            label: "Assignee Longitude"
        },
        {
            field: "assignee_location_latitude",
            type: "single",
            label: "Assignee Latitude"
        },
        
        {
            field: "assignee_organization",
            type: "single",
            label: "Assignee Organization"
        },
        {
            field: "assignee_type",
            type: "single",
            label: "Assignee Type"
        },
        {
            field: "assignee_name_first",
            type: "single",
            label: "Assignee First Name"
        },
        {
            field: "assignee_name_last",
            type: "single",
            label: "Assignee Last Name"
        },
        {
            field: "cpc_level",
            type: "single",
            label: "CPC Level"
        },
        {
            field: "cpc_category_label",
            type: "single",
            label: "CPC Category Label"
        },

        {
            field: "citations",
            type: "network",
            label: "Citation Network Graph"
        },
        {
            field: "references",
            type: "network",
            label: "Reference Network Graph"
        },
    ],
    input: {
        patent_type: "Patent Type",
        patent_number: "Patent Number",
        patent_date: { label: "Patent Date Range", type: "range" },
        patent_abstract: "Patent Abstract",
        patent_title: "Patent Title",
        inventor_name_first: "Inventor First Name",
        inventor_name_last: "Inventor Last Name",
        inventor_location_city: "Inventor City",
        inventor_location_country: "Inventor Country",
        inventor_location_state_fips: "Inventor State FIPS",
        inventor_location_country_fips: "Inventor Country FIPS",
        assignee_location_city: "Assignee City",
        assignee_location_country: "Assignee Country",
        assignee_location_state_fips: "Assignee State FIPS",
        assignee_location_country_fips: "Assignee Country FIPS",
        assignee_organization: "Assignee Organization",
        cpc_level: "CPC Level",
        cpc_category_label: "CPC Category Label"
    },
    exclusive_input_fields: [],
    default: [
        "patent_title",
        "patent_number",
        "patent_date",
        "inventor_name_first",
        "inventor_name_last"
    ],

    janus_map: {
        main_vertex: "Patent",
        path_to_main: {
            "Patent": [],
            "Inventor": ["InventorOf"],
            "InventorLocation": ["InventorOf", "InventorLocatedIn"],
            "Assignee": ["AssignedTo"],
            "AssigneeLocation": ["AssignedTo", "AssigneeLocatedIn"],
            "CPC": ["CpcCategoryOf"]
        },
        vertex_types:[
            "Patent",
            "Inventor",
            "InventorLocation",
            "Assignee",
            "AssigneeLocation",
            "CPC"
        ],
        edge_types: [
            {
                target: "Patent",
                source: "Patent",
                relation: "References"
            },
            {
                target: "Patent",
                source: "Patent",
                relation: "Citations"
            }
        ],
        input_field_map:
        {
            patent_type: {
                field: "type",
                vertex: "Patent"
            },
            patent_number: {
                field: "number",
                vertex: "Patent"
            },
            patent_date: {
                field: "date",
                vertex: "Patent"
            },
            patent_abstract: {
                field: "abstract",
                vertex: "Patent"
            },
            patent_title: {
                field: "title",
                vertex: "Patent"
            },
            inventor_name_first: {
                field: "name_first",
                vertex: "Inventor"
            },
            inventor_name_last: {
                field: "name_last",
                vertex: "Inventor"
            },
            inventor_location_city: {
                field: "city",
                vertex: "InventorLocation"
            },
            inventor_location_country: {
                field: "country",
                vertex: "InventorLocation"
            },
            inventor_location_state_fips: {
                field: "state_fips",
                vertex: "InventorLocation"
            },
            inventor_location_country_fips: {
                field: "country_fips",
                vertex: "InventorLocation"
            },
            assignee_location_city: {
                field: "city",
                vertex: "AssigneeLocation"
            },
            assignee_location_country: {
                field: "country",
                vertex: "AssigneeLocation"
            },
            assignee_location_state_fips: {
                field: "state_fips",
                vertex: "AssigneeLocation"
            },
            assignee_location_country_fips: {
                field: "country_fips",
                vertex: "AssigneeLocation"
            },
            assignee_organization: {
                field: "organization",
                vertex: "Assignee"
            },
            cpc_level: {
                field: "level",
                vertex: "CPC"
            },
            cpc_category_label: {
                field: "category_label",
                vertex: "CPC"
            }
        },
        network_map: {
            citations: {
                vertex: "Patent",
                relation: "Citations"
            },
            references: {
                vertex: "Patent",
                relation: "References"
            }
        },
        output_field_map: {
            patent_type: {
                field: "type",
                vertexType: "Patent"
            },
            patent_number: {
                field: "number",
                vertexType: "Patent"
            },
            patent_date: {
                field: "date",
                vertexType: "Patent"
            },
            patent_year: {
                field: "year",
                vertexType: "Patent"
            },
            patent_abstract: {
                field: "abstract",
                vertexType: "Patent"
            },
            patent_title: {
                field: "title",
                vertexType: "Patent"
            },
            inventor_name_first: {
                field: "name_first",
                vertexType: "Inventor"
            },
            inventor_name_last: {
                field: "name_last",
                vertexType: "Inventor"
            },
            inventor_location_city: {
                field: "city",
                vertexType: "InventorLocation"
            },
            inventor_location_state: {
                field: "state",
                vertexType: "InventorLocation"
            },
            inventor_location_country: {
                field: "country",
                vertexType: "InventorLocation"
            },
            inventor_location_state_fips: {
                field: "state_fips",
                vertexType: "InventorLocation"
            },
            inventor_location_country_fip: {
                field: "country_fip",
                vertexType: "InventorLocation"
            },
            inventor_location_longitude: {
                field: "longitude",
                vertexType: "InventorLocation"
            },
            inventor_location_latitude: {
                field: "latitude",
                vertexType: "InventorLocation"
            },
            assignee_location_city: {
                field: "city",
                vertexType: "AssigneeLocation"
            },
            assignee_location_state: {
                field: "state",
                vertexType: "AssigneeLocation"
            },
            assignee_location_country: {
                field: "country",
                vertexType: "AssigneeLocation"
            },
            assignee_location_state_fips: {
                field: "state_fips",
                vertexType: "AssigneeLocation"
            },
            assignee_location_country_fip: {
                field: "country_fip",
                vertexType: "AssigneeLocation"
            },
            assignee_location_longitude: {
                field: "longitude",
                vertexType: "AssigneeLocation"
            },
            assignee_location_latitude: {
                field: "latitude",
                vertexType: "AssigneeLocation"
            },
            assignee_organization: {
                field: "organization",
                vertexType: "Assignee"
            },
            assignee_type: {
                field: "type",
                vertexType: "Assignee"
            },
            assignee_name_first: {
                field: "name_first",
                vertexType: "Assignee"
            },
            assignee_name_last: {
                field: "name_last",
                vertexType: "Assignee"
            },
            cpc_level: {
                field: "level",
                vertexType: "CPC"
            },
            cpc_category_label: {
                field: "category_label",
                vertexType: "CPC"
            },
            // citations: {
            //     field: "citations",
            //     vertexType: ""
            // },
            // references: {
            //     field: "references",
            //     vertexType: ""
            // },
        }
    }
}



// export default {

//     janus_map: {

//         edge_types: [

//         network_map: {
//             citations: {
//                 vertex: "Paper",
//                 relation: "Citations"
//             },
//             references: {
//                 vertex: "Paper",
//                 relation: "References"
//             }
//         },
//         output_field_map: {
//             paper_id: {
//                 vertexType: "Paper",
//                 field: "paperId"
//             },
//             author_id: {
//                 vertexType: "Author",
//                 field: "authorId"
//             },
//             author_sequence_number: {
//                 vertexType: "Author",
//                 field: "rank"
//             },
//             authors_display_name: {
//                 vertexType: "Author",
//                 field: "displayName"
//             },
//             authors_last_known_affiliation_id: {
//                 vertexType: "Author",
//                 field: "lastKnownAffiliationId"
//             },
//             journal_id: {
//                 vertexType: "JournalFixed",
//                 field: "journalIdFixed"
//             },
//             // conference_series_id: {
//             //     vertexType: "ConferenceSeries",
//             //     field: "conferenceSeriesId"
//             // },
//             conference_instance_id: {
//                 vertexType: "ConferenceInstance",
//                 field: "conferenceInstanceId"
//             },
//             // paper_reference_id: { "vertexType": "", "field":""},
//             field_of_study_id: {
//                 vertexType: "FieldOfStudy",
//                 field: "fieldOfStudyId"
//             },
//             doi: {
//                 vertexType: "Paper",
//                 field: "doi"
//             },
//             doc_type: {
//                 vertexType: "Paper",
//                 field: "docType"
//             },
//             paper_title: {
//                 vertexType: "Paper",
//                 field: "paperTitle"
//             },
//             original_title: {
//                 vertexType: "Paper",
//                 field: "originalTitle"
//             },
//             book_title: {
//                 vertexType: "Paper",
//                 field: "bookTitle"
//             },
//             year: {
//                 vertexType: "Paper",
//                 field: "year"
//             },
//             date: {
//                 vertexType: "Paper",
//                 field: "date"
//             },
//             paper_publisher: {
//                 vertexType: "Paper",
//                 field: "publisher"
//             },
//             issue: {
//                 vertexType: "Paper",
//                 field: "issue"
//             },
//             // paper_abstract: {
//             //     vertexType: "",
//             //     field: ""
//             // },
//             paper_first_page: {
//                 vertexType: "Paper",
//                 field: "firstPage"
//             },
//             paper_last_page: {
//                 vertexType: "Paper",
//                 field: "lastPage"
//             },
//             paper_reference_count: {
//                 vertexType: "Paper",
//                 field: "referenceCount"
//             },
//             paper_citation_count: {
//                 vertexType: "Paper",
//                 field: "citationCount"
//             },
//             paper_estimated_citation: {
//                 vertexType: "Paper",
//                 field: "estimatedCitation"
//             },
//             // conference_display_name: {
//             //     vertexType: "ConferenceSeries",
//             //     field: "displayname"
//             // },
//             journal_display_name: {
//                 vertexType: "JournalFixed",
//                 field: "displayName"
//             },
//             journal_issn: {
//                 vertexType: "JournalFixed",
//                 field: "issn"
//             },
//             journal_publisher: {
//                 vertexType: "JournalFixed",
//                 field: "publisher"
//             },
//             affiliation_display_name: {
//                 vertexType: "Affiliation",
//                 field: "displayName"
//             }
//         }
//     }
// };

