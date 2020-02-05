<template>
    <div style="width: 100%;">
        <form @submit.stop.prevent="submitForm">
            <div class="form-group">
                <label>Name</label>
                <input
                    v-model="data_to_send.archive_name"
                    placeholder="e.g. My Archive"
                    type="text"
                    class="form-control"
                />
            </div>
            <div class="form-group">
                <label>Description</label>
                <small class="ml-1 text-muted">(optional)</small>
                <textarea
                    v-model="data_to_send.archive_description"
                    placeholder="e.g. Authors who publish in Science"
                    class="form-control"
                ></textarea>
            </div>
            <div class="form-group">
                <label>File to Archive</label>
                <small class="ml-1 text-muted">(Only CADRE Query Builder files can be archived)</small>
                <div class="form-control file-browser-control">
                    <file-browser
                        v-model="selected_files"
                        :select-one="true"
                        :files-only="true"
                    ></file-browser>
                </div>
            </div>
            <div class="form-group">
                <button class="btn btn-primary">Create New Archive</button>
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
                <p>Your archive has been created.</p>
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
                archive_name: "",
                archive_description: "",
                file_path: ""
            },
            selected_files: [],
            new_archive_endpoint:
                this.$cadreConfig.rac_api_prefix + "/archive-user-file",
            error_message: [],
            success: null
        };
    },
    props: {
        defaultName: {type: String, default: ""}
    },
    computed: {},
    components: {
        FileBrowser,
        Modal
    },
    methods: {
        submitForm: async function() {
            this.$emit("startLoading", {
                key: "newArchive",
                message: "Creating new archive"
            });

            let is_valid = await this.validateForm();
            // console.debug(this.data_to_send);
            if (!is_valid) {
                this.$emit("stopLoading", { key: "newArchive" });
            } else {
                let url = this.new_archive_endpoint;
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

                        if(error && error.response && error.response.data && error.response.data.error)
                        {
                            message = error.response.data.error;
                        }
                        if(error && error.response && error.response.data && error.response.data.message)
                        {
                            message += ". " + error.response.data.message;
                        }
                        console.debug(error);
                        this.error_message.push(message);
                    }
                ).finally(() => {
                    this.$emit("stopLoading", { key: "newArchive" });
                });
            }
        },
        closeSuccessModal: function() {
            this.$emit("archiveCreated", this.success.data.archive_id);
            this.success = null;
        },
        validateForm: async function() {
            let errors = [];

            if (this.data_to_send.archive_name.trim() == "") {
                errors.push("Name is a required field.");
            }
            // if (this.data_to_send.archive_description.trim() == "") {
            //     errors.push("Description is a required field.");
            // }

            return new Promise(resolve => {
                if (this.selected_files.length <= 0) {
                    errors.push("Must choose a file.");
                    this.$set(this, "error_message", errors);
                    this.$emit("stopLoading", { key: "verifyFile" });
                    resolve(false);
                } else {
                    //verify authenticity of file
                    this.$emit("startLoading", { key: "verifyFile" });
                    let url =
                        this.new_archive_endpoint +
                        "/check";
                    let prom = this.$cadre.axios({
                        url: url,
                        method: "POST",
                        data: this.data_to_send
                    });
                    prom.then(
                        response => {},
                        error => {
                            errors.push(
                                "Chosen file could not be verified as a CADRE result file.  Only results from the query builder can be archived."
                            );
                        }
                    ).finally(() => {
                        this.$set(this, "error_message", errors);
                        this.$emit("stopLoading", { key: "verifyFile" });
                        if (errors.length > 0) {
                            // console.debug("Form not valid.");
                            resolve(false);
                        } else {
                            resolve(true);
                        }
                    });
                }
            });
        }
    },
    watch: {
        selected_files: function() {
            this.data_to_send.file_path = this.selected_files[0];
        },
        "data_to_send.file_path": function() {
            this.$set(this, "selected_files", [this.data_to_send.file_path]);
        },
        defaultName: function(){
            this.data_to_send.archive_name = this.defaultName;
        }
    },
    mounted: function() {
        // this.data_to_send.environment = "python";
        if(this.defaultName)
        {
            this.data_to_send.archive_name = this.defaultName;
        }
    }
};
</script>

<style>
.form-control.file-browser-control {
    height: 10rem;
    overflow: auto;
}
</style>