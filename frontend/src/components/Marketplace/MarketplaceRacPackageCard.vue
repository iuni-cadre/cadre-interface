<template>
    <div>
        <div class="racpackage-card card p-3">
            <h4 v-text="racpackage.name">Package Name</h4>
            <div class="small"
                 v-text="`By: ${racpackage.author}`"></div>
            <div class="small"
                 v-text="`Created On: ${racpackage.created_date}`"></div>
            <div class="racpackage-body row mt-3">
                <div class="racpackage-info col">
                    <dl>
                        <dt class="mr-1">Tool: </dt>
                        <dd class="ml-1 "
                            v-text="racpackage.tools.join(', ')"></dd>

                        <dt class="mr-1">Input Data: </dt>
                        <dd class="ml-1 "
                            v-text="racpackage.input_files.join(', ')"></dd>

                    </dl>

                </div>
                <div class="col">
                    <button class=" float-right btn-lg btn btn-primary"
                            @click="show_run_modal = true">Run</button>
                </div>
            </div>

        </div>
        <modal v-if="show_run_modal"
               @close="show_run_modal = false">
            <div>
                <pre v-text="racpackage"></pre>
                <div class="form-group">
                    <label>Output Filename</label>
                    <input type="text"
                           placeholder="output_file.csv"
                           class="form-control"
                           v-model="output_filename" />
                </div>
                <div>
                    <button class="btn btn-primary"
                            @click="runPackage">Run Package</button>
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
            show_run_modal: false,
            output_filename: ""
        };
    },
    computed: {
        racpackage: function() {
            return this.RacPackage;
        }
    },
    props: {
        RacPackage: Object
    },
    methods: {
        runPackage: function() {
            this.$emit("startLoading", { key: "running_package" });

            let running_promise = this.$store.dispatch(
                "racpackage/runPackage",
                {
                    package_id: this.racpackage.package_id,
                    output_filename: this.output_filename
                }
            );

            running_promise.then(this.runSuccess, this.runFail).finally(this.runFinally);
        },

        runSuccess: function(response) {
            this.results = {
                job_id: response.job_id,
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
        }
    },
    components: {
        Modal
    }
};
</script>

<style>
</style>
