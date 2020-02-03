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
                <label>Data Sets</label>
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
                            <option :value="''">Select a Data Set</option>
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
                        >Select a Data Set to add</option>
                        <option
                            v-for="available_archive in available_archives"
                            :key="`${available_archive.archive_id}-New`"
                            v-text="available_archive.archive_name"
                            :value="available_archive.archive_id"
                        ></option>
                    </select>
                </div>
            </div>

            <div class="form-group">
                <label>Tool to Run</label>
                <select
                    class="form-control"
                    v-model="data_to_send.tools[0]"
                >
                    <option
                        value
                        disabled
                    >Select a tool</option>
                    <option
                        v-for="tool in available_tools"
                        :key="tool.tool_id"
                        v-text="tool.tool_name"
                        :value="tool.tool_id"
                    ></option>
                </select>
            </div>

            <div class="form-group">
                <label>
                    Package Description
                    <small class="text-muted">(optional)</small>
                </label>
                <textarea
                    type="text"
                    placeholder="Uses input files and generates output files"
                    class="form-control"
                    v-model="data_to_send.description"
                ></textarea>
            </div>

            <div class="form-group">
                <button class="btn btn-primary">Create New Package</button>
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
                <p>Your package has been created.</p>
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
                archives: [],
                tools: [""],
                type: "user_defined"
            },
            files_to_archive: [],
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
                    // reject({ error: "Test promise." });
                    let axios_prom = this.$cadre.axios({
                        url: this.get_archives_endpoint,
                        method: "GET"
                    });
                    axios_prom.then(
                        response => {
                            let archives = response.data;
                            this.$set(this, "available_archives", archives);
                            resolve(response);
                        },
                        error => {
                            this.error_message.push(
                                "Could not fetch the list of data sets."
                            );
                            reject(error);
                        }
                    );
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
                    let axios_prom = this.$cadre.axios({
                        url: this.get_tools_endpoint,
                        method: "GET"
                    });
                    axios_prom.then(
                        response => {
                            let tools = response.data;
                            this.$set(this, "available_tools", tools);
                            resolve(response);
                        },
                        error => {
                            this.error_message.push(
                                "Could not fetch the list of tools."
                            );
                            reject(error);
                        }
                    );
                }
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
                    console.error(errors);
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
                this.data_to_send.archives = this.data_to_send.archives.filter(
                    item => {
                        return item.trim() != "";
                    }
                );
                let url = this.new_package_endpoint;
                let prom = this.$cadre.axios({
                    url: url,
                    method: "POST",
                    data: this.data_to_send
                });
                prom.then(
                    response => {
                        this.success = response;
                        this.$store.commit("racpackage/refreshPackages");
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
            this.$emit("packageCreated");
        },
        validateForm: function() {
            let errors = [];

            if (this.data_to_send.name.trim() == "") {
                errors.push("Name is a required field.");
            }
            if (
                this.data_to_send.archives.filter(item => {
                    if (item.trim() == "") {
                        return false;
                    } else {
                        return item;
                    }
                }).length <= 0
            ) {
                errors.push("You must select at least one data set.");
            }
            if (this.data_to_send.tools[0].trim() == "") {
                errors.push("You must select a tool.");
            }
            // if (this.data_to_send.description.trim() == "") {
            //     errors.push("Description is a required field.");
            // }
            if (this.data_to_send.archives.length <= 0) {
                errors.push("Must include at least one file.");
            }
            // console.debug(errors);
            this.$set(this, "error_message", errors);
            if (errors.length > 0) {
                // console.debug("Form not valid.");
                return false;
            } else {
                return true;
            }
        },
        addArchive: function() {
            return new Promise((resolve, reject) => {});
        },
        validateArchive: function(file_path) {
            return new Promise((resolve, reject) => {
                if (this.selected_files.length <= 0) {
                    errors.push("Must choose a file.");
                    this.$set(this, "error_message", errors);
                    this.$emit("stopLoading", { key: "verifyFile" });
                    resolve(false);
                } else {
                    //verify authenticity of file
                    this.$emit("startLoading", { key: "verifyFile" });
                    let url = this.new_archive_endpoint + "/check";
                    let prom = this.$cadre.axios({
                        url: url,
                        method: "POST",
                        data: {
                            file_path: file_path
                        }
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
    mounted: function() {
        this.getArchivesAndTools();
        if (this.toolIds && this.toolIds.length > 0) {
            this.$set(this.data_to_send, "tools", this.toolIds);
        }
        if (this.archiveIds && this.archiveIds.length > 0) {
            this.$set(this.data_to_send, "archives", this.archiveIds);
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