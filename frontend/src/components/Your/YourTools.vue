<template>
    <div>
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
                    v-for="(ractool, index) in your_tools"
                    :key="`ractool_card_${index}`"
                    class="col-md-4 d-flex"
                >
                    <rac-tool-card
                        @startLoading="(data)=>{ $emit('startLoading', data); }"
                        @stopLoading="(data)=>{ $emit('stopLoading', data); }"
                        @toolDeleted="fetchYourTools()"
                        :rac-tool="ractool"
                    ></rac-tool-card>
                </div>
                <div
                    class="col"
                    v-if="your_tools.length == 0"
                >Could not find any tools created by you.</div>
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

        <modal
            @close="error_message = ''"
            v-if="error_message"
            modal-style="danger"
        >{{error_message}}</modal>
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

            your_tools: [],
            error_message: ""
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
            this.$emit("startLoading", { key: "get_your_tools", message: "" });

            let prom = this.$cadre.axios({
                url: this.$cadreConfig.rac_api_prefix + GET_TOOLS_ENDPOINT,
                method: "GET"
            });

            prom.then(
                response => {
                    this.$set(this, "your_tools", response.data);
                    // this.your_tools = response.data;
                },
                error => {
                    console.error(error);
                    this.error_message = "We tried to get your tools, but could not connect to the server.  Try again later.";
                }
            );
            prom.finally(() => {
                this.$emit("stopLoading", { key: "get_your_tools" });
            });
        }
    },
    mounted: function() {
        this.fetchYourTools();
    }
};
</script>

<style>
</style>
