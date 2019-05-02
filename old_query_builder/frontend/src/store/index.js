import Vue from "vue";
import Vuex from "vuex";

import UserModule from "./modules/user.js";
import QueryModule from "./modules/query.js";

Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        user: UserModule,
        query: QueryModule
    },
    state: {

    },
    mutations: {},
    actions: {}
});
