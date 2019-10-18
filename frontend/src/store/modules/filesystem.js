import Globals from "../../CadreGlobalsPlugin";
import axios from "axios";
import Vue from "vue";

export default {
    namespaced: true,
    state: {
        root: "",
        file_structure: [],
        flat_file_structure: []
    },
    getters: {
        getRoot: function(state) {
            return state.root;
        }
    },
    mutations: {
        setRoot: function(state, root) {
            state.root = root;
        },
        updateFileStructure: function(state, payload) {
            state.flat_file_structure = state.flat_file_structure.concat(payload);
            state.flat_file_structure.sort((a, b) => {
                if (a.path > b.path) {
                    return 1;
                } else if (a.path < b.path) {
                    return -1;
                } else {
                    return 0;
                }
            });

            let seen_paths = [];
            state.flat_file_structure = state.flat_file_structure.filter(item => {
                if (seen_paths.indexOf(item.path) < 0) {
                    seen_paths.push(item.path);
                    return true;
                } else {
                    return false;
                }
            });

            let list = state.flat_file_structure;

            let map = {
                "": {
                    path: "/",
                    type: "folder",
                    children: []
                }
            };

            for (let i in list) {
                let item = list[i];
                if (item.type == "file") {
                    continue;
                }
                // item.parent_folder = item.path.split("/"); //.pop();
                // item.parent_folder.pop();
                // item.parent_folder = item.parent_folder.join("/");
                item.children = [];
                map[item.path] = item;
            }
            // console.debug(map)
            for (let i in list) {
                let item = list[i];

                let parent_folder = item.path.split("/"); //.pop();
                parent_folder.pop();
                parent_folder = parent_folder.join("/");

                if (item.type == "file") {
                    map[parent_folder].children.push(item);
                } else if (item.type == "folder") {
                    map[parent_folder].children.push(map[item.path]);
                }
            }

            return (state.file_structure = [map[""]]);
        }
    },
    actions: {
        getFiles: function({ commit }) {
            // return 'test';
            return new Promise((resolve, reject) => {
                // let prom = axios.get("/");

                // let prom = axios({
                //     url: "/",
                //     method: "GET"
                // });
                let prom = Vue.$cadre.axios({
                    url: "/rac-api/user-files",
                    method: "GET"
                });

                prom.then(
                    resp => {
                        commit("updateFileStructure", resp.data);
                        resolve(resp);
                    },
                    err => {
                        reject(err);
                    }
                );
            });
        }
    }
};
