<template>
    <div class="flex-fill d-flex mb-3">
        <div class="racpackage-card card p-3 flex-fill d-flex flex-column justify-content-between">
            <div>
                <h4 v-text="racpackage.name">Package Name</h4>
                <div
                    v-if="racpackage.created_by == user_id"
                    class="small"
                    v-text="`By: You`"
                ></div>
                <div
                    v-else
                    class="small"
                    v-text="`By: ${racpackage.created_by || 'CADRE Team'}`"
                ></div>
                <div
                    class="small"
                    v-text="`Created On: ${new Date(racpackage.created_on).toUTCString()}`"
                ></div>
                <div class="racpackage-body row mt-3">
                    <div class="racpackage-info col jusify-content-between">
                        <dl>
                            <dt class="mr-1">Tool:</dt>
                            <dd
                                class="ml-1"
                                v-text="tool_names"
                            ></dd>

                            <dt class="mr-1">Input Data Sets:</dt>
                            <dd
                                class="ml-1"
                                v-text="input_files || 'No Input Data Required'"
                            ></dd>
                            <dt class="mr-1">Source Set{{datasets.length == 1?"":"s"}}:</dt>
                            <dd
                                class="ml-1"
                                v-text="datasets_names.join(',')"
                            ></dd>
                        </dl>
                    </div>
                    <!-- <div class="col">
                    </div>-->
                </div>
            </div>
            <button
                v-if="can_access_all_sets"
                class="float-right btn-lg btn btn-primary"
                @click="show_run_modal = true"
            >Run</button>
            <button
                v-else
                class="float-right btn-lg btn btn-primary disabled"
                disabled
            >Run</button>
            <div v-if="!can_access_all_sets">
                <small>This package requires data from a source that you don't have access to.</small>
            </div>

            <div class="mt-3">
                <button
                    v-if="racpackage.created_by == user_id && !racpackage.published"
                    class="float-left btn btn-primary"
                    @click="publish_package_open = true;"
                >Publish Package</button> 
                <button
                    class="float-right btn btn-primary"
                    @click="create_package_modal_open = true;"
                >Clone Package</button>             
            </div>
            <div
                class="mt-3"
                v-if="racpackage.created_by == user_id"
            >
                <!-- <button
                    class="float-right btn btn-outline-danger"
                    @click="delete_tool_open = true;"
                >Delete Tool</button>-->
                <button
                    class="float-right btn-link btn text-danger"
                    @click="delete_package_open = true;"
                >Delete Package</button>
            </div>
        </div>
        <modal
            v-if="show_run_modal"
            @close="show_run_modal = false"
        >
            <div class="run-modal-body">
                <!-- <pre v-text="racpackage"></pre> -->
                <div class="card mb-3">
                    <div>
                        Input Data Sets:
                        <strong v-text="input_files ||  'No Input Data Required'"></strong>
                    </div>
                </div>
                <div class="card mb-3">
                    <div>
                        Tool:
                        <strong v-text="tool_names"></strong>
                    </div>
                    <!-- <small>
                        created by
                        <span v-text="tool_authors"></span>
                    </small>-->
                    <div>
                        <span v-text="tool_descriptions"></span>
                    </div>
                </div>
                <div>
                    <button
                        class="btn btn-lg btn-primary"
                        @click="runPackage"
                    >Run Package</button>
                    
                <button
                    v-if="allow_overload"
                    @click.stop.prevent="overloadDatabase(true)"
                    class="btn btn-danger btn-lg float-right"
                    type="button"
                >&#x1F47F; Overload CADRE &#x1F47F;</button>
                </div>
            </div>
        </modal>
        <modal
            v-if="results"
            @close="results = undefined"
            modal-style="success"
            modal-type="success"
        >
            <div>
                <div>Package has been queued successfully.</div>
                <div>
                    Job ID:
                    <b v-text="results.job_id"></b>
                </div>
                <button
                    @click.prevent.stop="$router.push({name: 'jobs-list'})"
                    class="btn btn-primary"
                >Check Job Statuses</button>
            </div>
        </modal>
        <modal
            v-if="error"
            @close="error = undefined"
            modal-style="danger"
            modal-type="error"
        >
            <div>
                <p>There was a problem:</p>
                <p>{{error.error_message}}</p>
            </div>
        </modal>

        <modal
            @close="confirm_package_create_modal_close = true"
            close-button-label="Cancel"
            v-if="create_package_modal_open"
            modal-width="60%"
            modal-title="Create New Package"
        >
            <new-package-form
                :tool-ids="tool_ids"
                :archive-ids="archive_ids"
                @packageCreated="create_package_modal_open = false;"
                @startLoading="(key)=>$emit('startLoading',key)"
                @stopLoading="(key)=>$emit('stopLoading',key)"
            ></new-package-form>
        </modal>
        <modal
            @ok="create_package_modal_open = false; confirm_package_create_modal_close = false;"
            @close="confirm_package_create_modal_close = false"
            close-button-label="No"
            ok-button-label="Yes"
            :ok-in-footer="true"
            v-if="confirm_package_create_modal_close"
        >Are you sure you want to close this window?</modal>

        <modal
            v-if="delete_package_open"
            @close="delete_package_open = false"
            @ok="deletePackage()"
            modal-style="danger"
            modal-type="delete"
            ok-button-label="Yes, Delete Package"
            close-button-label="Cancel"
        >
            <p>Are you sure you want to delete this Package?</p>
        </modal>
        <modal
            v-if="delete_success_open"
            @close="deleteSuccess()"
            modal-style="success"
            close-button-label="OK"
        >
            <p>Package was deleted successfully</p>
        </modal>
        <modal
            v-if="delete_error_open"
            @close="delete_error_open=false"
            modal-style="danger"
            modal-type="error"
            close-button-label="Close"
        >
            <p>Package could not be deleted.</p>
        </modal>
        
        <modal
            v-if="publish_package_open"
            @close="publish_package_open = false"
            @ok="publishPackage()"
            :ok-in-footer="true"
            modal-style="success"
            ok-button-label="Yes, Publish Package"
            close-button-label="Cancel"
        >
            <p>This will make your package publicly accessible. Proceed?</p>
        </modal>
        <modal
            v-if="publish_success_open"
            @close="publishSuccess()"
            modal-style="success"
            close-button-label="OK"
        >
            <p>Package was published successfully.</p>
        </modal>
        <modal
            v-if="publish_error_open"
            @close="publish_error_open=false"
            modal-style="danger"
            modal-type="error"
            close-button-label="Close"
        >
            <p>Package could not be published.</p>
        </modal>
        
    </div>
