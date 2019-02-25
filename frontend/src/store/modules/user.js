import Globals from "../../CadreGlobalsPlugin";
import axios from "axios";
import Vue from "vue";

export default {
    namespaced: true,
    state: {
        isLoggedIn: !!localStorage.getItem("token"),
        pending: false,
        auth_token: null,
        token_is_valid: !!localStorage.getItem("token")
    },
    getters: {
        tokenValid: function(state) {
            return state.token_is_valid;
        },
        isLoggedIn: function(state) {
            return state.isLoggedIn;
        },
        pending: function(state) {
            return state.pending;
        },

        authToken: function(state) {
            return state.auth_token;
        }
    },
    mutations: {
        login: function(state) {
            state.pending = true;
        },
        login_success: function(state, payload) {
            state.isLoggedIn = true;
            state.pending = false;
            state.auth_token = payload.token;
            state.token_is_valid = true;

            localStorage.setItem("token", state.auth_token);
        },
        login_failure: function(state, payload) {
            state.pending = false;
        },
        logout: function(state) {
            state.isLoggedIn = false;
            state.auth_token = null;
            localStorage.removeItem("token");
        },
        setToken: function(state, token) {
            state.auth_token = token;
            localStorage.removeItem("token");
            localStorage.setItem("token", token);
            // console.debug("tokenSet");
        },
        initializeToken: function(state) {
            state.auth_token = localStorage.getItem("token");
        },
        invalidateToken: function(state) {
            state.token_is_valid = false;
        }
    },
    actions: {
        validateToken: function(state, token) {
            //We must validate the token every time. If the token is not valid, it just gets removed.
            return new Promise(function(resolve, reject) {
                let validate_prom = axios({
                    url: Vue.$cadreConfig.authentication_host + "/authenticate-token",
                    headers: {
                        //if token is passed, use that, otherwise use the one already stored
                        "auth-token": token || state.getters.auth_token
                    }
                });

                validate_prom.then(
                    result => {
                        //if passed, set the token
                        state.commit("setToken", token);
                        console.info("Token is valid");
                        resolve(result);
                    },
                    error => {
                        //if failed, unset the token
                        state.commit("logout");
                        console.error("Token not valid");
                        reject(error);
                    }
                );
            });
        }
    }
};
