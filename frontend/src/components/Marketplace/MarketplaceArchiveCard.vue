<template>
    <div
        class="flex-fill d-flex mb-3"
        v-if="archive"
    >
        <div class="archive-card card p-3 flex-fill d-flex flex-column justify-content-between">
            <div>
                <h4 v-text="archive.archive_name">Archive Name</h4>
                <div
                    v-if="archive.created_by == user_id"
                    class="small"
                    v-text="`By: You`"
                ></div>
                <div
                    v-else
                    class="small"
                    v-text="`By: ${archive.display_name || archive.created_by || 'CADRE Team'}`"
                ></div>
                <div
                    class="small"
                    v-text="`Created On: ${new Date(archive.created_on).toUTCString()}`"
                ></div>
                <p v-text="archive.archive_description || 'No Description'"></p>
            </div>
            <div class="mt-3">
                <button
                    class="float-right btn btn-primary"
                    @click="create_package_modal_open = true;"
                    :aria-label="`Create Package from Archive ${archive.archive_name}`"
                >Create Package</button>
            </div>
            <div
                class="mt-3"
                v-if="archive.created_by == user_id"
            >
                <button
                    class="float-right btn-link btn text-danger"
                    @click="delete_archive_open = true;"
                    :aria-label="`Delete Archive ${archive.archive_name}`"
                >Delete Archive</button>
            </div>
        </div>

        <modal
            @close="confirm_package_create_modal_close = true"
            close-button-label="Cancel"
            v-if="create_package_modal_open"
            modal-width="60%"
            modal-title="Create New Package"
        >
            <new-package-form
                :archive-ids="[archive.archive_id]"
                @packageCreated="create_package_modal_open = false;"
                @startLoading="startLoading"
                @stopLoading="stopLoading"
            ></new-package-form>
        </modal>
        
        <modal
            @ok="create_package_modal_open = false; confirm_package_create_modal_close = false;"
            @close="confirm_package_create_modal_close = false"
            close-button-label="No"
            ok-button-label="Yes"
            :ok-in-footer="true"
            v-if="confirm_package_create_modal_close"
        >Are you sure you want to close this window?</modal>

        <modal
            v-if="delete_archive_open"
            @close="delete_archive_open = false"
            @ok="deleteArchive()"
            modal-style="danger"
            modal-type="delete"
            ok-button-label="Yes, Delete Archive"
            close-button-label="Cancel"
        >
            <p>Are you sure you want to delete this archive?</p>
        </modal>
        <modal
            v-if="delete_success_open"
            @close="deleteSuccess()"
            modal-style="success"
            close-button-label="OK"
        >
            <p>Archive was deleted successfully</p>
        </modal>
        <modal
            v-if="delete_error_open"
            @close="delete_error_open=false"
            modal-style="danger"
            modal-type="error"
            close-button-label="Close"
        >
            <p>Archive could not be deleted.</p>
        </modal>
    </div>
</template>

<script>
import Modal from "@/components/Common/CommonModal.vue";
import NewPackageForm from "@/components/Marketplace/MarketplaceNewPackageForm";
export default {
    data: function() {
        return {
            results: undefined,
            error: undefined,
            create_package_modal_open: false,
            delete_archive_open: false,
            delete_success_open: false,
            delete_error_open: false,

            confirm_package_create_modal_close: false
        };
    },
    computed: {
        archive: function() {
            return this.RacArchive;
        },
        user_id: function() {
            return this.$store.state.user.user_id;
        }
    },
    props: {
        RacArchive: Object
    },
    methods: {
        startLoading({key, message}){
            this.$store.commit("loading/addKey", {key, message});
        },
        stopLoading({key}){
            this.$store.commit("loading/removeKey", {key});
        },
        deleteArchive: function() {
            if (this.archive.created_by != this.user_id) {
                return false;
            }
            this.startLoading({key: "archiveDelete"});
            let delete_prom = this.$cadre.axios({
                url: this.$cadreConfig.rac_api_prefix + "/archives/delete",
                method: "POST",
                data: {
                    archive_id: this.archive.archive_id
                }
            });
            delete_prom.then(
                response => {
                    this.delete_success_open = true;
                },
                error => {
                    console.error(error);
                    this.delete_error_open = true;
                }
            );
            delete_prom.finally(() => {
                this.delete_archive_open = false;
                this.stopLoading({key: "archiveDelete"});
            });

            this.delete_archive_open = false;
        },
        deleteSuccess: function() {
            this.delete_success_open = false;
            this.$emit("archiveDeleted", this.archive);
        }
    },
    watch: {
        RacArchive: function() {
            // this.initializeOutputFilenames();
        }
    },
    mounted: function() {
        // this.initializeOutputFilenames();
    },
    components: {
        Modal,
        NewPackageForm
    }
};
</script>

<style>
.run-modal-body {
    width: 90vw;
}
</style>
