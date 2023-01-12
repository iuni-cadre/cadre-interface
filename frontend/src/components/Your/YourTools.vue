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
    components: {
        Modal,
    },
    methods: {
        startLoading({key, message}){
            this.$store.commit("loading/addKey", {key, message});
        },
        stopLoading({key}){
            this.$store.commit("loading/removeKey", {key});
        },
        fetchYourTools: function() {
            this.startLoading({ key: "get_your_tools", message: "" });

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
                this.stopLoading({ key: "get_your_tools" });
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
