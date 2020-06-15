import Globals from "../../CadreGlobalsPlugin";
import axios from "axios";
import Vue from "vue";

import CryptoJS from "crypto-js";

const TEST_USER = {
    username: "test-user",
    roles: ["wos_gold"],
    //roles: [],
    token: "fake_token",
    user_id: 1000,
    cognito_groups: ["wos_gold"]
};

const HEARTBEAT_INTERVAL = 60000;

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
        roles: [],
        user_id: null,
        cognito_groups: [],
    },
    getters: {
        tokenValid: function (state) {
            return state.token_is_valid;
        },
        isLoggedIn: function (state) {
            return state.isLoggedIn;
        },
        pending: function (state) {
            return state.pending;
        },

        authToken: function (state) {
            return state.auth_token;
        },
        jToken: function (state) {
            return state.j_token;
        },
        username: function (state) {
            return state.username;
        },
        decodedUsername: function (state) {
            return Globals.base32decode(state.username);
        },
        roles: function (state) {
            return state.roles;
        },
        cognito_groups: function (state) {
            return state.roles;
        }
    },
    mutations: {
        login: function (state) {
            state.pending = true;
        },
        login_success: function (state, payload) {
            state.isLoggedIn = true;
            state.pending = false;
            state.auth_token = payload.token;
            state.token_is_valid = true;


            localStorage.setItem("token", state.auth_token);
        },
        login_failure: function (state, payload) {
            state.pending = false;
        },
        logout: function (state) {
            state.isLoggedIn = false;
            state.auth_token = null;
            state.username = null;
            state.user_id = null;
            Vue.set(state, "roles", []);
            Vue.set(state, "cognito_groups", []);
            localStorage.removeItem("token");
            localStorage.removeItem("username");
            localStorage.removeItem("roles");
            localStorage.removeItem("user_id");
            localStorage.removeItem("cognito_groups");
        },
        setToken: function (state, token) {
            state.auth_token = token;
            localStorage.removeItem("token");
            localStorage.setItem("token", token);
            // console.debug("tokenSet");
        },

        setJToken: function (state, j_token) {
            state.j_token = j_token;
            localStorage.removeItem("j_token");
            localStorage.setItem("j_token", j_token);
            // console.debug("tokenSet");
        },
        setUsername: function (state, username) {
            state.username = username;
            localStorage.removeItem("username");
            localStorage.setItem("username", username);
        },
        setRoles: function (state, roles) {
            Vue.set(state, "roles", roles);
            localStorage.removeItem("roles");
            localStorage.setItem("roles", roles);
        },
        setCognitoGroups: function (state, cognito_groups) {
            Vue.set(state, "cognito_groups", cognito_groups);
            localStorage.removeItem("cognito_groups");
            localStorage.setItem("cognito_groups", cognito_groups);
        },
        initializeToken: function (state) {
            state.auth_token = localStorage.getItem("token");
            state.username = localStorage.getItem("username");
            state.roles = localStorage.getItem("roles");
            state.cognito_groups = localStorage.getItem("cognito_groups");
        },
        invalidateToken: function (state) {
            state.token_is_valid = false;
        },
        setUserId: function (state, user_id) {
            state.user_id = user_id;
            localStorage.removeItem("user_id");
            localStorage.setItem("user_id", user_id);
        }
    },
    actions: {
        beatHeart: function ({ state, dispatch, getters, commit }) {
            clearTimeout(state.heartbeat_timer);
            state.heartbeat_timer = setTimeout(() => {
                // console.debug("Beat");
                let username = getters.username;
                let token = getters.authToken;

                if (Vue.$cadreConfig.force_validation !== false) {
                    let validate_prom = Globals.authAxios({
                        url: "/authenticate-token",
                        method: "POST",
                        data: {
                            username: username
                        }
                    });

                    validate_prom.then(
                        response => {
                            dispatch("beatHeart");

                            if (response.roles) {
                                commit("setRoles", response.roles)
                            }
                            if (response.user_id) {
                                commit("setUserId", response.user_id);
                            }
                            if (response.cognito_groups) {
                                commit("setCognitoGroups", response.cognito_groups);
                            }
                        },
                        error => {
                            console.warn(error);

                            // if (Vue.$cadreConfig.force_validation !== false) {
                            commit("logout");
                            // }
                        }
                    );
                }
                else {
                    console.log("fake validation");
                }
            }, HEARTBEAT_INTERVAL);
        },
        logout: function ({ getters, commit }, payload) {
            let username = getters.username;
            let token = getters.authToken;
            return new Promise((resolve, reject) => {
                let validate_prom = Globals.authAxios({
                    url: "/logout",
                    method: "POST",
                    data: {
                        username: username
                    },
                    headers: {
                        "auth-token": token,
                        "auth-username": username
                    }
                });

                validate_prom.then(
                    response => {
                        // dispatch("beatHeart");
                        commit("logout");
                        resolve(response);
                    },
                    error => {
                        // console.warn(error);
                        // if(Vue.$cadreConfig.force_validation !== false)
                        // {
                        //     commit("logout");
                        // }
                        reject(error);
                    }
                );
            });
        },
        validateToken: function (context, payload) {
            //We must validate the token every time. If the token is not valid, it just gets removed.
            let username = (payload && payload.username) || context.getters.username;
            let token = (payload && payload.token) || context.getters.authToken;
            let j_token = (payload && payload.j_token) || context.getters.jToken;
            return new Promise(function (resolve, reject) {
                // console.debug(context)

                if (Vue.$cadreConfig.force_validation === false) {
                    context.commit("setToken", TEST_USER.token);
                    context.commit("setUsername", Globals.base32encode(TEST_USER.username));
                    context.commit("setRoles", TEST_USER.roles);
                    context.commit("setUserId", TEST_USER.user_id);
                    context.commit("setCognitoGroups", TEST_USER.cognito_groups);
                    console.info("Fake user token is valid");
                    resolve({ msg: "Fake Validation" });
                } else {
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

                    validate_prom.then(
                        result => {
                            //if passed, set the token
                            context.commit("setToken", token);
                            context.commit("setJToken", j_token);
                            context.commit("setUsername", username);
                            context.commit("setRoles", result.data.roles);
                            context.commit("setUserId", result.data.user_id);
                            context.commit("setCognitoGroups", result.data.cognito_groups)
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
