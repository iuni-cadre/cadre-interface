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
    //    ###     ######  ######## ####  #######  ##    ##  ######
    //   ## ##   ##    ##    ##     ##  ##     ## ###   ## ##    ##
    //  ##   ##  ##          ##     ##  ##     ## ####  ## ##
    // ##     ## ##          ##     ##  ##     ## ## ## ##  ######
    // ######### ##          ##     ##  ##     ## ##  ####       ##
    // ##     ## ##    ##    ##     ##  ##     ## ##   ### ##    ##
    // ##     ##  ######     ##    ####  #######  ##    ##  ######
    actions: {
        getTools: function({ commit }) {
            return new Promise((resolve, reject) => {
                //FOR TESTING
                commit("setTools", TEST_RAC_TOOLS);
                resolve({ status: 200, data: { message: "Test Tools" } });
                return true;

                let axios_prom = Vue.$cadre.axios({
                    url: "/rac-api/packages/get-tools",
                    data: {
                        // limit: 50,
                        // page: 1,
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
                        // page: 1,
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
                commit("setPackages", TEST_RAC_PACKAGES);
                resolve({ status: 200, data: { message: "Test Packages" } });
                return true;

                let axios_prom = Vue.$cadre.axios({
                    url: "/rac-api/packages/get-packages",
                    data: {
                        limit: 50,
                        page: 1,
                        order: "name",
                        search: ""
                    }
                });
                axios_prom.then(
                    response => {
                        let packages = response.data.packages;
                        commit("setPackages", packages);
                        resolve(response);
                    },
                    error => {
                        reject(error);
                    }
                );
            });
        },
        runPackage: function({}, { package_id, input_files, output_filenames }) {
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
        createPackage: function({}, { package_name, tool_id, input, description }) {
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

const TEST_RAC_PACKAGES = [
    {
        package_id: "234221136",
        name: "ISSI Data Package",
        author: "CADRE Team",
        created_date: "2019-08-26 16:32:48",
        tools: ["11234221128"],
        input_files: ["data.tar"]
        // output_files: 2
    },
    {
        package_id: "234221132",
        name: "Line Count Package",
        author: "CADRE Team",
        created_date: "2019-07-16 10:51:26",
        tools: ["11234221124"],
        input_files: ["/dataset1.txt", "/dataset2.txt"]
        // output_files: 2
    },

    {
        package_id: "234221133",
        name: "Query2 Xnet Package",
        author: "CADRE Team",
        created_date: "2019-08-22 13:37:15",
        tools: ["11234221125"],
        input_files: ["/dataset.csv", "/dataset_edges.csv"]
        // output_files: 1 // extension .xnet
    },

    {
        package_id: "234221134",
        name: "Xnet Communities Package",
        author: "CADRE Team",
        created_date: "2019-08-22 13:37:15",
        tools: ["11234221126"],
        input_files: ["results.xnet"]
    },
    {
        package_id: "234221135",
        name: "Xnet Word Cloud",
        author: "CADRE Team",
        created_date: "2019-08-22 13:37:15",
        tools: ["11234221127"],
        input_files: ["results.xnet"]
    },



    // {
    //     package_id: "234221134",
    //     name: "Demo Download Package",
    //     author: "CADRE Team",
    //     created_date: "2019-08-22 15:04:43",
    //     tools: ["11234221126"],
    //     input_files: []
    //     // output_files: 1 // extension .xnet
    // }
    // {
    //     package_id: "package_2",
    //     name: "package 2",
    //     author: "author 2",
    //     created_date: "2019-07-16 10:51:26",
    //     tools: ["tool_2"],
    //     input_files: ["/dataset.csv"],
    //     output_files: ["/new_dataset.csv"]
    // },
    // {
    //     package_id: "package_3",
    //     name: "package 3",
    //     author: "author 3",
    //     created_date: "2019-07-16 10:51:26",
    //     tools: ["tool_3"],
    //     input_files: ["/dataset.csv"],
    //     output_files: ["/new_dataset.csv"]
    // }
];

const TEST_RAC_TOOLS = [
    {
        tool_id: "11234221124",
        name: "Line Count",
        author: "CADRE Team",
        description: "Counts lines in a file",
        output_files: ["file_1.csv", "file_2.csv"]
    },
    {
        tool_id: "11234221125",
        name: "query2_xnet",
        author: "CADRE Team",
        description: "Sends query to xnet package.",
        output_files: ["result.xnet"]
    },
    {
        tool_id: "11234221126",
        name: "xnet2_communities",
        author: "CADRE Team",
        description: "Sends query to xnet package.",
        output_files: ["result.xnet"]
    },
    {
        tool_id: "11234221127",
        name: "xnet2_wordcloud",
        author: "CADRE Team",
        description: "Sends query to xnet package.",
        output_files: ["word_cloud.pdf"]
    },
    {
        tool_id: "11234221128",
        name: "issi_data_package",
        author: "CADRE Team",
        description: "Get my data ready for the demo",
        output_files: ["issi_tutorial"]
    },
    // {
    //     tool_id: "11234221126",
    //     name: "Xiaoran's Demo",
    //     author: "CADRE Team",
    //     description: "Downloads demo files to user workspace.",
    //     output_files: ["demo_folder"]
    // },


    // {
    //     tool_id: "tool_2",
    //     name: "Word Count",
    //     author: "CADRE Team",
    //     description: "Counts words in a file"
    // },
    // {
    //     tool_id: "tool_3",
    //     name: "Graph",
    //     author: "CADRE Team",
    //     description: "Generates a graph"
    // }
];

const TEST_RAC_JOBS = [
    {
        job_id: "job1"
    },
    {
        job_id: "job2"
    },
    {
        job_id: "job3"
    },
    {
        job_id: "job4"
    }
];
