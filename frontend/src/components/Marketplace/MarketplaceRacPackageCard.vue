<template>
    <div class="flex-fill d-flex mb-3">
        <div class="racpackage-card card p-3 flex-fill d-flex flex-column justify-content-between">
            <div>
                <h4 v-text="racpackage.name">Package Name</h4>
                <div class="small"
                     v-text="`By: ${racpackage.author}`"></div>
                <div class="small"
                     v-text="`Created On: ${racpackage.created_date}`"></div>
                <div class="racpackage-body row mt-3">
                    <div class="racpackage-info col jusify-content-between">
                        <dl>
                            <dt class="mr-1">Tool: </dt>
                            <dd class="ml-1 "
                                v-text="tool_names"></dd>

                            <dt class="mr-1">Input Data: </dt>
                            <dd class="ml-1 "
                                v-text="input_files || 'No Input Data Required'"></dd>

                        </dl>

                    </div>
                    <!-- <div class="col">
                </div> -->
                </div>
            </div>

            <button class=" float-right btn-lg btn btn-primary"
                    @click="show_run_modal = true">Run</button>
        </div>
        <modal v-if="show_run_modal"
               @close="show_run_modal = false">
            <div class="run-modal-body">
                <!-- <pre v-text="racpackage"></pre> -->
                <div class="card mb-3">
                    <div>
                        Input Files: <strong v-text="input_files ||  'No Input Data Required'"></strong>
                    </div>
                </div>
                <div class="card mb-3">
                    <div>Tool: <strong v-text="tool_names"></strong></div>
                    <small>created by <span v-text="tool_authors"></span></small>
                    <div><span v-text="tool_descriptions"></span></div>

                </div>
                <div class="form-group card">
                    <label>Output Paths</label>

                    <ol v-if="tool_output_files.length > 0"
                        class="pl-3">
                        <li class="mb-1"
                            v-for="(filename, index) in tool_output_files"
                            :key="`filename_${index}`">

                            <div class="input-group">

                                <input type="text"
                                       placeholder=""
                                       class="form-control"
                                       v-model="output_filenames[index]" />
                                <!-- <div class="input-group-append">
                                <button class="btn btn-outline-danger not-round"
                                        @click="removeOutputFile(index)">X</button>
                            </div> -->
                            </div>
                        </li>
                    </ol>
                    <p v-else>
                        This package does not require any output paths.
                    </p>
                    <!-- <div class="d-flex justify-content-end text-right">
                        <button class="btn btn-outline-primary btn-sm"
                                @click="addOutputFile"> + Add Additional Filename</button>
                    </div> -->

                </div>
                <div>
                    <button class="btn btn-lg btn-primary"
                            @click="runPackage">Run Package</button>
                </div>
            </div>
        </modal>
        <modal v-if="results"
               @close="results = undefined"
               modal-style="success"
               modal-type="success">

            <div>
                <div>Package has been queued successfully.</div>
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
            show_run_modal: false,
            output_filenames: [] //[""]
        };
    },
    computed: {
        racpackage: function() {
            return this.RacPackage;
        },
        tool: function() {
            let packages = this.$store.getters["racpackage/tools"];
            // console.debug(packages);
            return tool_id => {
                if (!packages[tool_id]) {
                    console.warn(
                        "Trying to get name of unknown tool " + tool_id
                    );
                    return {};
                }
                return packages[tool_id] || {};
            };
        },
        tool_names: function() {
            return this.racpackage.tools
                .map(tool_id => {
                    return this.tool(tool_id).name;
                })
                .join(", ");
        },
        tool_descriptions: function() {
            return this.racpackage.tools
                .map(tool_id => {
                    return this.tool(tool_id).description;
                })
                .join(", ");
        },
        tool_authors: function() {
            return this.racpackage.tools
                .map(tool_id => {
                    return this.tool(tool_id).author;
                })
                .join(", ");
        },
        input_files: function() {
            return this.racpackage.input_files.join(", ");
        },
        tool_output_files: function() {
            let output_files = [];
            for (let tool_id of this.racpackage.tools) {
                let tool = this.tool(tool_id);
                if (tool) {
                    output_files = [...output_files, ...tool.output_files];
                }
            }

            return output_files;
        }
    },
    props: {
        RacPackage: Object
    },
    methods: {
        addOutputFile: function() {
            this.output_filenames.push("");
        },
        removeOutputFile: function(index) {
            this.output_filenames.splice(index, 1);
        },
        runPackage: function() {
            for (let filename of this.output_filenames) {
                if (filename.trim() == "") {
                    this.error = {
                        error_message: "Output path is empty."
                    };
                    return false;
                }
            }
            if (this.output_filenames.length != this.tool_output_files.length) {
                this.error = {
                    error_message: "Must specify the correct number of paths."
                };
                return false;
            }

            this.$emit("startLoading", { key: "running_package" });

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
                job_id: response.job_id || (response[0] && response[0].job_id) || "Unknown",
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
            this.$emit("stopLoading", { key: "running_package" });
        },
        initializeOutputFilenames: function() {
            // console.debug(this.racpackage);
            this.$set(this, "output_filenames", []);
            for (let i = 0; i < this.tool_output_files.length; i++) {
                this.output_filenames.push(this.tool_output_files[i]);
            }
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
        Modal
    }
};
</script>

<style>
.run-modal-body {
    width: 90vw;
}
</style>
