<template>
    <div>
        <h2>Marketplace</h2>
        <hr />

        <div class="packages-container">
            <h3>Packages</h3>

            <div class="row flex-wrap">
                <div v-for="(rac_package, index) in rac_packages"
                     :key="`rac_package_card_${index}`"
                     class="col-4">
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
                                        @click="running_package_id=rac_package.package_id">Run</button>
                            </div>
                        </div>

                    </div>
                </div>
                <modal v-if="running_package"
                       @close="running_package_id = null">
                    <div>
                        <pre v-text="running_package"></pre>
                        <div class="form-group">
                            <label>Output Filename</label>
                            <input type="text"
                                   placeholder="output_file.csv"
                                   class="form-control"
                                   v-model="output_filename" />
                        </div>
                        <div>
                            <button class="btn btn-primary"
                                    @click="run_package">Run Package</button>
                        </div>
                    </div>
                </modal>

            </div>
        </div>

        <modal v-if="success_message"
               @close="success_message = ''"
               modal-type="success">

            {{success_message}}
        </modal>

    </div>
</template>

<script>
const RAC_PACKAGES = [
    {
        package_id: "package_1",
        name: "package 1",
        author: "author 1",
        created_date: "2019-07-16 10:51:26",
        tools: ["tool 1"],
        input_files: ["/dataset.csv"],
        output_files: ["/new_dataset.csv"]
    },
    {
        package_id: "package_2",
        name: "package 2",
        author: "author 2",
        created_date: "2019-07-16 10:51:26",
        tools: ["tool 2"],
        input_files: ["/dataset.csv"],
        output_files: ["/new_dataset.csv"]
    },
    {
        package_id: "package_3",
        name: "package 3",
        author: "author 3",
        created_date: "2019-07-16 10:51:26",
        tools: ["tool 3"],
        input_files: ["/dataset.csv"],
        output_files: ["/new_dataset.csv"]
    }
];

import Modal from "@/components/Common/CommonModal";

export default {
    data: function() {
        return {
            running_package_id: "package_2",
            output_filename: "",
            success_message: ""
        };
    },
    computed: {
        rac_packages: function() {
            return RAC_PACKAGES;
        },
        running_package: function() {
            return this.rac_packages.find(rac_package => {
                return rac_package.package_id === this.running_package_id;
            });
        }
    },
    components: {
        Modal
    },
    methods: {
        run_package: function() {
            let running_promise = new Promise((resolve, reject) => {
                console.debug(
                    "running package " + this.running_package.package_id
                );
                console.debug("putting results into " + this.output_filename);

                resolve({ message: `Succeeded! ${this.running_package.name} successfully ran.`});
            });
            running_promise.then(response => {
                console.debug(response);
                this.success_message = response.message;
                this.output_filename = "";
                this.running_package_id = null;
            });
        }
    },
    mounted: function() {}
};
</script>

<style>
</style>
