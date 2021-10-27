export default {
    output: [
        { field: "abstract", type: "single", label: "abstract" },
        { field: "articlenumber", type: "single", label: "articlenumber" },
        { field: "authors", type: "single", label: "authors" },
        {
            field: "citedreferencecount",
            type: "single",
            label: "citedreferencecount"
        },
        { field: "conferencedate", type: "single", label: "conferencedate" },
        { field: "conferencehost", type: "single", label: "conferencehost" },
        {
            field: "conferencelocation",
            type: "single",
            label: "conferencelocation"
        },
        {
            field: "conferencesponsor",
            type: "single",
            label: "conferencesponsor"
        },
        { field: "conferencetitle", type: "single", label: "conferencetitle" },
        { field: "documenttype", type: "single", label: "documenttype" },
        { field: "doi", type: "single", label: "doi" },
        { field: "earlyaccessdate", type: "single", label: "earlyaccessdate" },
        { field: "eissn", type: "single", label: "eissn" },
        { field: "emailaddress", type: "single", label: "emailaddress" },
        { field: "endpage", type: "single", label: "endpage" },
        { field: "full_address", type: "single", label: "full_address" },
        { field: "fundingorgs", type: "single", label: "fundingorgs" },
        { field: "fundingtext", type: "single", label: "fundingtext" },
        { field: "isbn", type: "single", label: "isbn" },
        { field: "isopenaccess", type: "single", label: "isopenaccess" },
        { field: "issn", type: "single", label: "issn" },
        { field: "issue", type: "single", label: "issue" },
        { field: "journalabbrev", type: "single", label: "journalabbrev" },
        { field: "journaliso", type: "single", label: "journaliso" },
        { field: "journaltitle", type: "single", label: "journaltitle" },
        { field: "keywordplus", type: "single", label: "keywordplus" },
        {
            field: "lc_standard_names",
            type: "single",
            label: "lc_standard_names"
        },
        { field: "numberofpages", type: "single", label: "numberofpages" },
        { field: "openaccesstype", type: "single", label: "openaccesstype" },
        { field: "orcid", type: "single", label: "orcid" },
        { field: "papertitle", type: "single", label: "papertitle" },
        { field: "partnumber", type: "single", label: "partnumber" },
        { field: "pmid", type: "single", label: "pmid" },
        { field: "publicationdate", type: "single", label: "publicationdate" },
        { field: "publicationyear", type: "single", label: "publicationyear" },
        { field: "publisher", type: "single", label: "publisher" },
        {
            field: "publisheraddress",
            type: "single",
            label: "publisheraddress"
        },
        { field: "publishercity", type: "single", label: "publishercity" },
        { field: "reprintaddress", type: "single", label: "reprintaddress" },
        { field: "rids", type: "single", label: "rids" },
        { field: "specialissue", type: "single", label: "specialissue" },
        { field: "standardnames", type: "single", label: "standardnames" },
        { field: "startpage", type: "single", label: "startpage" },
        { field: "supplement", type: "single", label: "supplement" },
        { field: "volume", type: "single", label: "volume" },
        { field: "wosid", type: "single", label: "wosid" },
        // {
        //     field: "affiliation_address",
        //     type: "single",
        //     label: "affiliation_address"
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
        doi: { label: "DOI", operators: ["OR"] },
        issn: { label: "ISSN", operators: ["OR"] },
        publicationyear: { label: "Year", operators: ["OR"] },
        lc_standard_names: { label: "Author", operators: ["AND", "OR"] },
        journaltitle: { label: "Journal Name", operators: ["OR"] },
        jounaliso: { label: "Journal ISO", operators: ["OR"] },
        conferencetitle: { label: "Conference Title", operators: ["OR"] },
        papertitle: { label: "Paper Title", operators: ["AND", "OR"] }
    },
    exclusive_input_fields: ["publicationyear"],
    default: [
        "wosid",
        "publicationyear",
        "authors",
        "journaltitle",
        "papertitle"
    ],
    janus_map: {
        main_vertex: "Paper",
        path_to_main: {
            Paper: []
        },
        vertex_types: ["Paper"],
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
            }
        ],
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
        input_field_map: {
            doi: { vertex: "Paper", field: "doi" },
            issn: { vertex: "Paper", field: "issn" },
            publicationyear: { vertex: "Paper", field: "publicationyear" },
            lc_standard_names: { vertex: "Paper", field: "lc_standard_names" },
            journaltitle: { vertex: "Paper", field: "journaltitle" },
            jounaliso: { vertex: "Paper", field: "jounaliso" },
            conferencetitle: { vertex: "Paper", field: "conferencetitle" },
            papertitle: { vertex: "Paper", field: "papertitle" }
        },
        output_field_map: {
            abstract: { vertexType: "Paper", field: "abstract" },
            articlenumber: { vertexType: "Paper", field: "articlenumber" },
            authors: { vertexType: "Paper", field: "authors" },
            citedreferencecount: {
                vertexType: "Paper",
                field: "citedreferencecount"
            },
            conferencedate: { vertexType: "Paper", field: "conferencedate" },
            conferencehost: { vertexType: "Paper", field: "conferencehost" },
            conferencelocation: {
                vertexType: "Paper",
                field: "conferencelocation"
            },
            conferencesponsor: {
                vertexType: "Paper",
                field: "conferencesponsor"
            },
            conferencetitle: { vertexType: "Paper", field: "conferencetitle" },
            documenttype: { vertexType: "Paper", field: "documenttype" },
            doi: { vertexType: "Paper", field: "doi" },
            earlyaccessdate: { vertexType: "Paper", field: "earlyaccessdate" },
            eissn: { vertexType: "Paper", field: "eissn" },
            emailaddress: { vertexType: "Paper", field: "emailaddress" },
            endpage: { vertexType: "Paper", field: "endpage" },
            full_address: { vertexType: "Paper", field: "full_address" },
            fundingorgs: { vertexType: "Paper", field: "fundingorgs" },
            fundingtext: { vertexType: "Paper", field: "fundingtext" },
            isbn: { vertexType: "Paper", field: "isbn" },
            isopenaccess: { vertexType: "Paper", field: "isopenaccess" },
            issn: { vertexType: "Paper", field: "issn" },
            issue: { vertexType: "Paper", field: "issue" },
            journalabbrev: { vertexType: "Paper", field: "journalabbrev" },
            journaliso: { vertexType: "Paper", field: "journaliso" },
            journaltitle: { vertexType: "Paper", field: "journaltitle" },
            keywordplus: { vertexType: "Paper", field: "keywordplus" },
            lc_standard_names: {
                vertexType: "Paper",
                field: "lc_standard_names"
            },
            numberofpages: { vertexType: "Paper", field: "numberofpages" },
            openaccesstype: { vertexType: "Paper", field: "openaccesstype" },
            orcid: { vertexType: "Paper", field: "orcid" },
            papertitle: { vertexType: "Paper", field: "papertitle" },
            partnumber: { vertexType: "Paper", field: "partnumber" },
            pmid: { vertexType: "Paper", field: "pmid" },
            publicationdate: { vertexType: "Paper", field: "publicationdate" },
            publicationyear: { vertexType: "Paper", field: "publicationyear" },
            publisher: { vertexType: "Paper", field: "publisher" },
            publisheraddress: {
                vertexType: "Paper",
                field: "publisheraddress"
            },
            publishercity: { vertexType: "Paper", field: "publishercity" },
            reprintaddress: { vertexType: "Paper", field: "reprintaddress" },
            rids: { vertexType: "Paper", field: "rids" },
            specialissue: { vertexType: "Paper", field: "specialissue" },
            standardnames: { vertexType: "Paper", field: "standardnames" },
            startpage: { vertexType: "Paper", field: "startpage" },
            supplement: { vertexType: "Paper", field: "supplement" },
            volume: { vertexType: "Paper", field: "volume" },
            wosid: { vertexType: "Paper", field: "wosid" }
        }
    }
};
