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
                    <rac-package :rac-package="rac_package"></rac-package>
                </div>

            </div>
        </div>


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
import RacPackage from "@/components/Marketplace/MarketplaceRacPackageCard";

export default {
    data: function() {
        return {
        };
    },
    computed: {
        rac_packages: function() {
            return RAC_PACKAGES;
        },
    },
    components: {
        Modal,
        RacPackage
    },
    methods: {

    },
    mounted: function() {}
};
</script>

<style>
</style>
