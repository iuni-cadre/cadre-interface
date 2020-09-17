import { convertQueryDataToJanus } from "../src/store/modules/query.js";

describe("ConvertQueryDataToJanus", () => {
    test("returns something", () => {
        let result = convertQueryDataToJanus(sampleJSON);
        expect(result).toBeTruthy();
    });

    test("has all the parts", () => {
        let result = convertQueryDataToJanus(sampleJSON);
        expect(result.job_name).not.toBeUndefined();
        expect(result.graph).not.toBeUndefined();
        expect(result.csv_output).not.toBeUndefined();
        expect(result.dataset).not.toBeUndefined();
    });

    test("copies job_name and datasets", () => {
        let result = convertQueryDataToJanus(sampleJSON);
        expect(result.job_name).toBe(sampleJSON.job_name);
        expect(result.dataset).toBe(sampleJSON.dataset);
    });

    test("converts filters to graph", () => {
        let result = convertQueryDataToJanus(sampleJSON);
        expect(result.graph).toStrictEqual(sampleResult.graph);
    });

    test("converts output to csv_fields", () => {
        let result = convertQueryDataToJanus(sampleJSON);
        expect(result.csv_output).toStrictEqual(sampleResult.csv_output);
    });

    test("wos: converts input fields", () => {
        sampleJSON.dataset = "wos";
        sampleJSON.filters = [
            {
                field: "publicationYear",
                value: "2010",
                operation: "AND"
            }];
        const expected = [
                            {
                                field: "publicationYear",
                                filterType: "is",
                                value: "2010",
                                operator: "AND"
                            }
                        ];

        let result = convertQueryDataToJanus(sampleJSON);
        expect(result.graph.nodes.length).toBe(2);
        expect(result.graph.nodes[0].filters.length).toBe(1);
        expect(result.graph.nodes[1].filters.length).toBe(0);
        expect(result.graph.nodes[0].filters).toStrictEqual(expected);
    });

    test("converts output to graph with single vertex", () => {

        let input = {
            job_name: "Job Name",
            filters: [
                {
                    field: "year",
                    value: "2010",
                    operation: "AND"
                }
            ],
            output: [
            ],
            dataset: "mag"
        };

        const expected_output = {
            job_name: "Job Name",
            dataset: "mag",
            graph: {
                nodes: [
                    {
                        vertexType: "Paper",
                        filters: [
                            {
                                field: "year",
                                filterType: "is",
                                value: "2010",
                                operator: "AND"
                            }
                        ]
                    }
                ],
                edges: [
                    {
                        source: "Paper",
                        target: "Paper",
                        relation: "References"
                    }
                ],
            },
            csv_output: [

            ]
        };



        let result = convertQueryDataToJanus(input);
        expect(result.graph).toStrictEqual(expected_output.graph);
    });
});

const sampleResult = {
    job_name: "Job Name",
    dataset: "mag",
    graph: {
        nodes: [
            {
                vertexType: "Paper",
                filters: [
                    {
                        field: "year",
                        filterType: "is",
                        value: "TEST",
                        operator: "AND"
                    },
                    {
                        field: "title",
                        filterType: "is",
                        value: "SOME TITLE",
                        operator: ""
                    }
                ]
            },
            {
                vertexType: "Author",
                filters: [
                    {
                        field: "name",
                        filterType: "is",
                        value: "TEST AUTH",
                        operator: "AND"
                    }
                ]
            },
            {
                vertexType: "Paper",
                filters: []
            }
        ],
        edges: [
            {
                source: "Author",
                target: "Paper",
                relation: "AuthorOf"
            },
            {
                source: "Paper",
                target: "Paper",
                relation: "References"
            }
        ],
    },
    csv_output: [
        {
            field: "paperId",
            vertexType: "Paper"
        },
        {
            field: "year",
            vertexType: "Paper"
        },
        {
            field: "originalTitle",
            vertexType: "Paper"
        },
        {
            field: "displayName",
            vertexType: "Author"
        },
        {
            field: "displayName",
            vertexType: "JournalFixed"
        }
    ]
};

const sampleJSON = {
    job_name: "Job Name",
    filters: [
        {
            field: "year",
            value: "TEST",
            operation: "AND"
        },
        {
            field: "authors_display_name",
            value: "TEST AUTH",
            operation: "AND"
        },
        {
            field: "paper_title",
            value: "SOME TITLE",
            operation: ""
        }
    ],
    output: [
        {
            field: "paper_id",
            type: "single"
        },
        {
            field: "year",
            type: "single"
        },
        {
            field: "original_title",
            type: "single"
        },
        {
            field: "authors_display_name",
            type: "single"
        },
        {
            field: "journal_display_name",
            type: "single"
        },
        {
            field: "citations",
            type: "network",
            degree: 1
        }
    ],
    dataset: "mag"
};

// import { shallowMount, createLocalVue, mount } from "@vue/test-utils";
// import FilebrowserMain from "../src/components/Filebrowser/FilebrowserMain.vue"; // name of your Vue component

// import Vue from "vue";
// import Vuex from "vuex";
// Vue.use(Vuex);

// import { library } from "@fortawesome/fontawesome-svg-core";
// import { faCircleNotch, faSpinner, faAtom, faCompactDisc, faExclamationTriangle, faSyncAlt, faTrashAlt, faBars, faHamburger, faChevronRight, faChevronDown } from "@fortawesome/free-solid-svg-icons";
// import { faSquare, faCheckSquare, faCircle, faDotCircle, faFolder, faFolderOpen, faFile } from "@fortawesome/free-regular-svg-icons";
// import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

