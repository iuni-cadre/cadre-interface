export default {
    output: [
        {
            field: "paper_id",
            type: "single",
            label: "paper_id"
        },
        {
            field: "author_id",
            type: "single",
            label: "author_id"
        },
        {
            field: "author_sequence_number",
            type: "single",
            label: "author_sequence_number"
        },
        {
            field: "authors_display_name",
            type: "single",
            label: "authors_display_name"
        },
        {
            field: "authors_last_known_affiliation_id",
            type: "single",
            label: "authors_last_known_affiliation_id"
        },
        {
            field: "journal_id",
            type: "single",
            label: "journal_id"
        },
        // {
        //     field: "conference_series_id",
        //     type: "single",
        //     label: "conference_series_id"
        // },
        {
            field: "conference_instance_id",
            type: "single",
            label: "conference_instance_id"
        },
        // {
        //     field: "paper_reference_id",
        //     type: "single",
        //     label: "paper_reference_id"
        // },
        {
            field: "field_of_study_id",
            type: "single",
            label: "field_of_study_id"
        },
        {
            field: "doi",
            type: "single",
            label: "doi"
        },
        {
            field: "doc_type",
            type: "single",
            label: "doc_type"
        },
        {
            field: "paper_title",
            type: "single",
            label: "paper_title"
        },
        {
            field: "original_title",
            type: "single",
            label: "original_title"
        },
        {
            field: "book_title",
            type: "single",
            label: "book_title"
        },
        {
            field: "year",
            type: "single",
            label: "year"
        },
        {
            field: "date",
            type: "single",
            label: "date"
        },
        {
            field: "paper_publisher",
            type: "single",
            label: "paper_publisher"
        },
        {
            field: "issue",
            type: "single",
            label: "issue"
        },
        // {
        //     field: "paper_abstract",
        //     type: "single",
        //     label: "paper_abstract"
        // },
        {
            field: "paper_first_page",
            type: "single",
            label: "paper_first_page"
        },
        {
            field: "paper_last_page",
            type: "single",
            label: "paper_last_page"
        },
        {
            field: "paper_reference_count",
            type: "single",
            label: "paper_reference_count"
        },
        {
            field: "paper_citation_count",
            type: "single",
            label: "paper_citation_count"
        },
        {
            field: "paper_estimated_citation",
            type: "single",
            label: "paper_estimated_citation"
        },
        // {
        //     field: "conference_display_name",
        //     type: "single",
        //     label: "conference_display_name"
        // },
        {
            field: "journal_display_name",
            type: "single",
            label: "journal_display_name"
        },
        {
            field: "journal_issn",
            type: "single",
            label: "journal_issn"
        },
        {
            field: "journal_publisher",
            type: "single",
            label: "journal_publisher"
        },
        {
            field: "affiliation_display_name",
            type: "single",
            label: "affiliation_display_name"
        },
        // {
        //     field: "paper_title_tsv",
        //     type: "single",
        //     label: "paper_title_tsv"
        // },
        {
            field: "citations",
            type: "network",
            label: "Citation Network Graph"
        },
        {
            field: "references",
            type: "network",
            label: "References Network Graph"
        }
    ],
    input: {
        // year: "Year",
        // authors_full_name: "Author",
        // journals_name: "Journal Name",
        // title: "Title"
        // year: {"label": "Year", "operators": ["OR"]},
        // doi: {"label": "DOI", "operators": ["OR"]},
        // journal_display_name: {"label": "Journal Name", "operators": [ "OR"]},
        // conference_display_name: {"label": "Conference Name", "operators": [ "OR"]},
        // authors_display_name: {"label": "Author Names", "operators": ["OR"]},
        // paper_title: {"label": "Paper Title", "operators": ["AND", "OR"]},

        year: { label: "Paper Year", operators: ["OR"] },
        doi: { label: "Paper DOI", operators: ["OR"] },
        paper_title: { label: "Paper Title", operators: ["OR", "AND"] },
        paper_id: { label: "Paper ID", operators: ["OR"] },
        paper_date: {
            label: "Paper Date Range",
            type: "range",
            operators: ["OR"]
        },

        journal_display_name: { label: "Journal Name", operators: ["OR"] },
        journal_id: { label: "Journal ID", operators: ["OR"] },
        journal_issn: { label: "Journal ISSN", operators: ["OR"] },

        affilation_id: { label: "Affiliate ID", operators: ["OR"] },
        affiliation_name: { label: "Affiliate Name", operators: ["OR"] },

        authors_display_name: { label: "Author Name", operators: ["OR"] },
        author_id: { label: "Author ID", operators: ["OR"] },

        field_of_study_display_name: {
            label: "Field of Study Name",
            operators: ["OR"]
        },
        field_of_study_id: { label: "Field Of Study ID", operators: ["OR"] }

        // paper_abstract: "Paper Abstract"
    },
    exclusive_input_fields: ["year"],
    default: [
        "paper_id",
        "year",
        "original_title",
        "authors_display_name",
        "journal_display_name"
        // "author_id",
        // "citations"
    ],
    janus_map: {
        main_vertex: "Paper",
        path_to_main: {
            Paper: [],
            Journal: ["PublishedIn"],
            Author: ["AuthorOf"],
            ConferenceInstance: ["PresentedAt"],
            // "ConferenceSeries": ["InstanceOf", "PresentedAt"],
            FieldOfStudy: ["BelongsTo"],
            Affiliation: ["AuthorOf", "AffiliatedWith"]
        },
        vertex_types: [
            "Paper",
            "Journal",
            "Author",
            "ConferenceInstance",
            // "ConferenceSeries",
            "FieldOfStudy",
            "Affiliation"
        ],
        edge_types: [
            {
                target: "Paper",
                source: "Paper",
                relation: "References"
            },
            {
                target: "Paper",
                source: "Paper",
                relation: "Citations"
            },
            {
                target: "Journal",
                source: "Paper",
                relation: "PublishedIn"
            },
            {
                target: "Paper",
                source: "Author",
                relation: "AuthorOf"
            },
            {
                target: "Affiliation",
                source: "Author",
                relation: "AffiliatedWith"
            },
            {
                target: "ConferenceInstance",
                source: "Paper",
                relation: "PresentedAt"
            },
            // {
            //     target: "ConferenceInstance",
            //     source: "ConferenceSeries",
            //     relation: "InstanceOf"
            // },
            {
                target: "FieldOfStudy",
                source: "Paper",
                relation: "BelongsTo"
            }
        ],
        input_field_map: {
            // year: {
            //     vertex: "Paper",
            //     field: "year"
            // },
            // doi: {
            //     vertex: "Paper",
            //     field: "doi"
            // },
            // paper_title: {
            //     vertex: "Paper",
            //     field: "paperTitle"
            // },
            // paper_id: {
            //     vertex: "Paper",
            //     field: "paperId"
            // },
            // paper_date: {
            //     vertex: "Paper",
            //     field: "date"
            // },

            // journal_display_name: {
            //     vertex: "Journal",
            //     field: "normalizedName"
            // },
            // journal_id: {
            //     vertex: "Journal",
            //     field: "journalId"
            // },
            // journal_issn: {
            //     vertex: "Journal",
            //     field: "issn"
            // },

            // // conference_display_name: {
            // //     vertex: "ConferenceInstance",
            // //     field: "name"
            // // },
            // affilation_id: {
            //     vertex: "Affiliation",
            //     field: "affiliationId"
            // },
            // affiliation_name: {
            //     vertex: "Affiliation",
            //     field: "normalizedName"
            // },

            // authors_display_name: {
            //     vertex: "Author",
            //     field: "normalizedName"
            // },
            // author_id: {
            //     vertex: "Author",
            //     field: "authorId"
            // },

            // field_of_study_display_name: {
            //     vertex: "FieldOfStudy",
            //     field: "normalizedName"
            // },
            // field_of_study_id: {
            //     vertex: "FieldOfStudy",
            //     field: "fieldOfStudyId"
            // },

            year: { vertex: "Paper", field: "year" },
            doi: { vertex: "Paper", field: "doi" },
            paper_title: { vertex: "Paper", field: "paperTitle" },
            paper_id: { vertex: "Paper", field: "paperId" },
            paper_date: { vertex: "Paper", field: "date" },

            journal_display_name: { vertex: "Journal", field: "normalizedName"},
            journal_id: { vertex: "Journal", field: "journalId" },
            journal_issn: { vertex: "Journal", field: "issn" },
            
            affilation_id: { vertex: "Affiliation", field: "affiliationId"},
            affiliation_name: { vertex: "Affiliation", field: "normalizedName" },
            
            authors_display_name: { vertex: "Author", field: "normalizedName"},
            author_id: { vertex: "Author", field: "authorId" },
            
            field_of_study_display_name: { vertex: "FieldOfStudy", field: "normalizedName"},
            field_of_study_id: { vertex: "FieldOfStudy", field: "fieldOfStudyId" },

            // paper_abstract: {
            //     vertex: "Paper",
            //     field: "abstract"
            // }
        },
        network_map: {
            citations: {
                vertex: "Paper",
                relation: "Citations"
            },
            references: {
                vertex: "Paper",
                relation: "References"
            }
        },
        output_field_map: {
            paper_id: {
                vertexType: "Paper",
                field: "paperId"
            },
            author_id: {
                vertexType: "Author",
                field: "authorId"
            },
            author_sequence_number: {
                vertexType: "Author",
                field: "rank"
            },
            authors_display_name: {
                vertexType: "Author",
                field: "normalizedName"
            },
            authors_last_known_affiliation_id: {
                vertexType: "Author",
                field: "lastKnownAffiliationId"
            },
            journal_id: {
                vertexType: "Journal",
                field: "journalId"
            },
            // conference_series_id: {
            //     vertexType: "ConferenceSeries",
            //     field: "conferenceSeriesId"
            // },
            conference_instance_id: {
                vertexType: "ConferenceInstance",
                field: "conferenceInstanceId"
            },
            // paper_reference_id: { "vertexType": "", "field":""},
            field_of_study_id: {
                vertexType: "FieldOfStudy",
                field: "fieldOfStudyId"
            },
            doi: {
                vertexType: "Paper",
                field: "doi"
            },
            doc_type: {
                vertexType: "Paper",
                field: "docType"
            },
            paper_title: {
                vertexType: "Paper",
                field: "paperTitle"
            },
            original_title: {
                vertexType: "Paper",
                field: "originalTitle"
            },
            book_title: {
                vertexType: "Paper",
                field: "bookTitle"
            },
            year: {
                vertexType: "Paper",
                field: "year"
            },
            date: {
                vertexType: "Paper",
                field: "date"
            },
            paper_publisher: {
                vertexType: "Paper",
                field: "publisher"
            },
            issue: {
                vertexType: "Paper",
                field: "issue"
            },
            // paper_abstract: {
            //     vertexType: "",
            //     field: ""
            // },
            paper_first_page: {
                vertexType: "Paper",
                field: "firstPage"
            },
            paper_last_page: {
                vertexType: "Paper",
                field: "lastPage"
            },
            paper_reference_count: {
                vertexType: "Paper",
                field: "referenceCount"
            },
            paper_citation_count: {
                vertexType: "Paper",
                field: "citationCount"
            },
            paper_estimated_citation: {
                vertexType: "Paper",
                field: "estimatedCitation"
            },
            // conference_display_name: {
            //     vertexType: "ConferenceSeries",
            //     field: "displayname"
            // },
            journal_display_name: {
                vertexType: "Journal",
                field: "normalizedName"
            },
            journal_issn: {
                vertexType: "Journal",
                field: "issn"
            },
            journal_publisher: {
                vertexType: "Journal",
                field: "publisher"
            },
            affiliation_display_name: {
                vertexType: "Affiliation",
                field: "normalizedName"
            }
        }
    }
};

