<template>
    <div>
        <div class="archives-container">
            <h3>Your Archives</h3>
            <div class="row">
                <div class="col mb-3">
                    <button
                        class="btn btn-primary"
                        @click="show_create_archive_modal = true"
                    >Create New Archive</button>
                </div>
            </div>
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
import NewArchiveForm from "@/components/Marketplace/MarketplaceNewArchiveForm";

const GET_TOOLS_ENDPOINT = "/get-archives/user";

export default {
    data: function() {
        return {
            show_create_modal: false,
            show_create_archive_modal: false,
            confirm_archive_create_modal_close: false,

            your_archives: [],
            error_message: ""
        };
    },
    computed: {
        // racpackages: function() {
        //     return this.$store.getters["racpackage/packages"];
        // },
        // racarchives: function() {
        //     return this.$store.getters["racpackage/archives"];
        // }
    },
    components: {
        Modal,
        NewArchiveForm
    },
    methods: {
        startLoading({key, message}){
            this.$store.commit("loading/addKey", {key, message});
        },
        stopLoading({key}){
            this.$store.commit("loading/removeKey", {key});
        },
        // openCreateArchiveModal: function(){
        //     this.show_create_archive_modal = true;
        // }
        fetchYourArchives: function() {
            this.startLoading({ key: "get_your_archives", message: "" });

            let prom = this.$cadre.axios({
                url: this.$cadreConfig.rac_api_prefix + GET_TOOLS_ENDPOINT,
                method: "GET"
            });

            prom.then(
                response => {
                    this.your_archives = response.data;
                },
                error => {
                    console.error(error);
                    this.error_message = "We tried to get your archives, but could not connect to the server.  Try again later.";
                }
            );
            prom.finally(() => {
                this.stopLoading({ key: "get_your_archives" });
            });
        }
    },
    mounted: function() {
        this.fetchYourArchives();
    }
};
</script>

<style>
</style>
