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


    </div>
</template>

<script>


import Modal from "@/components/Common/CommonModal";
import RacPackageCard from "@/components/Marketplace/MarketplaceRacPackageCard";

export default {
    data: function() {
        return {
        };
    },
    computed: {
        racpackages: function() {
            return this.$store.getters["racpackage/packages"];
        },
    },
    components: {
        Modal,
        RacPackageCard
    },
    methods: {
        },
    mounted: function() {
        //start loading
        if(this.racpackages.length === 0)
        {
            this.$emit("startLoading", {key:"get_packages", message: ""});
            let get_packages_prom = this.$store.dispatch("racpackage/getPackages");
            get_packages_prom.finally(()=>{
                //stop loading
                this.$emit("stopLoading", {key: "get_packages"});
            });
        }
    }
};
</script>

<style>
</style>
