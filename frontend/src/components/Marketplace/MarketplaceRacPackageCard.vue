<template>
    <div>
        <div class="rac_package-card card p-3">
            <h4 v-text="rac_package.name">Package Name</h4>
            <div class="small"
                 v-text="`By: ${rac_package.author}`"></div>
            <div class="small"
                 v-text="`Created On: ${rac_package.created_date}`"></div>
            <div class="rac_package-body row mt-3">
                <div class="rac_package-info col">
                    <dl>
                        <dt class="mr-1">Tool: </dt>
                        <dd class="ml-1 "
                            v-text="rac_package.tools.join(', ')"></dd>

                        <dt class="mr-1">Input Data: </dt>
                        <dd class="ml-1 "
                            v-text="rac_package.input_files.join(', ')"></dd>

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
                <pre v-text="rac_package"></pre>
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
    </div>

</template>

<script>
import Modal from "@/components/Common/CommonModal.vue";
export default {
    data: function() {
        return {
            results: undefined,
            show_run_modal: false,
            output_filename: ""
        };
    },
    computed: {
        rac_package: function() {
            return this.RacPackage;
        }
    },
    props: {
        RacPackage: Object
    },
    methods: {
        runPackage: function() {
            let running_promise = new Promise((resolve, reject) => {
                console.debug("running package " + this.rac_package.package_id);
                console.debug("putting results into " + this.output_filename);

                resolve({
                    message: `Succeeded! ${this.rac_package.name} successfully ran.`
                });
            });
            running_promise.then(this.runSuccess, this.runFail);
        },

        runSuccess: function(response) {
            this.results = response;
            console.debug(this.results);
            this.output_filename = "";
            this.show_run_modal = null;
        },
        runFail: function(error) {}
    },
    components: {
        Modal
    }
};
</script>

<style>
</style>
