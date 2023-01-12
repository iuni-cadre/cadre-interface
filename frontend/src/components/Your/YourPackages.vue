<template>
    <div>
        <div class="racpackages-container">
            <h3>Your Packages</h3>
            <!-- <div class="row">
                <div class="col mb-3">
                    <button
                        class="btn btn-primary"
                        @click="show_create_racpackage_modal = true"
                    >Create New Archive</button>
                </div>
            </div> -->
            <div class="row flex-wrap">
                <div
                    v-for="(racpackage, index) in your_racpackages"
                    :key="`racpackage_card_${index}`"
                    class="col-md-4 d-flex"
                >
                </div>
                <div
                    class="col"
                    v-if="your_racpackages.length == 0"
                >Could not find any packages created by you.</div>
            </div>
            <!-- <modal
                @close="confirm_racpackage_create_modal_close = true"
                close-button-label="Cancel"
                v-if="show_create_racpackage_modal"
                modal-width="60%"
                modal-title="Create New Archive"
            >
                <new-racpackage-form @racpackageCreated="show_create_racpackage_modal = false;"></new-racpackage-form>
            </modal> -->
            <!-- <modal
                @ok="show_create_racpackage_modal = false; confirm_racpackage_create_modal_close = false;"
                @close="confirm_racpackage_create_modal_close = false"
                close-button-label="No"
                ok-button-label="Yes"
                :ok-in-footer="true"
                v-if="confirm_racpackage_create_modal_close"
            >Are you sure you want to close this window?</modal>
        </div> -->
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

const GET_PACKAGES_ENDPOINT = "/get-packages/user";

export default {
    data: function() {
        return {
            show_create_modal: false,
            show_create_racpackage_modal: false,
            confirm_racpackage_create_modal_close: false,

            your_racpackages: [],
            error_message: ""
        };
    },
    computed: {
        // racpackages: function() {
        //     return this.$store.getters["racpackage/packages"];
        // },
        // racracpackages: function() {
        //     return this.$store.getters["racpackage/racpackages"];
        // }
        refresh_packages: function(){
            return this.$store.getters["racpackage/refresh_packages"];
        }
    },
    components: {
        Modal,
    },
    methods: {
        // openCreateArchiveModal: function(){
        //     this.show_create_racpackage_modal = true;
        // }
        startLoading({key, message}){
            this.$store.commit("loading/addKey", {key, message});
        },
        stopLoading({key}){
            this.$store.commit("loading/removeKey", {key});
        },
        fetchYourPackages: function() {
            // this.$emit("startLoading", { key: "get_your_racpackages", message: "" });
            this.$store.commit("loading/addKey", { key: "get_your_racpackages", message: "" });

            let prom = this.$cadre.axios({
                url: this.$cadreConfig.rac_api_prefix + GET_PACKAGES_ENDPOINT,
                method: "GET"
            });

            prom.then(
                response => {
                    this.your_racpackages = response.data;
                },
                error => {
                    console.error(error);
                    this.error_message = "We tried to get your packages, but could not connect to the server.  Try again later.";
                }
            ).finally(() => {
                this.$store.commit("loading/removeKey", {key: "get_your_racpackages"});
            });
        }
    },
    watch: {
        refresh_packages: function(){
            this.fetchYourPackages();
        }
    },
    mounted: function() {
        this.fetchYourPackages();
    }
};
</script>

<style>
</style>
