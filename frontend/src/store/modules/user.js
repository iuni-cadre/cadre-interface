import Globals from "../../CadreGlobalsPlugin";
import axios from "axios";
import Vue from "vue";

export default {
    namespaced: true,
    state: {
        isLoggedIn: !!localStorage.getItem("token"),
        pending: false,
        auth_token: null,
        j_token: null,
        token_is_valid: !!localStorage.getItem("token"),
        username: "",
        heartbeat_timer: 0,
        heartbeat_interval: 30000
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
        },
        jToken: function(state) {
            return state.j_token;
        },
        username: function(state) {
            return state.username;
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
            state.username = null;
            localStorage.removeItem("token");
            localStorage.removeItem("username");
        },
        setToken: function(state, token) {
            state.auth_token = token;
            localStorage.removeItem("token");
            localStorage.setItem("token", token);
            // console.debug("tokenSet");
        },

        setJToken: function(state, j_token) {
            state.j_token = j_token;
            localStorage.removeItem("j_token");
            localStorage.setItem("j_token", j_token);
            // console.debug("tokenSet");
        },
        setUsername: function(state, username) {
            state.username = username;
            localStorage.removeItem("username");
            localStorage.setItem("username", username);
        },
        initializeToken: function(state) {
            state.auth_token = localStorage.getItem("token");
            state.username = localStorage.getItem("username");
        },
        invalidateToken: function(state) {
            state.token_is_valid = false;
        }
    },
    actions: {
        beatHeart: function({ state, dispatch, getters, commit }) {
            clearTimeout(state.heartbeat_timer);
            state.heartbeat_timer = setTimeout(() => {
                // console.debug("Beat");
                let username = getters.username;
                let token = getters.authToken;
                let validate_prom = Globals.authAxios({
                    url: "/authenticate-token",
                    method: "POST",
                    data: {
                        username: username
                    },
                });

                validate_prom.then(
                    response => {
                        dispatch("beatHeart");
                    },
                    error => {
                        console.warn(error);

                        if(Vue.$cadreConfig.force_validation !== false)
                        {
                            commit("logout");
                        }
                    }
                );
            }, state.heartbeat_interval);
        },
        validateToken: function(context, payload) {
            //We must validate the token every time. If the token is not valid, it just gets removed.
            let username = (payload && payload.username) || context.getters.username;
            let token = (payload && payload.token) || context.getters.authToken;
            let j_token = (payload && payload.j_token) || context.getters.jToken;
            return new Promise(function(resolve, reject) {
                // console.debug(context)

                // console.debug(username, token);
                let validate_prom = Globals.authAxios({
                    url: "/authenticate-token", //?username=" + (username || state.getters.username),
                    method: "POST",
                    data: {
                        username: username
                    },
                    headers: {
                        "auth-token": token,
                        "auth-username": username
                    }
                });

                if (Vue.$cadreConfig.force_validation === false) {
                    context.commit("setToken", "fake");
                    context.commit("setUsername", "fake");
                    console.info("Token is valid");
                    resolve({ msg: "Fake Validation" });
                } else {
                    validate_prom.then(
                        result => {
                            //if passed, set the token
                            context.commit("setToken", token);
                            context.commit("setJToken", j_token);
                            context.commit("setUsername", username);
                            console.info("Token is valid");
                            resolve(result);
                        },
                        error => {
                            //if failed, unset the token
                            context.commit("logout");
                            console.error("Token not valid");
                            reject(error);
                        }
                    );
                }
            });
        }
    }
};
