<template>
    <div
        class="flex-fill d-flex mb-3"
        v-if="ractool"
    >
        <div class="ractool-card card p-3 flex-fill d-flex flex-column justify-content-between">
            <div>
                <h4 v-text="ractool.tool_name">Tool Name</h4>
                <!-- <div
                    class="small"
                    v-text="`By: ${ractool.created_by || 'CADRE Team'}`"
                ></div>-->
                <div
                    class="small"
                    v-text="`Created On: ${new Date(ractool.created_on).toUTCString()}`"
                ></div>
                <p v-text="ractool.tool_description"></p>
            </div>
            <div class="mt-3">
                <button
                    class="float-right btn btn-primary"
                    @click="create_package_modal_open = true;"
                >Create Package</button>
            </div>
            <div class="mt-3" v-if="ractool.created_by == user_id">
                <!-- <button
                    class="float-right btn btn-outline-danger"
                    @click="delete_tool_open = true;"
                >Delete Tool</button>-->
                <button
                    class="float-right btn-link btn text-danger"
                    @click="delete_tool_open = true;"
                >Delete Tool</button>
            </div>
        </div>
        <modal
            v-if="create_package_modal_open"
            @close="create_package_modal_open = false"
        >
            <div>This feature not yet implemented.</div>
        </modal>
        <modal
            v-if="delete_tool_open"
            @close="delete_tool_open = false"
            @ok="deleteTool()"
            modal-style="danger"
            modal-type="delete"
            ok-button-label="Yes, Delete Tool"
            close-button-label="Cancel"
        >
            <p>Are you sure you want to delete this tool?</p>
        </modal>
        <modal
            v-if="delete_success_open"
            @close="deleteSuccess()"
            modal-style="success"
            close-button-label="OK"
        >
            <p>Tool was deleted successfully</p>
        </modal>
        <modal
            v-if="delete_error_open"
            @close="delete_error_open=false"
            modal-style="danger"
            modal-type="error"
            close-button-label="Close"
        >
            <p>Tool could not be deleted.</p>
        </modal>

        <!-- </div>
                        </li>
                    </ol>
                    <p v-else>
                        This tool does not require any output paths.
                    </p>
                    <div class="d-flex justify-content-end text-right">
                        <button class="btn btn-outline-primary btn-sm"
                                @click="addOutputFile"> + Add Additional Filename</button>
                    </div>

                </div>
                <div>
                    <button class="btn btn-lg btn-primary"
                            @click="runtool">Run tool</button>
                </div>
            </div>
        </modal>-->
        <!-- <modal v-if="results"
               @close="results = undefined"
               modal-style="success"
               modal-type="success">

            <div>
                <div>tool has been queued successfully.</div>
                <div>
                    Job ID: <b v-text="results.job_id"></b>
                </div>
                <button @click.prevent.stop="$router.push({name: 'jobs-list'})"
                        class="btn btn-primary">Check Job Statuses</button>
            </div>
        </modal>
        <modal v-if="error"
               @close="error = undefined"
               modal-style="danger"
               modal-type="error">
            <div>
                <p>There was a problem:</p>
                <p>{{error.error_message}}</p>
            </div>
        </modal>-->
    </div>
</template>

<script>
import Modal from "@/components/Common/CommonModal.vue";
export default {
    data: function() {
        return {
            results: undefined,
            error: undefined,
            create_package_modal_open: false,
            delete_tool_open: false,
            delete_success_open: false,
            delete_error_open: false
            // output_filenames: [] //[""]
        };
    },
    computed: {
        ractool: function() {
            return this.RacTool;
        },
        user_id: function(){
            return this.$store.state.user.user_id;
        }
        // tool: function() {
        //     let tools = this.$store.getters["ractool/tools"];
        //     // console.debug(tools);
        //     return tool_id => {
        //         if (!tools[tool_id]) {
        //             console.warn(
        //                 "Trying to get name of unknown tool " + tool_id
        //             );
        //             return {};
        //         }
        //         return tools[tool_id] || {};
        //     };
        // },
        // tool_names: function() {
        //     return this.ractool.tools
        //         .map(tool => {
        //             return tool.name;
        //         })
        //         .join(", ");
        // },
        // tool_descriptions: function() {
        //     return this.ractool.tools
        //         .map(tool => {
        //             return tool.description;
        //         })
        //         .join(", ");
        // },
        // tool_authors: function() {
        //     return this.ractool.tools
        //         .map(tool => {
        //             return tool.created_by;
        //         })
        //         .join(", ");
        // },
        // // input_files: function() {
        // //     return this.ractool.input_files.join(", ");
        // // },
        // tool_output_files: function() {
        //     let output_files = [];
        //     for (let tool of this.ractool.tools) {
        //         // let tool = this.tool(tool_id);
        //         try {
        //             if (tool) {
        //                 output_files = [...output_files, ...tool.output_files];
        //             }
        //         } catch (err) {

        //         }
        //     }

        //     return output_files;
        // }
    },
    props: {
        RacTool: Object
    },
    methods: {
        deleteTool: function() {
            if( ractool.created_by != user_id )
            {
                return false;
            }
            this.$emit("startLoading", "toolDelete");
            let delete_prom = this.$cadre.axios({
                url: this.$cadreConfig.rac_api_prefix + "/tools/delete",
                method: "POST",
                data: {
                    tool_id: this.ractool.tool_id
                }
            });
            delete_prom.then(
                response => {
                    this.delete_success_open = true;
                },
                error => {
                    console.error(error);
                    this.delete_error_open = true;
                }
            );
            delete_prom.finally(() => {
                this.delete_tool_open = false;
                this.$emit("stopLoading", "toolDelete");
            });

            this.delete_tool_open = false;
        },
        deleteSuccess: function(){
            this.delete_success_open = false;
            this.$emit("toolDeleted", this.ractool);
        }
        // addOutputFile: function() {
        //     this.output_filenames.push("");
        // },
        // removeOutputFile: function(index) {
        //     this.output_filenames.splice(index, 1);
        // },
        // runtool: function() {
        //     for (let filename of this.output_filenames) {
        //         if (filename.trim() == "") {
        //             this.error = {
        //                 error_message: "Output path is empty."
        //             };
        //             return false;
        //         }
        //     }
        //     if (this.output_filenames.length != this.tool_output_files.length) {
        //         this.error = {
        //             error_message: "Must specify the correct number of paths."
        //         };
        //         return false;
        //     }
        //     this.$emit("startLoading", { key: "running_tool" });
        //     let running_promise = this.$store.dispatch(
        //         "ractool/runtool",
        //         {
        //             tool_id: this.ractool.tool_id,
        //             output_filenames: this.output_filenames
        //         }
        //     );
        //     running_promise
        //         .then(this.runSuccess, this.runFail)
        //         .finally(this.runFinally);
        // },
        // runSuccess: function(response) {
        //     this.results = {
        //         job_id: response.job_id || (response[0] && response[0].job_id) || "Unknown",
        //         success_message: "tool is running."
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
        //     this.$emit("stopLoading", { key: "running_tool" });
        // },
        // initializeOutputFilenames: function() {
        //     // console.debug(this.ractool);
        //     this.$set(this, "output_filenames", []);
        //     for (let i = 0; i < this.tool_output_files.length; i++) {
        //         this.output_filenames.push(this.tool_output_files[i]);
        //     }
        // }
    },
    watch: {
        RacTool: function() {
            // this.initializeOutputFilenames();
        }
    },
    mounted: function() {
        // this.initializeOutputFilenames();
    },
    components: {
        Modal
    }
};
</script>

<style>
.run-modal-body {
    width: 90vw;
}
</style>
