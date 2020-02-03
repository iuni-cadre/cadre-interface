export default {
    output: [
        // wosId: "wosId",
        // year: "year",
        // number: "number",
        // issue: "issue",
        // pages: "pages",
        // authorsFullName: "authorsFullName",
        // authorsIdOrcid: "authorsIdOrcid",
        // authorsIdDais: "authorsIdDais",
        // authorsIdResearch: "authorsIdResearch",
        // authorsPrefix: "authorsPrefix",
        // authorsFirstName: "authorsFirstName",
        // authorsMiddleName: "authorsMiddleName =  ",
        // authorsLastName: "authorsLastName",
        // authorsSuffix: "authorsSuffix",
        // authorsInitials: "authorsInitials",
        // authorsDisplayNames: "authorsDisplayNames",
        // authorsWosName: "authorsWosName",
        // authorsIdLang: "authorsIdLang",
        // authorsEmails: "authorsEmails",
        // references: "references",
        // issn: "issn",
        // doi: "doi",
        // title: "title",
        // journalsName: "journalsName",
        // journalsAbbrev: "journalsAbbrev",
        // journalsIso: "journalsIso",
        // abstractParagraphs: "abstractParagraphs"

        {
            field: 'wos_id',
            label: "wos_id",
            type: 'single'
        },
        {
            field: 'year',
            label: "year",
            type: 'single'
        },
        {
            field: 'number',
            label: "number",
            type: 'single'
        },
        {
            field: 'issue',
            label: "issue",
            type: 'single'
        },
        {
            field: 'pages',
            label: "pages",
            type: 'single'
        },
        {
            field: 'authors_full_name',
            label: "authors_full_name",
            type: 'single'
        },
        {
            field: 'authors_id_orcid',
            label: "authors_id_orcid",
            type: 'single'
        },
        {
            field: 'authors_id_dais',
            label: "authors_id_dais",
            type: 'single'
        },
        {
            field: 'authors_id_research',
            label: "authors_id_research",
            type: 'single'
        },
        {
            field: 'authors_prefix',
            label: "authors_prefix",
            type: 'single'
        },
        {
            field: 'authors_first_name',
            label: "authors_first_name",
            type: 'single'
        },
        {
            field: 'authors_middle_name',
            label: "authors_middle_name",
            type: 'single'
        },
        {
            field: 'authors_last_name',
            label: "authors_last_name",
            type: 'single'
        },
        {
            field: 'authors_suffix',
            label: "authors_suffix",
            type: 'single'
        },
        {
            field: 'authors_initials',
            label: "authors_initials",
            type: 'single'
        },
        {
            field: 'authors_display_name',
            label: "authors_display_name",
            type: 'single'
        },
        {
            field: 'authors_wos_name',
            label: "authors_wos_name",
            type: 'single'
        },
        {
            field: 'authors_id_lang',
            label: "authors_id_lang",
            type: 'single'
        },
        {
            field: 'authors_email',
            label: "authors_email",
            type: 'single'
        },
        {
            field: 'references',
            label: "Citation Network",
            type: 'network'
        },
        // {
        //     field: 'references',
        //     label: "references",
        //     type: 'single'
        // },
        {
            field: 'issn',
            label: "issn",
            type: 'single'
        },
        {
            field: 'doi',
            label: "doi",
            type: 'single'
        },
        {
            field: 'title',
            label: "title",
            type: 'single'
        },
        {
            field: 'journal_name',
            label: "journal_name",
            type: 'single'
        },
        {
            field: 'journal_abbrev',
            label: "journal_abbrev",
            type: 'single'
        },
        {
            field: 'journal_iso',
            label: "journal_iso",
            type: 'single'
        },
        {
            field: 'abstract_paragraphs',
            label: "abstract_paragraphs",
            type: 'single'
        },
        {
            field: 'title_tsv',
            label: "title_tsv",
            type: 'single'
        },
        {
            field: 'abstract_tsv',
            label: "abstract_tsv",
            type: 'single'
        },
        {
            field: 'journal_tsv',
            label: "journal_tsv",
            type: 'single'
        },
        {
            field: 'reference_count',
            label: "reference_count",
            type: 'single'
        },
    ],
    input: {
        year: "Year",
        authors_full_name: "Author",
        journal_name: "Journal Name",
        title: "Title"
    },
    default: [
        "wos_id",
        "year",
        "authors_full_name",
        // "references"
    ]
};