</template>

<script>
import Modal from "@/components/Common/CommonModal.vue";
import NewPackageForm from "@/components/Marketplace/MarketplaceNewPackageForm";

import Datasets from "../../datasets";

export default {
    data: function() {
        return {
            results: undefined,
            error: undefined,
            show_run_modal: false,
            output_filenames: [], //[""]
            create_package_modal_open: false,
            create_package_modal_open: false,
            confirm_package_create_modal_close: false,

            
            delete_package_open: false,
            delete_success_open: false,
            delete_error_open: false,

            publish_package_open:false,
            publish_success_open:false,
            publish_error_open:false
        };
    },
    computed: {
        allow_overload: function() {
            return this.$cadreConfig.allow_overload || false;
        },
        datasets_names: function() {
            let names = [];
            for (let dataset of this.datasets) {
                names.push(
                    (Datasets[dataset] && Datasets[dataset].name) || "Unknown"
                );
            }
            return names;
        },
        datasets: function() {
            let datasets = new Set();
            for (let perm of this.racpackage.permissions) {
                if (!perm || !perm.data_type) {
                    datasets.add("unknown");
                    continue;
                }
                let name = perm.data_type;
                datasets.add(name.toLowerCase());
            }
            return [...datasets];
        },
        can_access_dataset: function() {
            let user_roles = this.$store.getters["user/roles"], user_groups = this.$store.getters["user/cognito_groups"];
            return function(dataset_id) {
                let allow = false;
                let dataset_roles =
                    Datasets[dataset_id] && Datasets[dataset_id].allowed_roles;
                //if it's not a defined dataset, you can't run it.
                if (!dataset_roles) {
                    return false;
                }

                //short circuit... if dataset has no allowed roles, it's open for all
                if (dataset_roles.length == 0) {
                    return true;
                }
                //check all my roles.  If at least one of my roles is allowed for this data set, return true
                for (let role of user_roles) {
                    if (dataset_roles.indexOf(role) > -1) {
                        return true;
                    }
                }
                for (let group of user_groups) {
                    if (dataset_roles.indexOf(group) > -1) {
                        return true;
                    }
                }
            };
        },
        can_access_all_sets: function() {
            for (let set of this.datasets) {
                if (!this.can_access_dataset(set)) {
                    return false;
                }
            }
            return true;
        },
        racpackage: function() {
            return this.RacPackage;
        },
        user_id: function() {
            return this.$store.state.user.user_id;
        },
        // tool: function() {
        //     let packages = this.$store.getters["racpackage/tools"];
        //     // console.debug(packages);
        //     return tool_id => {
        //         if (!packages[tool_id]) {
        //             console.warn(
        //                 "Trying to get name of unknown tool " + tool_id
        //             );
        //             return {};
        //         }
        //         return packages[tool_id] || {};
        //     };
        // },
        tool_names: function() {
            return this.racpackage.tools
                .map(tool => {
                    return tool.name;
                })
                .join(", ");
        },
        tool_ids: function() {
            return this.racpackage.tools.map(tool => {
                return tool.tool_id;
            });
        },
        archive_ids: function() {
            // return this.racpackage.archives
            //     .map(archive => {
            //         return archive.archive_id;
            //     })
            return this.racpackage.archive_ids || [];
        },
        tool_descriptions: function() {
            return this.racpackage.tools
                .map(tool => {
                    return tool.description;
                })
                .join(", ");
        },
        tool_authors: function() {
            return this.racpackage.tools
                .map(tool => {
                    return tool.created_by;
                })
                .join(", ");
        },
        input_files: function() {
            return this.racpackage.input_files.join(", ");
        },
        tool_output_files: function() {
            let output_files = [];
            for (let tool of this.racpackage.tools) {
                // let tool = this.tool(tool_id);
                try {
                    if (tool) {
                        output_files = [...output_files, ...tool.output_files];
                    }
                } catch (err) {}
            }

            return output_files;
        }
    },
    props: {
        RacPackage: Object
    },
    methods: {
        deletePackage: function() {
            if (this.racpackage.created_by != this.user_id) {
                return false;
            }
            this.$store.commit("loading/addKey", {key: "packageDelete"});
            let delete_prom = this.$cadre.axios({
                url: this.$cadreConfig.rac_api_prefix + "/packages/delete",
                method: "POST",
                data: {
                    package_id: this.racpackage.package_id
                }
            });
            delete_prom.then(
                response => {
                    this.delete_success_open = true;
                    this.$store.commit("racpackage/refreshPackages");
                },
                error => {
                    console.error(error);
                    this.delete_error_open = true;
                }
            );
            delete_prom.finally(() => {
                this.delete_package_open = false;
                this.$store.commit("loading/removeKey", {key: "packageDelete"});
            });

            this.delete_package_open = false;
        },
        deleteSuccess: function() {
            this.delete_success_open = false;
            this.$emit("packageDeleted", this.racpackage);
        },
        publishPackage: function(){
            //uncomment after testing 1
            if (this.racpackage.created_by != this.user_id || this.racpackage.published){
                return false;
            }
            this.$store.commit("loading/addKey", {key: "packagePublish"});
            let publish_promise = this.$cadre.axios({
                url: this.$cadreConfig.rac_api_prefix + "/packages/publish",
                method:"POST",
                data: {
                    package_id: this.racpackage.package_id
                }
            });
            publish_promise.then(
                response => {
                    this.publish_success_open = true;
                    this.$store.commit("racpackage/refreshPackages"); //?check this too
                },
                error => {
                    console.error(error);
                    this.publish_error_open = true;
                }
            );
            publish_promise.finally(() => {
                this.publish_package_open = false;
                this.$store.commit("loading/removeKey", {key: "packagePublish"});
                //passing on updating the store view -- should the package share button no longer be visible. done in ln434
                //refresh
            });
            this.publish_package_open = false;
        },
        publishSuccess: function(){
            this.publish_success_open = false;
            this.$emit("packagePublished", this.racpackage);
        },
        // addOutputFile: function() {
        //     this.output_filenames.push("");
        // },
        // removeOutputFile: function(index) {
        //     this.output_filenames.splice(index, 1);
        // },
        runPackage: function() {
            // for (let filename of this.output_filenames) {
            //     if (filename.trim() == "") {
            //         this.error = {
            //             error_message: "Output path is empty."
            //         };
            //         return false;
            //     }
            // }
            // if (this.output_filenames.length != this.tool_output_files.length) {
            //     this.error = {
            //         error_message: "Must specify the correct number of paths."
            //     };
            //     return false;
            // }

            if (!this.can_access_all_sets) {
                this.error = {
                    error_message:
                        "Your account doesn't have permission to use the source dataset of this package."
                };
                return false;
            }

            this.$store.commit("loading/addKey", { key: "running_package" });

            let running_promise = this.$store.dispatch(
                "racpackage/runPackage",
                {
                    package_id: this.racpackage.package_id,
                    output_filenames: this.output_filenames
                }
            );

            running_promise
                .then(this.runSuccess, this.runFail)
                .finally(this.runFinally);
        },

        runSuccess: function(response) {
            this.results = {
                job_id:
                    response.job_id ||
                    (response[0] && response[0].job_id) ||
                    "Unknown",
                success_message: "Package is running."
            };
            console.debug(this.results);
            this.output_filename = "";
            this.show_run_modal = null;
        },
        runFail: function(error) {
            console.debug(error);
            this.error = {
                error_message: error.error_message
            };
        },
        runFinally: function() {
            this.$store.commit("loading/removeKey", { key: "running_package" });
        },
        initializeOutputFilenames: function() {
            // console.debug(this.racpackage);
            this.$set(this, "output_filenames", []);
            for (let i = 0; i < this.tool_output_files.length; i++) {
                this.output_filenames.push(this.tool_output_files[i]);
            }
        },
        overloadDatabase: function() {
            if (!this.allow_overload) {
                console.error(
                    "What in the everloving hell do you think you're doing!?"
                );
                return false;
            } else {
                console.error(
                    "You're about to cause major havok and overload CADRE."
                );
            }

            let confirmed = confirm(
                "Are you absolutely sure you want to set CADRE on fire?"
            );

            if (confirmed) {
                confirmed = confirm("Last chance to cancel... ");
            }

            if (confirmed) {
                console.error("Here we go...");
                for (let i = 0; i < 80; i++) {
                    console.warn("Sending query " + i);
                    this.runPackage();
                }
                console.error("You monster...");
            }

            return false;
        }
    },
    watch: {
        RacPackage: function() {
            this.initializeOutputFilenames();
        }
    },
    mounted: function() {
        this.initializeOutputFilenames();
    },
    components: {
        Modal,
        NewPackageForm
    }
};
</script>

<style>
.run-modal-body {
    width: 90vw;
}
</style>
