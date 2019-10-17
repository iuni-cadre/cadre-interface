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

describe("filesystem store", () => {
    let store;
    beforeEach(() => {
        console.error = msg => {
            throw new Error(msg);
        };
        store = new Vuex.Store({
            state: Filesystem.state,
            getters: Filesystem.getters,
            mutations: Filesystem.mutations,
            actions: Filesystem.actions
        });
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
    let store;
    beforeEach(() => {
        console.error = msg => {
            throw new Error(msg);
        };
        store = new Vuex.Store({
            state: Filesystem.state,
            getters: Filesystem.getters,
            mutations: Filesystem.mutations,
            actions: Filesystem.actions
        });
    });

    afterEach(() => {
        // mockAxios.reset();
    });

    it("calls the correct endpoint", () => {
        // let catchFn = jest.fn();
        // let thenFn = jest.fn();

        // axios.mockResolvedValue("TEST");

        let prom = store.dispatch("getFiles").catch(err => {});

        expect(axios.mock.calls[0][0].url).toBe("/rac-api/user-files");
        expect(axios.mock.calls[0][0].method).toBe("GET");

        return expect(prom).resolves.toBeTruthy();
        // expect(mockAxios.get).toHaveBeenCalledWith('/');

        // return expect(prom).rejects.toEqual("test");
    });
});
