export default {
    "output": [{
        "field": "ISBN",
        "type": "single",
        "label": "ISBN"
    }, {
        "field": "DOI",
        "type": "single",
        "label": "DOI"
    }, {
        "field": "pubmedId",
        "type": "single",
        "label": "pubmedId"
    }, {
        "field": "bookEditors",
        "type": "single",
        "label": "bookEditors"
    }, {
        "field": "groupAuthors",
        "type": "single",
        "label": "groupAuthors"
    }, {
        "field": "bookSeriesTitle",
        "type": "single",
        "label": "bookSeriesTitle"
    }, {
        "field": "bookSeriesSubtitle",
        "type": "single",
        "label": "bookSeriesSubtitle"
    }, {
        "field": "conferenceDate",
        "type": "single",
        "label": "conferenceDate"
    }, {
        "field": "conferenceLocation",
        "type": "single",
        "label": "conferenceLocation"
    }, {
        "field": "conferenceSponsor",
        "type": "single",
        "label": "conferenceSponsor"
    }, {
        "field": "conferenceHost",
        "type": "single",
        "label": "conferenceHost"
    }, {
        "field": "keywordsPlus",
        "type": "single",
        "label": "keywordsPlus"
    }, {
        "field": "reprintAddresses",
        "type": "single",
        "label": "reprintAddresses"
    }, {
        "field": "emailAddresses",
        "type": "single",
        "label": "emailAddresses"
    }, {
        "field": "RIDs",
        "type": "single",
        "label": "RIDs"
    }, {
        "field": "ORCIDs",
        "type": "single",
        "label": "ORCIDs"
    }, {
        "field": "fundingOrgs",
        "type": "single",
        "label": "fundingOrgs"
    }, {
        "field": "publisherCity",
        "type": "single",
        "label": "publisherCity"
    }, {
        "field": "publisherAddress",
        "type": "single",
        "label": "publisherAddress"
    }, {
        "field": "journalAbbreviation",
        "type": "single",
        "label": "journalAbbreviation"
    }, {
        "field": "journalISOAbbreviation",
        "type": "single",
        "label": "journalISOAbbreviation"
    }, {
        "field": "publicationDate",
        "type": "single",
        "label": "publicationDate"
    }, {
        "field": "volume",
        "type": "single",
        "label": "volume"
    }, {
        "field": "issue",
        "type": "single",
        "label": "issue"
    }, {
        "field": "partNumber",
        "type": "single",
        "label": "partNumber"
    }, {
        "field": "supplement",
        "type": "single",
        "label": "supplement"
    }, {
        "field": "specialIssue",
        "type": "single",
        "label": "specialIssue"
    }, {
        "field": "startPage",
        "type": "single",
        "label": "startPage"
    }, {
        "field": "endPage",
        "type": "single",
        "label": "endPage"
    }, {
        "field": "articleNumber",
        "type": "single",
        "label": "articleNumber"
    }, {
        "field": "bookDOI",
        "type": "single",
        "label": "bookDOI"
    }, {
        "field": "earlyAccessDate",
        "type": "single",
        "label": "earlyAccessDate"
    }, {
        "field": "numberOfPages",
        "type": "single",
        "label": "numberOfPages"
    }, {
        "field": "wosId",
        "type": "single",
        "label": "wosId"
    }, {
        "field": "publicationYear",
        "type": "single",
        "label": "publicationYear"
    }, {
        "field": "standardNames",
        "type": "single",
        "label": "standardNames"
    }, {
        "field": "authorFullNames",
        "type": "single",
        "label": "authorFullNames"
    }, {
        "field": "articleTitle",
        "type": "single",
        "label": "articleTitle"
    }, {
        "field": "sourceTitle",
        "type": "single",
        "label": "sourceTitle"
    }, {
        "field": "documentType",
        "type": "single",
        "label": "documentType"
    }, {
        "field": "conferenceTitle",
        "type": "single",
        "label": "conferenceTitle"
    }, {
        "field": "abstract",
        "type": "single",
        "label": "abstract"
    }, {
        "field": "addresses",
        "type": "single",
        "label": "addresses"
    }, {
        "field": "fundingText",
        "type": "single",
        "label": "fundingText"
    }, {
        "field": "citedReferenceCount",
        "type": "single",
        "label": "citedReferenceCount"
    }, {
        "field": "publisher",
        "type": "single",
        "label": "publisher"
    }, {
        "field": "ISSN",
        "type": "single",
        "label": "ISSN"
    }, {
        "field": "eISSN",
        "type": "single",
        "label": "eISSN"
    }
    ],
    input: {
        publicationYear: "Year",
        authorFullNames: "Author",
        sourceTitle: "Journal Name",
        articleTitle: "Title"
    },
    default: [
        "wosId",
        "publicationYear",
        "authorFullNames",
        "sourceTitle",
        "articleTitle"
        // "references"
    ],
    janus_map: {
        main_vertext: "Paper",
        path_to_main: {
            "Paper": ["References"],
        },
        vertex_types: [
            "Paper",
        ],
        edge_types: [
            {
                target: "Paper",
                source: "Paper",
                relation: "References"
            }],
        network_map: {
            citations: {
                vertex: "Paper",
                relation: "References"
            }
        },
        input_field_map: {
            "publisherCity": {
                "field": "publisherCity",
                "vertex": "Paper"
            },
            "authorFullNames": {
                "field": "authorFullNames",
                "vertex": "Paper"
            },
            "DOI": {
                "field": "DOI",
                "vertex": "Paper"
            },
            "ISBN": {
                "field": "ISBN",
                "vertex": "Paper"
            },
            "addresses": {
                "field": "addresses",
                "vertex": "Paper"
            },
            "conferenceHost": {
                "field": "conferenceHost",
                "vertex": "Paper"
            },
            "standardNames": {
                "field": "standardNames",
                "vertex": "Paper"
            },
            "bookDOI": {
                "field": "bookDOI",
                "vertex": "Paper"
            },
            "keywordsPlus": {
                "field": "keywordsPlus",
                "vertex": "Paper"
            },
            "citedReferenceCount": {
                "field": "citedReferenceCount",
                "vertex": "Paper"
            },
            "supplement": {
                "field": "supplement",
                "vertex": "Paper"
            },
            "startPage": {
                "field": "startPage",
                "vertex": "Paper"
            },
            "publicationDate": {
                "field": "publicationDate",
                "vertex": "Paper"
            },
            "documentType": {
                "field": "documentType",
                "vertex": "Paper"
            },
            "eISSN": {
                "field": "eISSN",
                "vertex": "Paper"
            },
            "RIDs": {
                "field": "RIDs",
                "vertex": "Paper"
            },
            "publicationYear": {
                "field": "publicationYear",
                "vertex": "Paper"
            },
            "conferenceDate": {
                "field": "conferenceDate",
                "vertex": "Paper"
            },
            "conferenceLocation": {
                "field": "conferenceLocation",
                "vertex": "Paper"
            },
            "ISSN": {
                "field": "ISSN",
                "vertex": "Paper"
            },
            "conferenceSponsor": {
                "field": "conferenceSponsor",
                "vertex": "Paper"
            },
            "specialIssue": {
                "field": "specialIssue",
                "vertex": "Paper"
            },
            "journalAbbreviation": {
                "field": "journalAbbreviation",
                "vertex": "Paper"
            },
            "issue": {
                "field": "issue",
                "vertex": "Paper"
            },
            "abstract": {
                "field": "abstract",
                "vertex": "Paper"
            },
            "reprintAddresses": {
                "field": "reprintAddresses",
                "vertex": "Paper"
            },
            "endPage": {
                "field": "endPage",
                "vertex": "Paper"
            },
            "numberOfPages": {
                "field": "numberOfPages",
                "vertex": "Paper"
            },
            "sourceTitle": {
                "field": "sourceTitle",
                "vertex": "Paper"
            },
            "wosId": {
                "field": "wosId",
                "vertex": "Paper"
            },
            "fundingOrgs": {
                "field": "fundingOrgs",
                "vertex": "Paper"
            },
            "pubmedId": {
                "field": "pubmedId",
                "vertex": "Paper"
            },
            "volume": {
                "field": "volume",
                "vertex": "Paper"
            },
            "journalISOAbbreviation": {
                "field": "journalISOAbbreviation",
                "vertex": "Paper"
            },
            "conferenceTitle": {
                "field": "conferenceTitle",
                "vertex": "Paper"
            },
            "publisherAddress": {
                "field": "publisherAddress",
                "vertex": "Paper"
            },
            "Property": {
                "field": "Property",
                "vertex": "Paper"
            },
            "partNumber": {
                "field": "partNumber",
                "vertex": "Paper"
            },
            "bookSeriesSubtitle": {
                "field": "bookSeriesSubtitle",
                "vertex": "Paper"
            },
            "bookEditors": {
                "field": "bookEditors",
                "vertex": "Paper"
            },
            "articleNumber": {
                "field": "articleNumber",
                "vertex": "Paper"
            },
            "ORCIDs": {
                "field": "ORCIDs",
                "vertex": "Paper"
            },
            "groupAuthors": {
                "field": "groupAuthors",
                "vertex": "Paper"
            },
            "publisher": {
                "field": "publisher",
                "vertex": "Paper"
            },
            "bookSeriesTitle": {
                "field": "bookSeriesTitle",
                "vertex": "Paper"
            },
            "earlyAccessDate": {
                "field": "earlyAccessDate",
                "vertex": "Paper"
            },
            "articleTitle": {
                "field": "articleTitle",
                "vertex": "Paper"
            },
            "emailAddresses": {
                "field": "emailAddresses",
                "vertex": "Paper"
            },
            "fundingText": {
                "field": "fundingText",
                "vertex": "Paper"
            }
        },
        output_field_map: {
            "publisherCity": {
                "vertexType": "Paper",
                "field": "publisherCity"
            },
            "authorFullNames": {
                "vertexType": "Paper",
                "field": "authorFullNames"
            },
            "DOI": {
                "vertexType": "Paper",
                "field": "DOI"
            },
            "ISBN": {
                "vertexType": "Paper",
                "field": "ISBN"
            },
            "addresses": {
                "vertexType": "Paper",
                "field": "addresses"
            },
            "conferenceHost": {
                "vertexType": "Paper",
                "field": "conferenceHost"
            },
            "standardNames": {
                "vertexType": "Paper",
                "field": "standardNames"
            },
            "bookDOI": {
                "vertexType": "Paper",
                "field": "bookDOI"
            },
            "keywordsPlus": {
                "vertexType": "Paper",
                "field": "keywordsPlus"
            },
            "citedReferenceCount": {
                "vertexType": "Paper",
                "field": "citedReferenceCount"
            },
            "supplement": {
                "vertexType": "Paper",
                "field": "supplement"
            },
            "startPage": {
                "vertexType": "Paper",
                "field": "startPage"
            },
            "publicationDate": {
                "vertexType": "Paper",
                "field": "publicationDate"
            },
            "documentType": {
                "vertexType": "Paper",
                "field": "documentType"
            },
            "eISSN": {
                "vertexType": "Paper",
                "field": "eISSN"
            },
            "RIDs": {
                "vertexType": "Paper",
                "field": "RIDs"
            },
            "publicationYear": {
                "vertexType": "Paper",
                "field": "publicationYear"
            },
            "conferenceDate": {
                "vertexType": "Paper",
                "field": "conferenceDate"
            },
            "conferenceLocation": {
                "vertexType": "Paper",
                "field": "conferenceLocation"
            },
            "ISSN": {
                "vertexType": "Paper",
                "field": "ISSN"
            },
            "conferenceSponsor": {
                "vertexType": "Paper",
                "field": "conferenceSponsor"
            },
            "specialIssue": {
                "vertexType": "Paper",
                "field": "specialIssue"
            },
            "journalAbbreviation": {
                "vertexType": "Paper",
                "field": "journalAbbreviation"
            },
            "issue": {
                "vertexType": "Paper",
                "field": "issue"
            },
            "abstract": {
                "vertexType": "Paper",
                "field": "abstract"
            },
            "reprintAddresses": {
                "vertexType": "Paper",
                "field": "reprintAddresses"
            },
            "endPage": {
                "vertexType": "Paper",
                "field": "endPage"
            },
            "numberOfPages": {
                "vertexType": "Paper",
                "field": "numberOfPages"
            },
            "sourceTitle": {
                "vertexType": "Paper",
                "field": "sourceTitle"
            },
            "wosId": {
                "vertexType": "Paper",
                "field": "wosId"
            },
            "fundingOrgs": {
                "vertexType": "Paper",
                "field": "fundingOrgs"
            },
            "pubmedId": {
                "vertexType": "Paper",
                "field": "pubmedId"
            },
            "volume": {
                "vertexType": "Paper",
                "field": "volume"
            },
            "journalISOAbbreviation": {
                "vertexType": "Paper",
                "field": "journalISOAbbreviation"
            },
            "conferenceTitle": {
                "vertexType": "Paper",
                "field": "conferenceTitle"
            },
            "publisherAddress": {
                "vertexType": "Paper",
                "field": "publisherAddress"
            },
            "Property": {
                "vertexType": "Paper",
                "field": "Property"
            },
            "partNumber": {
                "vertexType": "Paper",
                "field": "partNumber"
            },
            "bookSeriesSubtitle": {
                "vertexType": "Paper",
                "field": "bookSeriesSubtitle"
            },
            "bookEditors": {
                "vertexType": "Paper",
                "field": "bookEditors"
            },
            "articleNumber": {
                "vertexType": "Paper",
                "field": "articleNumber"
            },
            "ORCIDs": {
                "vertexType": "Paper",
                "field": "ORCIDs"
            },
            "groupAuthors": {
                "vertexType": "Paper",
                "field": "groupAuthors"
            },
            "publisher": {
                "vertexType": "Paper",
                "field": "publisher"
            },
            "bookSeriesTitle": {
                "vertexType": "Paper",
                "field": "bookSeriesTitle"
            },
            "earlyAccessDate": {
                "vertexType": "Paper",
                "field": "earlyAccessDate"
            },
            "articleTitle": {
                "vertexType": "Paper",
                "field": "articleTitle"
            },
            "emailAddresses": {
                "vertexType": "Paper",
                "field": "emailAddresses"
            },
            "fundingText": {
                "vertexType": "Paper",
                "field": "fundingText"
            }
        }


    }
};
// ==>------------------------------------------------------------------------------------------------
//     Vertex Label Name              | Partitioned | Static                                             |
// ---------------------------------------------------------------------------------------------------
//     Paper                          | false       | false                                              |
// ---------------------------------------------------------------------------------------------------
//     Edge Label Name                | Directed    | Unidirected | Multiplicity                         |
// ---------------------------------------------------------------------------------------------------
//     References                     | true        | false       | MULTI                                |
// ---------------------------------------------------------------------------------------------------
//     Property Key Name              | Cardinality | Data Type                                          |
// ---------------------------------------------------------------------------------------------------
//     ISBN                           | SINGLE      | class java.lang.String                             |
// DOI                            | SINGLE      | class java.lang.String                             |
// pubmedId                       | SINGLE      | class java.lang.String                             |
// bookEditors                    | SINGLE      | class java.lang.String                             |
// groupAuthors                   | SINGLE      | class java.lang.String                             |
// bookSeriesTitle                | SINGLE      | class java.lang.String                             |
// bookSeriesSubtitle             | SINGLE      | class java.lang.String                             |
// conferenceDate                 | SINGLE      | class java.lang.String                             |
// conferenceLocation             | SINGLE      | class java.lang.String                             |
// conferenceSponsor              | SINGLE      | class java.lang.String                             |
// conferenceHost                 | SINGLE      | class java.lang.String                             |
// keywordsPlus                   | SINGLE      | class java.lang.String                             |
// reprintAddresses               | SINGLE      | class java.lang.String                             |
// emailAddresses                 | SINGLE      | class java.lang.String                             |
// RIDs                           | SINGLE      | class java.lang.String                             |
// ORCIDs                         | SINGLE      | class java.lang.String                             |
// fundingOrgs                    | SINGLE      | class java.lang.String                             |
// publisherCity                  | SINGLE      | class java.lang.String                             |
// publisherAddress               | SINGLE      | class java.lang.String                             |
// journalAbbreviation            | SINGLE      | class java.lang.String                             |
// journalISOAbbreviation         | SINGLE      | class java.lang.String                             |
// publicationDate                | SINGLE      | class java.lang.String                             |
// volume                         | SINGLE      | class java.lang.String                             |
// issue                          | SINGLE      | class java.lang.String                             |
// partNumber                     | SINGLE      | class java.lang.String                             |
// supplement                     | SINGLE      | class java.lang.String                             |
// specialIssue                   | SINGLE      | class java.lang.String                             |
// startPage                      | SINGLE      | class java.lang.String                             |
// endPage                        | SINGLE      | class java.lang.String                             |
// articleNumber                  | SINGLE      | class java.lang.String                             |
// bookDOI                        | SINGLE      | class java.lang.String                             |
// earlyAccessDate                | SINGLE      | class java.lang.String                             |
// numberOfPages                  | SINGLE      | class java.lang.Integer                            |
// wosId                          | SINGLE      | class java.lang.String                             |
// publicationYear                | SINGLE      | class java.lang.Integer                            |
// standardNames                  | SINGLE      | class java.lang.String                             |
// authorFullNames                | SINGLE      | class java.lang.String                             |
// articleTitle                   | SINGLE      | class java.lang.String                             |
// sourceTitle                    | SINGLE      | class java.lang.String                             |
// documentType                   | SINGLE      | class java.lang.String                             |
// conferenceTitle                | SINGLE      | class java.lang.String                             |
// abstract                       | SINGLE      | class java.lang.String                             |
// addresses                      | SINGLE      | class java.lang.String                             |
// fundingText                    | SINGLE      | class java.lang.String                             |
// citedReferenceCount            | SINGLE      | class java.lang.Integer                            |
// publisher                      | SINGLE      | class java.lang.String                             |
// ISSN                           | SINGLE      | class java.lang.String                             |
// eISSN                          | SINGLE      | class java.lang.String                             |
// ---------------------------------------------------------------------------------------------------
//     Vertex Index Name              | Type        | Unique    | Backing        | Key:           Status |
// ---------------------------------------------------------------------------------------------------
//     wosPubYearMixed                | Mixed       | false     | search         | publicationYear:    ENABLED |
// wosCitedRefCountMixed          | Mixed       | false     | search         | citedReferenceCount:    ENABLED |
// wosFundingTextMixed            | Mixed       | false     | search         | fundingText:    ENABLED |
// wosSourceTitleComposite        | Composite   | false     | internalindex  | sourceTitle:    ENABLED |
// wosSourceTitleMixed            | Mixed       | false     | search         | sourceTitle:    ENABLED |
// wosArticleTitleMixed           | Mixed       | false     | search         | articleTitle:    ENABLED |
// wosArticleTitleComposite       | Composite   | false     | internalindex  | articleTitle:    ENABLED |
// wosWosIdComposite              | Composite   | false     | internalindex  | wosId:        ENABLED |
// wosAbstractMixed               | Mixed       | false     | search         | abstract:     ENABLED |
// wosStandardNamesMixed          | Mixed       | false     | search         | standardNames:    ENABLED |
// wosAuthorFullNamesMixed        | Mixed       | false     | search         | authorFullNames:    ENABLED |
// wosConferenceTitleComposite    | Composite   | false     | internalindex  | conferenceTitle:    ENABLED |
// wosConferenceTitleMixed        | Mixed       | false     | search         | conferenceTitle:    ENABLED |
// wosDocumentTypeComposite       | Composite   | false     | internalindex  | documentType:    ENABLED |
// wosPublisherComposite          | Composite   | false     | internalindex  | publisher:    ENABLED |
// wosAddressesMixed              | Mixed       | false     | search         | addresses:    ENABLED |
// wosPubmedIdComposite           | Composite   | false     | internalindex  | pubmedId:     ENABLED |
// wosIsbnComposite               | Composite   | false     | internalindex  | ISBN:         ENABLED |
// wosEissnComposite              | Composite   | false     | internalindex  | eISSN:        ENABLED |
// wosDoiComposite                | Composite   | false     | internalindex  | DOI:          ENABLED |
// wosIssnComposite               | Composite   | false     | internalindex  | ISSN:         ENABLED |
// wosPubYearComposite            | Composite   | false     | internalindex  | publicationYear:    ENABLED |
// ---------------------------------------------------------------------------------------------------
//     Edge Index (VCI) Name          | Type        | Unique    | Backing        | Key:           Status |
// ---------------------------------------------------------------------------------------------------
//     ---------------------------------------------------------------------------------------------------
//         Relation Index                 | Type        | Direction | Sort Key       | Order    |     Status |
// ---------------------------------------------------------------------------------------------------
