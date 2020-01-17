import { shallowMount, createLocalVue, mount } from "@vue/test-utils";
import CreateToolForm from "../src/components/Marketplace/MarketplaceNewToolForm.vue"; // name of your Vue component

import Vue from "vue";
import Vuex from "vuex";
Vue.use(Vuex);

import VueRouter from 'vue-router';
Vue.use(VueRouter);

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

// const router = new VueRouter();

let store;
let wrapper;
import router from "../src/router"

beforeEach(() => {
    store = new Vuex.Store({
        modules: {
            // user: UserModule,
            // query: QueryModule,
            // racpackage: RacPackageModule,
            filesystem: FilesystemModule
        }
    });
    // axios.mockReturnValue(Promise.resolve(sample_response_1));
    wrapper = shallowMount(CreateToolForm, {
        propsData: {},
        mocks: {},
        stubs: {},
        store,
        router

    });
});

afterEach(() => {
    wrapper.destroy();
});

describe("CreateToolForm", () => {
    test("is a Vue instance", () => {
        expect(wrapper.isVueInstance).toBeTruthy();
    });
    test("sets success value upon successful submission", async () => {
        axios.mockReturnValue(Promise.resolve(sample_response_1));
        let wrapper = mount(CreateToolForm, {
            propsData: {},
            mocks: {},
            stubs: {},
            store,
            router
        });

        wrapper.vm.data_to_send = {
            name: "test 1",
            install_commands: "none",
            description: "test 1",
            file_paths: ['/test_1.py'],
            entrypoint: "/test_1.py",
            environment: "python"
        }
        wrapper.vm.submitForm();
        
        await wrapper.vm.$nextTick();

        expect(wrapper.vm.success).toEqual(sample_response_1);
    })
})


let sample_response_1 = { "job_id": "d454f8c8-5b33-48b5-972e-1f68bcb80aa3", "message_id": "7ebd734b-424a-4e12-a456-367f825d5e66", "tool_id": "c5708016-5d2f-4d54-ac53-e13ee14fb2d3" };