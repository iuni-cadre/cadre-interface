import Globals from "../../CadreGlobalsPlugin";
import axios from "axios";
import Vue from "vue";

export default {
    namespaced: true,
    state: {
        root: ""
    },
    getters: {
        getRoot: function(state) {
            return state.root;
        }
    },
    mutations: {
        setRoot: function(state, root) {
            state.root = root;
        }
    },
    actions: {
        getFiles: function() {
            // return 'test';
            return new Promise((resolve, reject) => {
                reject({error: "balls"});
            });
        }
    }
};