// Column          |            Type             | Collation | Nullable | Default
// --------------------------+-----------------------------+-----------+----------+---------
//  paper_id                 | character varying           |           |          |
//  author_id                | text                        |           |          |
//  author_sequence_number   | text                        |           |          |
//  journal_id               | text                        |           |          |
//  conference_series_id     | text                        |           |          |
//  conference_instance_id   | text                        |           |          |
//  paper_reference_id       | text                        |           |          |
//  field_of_study_id        | text                        |           |          |
//  doi                      | text                        |           |          |
//  doc_type                 | text                        |           |          |
//  paper_title              | text                        |           |          |
//  original_title           | text                        |           |          |
//  book_title               | text                        |           |          |
//  year                     | text                        |           |          |
//  date                     | timestamp without time zone |           |          |
//  paper_publisher          | text                        |           |          |
//  issue                    | text                        |           |          |
//  paper_abstract           | text                        |           |          |
//  paper_first_page         | text                        |           |          |
//  paper_last_page          | text                        |           |          |
//  paper_reference_count    | bigint                      |           |          |
//  paper_citation_count     | bigint                      |           |          |
//  paper_estimated_citation | bigint                      |           |          |
//  conference_display_name  | text                        |           |          |
//  journal_display_name     | text                        |           |          |
//  journal_issn             | text                        |           |          |
//  journal_publisher        | text                        |           |          |
//  paper_title_tsv          | tsvector                    |           |          |
// Indexes:
//     "conference_display_name_idx" gin (conference_display_name gin_trgm_ops)
//     "journal_display_name_idx" gin (journal_display_name gin_trgm_ops)
//     "mag_doi_idx" btree (doi)
//     "paper_title_tsv_idx" gin (paper_title_tsv)
//     "year_idx" btree (year)
