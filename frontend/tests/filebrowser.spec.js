import { shallowMount, createLocalVue, mount } from "@vue/test-utils";
import FilebrowserMain from "../src/components/Filebrowser/FilebrowserMain.vue"; // name of your Vue component

import Vue from "vue";
import Vuex from "vuex";
Vue.use(Vuex);

// import UserModule from "../src/store/modules/user.js";
// import QueryModule from "../src/store/modules/query.js";
// import RacPackageModule from "../src/store/modules/racpackage.js";

// const localVue = createLocalVue();

import axios from "axios";
jest.mock("axios");

import FilesystemModule from "../src/store/modules/filesystem";
import CadreGlobalFunctions from "./mock-plugin";
Vue.use(CadreGlobalFunctions, {
    store: {
        getters: {
            "user/authToken": "fake-token",
            "user/username": "fake-username"
        }
    },
    axios: axios,
    config: {
        rac_api_prefix: "/rac-api"
    }
});

let store;
let wrapper;

beforeEach(() => {
    store = new Vuex.Store({
        modules: {
            // user: UserModule,
            // query: QueryModule,
            // racpackage: RacPackageModule,
            filesystem: FilesystemModule
        }
    });
    axios.mockReturnValue(Promise.resolve(sample_response_1));
    wrapper = shallowMount(FilebrowserMain, {
        propsData: {},
        mocks: {},
        stubs: {},
        store,

    });
});

afterEach(() => {
    wrapper.destroy();
});

describe("FilebrowserMain", () => {
    test("is a Vue instance", () => {
        expect(wrapper.isVueInstance).toBeTruthy();
    });

    test("computed file structure matches store", () => {
        expect(wrapper.vm.file_structure).toEqual(store.state.filesystem.file_structure);
    });

    test("renders list items for all folders and files", () =>{
        axios.mockReturnValue(Promise.resolve(sample_response_1));
        let wrapper = mount(FilebrowserMain, {
            propsData: {},
            mocks: {},
            stubs: {},
            store,

        });

        let li_count = wrapper.findAll('li').length;
        expect(li_count).toEqual(store.state.filesystem.flat_file_structure.length);
        wrapper.destroy();
    });
});



let sample_response_1 = {
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
