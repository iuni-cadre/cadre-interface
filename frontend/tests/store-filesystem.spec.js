import Vue from "vue";
import Vuex from "vuex";
Vue.use(Vuex);

import axios from "axios";
jest.mock("axios");

import CadreGlobalFunctions from "./mock-plugin";

// import mockAxios from "jest-mock-axios";

import { actions, mutations, getters, state } from "../src/store";
import FullStore from "../src/store";
import Filesystem from "../src/store/modules/filesystem";

Vue.use(CadreGlobalFunctions, {
    store: {
        getters: {
            "user/authToken": "fake-token",
            "user/username": "fake-username"
        }
    },
    axios: axios,
    config: {}
});

let store;
beforeEach(() => {
    store = new Vuex.Store({
        state: Filesystem.state,
        getters: Filesystem.getters,
        mutations: Filesystem.mutations,
        actions: Filesystem.actions
    });
});

describe.skip("filesystem store", () => {
    beforeEach(() => {
        console.error = msg => {
            throw new Error(msg);
        };
    });
    it("can be accessed with filesystem namespace", () => {
        FullStore.commit("filesystem/setRoot", "/");
        let root = FullStore.getters["filesystem/getRoot"];
        expect(root).toEqual("/");
    });

    it("can set root", () => {
        store.commit("setRoot", "test_root");
        let root = store.state.root;
        expect(root).toEqual("test_root");
    });

    it("has a getFiles action", () => {
        expect(() => {
            store.dispatch("getFiles");
        }).not.toThrow();
    });

    // it("has a getFiles action that returns a promise", async () => {
    //     let prom = store.dispatch("getFiles");
    //     expect(prom).not.toBeUndefined();
    //     // expect(prom.not.toBeUndefined());
    //     // prom.finally(()=>{
    //     //     // aexpect()
    //     // })
    // });
});

describe("getFiles", () => {
    afterEach(() => {
        // mockAxios.reset();
    });

    it("calls the correct endpoint", () => {
        let prom = store.dispatch("getFiles").catch(err => {});

        expect(axios.mock.calls[0][0].url).toBe("/rac-api/user-files");
        expect(axios.mock.calls[0][0].method).toBe("GET");
    });

    it("calls with correct parameters", () => {
        let prom = store.dispatch("getFiles", {path: "/query-results"}).catch(err => {});

        expect(axios.mock.calls[0][0].params).toEqual({path: "/query-results"});
    });

    it("saves output structure to state", () => {
        let sample_response = {
            data: [
                {
                    path: "/packages",
                    type: "folder"
                },
                {
                    path: "/query-results",
                    type: "folder"
                },
                {
                    path: "/query-results/JOBID1234.csv",
                    type: "file",
                    download_url: "https://xxxxxxxxxxx" //S3 bucket path or custom proxy url for downloading... however we decide to implement downloads
                },
                {
                    path: "/query-results/JOBID2345.csv",
                    type: "file",
                    download_url: "https://xxxxxxxxxxx" //S3 bucket path or custom proxy url for downloading... however we decide to implement downloads
                }
            ]
        };

        axios.mockResolvedValue(sample_response);

        let prom = store.dispatch("getFiles").catch(err => {});
        return prom.then(response => {
            expect(store.state.file_structure).toEqual([
                {
                    path: "/",
                    type: "folder",
                    children: [
                        {
                            path: "/packages",
                            type: "folder",
                            children: []
                        },
                        {
                            path: "/query-results",
                            type: "folder",
                            children: [
                                {
                                    path: "/query-results/JOBID1234.csv",
                                    type: "file",
                                    download_url: "https://xxxxxxxxxxx" //S3 bucket path or custom proxy url for downloading... however we decide to implement downloads
                                },
                                {
                                    path: "/query-results/JOBID2345.csv",
                                    type: "file",
                                    download_url: "https://xxxxxxxxxxx" //S3 bucket path or custom proxy url for downloading... however we decide to implement downloads
                                }
                            ]
                        }
                    ]
                }
            ]);
        });
    });
});
describe("updateFileStructure mutation", () => {
    it("orders structure properly", () => {
        let sample_part1 = [
            {
                path: "/packages",
                type: "folder"
            },
            {
                path: "/query-results",
                type: "folder"
            },
            {
                path: "/query-results/JOBID1234.csv",
                type: "file",
                download_url: "https://xxxxxxxxxxx" //S3 bucket path or custom proxy url for downloading... however we decide to implement downloads
            },
            {
                path: "/query-results/JOBID2345.csv",
                type: "file",
                download_url: "https://xxxxxxxxxxx" //S3 bucket path or custom proxy url for downloading... however we decide to implement downloads
            }
        ];

        let sample_part2 = [
            {
                path: "/query-results/JOBID123410.csv",
                type: "file",
                download_url: "https://xxxxxxxxxxx" //S3 bucket path or custom proxy url for downloading... however we decide to implement downloads
            },
            {
                path: "/query-results/JOBID234510.csv",
                type: "file",
                download_url: "https://xxxxxxxxxxx" //S3 bucket path or custom proxy url for downloading... however we decide to implement downloads
            },
            {
                path: "/query-results/packages",
                type: "folder"
            }
        ];

        store.commit("updateFileStructure", sample_part1);
        store.commit("updateFileStructure", sample_part2);

        expect(store.state.file_structure).toEqual([
            {
                path: "/",
                type: "folder",
                children: [
                    {
                        path: "/packages",
                        type: "folder",
                        children: []
                    },
                    {
                        path: "/query-results",
                        type: "folder",
                        children: [
                            {
                                path: "/query-results/JOBID1234.csv",
                                type: "file",
                                download_url: "https://xxxxxxxxxxx" //S3 bucket path or custom proxy url for downloading... however we decide to implement downloads
                            },
                            {
                                path: "/query-results/JOBID123410.csv",
                                type: "file",
                                download_url: "https://xxxxxxxxxxx" //S3 bucket path or custom proxy url for downloading... however we decide to implement downloads
                            },
                            {
                                path: "/query-results/JOBID2345.csv",
                                type: "file",
                                download_url: "https://xxxxxxxxxxx" //S3 bucket path or custom proxy url for downloading... however we decide to implement downloads
                            },
                            {
                                path: "/query-results/JOBID234510.csv",
                                type: "file",
                                download_url: "https://xxxxxxxxxxx" //S3 bucket path or custom proxy url for downloading... however we decide to implement downloads
                            },

                            {
                                path: "/query-results/packages",
                                type: "folder",
                                children: []
                            }
                        ]
                    }
                ]
            }
        ]);
    });
});
