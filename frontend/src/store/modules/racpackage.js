import Vue from "vue";

export default {
    namespaced: true,
    state: {},
    getters: {},
    mutations: {},
    actions: {
        runPackage: function({}, {package_id, input_files, output_filename})
        {
            return new Promise((resolve, reject)=>{
                let axios_prom = Vue.$cadre.axios({
                    url: "/run-package",
                    method: "POST",
                    data: {
                        package_id: package_id,
                        output_filename: output_filename || ""
                    }
                });

                axios_prom.then((response)=>{
                    resolve({
                        job_id: response.data.job_id,
                        job_status: response.data.job_status
                    })
                }, (error)=>{
                    let reject_obj = {
                        error_message: error.response.data.error_message || "Unknown error. Couldn't run package.",
                        job_status: error.response.data.job_status
                    };

                    reject(reject_obj);
                });
            })
        }
    }
};