// library.add(faSpinner,
//     faCircleNotch,
//     faAtom,
//     faCompactDisc,
//     faSquare,
//     faCheckSquare,
//     faExclamationTriangle,
//     faSyncAlt,
//     faTrashAlt,
//     faBars,
//     faHamburger,
//     faCircle,
//     faDotCircle,
//     faFolder,
//     faFolderOpen,
//     faChevronDown,
//     faChevronRight,
//     faFile);

// Vue.component("fa", FontAwesomeIcon);

// // import UserModule from "../src/store/modules/user.js";
// // import QueryModule from "../src/store/modules/query.js";
// // import RacPackageModule from "../src/store/modules/racpackage.js";

// // const localVue = createLocalVue();

// import axios from "axios";
// jest.mock("axios");

// import FilesystemModule from "../src/store/modules/filesystem";
// import CadreGlobalFunctions from "./mock-plugin";
// Vue.use(CadreGlobalFunctions, {
//     store: {
//         getters: {
//             "user/authToken": "fake-token",
//             "user/username": "fake-username"
//         }
//     },
//     axios: axios,
//     config: {
//         rac_api_prefix: "/rac-api"
//     }
// });

// let store;
// let wrapper;

// beforeEach(() => {
//     store = new Vuex.Store({
//         modules: {
//             // user: UserModule,
//             // query: QueryModule,
//             // racpackage: RacPackageModule,
//             filesystem: FilesystemModule
//         }
//     });
//     axios.mockReturnValue(Promise.resolve(sample_response_1));
//     wrapper = shallowMount(FilebrowserMain, {
//         propsData: {},
//         mocks: {},
//         stubs: {},
//         store,

//     });
// });

// afterEach(() => {
//     wrapper.destroy();
// });

// describe("FilebrowserMain", () => {
//     test("is a Vue instance", () => {
//         expect(wrapper.isVueInstance).toBeTruthy();
//     });

//     test("computed file structure matches store", () => {
//         expect(wrapper.vm.file_structure).toEqual(store.state.filesystem.file_structure);
//     });

//     test("renders list items for all folders and files", async () => {
//         axios.mockReturnValue(Promise.resolve(sample_response_1));
//         let wrapper = mount(FilebrowserMain, {
//             propsData: {},
//             mocks: {},
//             stubs: {},
//             store,

//         });
//         let folders = wrapper.findAll('ul .folder-name'); //all folders not including root
//         folders.trigger("click"); //click those folder names
//         await wrapper.vm.$nextTick();

//         let files = wrapper.findAll('.file-name'); //all files
//         expect(files.length + folders.length).toEqual(store.state.filesystem.flat_file_structure.length);
//         wrapper.destroy();

//     });

//     test("folders and files have checkboxes", async () => {
//         axios.mockReturnValue(Promise.resolve(sample_response_1));
//         let wrapper = mount(FilebrowserMain, {
//             propsData: {},
//             mocks: {},
//             stubs: {},
//             store,

//         });
//         let folders = wrapper.findAll('ul .folder-name'); //all folders not including root
//         folders.trigger("click"); //click those folder names
//         await wrapper.vm.$nextTick();

//         let checkboxes = wrapper.findAll('input[type=checkbox]'); //all files
//         expect(checkboxes.length).toEqual(store.state.filesystem.flat_file_structure.length);
//         wrapper.destroy();

//     });

//     test("checking files bubbles up the selected items", async () => {
//         axios.mockReturnValue(Promise.resolve(sample_response_1));
//         let wrapper = mount(FilebrowserMain, {
//             propsData: {},
//             mocks: {},
//             stubs: {},
//             store,

//         });
//         let folders = wrapper.findAll('ul .folder-name'); //all folders not including root
//         folders.trigger("click"); //click those folder names
//         await wrapper.vm.$nextTick();

//         let checkboxes = wrapper.findAll('input[type=checkbox]'); //all files
//         checkboxes.trigger("click");
//         await wrapper.vm.$nextTick();

//         expect(wrapper.vm.selected_paths.length).toEqual(4);
//         wrapper.destroy();

//     });

//     test("checkboxes add to selected_paths array", async () => {
//         axios.mockReturnValue(Promise.resolve(sample_response_1));
//         let wrapper = mount(FilebrowserMain, {
//             propsData: {},
//             mocks: {},
//             stubs: {},
//             store,

//         });
//         let folders = wrapper.findAll('input[type=checkbox]');
//         folders.trigger("click");
//         await wrapper.vm.$nextTick();

//         expect(wrapper.vm.selected_paths.length).toEqual(2);
//         wrapper.destroy();

//     });

//     test("selected paths get put on selected_paths array ", async () => {
//         axios.mockReturnValue(Promise.resolve(sample_response_1));
//         let wrapper = mount(FilebrowserMain, {
//             propsData: {},
//             mocks: {},
//             stubs: {},
//             store,

//         });
//         let folders = wrapper.findAll('input[type=checkbox]');
//         folders.trigger("click");
//         await wrapper.vm.$nextTick();
//         let expected = [
//             sample_response_1.data[0].path,
//             sample_response_1.data[1].path,
//         ]
//         expect(wrapper.vm.selected_paths).toEqual(expected);
//         wrapper.destroy();

//     });

//     test("deselecting box removes from selected_paths", async () => {
//         axios.mockReturnValue(Promise.resolve(sample_response_1));
//         let wrapper = mount(FilebrowserMain, {
//             propsData: {},
//             mocks: {},
//             stubs: {},
//             store,

//         });
//         let folders = wrapper.findAll('input[type=checkbox]');
//         folders.trigger("click");
//         await wrapper.vm.$nextTick();
//         folders.at(0).trigger("click");
//         await wrapper.vm.$nextTick();

//         expect(wrapper.vm.selected_paths.length).toEqual(1);
//         wrapper.destroy();

//     });

// });
