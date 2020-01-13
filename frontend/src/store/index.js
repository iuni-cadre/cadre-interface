import Vue from "vue";
import Vuex from "vuex";

import UserModule from "./modules/user.js";
import QueryModule from "./modules/query.js";
import RacPackageModule from "./modules/racpackage.js";
import FilesystemModule from "./modules/filesystem";

Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        user: UserModule,
        query: QueryModule,
        racpackage: RacPackageModule,
        filesystem: FilesystemModule

    },
    state: {

    },
    mutations: {},
    actions: {}
});
