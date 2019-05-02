import Vue from "vue";
import Vuex from "vuex";

import UserModule from "./modules/user.js";

Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        user: UserModule
    },
    state: {

    },
    mutations: {},
    actions: {}
});
