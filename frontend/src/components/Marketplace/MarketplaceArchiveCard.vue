<template>
    <div class="flex-fill d-flex mb-3">
        <div class="archive-card card p-3 flex-fill d-flex flex-column justify-content-between">
            <div>
                <h4 v-text="archive.name">Archive Name</h4>
                <div
                    class="small"
                    v-text="`By: ${archive.created_by || 'CADRE Team'}`"
                ></div>
                <div
                    class="small"
                    v-text="`Created On: ${new Date(archive.created_on).toUTCString()}`"
                ></div>
            </div>
            <div class="mt-3">
                <button
                    class="float-right btn btn-primary"
                    @click="create_package_modal_open = true;"
                >Create Package</button>
            </div>
        </div>
        <modal
            v-if="create_package_modal_open"
            @close="create_package_modal_open = false"
        >
            <div>
                This feature not yet implemented.
            </div>
        </modal>
        <!-- </div>
                        </li>
                    </ol>
                    <p v-else>
                        This archive does not require any output paths.
                    </p>
                    <div class="d-flex justify-content-end text-right">
                        <button class="btn btn-outline-primary btn-sm"
                                @click="addOutputFile"> + Add Additional Filename</button>
                    </div>

                </div>
                <div>
                    <button class="btn btn-lg btn-primary"
                            @click="runarchive">Run archive</button>
                </div>
            </div>
        </modal>-->
        <!-- <modal v-if="results"
               @close="results = undefined"
               modal-style="success"
               modal-type="success">

            <div>
                <div>archive has been queued successfully.</div>
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
            create_package_modal_open: false
            // output_filenames: [] //[""]
        };
    },
    computed: {
        archive: function() {
            return this.RacArchive;
        }
        // archive: function() {
        //     let archives = this.$store.getters["archive/archives"];
        //     // console.debug(archives);
        //     return archive_id => {
        //         if (!archives[archive_id]) {
        //             console.warn(
        //                 "Trying to get name of unknown archive " + archive_id
        //             );
        //             return {};
        //         }
        //         return archives[archive_id] || {};
        //     };
        // },
        // archive_names: function() {
        //     return this.archive.archives
        //         .map(archive => {
        //             return archive.name;
        //         })
        //         .join(", ");
        // },
        // archive_descriptions: function() {
        //     return this.archive.archives
        //         .map(archive => {
        //             return archive.description;
        //         })
        //         .join(", ");
        // },
        // archive_authors: function() {
        //     return this.archive.archives
        //         .map(archive => {
        //             return archive.created_by;
        //         })
        //         .join(", ");
        // },
        // // input_files: function() {
        // //     return this.archive.input_files.join(", ");
        // // },
        // archive_output_files: function() {
        //     let output_files = [];
        //     for (let archive of this.archive.archives) {
        //         // let archive = this.archive(archive_id);
        //         try {
        //             if (archive) {
        //                 output_files = [...output_files, ...archive.output_files];
        //             }
        //         } catch (err) {

        //         }
        //     }

        //     return output_files;
        // }
    },
    props: {
        RacArchive: Object
    },
    methods: {
        // addOutputFile: function() {
        //     this.output_filenames.push("");
        // },
        // removeOutputFile: function(index) {
        //     this.output_filenames.splice(index, 1);
        // },
        // runarchive: function() {
        //     for (let filename of this.output_filenames) {
        //         if (filename.trim() == "") {
        //             this.error = {
        //                 error_message: "Output path is empty."
        //             };
        //             return false;
        //         }
        //     }
        //     if (this.output_filenames.length != this.archive_output_files.length) {
        //         this.error = {
        //             error_message: "Must specify the correct number of paths."
        //         };
        //         return false;
        //     }
        //     this.$emit("startLoading", { key: "running_archive" });
        //     let running_promise = this.$store.dispatch(
        //         "archive/runarchive",
        //         {
        //             archive_id: this.archive.archive_id,
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
        //         success_message: "archive is running."
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
        //     this.$emit("stopLoading", { key: "running_archive" });
        // },
        // initializeOutputFilenames: function() {
        //     // console.debug(this.archive);
        //     this.$set(this, "output_filenames", []);
        //     for (let i = 0; i < this.archive_output_files.length; i++) {
        //         this.output_filenames.push(this.archive_output_files[i]);
        //     }
        // }
    },
    watch: {
        RacArchive: function() {
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
