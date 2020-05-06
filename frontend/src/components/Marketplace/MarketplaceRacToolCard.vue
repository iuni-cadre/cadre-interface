<template>
    <div
        class="flex-fill d-flex mb-3"
        v-if="ractool"
    >
        <div class="ractool-card card p-3 flex-fill d-flex flex-column justify-content-between">
            <div>
                <h4 v-text="ractool.tool_name">Tool Name</h4>
                <!-- <div
                    class="small"
                    v-text="`By: ${ractool.created_by || 'CADRE Team'}`"
                ></div>-->
                <div
                    class="small"
                    v-text="`Created On: ${new Date(ractool.created_on).toUTCString()}`"
                ></div>
                <p v-text="ractool.tool_description"></p>
            </div>
            <div class="mt-3">
                <button
                    v-if="ractool.created_by == user_id && ractool.published == false"
                    class="float-left btn btn-primary"
                    @click="publish_tool_open = true;"
                >Publish Tool</button>
                <button
                    class="float-right btn btn-primary"
                    @click="create_package_modal_open = true;"
                >Create Package</button>
            </div>
            <div
                class="mt-3"
                v-if="ractool.created_by == user_id"
            >
                <!-- <button
                    class="float-right btn btn-outline-danger"
                    @click="delete_tool_open = true;"
                >Delete Tool</button>-->
                <button
                    class="float-right btn-link btn text-danger"
                    @click="delete_tool_open = true;"
                >Delete Tool</button>
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
                :tool-ids="[ractool.tool_id]"
                @packageCreated="create_package_modal_open = false;"
                @startLoading="(key)=>$emit('startLoading',key)"
                @stopLoading="(key)=>$emit('stopLoading',key)"
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
            v-if="delete_tool_open"
            @close="delete_tool_open = false"
            @ok="deleteTool()"
            modal-style="danger"
            modal-type="delete"
            ok-button-label="Yes, Delete Tool"
            close-button-label="Cancel"
        >
            <p>Are you sure you want to delete this tool?</p>
        </modal>
        <modal
            v-if="delete_success_open"
            @close="deleteSuccess()"
            modal-style="success"
            close-button-label="OK"
        >
            <p>Tool was deleted successfully</p>
        </modal>
        <modal
            v-if="delete_error_open"
            @close="delete_error_open=false"
            modal-style="danger"
            modal-type="error"
            close-button-label="Close"
        >
            <p>Tool could not be deleted.</p>
        </modal>
        <modal
            v-if="publish_tool_open"
            @close="publish_tool_open = false"
            @ok="publishTool()"
            :ok-in-footer="true"
            modal-style="success"
            ok-button-label="Yes, Publish Tool"
            close-button-label="Cancel"
        >
            <p>This will make your tool publicly accessible. Proceed?</p>
        </modal>
        <modal
            v-if="publish_success_open"
            @close="publishSuccess()"
            modal-style="success"
            close-button-label="OK"
        >
            <p>Tool was published successfully.</p>
        </modal>
        <modal
            v-if="publish_error_open"
            @close="publish_error_open=false"
            modal-style="danger"
            modal-type="error"
            close-button-label="Close"
        >
            <p>Tool could not be published</p>
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
            delete_tool_open: false,
            delete_success_open: false,
            delete_error_open: false,

            create_package_modal_open: false,
            confirm_package_create_modal_close: false,

            publish_tool_open:false,
            publish_success_open:false,
            publish_error_open:false
        };
    },
    computed: {
        ractool: function() {
            return this.RacTool;
        },
        user_id: function() {
            return this.$store.state.user.user_id;
        }
    },
    props: {
        RacTool: Object
    },
    methods: {
        deleteTool: function() {
            if (this.ractool.created_by != this.user_id) {
                return false;
            }
            this.$emit("startLoading", "toolDelete");
            let delete_prom = this.$cadre.axios({
                url: this.$cadreConfig.rac_api_prefix + "/tools/delete",
                method: "POST",
                data: {
                    tool_id: this.ractool.tool_id
                }
            });
            delete_prom.then(
                response => {
                    this.delete_success_open = true;
                    this.$store.commit("racpackage/refreshTools");
                },
                error => {
                    console.error(error);
                    this.delete_error_open = true;
                }
            );
            delete_prom.finally(() => {
                this.delete_tool_open = false;
                this.$emit("stopLoading", "toolDelete");
            });

            this.delete_tool_open = false;
        },
        deleteSuccess: function() {
            this.delete_success_open = false;
            this.$emit("toolDeleted", this.ractool);
        },
        publishTool: function(){
            //uncomment after testing 1
            // if (this.racpackage.created_by != this.user_id || this.racpackage.published){
            //     return false;
            // }
            this.$emit("startLoading", "toolPublish");
            let publish_promise = this.$cadre.axios({
                url: this.$cadreConfig.rac_api_prefix + "/tools/publish",
                method:"POST",
                data: {
                    tool_id: this.ractool.tool_id
                }
            });
            publish_promise.then(
                response => {
                    this.publish_success_open = true;
                    this.$store.commit("racpackage/refreshTools");
                },
                error => {
                    console.error(error);
                    this.publish_error_open = true;
                }
            );
            publish_promise.finally(() => {
                this.publish_tool_open = false;
                this.$emit("stopLoading", "toolPublish");
            });
            this.publish_tool_open = false;
        },
        publishSuccess: function(){
            this.publish_success_open = false;
            this.$emit("toolPublished", this.ractool);
        }       
    },
    watch: {
        RacTool: function() {
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
