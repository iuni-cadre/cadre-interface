<template>
    <div style="width: 100%;">
        <form @submit.stop.prevent="submitForm">
            <div class="form-group">
                <label>Environment</label>
                <div class="form-control">Python</div>
            </div>
            <div class="form-group">
                <label>Name</label>
                <input
                    v-model="data_to_send.name"
                    placeholder="e.g. My Tool"
                    type="text"
                    class="form-control"
                />
            </div>
            <div class="form-group">
                <label>Description</label>
                <textarea
                    v-model="data_to_send.description"
                    placeholder="e.g. My Tool transforms the given data and returns 2 files."
                    class="form-control"
                ></textarea>
            </div>
            <div class="form-group">
                <label>Script Files</label>
                <div class="form-control file-browser-control">
                    <file-browser v-model="data_to_send.file_paths"></file-browser>
                </div>
            </div>
            <div class="form-group">
                <label>Entrypoint File</label>
                <!-- <input
                    v-model="data_to_send.entrypoint"
                    type="text"
                    class="form-control"
                    placeholder="e.g. /directory/start.py"
                />-->
                <select
                    class="form-control"
                    v-model="data_to_send.entrypoint"
                >
                    <option
                        value
                        disabled
                    >Choose an entrypoint file</option>
                    <option
                        v-for="path in entrypoint_options"
                        :key="path"
                        v-text="path"
                        :value="path"
                    ></option>
                </select>
            </div>
            <div class="form-group">
                <label>Installation Commands</label>
                <small class="ml-1 text-muted">(optional)</small>
                <textarea
                    v-model="data_to_send.install_commands"
                    class="form-control"
                    placeholder="e.g. pip install -r tool_dir/requirements.txt"
                ></textarea>
            </div>
            <div class="form-group">
                <button class="btn btn-primary">Create New Tool</button>
            </div>
            <!-- {{data_to_send}} -->
        </form>
        <modal
            v-if="error_message.length > 0"
            @close="error_message=[]"
            modalStyle="danger"
        >
            <div>
                <p>There was a problem with your submission.</p>
                <ul>
                    <li
                        v-for="(message, index) in error_message"
                        :key="`error_message_${index}`"
                        v-text="message"
                    ></li>
                </ul>
            </div>
        </modal>
        <modal
            v-if="success"
            @close="closeSuccessModal"
            modalStyle="success"
        >
            <div>
                <p>Your tool is being created.</p>
                <p>You can check on its status on the Job Status page:</p>
                <p>
                    <router-link :to="{name: 'jobs-list'}">View Jobs</router-link>
                </p>
            </div>
        </modal>
    </div>
</template>

<script>
import FileBrowser from "../../components/Filebrowser/FilebrowserMain";
import Modal from "../../components/Common/CommonModal";
export default {
    data: function() {
        return {
            data_to_send: {
                name: "",
                install_commands: "",
                description: "",
                file_paths: [],
                entrypoint: "",
                environment: ""
            },
            new_tool_endpoint: this.$cadreConfig.rac_api_prefix + "/tools/new",
            error_message: [],
            success: null
        };
    },
    computed: {
        entrypoint_options: function() {
            return this.data_to_send.file_paths.filter(path => {
                if (path.slice(-3) == ".py") {
                    return true;
                } else {
                    return false;
                }
            });
        }
    },
    components: {
        FileBrowser,
        Modal
    },
    methods: {
        submitForm: function() {
            this.$emit("startLoading", {
                key: "newTool",
                message: "Creating new tool"
            });
            let is_valid = this.validateForm();
            // console.debug(this.data_to_send);
            if (!is_valid) {
                this.$emit("stopLoading", { key: "newTool" });
            } else {
                // let prom = new Promise((resolve, reject) => {
                //     setTimeout(() => {
                //         console.debug("RESOLVED"), resolve();
                //     }, 5000);
                // });
                // console.debug("TEST");
                let url = this.$cadreConfig.rac_api_prefix + "/tools/new";
                let prom = this.$cadre.axios({
                    url: url,
                    method: "POST",
                    data: this.data_to_send
                });
                prom.then(
                    response => {
                        this.success = response;
                    },
                    error => {
                        let message =
                            (error &&
                                error.response &&
                                error.response.statusText) ||
                            "Unknown error.";
                        console.debug(error);
                        this.error_message.push(message);
                    }
                ).finally(() => {
                    this.$emit("stopLoading", { key: "newTool" });
                });
            }
        },
        closeSuccessModal: function() {
            this.success = null;
            this.$emit("toolCreated");
        },
        validateForm: function() {
            let errors = [];

            if (this.data_to_send.name.trim() == "") {
                errors.push("Name is a required field.");
            }
            if (this.data_to_send.description.trim() == "") {
                errors.push("Description is a required field.");
            }
            if (this.data_to_send.file_paths.length <= 0) {
                errors.push("Must include at least one file.");
            }
            if (this.data_to_send.entrypoint.trim() == "") {
                errors.push("Entrypoint is a required field.");
            } else if (
                this.data_to_send.file_paths.indexOf(
                    this.data_to_send.entrypoint
                ) < 0
            ) {
                errors.push("Chosen entrypoint file must be added explicitly.");
            }
            // console.debug(errors);
            this.$set(this, "error_message", errors);
            if (errors.length > 0) {
                // console.debug("Form not valid.");
                return false;
            } else {
                return true;
            }
        }
    },
    mounted: function() {
        this.data_to_send.environment = "python";
    }
};
</script>

<style>
.form-control.file-browser-control {
    height: 10rem;
    overflow: auto;
}
</style>