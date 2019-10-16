import Vue from "vue";
import Vuex from "vuex";
Vue.use(Vuex);

import { actions, mutations, getters, state } from "../src/store";
import FullStore from "../src/store";
import Filesystem from "../src/store/modules/filesystem";

describe("filesystem store", () => {
    let store;
    beforeEach(() => {
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
    })

});
