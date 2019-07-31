<template>
    <div>
        <h2>Marketplace</h2>
        <hr />

        <div class="packages-container">
            <h3>Packages</h3>

            <div class="row flex-wrap">
                <div v-for="(racpackage, index) in racpackages"
                     :key="`racpackage_card_${index}`"
                     class="col-4">
                    <rac-package-card
                        @startLoading="(data)=>{ $emit('startLoading', data); }"
                        @stopLoading="(data)=>{ $emit('stopLoading', data); }"
                        :rac-package="racpackage"></rac-package-card>
                </div>

            </div>
        </div>

        <create-package-modal
            :show-modal="show_create_modal"
            @close="show_create_modal = false"
        ></create-package-modal>


    </div>
</template>

<script>


import Modal from "@/components/Common/CommonModal";
import RacPackageCard from "@/components/Marketplace/MarketplaceRacPackageCard";
import CreatePackageModal from "@/components/Marketplace/MarketplaceCreateRacPackageModal";

export default {
    data: function() {
        return {
            show_create_modal: true
        };
    },
    computed: {
        racpackages: function() {
            return this.$store.getters["racpackage/packages"];
        },
    },
    components: {
        Modal,
        RacPackageCard,
        CreatePackageModal
    },
    methods: {
        },
    mounted: function() {
        //start loading
        if(this.racpackages.length === 0)
        {
            this.$emit("startLoading", {key:"get_packages", message: ""});
            let get_packages_prom = this.$store.dispatch("racpackage/getPackages");
            let get_tools_prom = this.$store.dispatch("racpackage/getTools");
            Promise.all([get_packages_prom, get_tools_prom]).finally(()=>{
                //stop loading
                this.$emit("stopLoading", {key: "get_packages"});
            });
        }
    }
};
</script>

<style>
</style>
