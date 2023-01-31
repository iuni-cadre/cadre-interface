import Vue from "vue";
import Vuex from "vuex";

import UserModule from "./modules/user.js";
import QueryModule from "./modules/query.js";
import FilesystemModule from "./modules/filesystem";
import LoadingModule from "./modules/loading";

Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        user: UserModule,
        query: QueryModule,
        filesystem: FilesystemModule,
        loading: LoadingModule

    },
    state: {

    },
    mutations: {},
    actions: {}
});
