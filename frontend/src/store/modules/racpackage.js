import Vue from "vue";

export default {
    namespaced: true,
    state: {
        search_query: "",
        packages: [],
        tools: {},
        my_jobs: []
    },
    getters: {
        packages: function(state) {
            return state.packages;
        },
        tools: function(state) {
            return state.tools;
        },
        my_jobs: function(state) {
            return state.my_jobs;
        }
    },
    mutations: {
        setPackages: function(state, packages) {
            Vue.set(state, "packages", []);
            for (let racpackage of packages) {
                state.packages.push(racpackage);
            }
        },
        setTools: function(state, tools) {
            Vue.set(state, "tools", {});
            for (let tool of tools) {
                // state.tools.push(tool);
                Vue.set(state.tools, tool.tool_id, tool);
            }
        },
        setMyJobs: function(state, jobs) {
            Vue.set(state, "my_jobs", []);
            for (let job of jobs) {
                state.my_jobs.push(job);
                // Vue.set(state.my_jobs, tool.tool_id, tool);
            }
        }
    },
//     //    ###     ######  ######## ####  #######  ##    ##  ######
//     //   ## ##   ##    ##    ##     ##  ##     ## ###   ## ##    ##
//     //  ##   ##  ##          ##     ##  ##     ## ####  ## ##
//     // ##     ## ##          ##     ##  ##     ## ## ## ##  ######
//     // ######### ##          ##     ##  ##     ## ##  ####       ##
//     // ##     ## ##    ##    ##     ##  ##     ## ##   ### ##    ##
//     // ##     ##  ######     ##    ####  #######  ##    ##  ######
    actions: {
        getTools: function({ commit }) {
            return new Promise((resolve, reject) => {
                //FOR TESTING
                // console.debug(TEST_RAC_TOOLS);
                commit("setTools", TEST_RAC_TOOLS);
                resolve({ status: 200, data: { message: "Test Tools" } });
                return true;

                let axios_prom = Vue.$cadre.axios({
                    url: "/rac-api/packages/get-tools",
                    data: {
                        // limit: 50,
                        // page: 0,
                        // order: 'name',
                        // search: ''
                    }
                });
                axios_prom.then(
                    response => {
                        let tools = response.data.tools;
                        commit("setTools", tools);
                        resolve(response);
                    },
                    error => {
                        reject(error);
                    }
                );
            });
        },
        getMyJobs: function({ commit }) {
            return new Promise((resolve, reject) => {
                //FOR TESTING
                commit("setMyJobs", TEST_RAC_JOBS);
                resolve({ status: 200, data: { message: "Test JOBS" } });
                return true;

                let axios_prom = Vue.$cadre.axios({
                    url: "/rac-api/packages/get-jobs",
                    data: {
                        // limit: 50,
                        // page: 0,
                        // order: 'name',
                        // search: ''
                    }
                });
                axios_prom.then(
                    response => {
                        let jobs = response.data.jobs;
                        commit("setMyJobs", jobs);
                        resolve(response);
                    },
                    error => {
                        reject(error);
                    }
                );
            });
        },
        getPackages: function({ commit }) {
            return new Promise((resolve, reject) => {
                //FOR TESTING
                // commit("setPackages", TEST_RAC_PACKAGES);
                // resolve({ status: 200, data: { message: "Test Packages" } });
                // return true;

                let axios_prom = Vue.$cadre.axios({
                    url: Vue.$cadreConfig.rac_api_prefix + "/packages/get-packages",
                    params: {
                        limit: 50,
                        page: 0,
                        order: "name",
                        search: ""
                    },
                    responseType: "json"
                });
                axios_prom.then(
                    response => {
                        let packages = response.data;
                        console.debug(response);
                        commit("setPackages", packages);
                        resolve(response);
                    },
                    error => {
                        reject(error);
                    }
                );
            });
        },
        runPackage: function(context, { package_id, input_files, output_filenames }) {
            return new Promise((resolve, reject) => {
                let axios_prom = Vue.$cadre.axios({
                    url: "/rac-api/packages/run-package",
                    method: "POST",
                    data: {
                        package_id: package_id,
                        output_filename: output_filenames || []
                    }
                });

                axios_prom.then(
                    response => {
                        resolve({
                            job_id: response.data.job_id,
                            job_status: response.data.job_status
                        });
                    },
                    error => {
                        let reject_obj = {};

                        (reject_obj.error_message = error.response.data.error_message || "Unknown error. Couldn't run package."),
                            // reject_obj.job_status = error.response.data.job_status

                            (reject_obj.http_status = error.response.status);

                        reject(reject_obj);
                    }
                );
            });
        },
        createPackage: function(context, { package_name, tool_id, input, description }) {
            return new Promise((resolve, reject) => {
                let axios_prom = Vue.$cadre.axios({
                    url: "/rac-api/packages/new-package",
                    method: "POST",
                    data: {
                        package_name: package_name,
                        tool_id: tool_id,
                        input: input,
                        description: description
                    }
                });

                axios_prom.then(
                    response => {
                        resolve({
                            package_id: response.data.package_id
                        });
                    },
                    error => {
                        let reject_obj = {};

                        reject_obj.error_message = error.response.data.error_message || "Unknown error. Couldn't create new package.";
                        reject_obj.http_status = error.response.status;

                        reject(reject_obj);
                    }
                );
            });
        }
    }
};


const TEST_RAC_TOOLS = [
    {
        tool_id: "112342211261",
        name: "tool_name1",
        author: "username",
        description: "some description",
        entrypoint: "some_script1.py",
        created_on: "2020-01-07 14:15:00",
    },
    {
        tool_id: "112342211262",
        name: "tool_name2",
        author: "username",
        description: "some description",
        entrypoint: "some_script2.py",
        created_on: "2020-01-07 14:15:00",
    }
    
]
const TEST_RAC_JOBS = {}
