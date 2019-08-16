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
        {
            field: "conference_series_id",
            type: "single",
            label: "conference_series_id"
        },
        {
            field: "conference_instance_id",
            type: "single",
            label: "conference_instance_id"
        },
        {
            field: "paper_reference_id",
            type: "single",
            label: "paper_reference_id"
        },
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
        {
            field: "paper_abstract",
            type: "single",
            label: "paper_abstract"
        },
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
        {
            field: "conference_display_name",
            type: "single",
            label: "conference_display_name"
        },
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
            field: "paper_title_tsv",
            type: "single",
            label: "paper_title_tsv"
        },
        {
            field: "citations",
            type: "network",
            label: "Citation Network"
        },

    ],
    input: {
        // year: "Year",
        // authors_full_name: "Author",
        // journals_name: "Journal Name",
        // title: "Title"
        year: "Year",
        doi: "DOI",
        journal_display_name: "Journal Name",
        conference_display_name: "Conference Name",
        authors_display_name: "Author Names",
        paper_title: "Paper Title",
        paper_abstract: "Paper Abstract",
    },
    default: [
        "paper_id",
        "year",
        "original_title",
        "authors_display_name",
        // "author_id",
        // "citations"
    ]
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
