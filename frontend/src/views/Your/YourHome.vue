<template>
    <div>
        <section>
            <div class="container">
                <h2>Your CADRE</h2>
                <hr />

                <!-- <div class="packages-container">
                    <h3>Packages</h3>

                    <div class="row flex-wrap">
                        <div
                            v-for="(racpackage, index) in racpackages"
                            :key="`racpackage_card_${index}`"
                            class="col-md-4 d-flex"
                        >
                            <rac-package-card
                                @startLoading="(data)=>{ $emit('startLoading', data); }"
                                @stopLoading="(data)=>{ $emit('stopLoading', data); }"
                                :rac-package="racpackage"
                            ></rac-package-card>
                        </div>
                    </div>
                </div>

                <hr />-->

                <div class="tools-container">
                    <h3>Your Tools</h3>
                    <div class="row">
                        <div class="col mb-3">
                            <button
                                class="btn btn-primary"
                                @click="show_create_tool_modal = true"
                            >Create New Tool</button>
                        </div>
                    </div>
                    <div class="row flex-wrap">
                        <div
                            v-for="(ractool, index) in ractools"
                            :key="`ractool_card_${index}`"
                            class="col-md-4 d-flex"
                        >
                            <rac-tool-card
                                @startLoading="(data)=>{ $emit('startLoading', data); }"
                                @stopLoading="(data)=>{ $emit('stopLoading', data); }"
                                :rac-tool="ractool"
                            ></rac-tool-card>
                        </div>
                        <div
                            class="col"
                            v-if="your_tools.length == 0"
                        >Could not find any tools.</div>
                    </div>
                    <modal
                        @close="confirm_tool_create_modal_close = true"
                        close-button-label="Cancel"
                        v-if="show_create_tool_modal"
                        modal-width="60%"
                        modal-title="Create New Tool"
                    >
                        <new-tool-form @toolCreated="show_create_tool_modal = false;"></new-tool-form>
                    </modal>
                    <modal
                        @ok="show_create_tool_modal = false; confirm_tool_create_modal_close = false;"
                        @close="confirm_tool_create_modal_close = false"
                        close-button-label="No"
                        ok-button-label="Yes"
                        :ok-in-footer="true"
                        v-if="confirm_tool_create_modal_close"
                    >Are you sure you want to close this window?</modal>
                </div>

                <!-- <create-package-modal :show-modal="show_create_modal"
                @close="show_create_modal = false"></create-package-modal>-->
            </div>
        </section>
    </div>
</template>

<script>
import Modal from "@/components/Common/CommonModal";
// import RacPackageCard from "@/components/Marketplace/MarketplaceRacPackageCard";
// import CreatePackageModal from "@/components/Marketplace/MarketplaceCreateRacPackageModal";
import RacToolCard from "@/components/Marketplace/MarketplaceRacToolCard";
import NewToolForm from "@/components/Marketplace/MarketplaceNewToolForm";

const GET_TOOLS_ENDPOINT = "/get-tools/user";

export default {
    data: function() {
        return {
            show_create_modal: false,
            show_create_tool_modal: false,
            confirm_tool_create_modal_close: false,

            your_tools: []
        };
    },
    computed: {
        // racpackages: function() {
        //     return this.$store.getters["racpackage/packages"];
        // },
        // ractools: function() {
        //     return this.$store.getters["racpackage/tools"];
        // }
    },
    components: {
        Modal,
        // RacPackageCard,
        RacToolCard,
        // CreatePackageModal,
        NewToolForm
    },
    methods: {
        // openCreateToolModal: function(){
        //     this.show_create_tool_modal = true;
        // }
        fetchYourTools: function() {
            this.$store.commit("loading/addKey", { key: "get_your_tools", message: "" });

            let prom = this.$axios({
                url: this.$cadreConfig.rac_api_prefix + GET_TOOLS_ENDPOINT,
                method: "GET"
            });

            prom.then(
                () => {},
                () => {}
            );
            prom.finally(() => {
                this.$store.commit("loading/removeKey", { key: "get_your_tools" });
            });
        }
    },
    mounted: function() {
        //start loading
        // if (this.racpackages.length === 0) {
        //     this.$emit("startLoading", { key: "get_packages", message: "" });
        //     let get_packages_prom = this.$store.dispatch(
        //         "racpackage/getPackages"
        //     );
        //     let get_tools_prom = this.$store.dispatch("racpackage/getTools");
        //     Promise.all([get_packages_prom, get_tools_prom]).finally(() => {
        //         //stop loading
        //         this.$emit("stopLoading", { key: "get_packages" });
        //     });
        // }
    }
};
</script>

<style>
</style>
