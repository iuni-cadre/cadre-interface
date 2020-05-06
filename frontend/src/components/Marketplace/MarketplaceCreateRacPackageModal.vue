<template>
    <div>
        <modal v-if="show_modal"
               :close-button-label="'Cancel'"
               @close="$emit('close')">
            <div class="">
                <h4>Create New Package</h4>

                <div class="form-group">
                    <label>Package Name</label>
                    <input type="text"
                           placeholder="New Package Name"
                           class="form-control"
                           v-model="new_package_name" />
                </div>

                <div class="form-group">
                    <label>Input File</label>
                    <select class="form-control"
                            v-model="new_package_input_file">
                        <option value=""
                                disabled>Select a job</option>
                        <option v-for="job_id in input_job_ids"
                                :key="job_id"
                                v-text="job_id"
                                :value="job_id"></option>
                    </select>
                </div>

                <div class="form-group">
                    <label>Tool to Run</label>
                    <select class="form-control"
                            v-model="new_package_tool">
                        <option value=""
                                disabled>Select a tool</option>
                        <option v-for="tool in tools"
                                :key="tool.tool_id"
                                v-text="tool.name"
                                :value="tool.tool_id"></option>
                    </select>
                </div>

                <div class="form-group">
                    <label>Package Description</label>
                    <textarea type="text"
                              placeholder="Uses input files and generates output files"
                              class="form-control"
                              v-model="new_package_description"></textarea>
                </div>

                <div class="col">
                    <button class=" float-right btn-lg btn btn-primary"
                            @click="createPackage()">Create Package</button>
                </div>

            </div>

        </modal>
        <modal v-if="results"
               @close="results = undefined"
               modal-style="success"
               modal-type="success">

            {{results}}
        </modal>
        <modal v-if="error"
               @close="error = undefined"
               modal-style="danger"
               modal-type="error">

            {{error}}
        </modal>
    </div>

</template>

<script>
import Modal from "@/components/Common/CommonModal.vue";
export default {
    data: function() {
        return {
            results: undefined,
            error: undefined,

            new_package_name: "",
            new_package_tool: "",
            new_package_input_file: "",
            new_package_description: ""
        };
    },
    computed: {
        show_modal: function() {
            return this.showModal;
        },
        tools: function() {
            return this.$store.getters["racpackage/tools"];
        },
        input_job_ids: function() {
            return this.$store.getters["racpackage/my_jobs"].map(job => {
                return job.job_id;
            });
            // let my_files = this.$store.getters["racpackage/myfiles"];
            // let package_files = [];
            // for( let p of this.$store.getters["racpackage/packages"]){
            //     package_files.concat(p.input_paths);
            // }
            // return my_files.concat(package_files);
        }
    },
    props: {
        existingPackage: Object,
        showModal: Boolean,
        defaultInput: String,
        defaultToolId: String
    },
    methods: {
        // runPackage: function() {
        //     this.$emit("startLoading", { key: "running_package" });
        //     let running_promise = this.$store.dispatch(
        //         "racpackage/runPackage",
        //         {
        //             package_id: this.racpackage.package_id,
        //             output_filename: this.output_filename
        //         }
        //     );
        //     running_promise
        //         .then(this.runSuccess, this.runFail)
        //         .finally(this.runFinally);
        // },
        // runSuccess: function(response) {
        //     this.results = {
        //         job_id: response.job_id,
        //         success_message: "Package is running."
        //     };
        //     console.debug(this.results);
        //     this.output_filename = "";
        //     this.show_run_modal = null;
        // },
        // runFail: function(error) {
        //     console.debug(error);
        //     this.error = {
        //         error_message: error.error_message
        //     };
        // },
        // runFinally: function() {
        //     this.$emit("stopLoading", { key: "running_package" });
        // }
        createPackage: function() {
            this.$store.commit("loading/addKey", { key: "create_package", message: "" });
            let create_prom = this.$store.dispatch("racpackage/createPackage", {
                package_name: this.new_package_name,
                tool_id: this.new_package_tool,
                input: this.new_package_input_file,
                description: this.new_package_description
            });
            create_prom
                .then(
                    response => {},
                    error => {
                        this.error = error.error_message;
                    }
                )
                .finally(() => {
                    //stop loading
                    this.$store.commit("loading/removeKey", { key: "create_package" });
                });
        },
        refreshMyJobs: function() {
            // this.$emit("startLoading", { key: "get_jobs", message: "" });
            // let get_jobs_prom = this.$store.dispatch("racpackage/getMyJobs");
            // Promise.all([get_jobs_prom]).finally(() => {
            //     //stop loading
            //     this.$emit("stopLoading", { key: "get_jobs" });
            // });
        }
    },
    watch: {
        show_modal: function(o, n) {
            if (this.show_modal) {
                this.refreshMyJobs();
            }
        },
        defaultJobId: function() {
            this.new_package_input_file = this.defaultInput;
        },
        defaultToolId: function() {
            this.new_package_tool = this.defaultToolId;
        }
    },
    components: {
        Modal
    },
    mounted: function() {
        this.refreshMyJobs();
        this.new_package_input_file = this.defaultInput;
        this.new_package_tool = this.defaultToolId;
    }
};
</script>

<style>
</style>
