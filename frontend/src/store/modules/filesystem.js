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

        /**
         * Updates the file structure and flat file structure
         * @param {array} payload - expects an array filled with pieces of file structure
         * */
        updateFileStructure: function(state, payload) {
            /* TODO: empty folder if a folder is refreshed. */

            let list = state.flat_file_structure;

            // join the existing structure with the new structure
            list = list.concat(payload);
            list.sort((a, b) => {
                if (a.path > b.path) {
                    return 1;
                } else if (a.path < b.path) {
                    return -1;
                } else {
                    return 0;
                }
            });

            //remove duplicates
            let seen_paths = [];
            list = list.filter(item => {
                if (seen_paths.indexOf(item.path) < 0) {
                    seen_paths.push(item.path);
                    return true;
                } else {
                    return false;
                }
            });

            //construct tree structure

            //start empty map
            let map = {
                "": {
                    path: "/",
                    type: "folder",
                    children: []
                }
            };

            //put all folders into map and add children array
            for (let i in list) {
                let item = list[i];
                if (item.type == "file") {
                    continue;
                }
                item.children = [];
                map[item.path] = item;
            }

            //build the tree structure
            for (let i in list) {
                let item = list[i];

                //parent folder will be the key in the map
                let parent_folder = item.path.split("/");
                parent_folder.pop();
                parent_folder = parent_folder.join("/");

                //if a file, just add to folder
                if (item.type == "file") {
                    map[parent_folder].children.push(item);
                } else if (item.type == "folder") {
                    //if folder, add the map item to the parent folder, preserving the folder's chidlren
                    map[parent_folder].children.push(map[item.path]);
                }
            }

            //update the structure
            state.flat_file_structure = list;
            state.file_structure = [map[""]];
        }
    },
    actions: {

        /**
         * Should hit the rac API and return the children of a folder
         */
        getFiles: function({ commit }, payload) {
            // console.debug(payload);
            let path = payload && payload.path || "";
            let level = 1;

            return new Promise((resolve, reject) => {
                let prom = Vue.$cadre.axios({
                    url: Vue.$cadreConfig.rac_api_prefix + "/user-files",
                    method: "GET",
                    params: {
                        path: path,
                        level: level
                    }
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
