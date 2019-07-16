import Vue from "vue";

const TEST_RAC_PACKAGES = [
    {
        package_id: "package_1",
        name: "package 1",
        author: "author 1",
        created_date: "2019-07-16 10:51:26",
        tools: ["tool 1"],
        input_files: ["/dataset.csv"],
        output_files: ["/new_dataset.csv"]
    },
    {
        package_id: "package_2",
        name: "package 2",
        author: "author 2",
        created_date: "2019-07-16 10:51:26",
        tools: ["tool 2"],
        input_files: ["/dataset.csv"],
        output_files: ["/new_dataset.csv"]
    },
    {
        package_id: "package_3",
        name: "package 3",
        author: "author 3",
        created_date: "2019-07-16 10:51:26",
        tools: ["tool 3"],
        input_files: ["/dataset.csv"],
        output_files: ["/new_dataset.csv"]
    }
];

export default {
    namespaced: true,
    state: {
        search_query: "",
        packages: []
    },
    getters: {
        packages: function(state) {
            return state.packages;
        }
    },
    mutations: {
        setPackages: function(state, packages) {
            Vue.set(state, "packages", []);
            for (let racpackage of packages) {
                state.packages.push(racpackage);
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
        getPackages: function({ commit }) {
            return new Promise((resolve, reject) => {

                //FOR TESTING
                commit("setPackages", TEST_RAC_PACKAGES);
                resolve({status: 200, data: {message: "Test Packages"}});
                return true;

                let axios_prom = Vue.$cadre.axios({
                    url: "/packages/get-packages",
                    data: {
                        limit: 50,
                        page: 1,
                        order: 'name',
                        search: ''
                    }
                });
                axios_prom.then(response => {
                    let packages = response.data.packages;
                    commit("setPackages", packages);
                    resolve(response);
                }, error => {
                    reject(error);
                });
            });
        },
        runPackage: function({}, { package_id, input_files, output_filename }) {
            return new Promise((resolve, reject) => {
                let axios_prom = Vue.$cadre.axios({
                    url: "/packages/run-package",
                    method: "POST",
                    data: {
                        package_id: package_id,
                        output_filename: output_filename || ""
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
        }
    }
};
