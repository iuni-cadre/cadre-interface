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
            <div class="row flex-wrap">
                <div
                    v-for="(archive, index) in your_archives"
                    :key="`archive_card_${index}`"
                    class="col-md-4 d-flex"
                >
                    <archive-card
                        @startLoading="(data)=>{ $emit('startLoading', data); }"
                        @stopLoading="(data)=>{ $emit('stopLoading', data); }"
                        @archiveDeleted="fetchYourArchives()"
                        :rac-archive="archive"
                    ></archive-card>
                </div>
                <div
                    class="col"
                    v-if="your_archives.length == 0"
                >Could not find any archives created by you.</div>
            </div>
            <modal
                @close="confirm_archive_create_modal_close = true"
                close-button-label="Cancel"
                v-if="show_create_archive_modal"
                modal-width="60%"
                modal-title="Create New Archive"
            >
                <new-archive-form @archiveCreated="show_create_archive_modal = false;"></new-archive-form>
            </modal>
            <modal
                @ok="show_create_archive_modal = false; confirm_archive_create_modal_close = false;"
                @close="confirm_archive_create_modal_close = false"
                close-button-label="No"
                ok-button-label="Yes"
                :ok-in-footer="true"
                v-if="confirm_archive_create_modal_close"
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
import ArchiveCard from "@/components/Marketplace/MarketplaceArchiveCard";
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
        // RacPackageCard,
        ArchiveCard,
        // CreatePackageModal,
        NewArchiveForm
    },
    methods: {
        // openCreateArchiveModal: function(){
        //     this.show_create_archive_modal = true;
        // }
        fetchYourArchives: function() {
            this.$emit("startLoading", { key: "get_your_archives", message: "" });

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
                this.$emit("stopLoading", { key: "get_your_archives" });
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
