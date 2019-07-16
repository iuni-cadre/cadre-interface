import Vue from "vue";
import Vuex from "vuex";

import UserModule from "./modules/user.js";
import QueryModule from "./modules/query.js";
import RacPackageModule from "./modules/racpackage.js";

Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        user: UserModule,
        query: QueryModule,
        racpackage: RacPackageModule

    },
    state: {

    },
    mutations: {},
    actions: {}
});
