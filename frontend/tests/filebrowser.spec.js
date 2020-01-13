import { shallowMount, createLocalVue, mount } from "@vue/test-utils";
import FilebrowserMain from "../src/components/Filebrowser/FilebrowserMain.vue"; // name of your Vue component

import Vue from "vue";
import Vuex from "vuex";
Vue.use(Vuex);

import { library } from "@fortawesome/fontawesome-svg-core";
import { faCircleNotch, faSpinner, faAtom, faCompactDisc, faExclamationTriangle, faSyncAlt, faTrashAlt, faBars, faHamburger, faChevronRight, faChevronDown } from "@fortawesome/free-solid-svg-icons";
import { faSquare, faCheckSquare, faCircle, faDotCircle, faFolder, faFolderOpen, faFile } from "@fortawesome/free-regular-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

library.add(faSpinner,
    faCircleNotch,
    faAtom,
    faCompactDisc,
    faSquare,
    faCheckSquare,
    faExclamationTriangle,
    faSyncAlt,
    faTrashAlt,
    faBars,
    faHamburger,
    faCircle,
    faDotCircle,
    faFolder,
    faFolderOpen,
    faChevronDown,
    faChevronRight,
    faFile);

Vue.component("fa", FontAwesomeIcon);

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

    test("renders list items for all folders and files", async () => {
        axios.mockReturnValue(Promise.resolve(sample_response_1));
        let wrapper = mount(FilebrowserMain, {
            propsData: {},
            mocks: {},
            stubs: {},
            store,

        });
        let folders = wrapper.findAll('ul .folder-name'); //all folders not including root
        folders.trigger("click"); //click those folder names
        await wrapper.vm.$nextTick();

        let files = wrapper.findAll('.file-name'); //all files
        expect(files.length + folders.length).toEqual(store.state.filesystem.flat_file_structure.length);
        wrapper.destroy();

    });

    test("folders and files have checkboxes", async () => {
        axios.mockReturnValue(Promise.resolve(sample_response_1));
        let wrapper = mount(FilebrowserMain, {
            propsData: {},
            mocks: {},
            stubs: {},
            store,

        });
        let folders = wrapper.findAll('ul .folder-name'); //all folders not including root
        folders.trigger("click"); //click those folder names
        await wrapper.vm.$nextTick();

        let checkboxes = wrapper.findAll('input[type=checkbox]'); //all files
        expect(checkboxes.length).toEqual(store.state.filesystem.flat_file_structure.length);
        wrapper.destroy();

    });

    test("checking files bubbles up the selected items", async () => {
        axios.mockReturnValue(Promise.resolve(sample_response_1));
        let wrapper = mount(FilebrowserMain, {
            propsData: {},
            mocks: {},
            stubs: {},
            store,

        });
        let folders = wrapper.findAll('ul .folder-name'); //all folders not including root
        folders.trigger("click"); //click those folder names
        await wrapper.vm.$nextTick();

        let checkboxes = wrapper.findAll('input[type=checkbox]'); //all files
        checkboxes.trigger("click");
        await wrapper.vm.$nextTick();
        
        expect(wrapper.vm.selected_paths.length).toEqual(4);
        wrapper.destroy();

    });

    test("checkboxes add to selected_paths array", async () => {
        axios.mockReturnValue(Promise.resolve(sample_response_1));
        let wrapper = mount(FilebrowserMain, {
            propsData: {},
            mocks: {},
            stubs: {},
            store,

        });
        let folders = wrapper.findAll('input[type=checkbox]'); 
        folders.trigger("click"); 
        await wrapper.vm.$nextTick();

        expect(wrapper.vm.selected_paths.length).toEqual(2);
        wrapper.destroy();

    });

    test("selected paths get put on selected_paths array ", async () => {
        axios.mockReturnValue(Promise.resolve(sample_response_1));
        let wrapper = mount(FilebrowserMain, {
            propsData: {},
            mocks: {},
            stubs: {},
            store,

        });
        let folders = wrapper.findAll('input[type=checkbox]'); 
        folders.trigger("click"); 
        await wrapper.vm.$nextTick();
        let expected = [
            sample_response_1.data[0].path,
            sample_response_1.data[1].path,
        ]
        expect(wrapper.vm.selected_paths).toEqual(expected);
        wrapper.destroy();

    });
    

    test("deselecting box removes from selected_paths", async () => {
        axios.mockReturnValue(Promise.resolve(sample_response_1));
        let wrapper = mount(FilebrowserMain, {
            propsData: {},
            mocks: {},
            stubs: {},
            store,

        });
        let folders = wrapper.findAll('input[type=checkbox]'); 
        folders.trigger("click"); 
        await wrapper.vm.$nextTick();
        folders.at(0).trigger("click");
        await wrapper.vm.$nextTick();

        expect(wrapper.vm.selected_paths.length).toEqual(1);
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
