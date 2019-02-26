/* Global utility functions used by cadre */

// import $axios from "axios";
import $config from "../../conf/frontend.config.json";
// import Moment from "moment";
export default {
    $store: undefined,
    $axios: undefined,
    setAxios: function(axios) {
        this.$axios = axios;
    },
    setStore: function(store) {
        this.$store = store;
    },
    install: function(Vue, options) {
        this.setStore(options.store);
        this.setAxios(options.axios);
        console.debug("Cadre Globals Installed");
        // console.debug(this);
        var cadreGlobals = this;

        // // 1. add global method or property
        // Vue.myGlobalMethod = function () {
        //   // something logic ...
        // }
        //
        // // 2. add a global asset
        // Vue.directive('my-directive', {
        //   bind (el, binding, vnode, oldVnode) {
        //     // something logic ...
        //   }
        //   ...
        // })
        //
        // // 3. inject some component options
        // Vue.mixin({
        //   created: function () {
        //     // something logic ...
        //   }
        //   ...
        // })
        //
        // // 4. add an instance method
        // Vue.prototype.$myMethod = function (methodOptions) {
        //   // something logic ...
        // }


        /* axios proxy so that I don't have to add the auth-token header on every single request.  DRY. */
        function axiosWithAuthToken(options) {
            return cadreGlobals.axiosProxy(options);
        }


        function changeBaseURL(baseURL) {
            try {
                cadreGlobals.$axios.defaults.baseURL = baseURL;
                console.debug("baseURL changed to: " + this.$axios.defaults.baseURL);
            } catch (err) {
                console.debug("baseURL not changed." + err.message);
            }
        }

        let debounce_timer = 0;
        function debounce(callback) {
            clearTimeout(debounce_timer);
            debounce_timer = setTimeout(callback, 100);
        }

        let cadre_global_functions = {
            axios: axiosWithAuthToken,
            cloneObject: function(o) {
                return cadreGlobals.cloneObject(o);
            },
            debounce: debounce,
            changeBaseURL: changeBaseURL,
            // startLoading: function(key) {
            //     cadreGlobals.$store.commit("startLoading", key);
            // },
            // stopLoading: function(key) {
            //     cadreGlobals.$store.commit("stopLoading", key);
            // }
        };

        Vue.prototype.$cadre = (function() {
            return cadre_global_functions;
        })();
        Vue.$cadre = Vue.prototype.$cadre;

        Vue.prototype.$cadreConfig = (function() {
            return $config;
        })();

        Vue.$cadreConfig = Vue.prototype.$cadreConfig;

    },
    cloneObject: function(object) {
        if (object) {
            try {
                return JSON.parse(JSON.stringify(object));
            } catch (e) {
                console.error("Could not clone object.", e);
            }
        }
        return object;
    },

    axiosProxy: function(options) {
        if (!this.$store || !this.$store.getters || !this.$store.getters["user/authToken"]) {
            // throw new Error("No auth token found");
            console.info("No auth token found.");
        }
        options.headers = options.headers || {};
        options.headers["auth-token"] = this.$store.getters['user/authToken'];
        var cadreGlobals = this;
        if ($config.show_log) {
            // cadreGlobals.$store.commit("addToDebugLog", options);
            console.info(options);
        }

        // console.log(options.url);
        return new Promise(function(resolve, reject) {
            cadreGlobals.$axios(options).then(
                function(response) {
                    if ($config.show_log) {
                        console.info(response);
                    }
                    // if (response.headers["x-cadre-auth-token"]) {
                    //     cadreGlobals.$store.commit("setToken", response.headers["x-cadre-auth-token"]);
                    // }

                    resolve(response);
                },
                function(error) {
                    if ($config.show_log) {
                        console.error(error);
                    }
                    if (error && !error.response && error.request && Object.keys(error.request).length === 0) {
                        console.info("cadre could not connect to server.", error.message);
                        // console.debug(`cadre could not connect to server. Error: ${error.message} - (${cadreGlobals.$axios.defaults.baseURL}) - ${JSON.stringify(options, null, 1)}`);
                    } else if (error && error.response && error.response.status && error.response.status === 401) {
                        console.debug("Unauthorized");
                        // cadreGlobals.$store.commit("invalidateToken");
                    }


                    // console.debug(error);
                    reject(error);
                }
            );
        });
    }
};
