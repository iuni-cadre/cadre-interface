/* Global utility functions used by cadre */

// import $axios from "axios";
import $config from "../../conf/frontend.config.json";
// import CryptoJS from "crypto-js";

import Base32 from "hi-base32";

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
            axios: options => {
                return this.axiosProxy(options);
            },
            racAxios: options => {
                return this.racAxios(options);
            },
            qbAxios: options => {
                return this.qbAxios(options);
            },
            authAxios: options => {
                return this.authAxios(options);
            },
            cloneObject: function(o) {
                return cadreGlobals.cloneObject(o);
            },
            debounce: debounce,
            changeBaseURL: changeBaseURL
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
    // base64encode: function(rawStr) {

    //     let wordArray = CryptoJS.enc.Utf8.parse(rawStr);
    //     let base64 = CryptoJS.enc.Base64.stringify(wordArray);
    //     base64 = base64.replace(/\+/g, "-");
    //     base64 = base64.replace(/\//g, "_");
    //     return base64;
    // },
    // base64decode: function(base64) {
    //     base64 = base64.replace(/-/g, "+");
    //     base64 = base64.replace(/_/g, "/");
    //     let parsedWordArray = CryptoJS.enc.Base64.parse(base64);
    //     let parsedStr = parsedWordArray.toString(CryptoJS.enc.Utf8);
    //     return parsedStr;
    // },
    base32encode: function(string){
        return Base32.encode(string).toLowerCase();
    },
    base32decode: function(base32str)
    {
        return Base32.decode(base32str.toUpperCase());
    },
    axios: function(options) {
        return this.axiosProxy(options);
    },
    qbAxios: function(options) {
        options.url = $config.query_builder_api_prefix + options.url;
        return this.axiosProxy(options);
    },
    racAxios: function(options) {
        options.url = $config.rac_api_prefix + options.url;
        return this.axiosProxy(options);
    },
    authAxios: function(options) {
        options.url = $config.authentication_host + options.url;
        return this.axiosProxy(options);
    },
    axiosProxy: function(options) {
        options.headers = options.headers || {};

        if (!options.headers["auth-token"]) {
            if (!this.$store || !this.$store.getters || !this.$store.getters["user/authToken"]) {
                // throw new Error("No auth token found");
                console.info("No auth token found.");
            }
            options.headers["auth-token"] = options.headers["auth-token"] || this.$store.getters["user/authToken"];
        }

        if (!options.headers["auth-username"]) {
            if (!this.$store || !this.$store.getters || !this.$store.getters["user/username"]) {
                // throw new Error("No auth token found");
                console.info("No auth token found.");
            }
            options.headers["auth-username"] = options.headers["auth-username"] || this.$store.getters["user/username"];
        }

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
