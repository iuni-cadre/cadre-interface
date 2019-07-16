import Vue from "vue";
import Vuex from "vuex";
import App from "./App.vue";
import router from "./router";
import store from "./store";

import axios from "axios";
import VueAxios from "vue-axios";
import Config from "../../conf/frontend.config.json";

import { library } from '@fortawesome/fontawesome-svg-core';
import { faCircleNotch, faSpinner, faAtom, faCompactDisc, faExclamationTriangle} from '@fortawesome/free-solid-svg-icons';
import { faSquare, faCheckSquare } from '@fortawesome/free-regular-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

library.add(faSpinner, faCircleNotch, faAtom, faCompactDisc, faSquare, faCheckSquare, faExclamationTriangle);

Vue.component('fa', FontAwesomeIcon);

import CadreGlobalFunctions from "./CadreGlobalsPlugin.js";

let axiosInstance = axios.create({
    baseURL: process.env.BASE_URL
});

Vue.use(VueAxios, axiosInstance);
Vue.use(Vuex);

Vue.use(CadreGlobalFunctions, { store: store, axios: axiosInstance });

Vue.config.productionTip = false;

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount("#app");
