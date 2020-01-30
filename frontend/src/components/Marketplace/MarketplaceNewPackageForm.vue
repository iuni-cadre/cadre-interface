<template>
    <div style="width: 100%;">
        <form @submit.stop.prevent="submitForm">
            <div class="form-group">
                <label>Package Name</label>
                <input
                    type="text"
                    placeholder="New Package Name"
                    class="form-control"
                    v-model="data_to_send.name"
                />
            </div>
            <!-- {{data_to_send.archives}} -->
            <!-- {{available_archives}} -->
            <div class="form-group">
                <label>Input Files</label>
                <div
                    class="mb-2"
                    v-for="(archive_id, index) in data_to_send.archives"
                    :key="`archive_to_send_${index}`"
                >
                    <div class="input-group">
                        <span class="input-group-prepend input-group-text">{{index + 1}}</span>
                        <select
                            class="form-control"
                            v-model="data_to_send.archives[index]"
                        >
                            <option :value="''">Select a File</option>
                            <option
                                v-for="available_archive in available_archives"
                                :key="`${available_archive.archive_id}-${index}`"
                                v-text="available_archive.archive_name"
                                :value="available_archive.archive_id"
                            ></option>
                        </select>
                        <div class="input-group-append">
                            <button
                                @click.stop.prevent="()=>{removeArchiveId(index)}"
                                class="btn btn-outline-danger not-round"
                            >X</button>
                        </div>
                    </div>
                </div>
                <div>
                    <select
                        class="form-control"
                        @input="selectNewArchiveId"
                        :value="0"
                    >
                        <option
                            :value="0"
                            disabled
                        >Select a file to add</option>
                        <option
                            v-for="available_archive in available_archives"
                            :key="`${available_archive.archive_id}-New`"
                            v-text="available_archive.archive_name"
                            :value="available_archive.archive_id"
                        ></option>
                    </select>
                </div>
            </div>

            <!-- 
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
            </div>-->

            <div class="form-group">
                <label>Package Description</label>
                <textarea
                    type="text"
                    placeholder="Uses input files and generates output files"
                    class="form-control"
                    v-model="data_to_send.description"
                ></textarea>
            </div>

            <!-- <div class="form-group">
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
            </div>-->
            <!-- <div class="form-group">
                <label>Script Files</label>
                <div class="form-control file-browser-control">
                    <file-browser v-model="data_to_send.file_paths"></file-browser>
                </div>
            </div>-->
            <!-- <div class="form-group">
            <label>Entrypoint File</label>-->
            <!-- <input
                    v-model="data_to_send.entrypoint"
                    type="text"
                    class="form-control"
                    placeholder="e.g. /directory/start.py"
            />-->
            <!-- <select
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
            </div>-->
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
                description: "",
                archives: ["1", "2", "3"],
                tools: ["1", "2", "3"]
            },
            available_archives: [],
            available_tools: [],
            new_package_endpoint:
                this.$cadreConfig.rac_api_prefix + "/packages/new",
            get_archives_endpoint:
                this.$cadreConfig.rac_api_prefix + "/get-archives",
            get_tools_endpoint: this.$cadreConfig.rac_api_prefix + "/get-tools",
            error_message: [],
            success: null
        };
    },
    computed: {},
    props: {
        archiveIds: Array,
        toolIds: Array,
        existingArchives: {
            type: Array,
            default: () => {
                return [];
            }
        }, //of objects
        existingTools: {
            type: Array,
            default: () => {
                return [];
            }
        } //of objects
    },
    components: {
        Modal
    },
    methods: {
        getArchives: function() {
            let prom = new Promise((resolve, reject) => {
                if (this.existingTools.length > 0) {
                    this.$set(
                        this,
                        "available_archives",
                        this.existingArchives
                    );
                    resolve();
                } else {
                    //do ajax
                    reject({ error: "Test promise." });
                }
            });
            return prom;
        },
        getTools: function() {
            let prom = new Promise((resolve, reject) => {
                if (this.existingTools.length > 0) {
                    this.$set(this, "available_tools", this.existingTools);
                    resolve();
                } else {
                    //do ajax
                    reject({ error: "Test promise." });
                }
                prom.catch(err => {
                    console.debug(err);
                });
            });
            return prom;
        },
        getArchivesAndTools: function() {
            this.$emit("startLoading", "getPackageOptions");
            let proms = [];
            proms.push(this.getArchives());
            proms.push(this.getTools());

            let prom = Promise.all(proms);
            prom.then(
                responses => {
                    console.debug(responses);
                },
                errors => {
                    console.debug(errors);
                }
            );
            prom.finally(() => {
                this.$emit("stopLoading", "getPackageOptions");
            });
            return prom;
        },

        selectNewArchiveId: function(event) {
            let value = event.target.value;
            this.data_to_send.archives.push(value);
            console.debug(value);
        },
        removeArchiveId: function(index) {
            this.data_to_send.archives.splice(index, 1);
        },

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
        this.getArchivesAndTools();
    }
};
</script>

<style>
.form-control.file-browser-control {
    height: 10rem;
    overflow: auto;
}
</style>