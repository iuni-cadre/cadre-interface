<template>
    <div>
        <section>
            <div class="container">
                <h2>Marketplace</h2>
                <!--
########     ###     ######  ##    ##    ###     ######   ########  ######
##     ##   ## ##   ##    ## ##   ##    ## ##   ##    ##  ##       ##    ##
##     ##  ##   ##  ##       ##  ##    ##   ##  ##        ##       ##
########  ##     ## ##       #####    ##     ## ##   #### ######    ######
##        ######### ##       ##  ##   ######### ##    ##  ##             ##
##        ##     ## ##    ## ##   ##  ##     ## ##    ##  ##       ##    ##
##        ##     ##  ######  ##    ## ##     ##  ######   ########  ######
                -->

                <hr />

                <div class="packages-container">
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
                                @packageDeleted="getPackages()"
                                @packagePublished="getPackages()"
                                @packageUnpublished="getPackages()"
                            ></rac-package-card>
                        </div>
                    </div>
                </div>
                <!--
########  #######   #######  ##        ######
   ##    ##     ## ##     ## ##       ##    ##
   ##    ##     ## ##     ## ##       ##
   ##    ##     ## ##     ## ##        ######
   ##    ##     ## ##     ## ##             ##
   ##    ##     ## ##     ## ##       ##    ##
   ##     #######   #######  ########  ######
                -->

                <hr />

                <div class="tools-container">
                    <h3>Tools</h3>
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

                <!--
   ###    ########   ######  ##     ## #### ##     ## ########  ######
  ## ##   ##     ## ##    ## ##     ##  ##  ##     ## ##       ##    ##
 ##   ##  ##     ## ##       ##     ##  ##  ##     ## ##       ##
##     ## ########  ##       #########  ##  ##     ## ######    ######
######### ##   ##   ##       ##     ##  ##   ##   ##  ##             ##
##     ## ##    ##  ##    ## ##     ##  ##    ## ##   ##       ##    ##
##     ## ##     ##  ######  ##     ## ####    ###    ########  ######
                -->
                <hr />

                <div class="archives-container">
                    <h3>Data Archives</h3>
                    <div class="row">
                        <div class="col mb-3">
                            <button
                                class="btn btn-primary"
                                @click="show_create_archive_modal = true"
                            >Create New Data Archive</button>
                        </div>
                    </div>
                    <div class="row flex-wrap">
                        <div
                            v-for="(racarchive, index) in available_archives"
                            :key="`racarchive_card_${index}`"
                            class="col-md-4 d-flex"
                        >
                        </div>
                    </div>
                </div>

                <!-- <create-package-modal :show-modal="show_create_modal"
                @close="show_create_modal = false"></create-package-modal>-->
            </div>
        </section>
    </div>
</template>

<script>
import Modal from "@/components/Common/CommonModal";
import RacPackageCard from "@/components/Marketplace/MarketplaceRacPackageCard";
import CreatePackageModal from "@/components/Marketplace/MarketplaceCreateRacPackageModal";
import NewArchiveForm from "@/components/Marketplace/MarketplaceNewArchiveForm";

export default {
    data: function() {
        return {
            show_create_modal: false,
            show_create_tool_modal: false,
            confirm_tool_create_modal_close: false,
            show_create_archive_modal: false,
            confirm_archive_create_modal_close: false,

            available_tools: [],
            available_archives: [],

            get_archives_endpoint:
                this.$cadreConfig.rac_api_prefix + "/get-archives",
            get_tools_endpoint: this.$cadreConfig.rac_api_prefix + "/get-tools"
        };
    },
    computed: {
        racpackages: function() {
            return this.$store.getters["racpackage/packages"];
        },
        ractools: function() {
            return this.$store.getters["racpackage/tools"];
        },
        refresh_packages: function(){
            return this.$store.state.racpackage.refresh_packages;
        },
        refresh_tools: function(){
            return this.$store.state.racpackage.refresh_tools;
        }
    },
    components: {
        Modal,
        RacPackageCard,
        CreatePackageModal,
        NewArchiveForm
    },
    methods: {
        // openCreateToolModal: function(){
        //     this.show_create_tool_modal = true;
        // }
        getArchives: function() {
            let prom = new Promise((resolve, reject) => {
                //FOR TESTING
                // console.debug(TEST_RAC_ARCHIVES);
                // this.$set(this, "available_archives", TEST_RAC_ARCHIVES)
                // resolve({ status: 200, data: { message: "Test Tools" } });
                // return true;

                if (this.existingTools && this.existingTools.length > 0) {
                    this.$set(
                        this,
                        "available_archives",
                        this.existingArchives
                    );
                    resolve();
                } else {
                    //do ajax
                    // reject({ error: "Test promise." });
                    let axios_prom = this.$cadre.axios({
                        url: this.get_archives_endpoint,
                        method: "GET"
                    });
                    axios_prom.then(
                        response => {
                            let archives = response.data;
                            this.$set(this, "available_archives", archives);
                            resolve(response);
                        },
                        error => {
                            this.error_message.push(
                                "Could not fetch the list of data sets."
                            );
                            reject(error);
                        }
                    );
                }
            });
            return prom;
        },
        getTools: function() {
            let prom = new Promise((resolve, reject) => {
                if (this.existingTools && this.existingTools.length > 0) {
                    this.$set(this, "available_tools", this.existingTools);
                    resolve();
                } else {
                    let axios_prom = this.$cadre.axios({
                        url: this.get_tools_endpoint,
                        method: "GET"
                    });
                    axios_prom.then(
                        response => {
                            let tools = response.data;
                            this.$set(this, "available_tools", tools);
                            resolve(response);
                        },
                        error => {
                            this.error_message.push(
                                "Could not fetch the list of tools."
                            );
                            reject(error);
                        }
                    );
                }
            });
            return prom;
        },
        getPackages: function() {
            this.$store.commit("loading/addKey", { key: "get_packages", message: "" });
            let get_packages_prom = this.$store.dispatch(
                "racpackage/getPackages"
            );
            let get_tools_prom = this.$store.dispatch("racpackage/getTools");
            Promise.all([get_packages_prom, get_tools_prom]).finally(() => {
                //stop loading
                this.$store.commit("loading/removeKey", { key: "get_packages" });
            });
        }
    },
    watch: {
        refresh_packages: function(){
            this.getPackages();
            console.debug("refresh" );
        },
        refresh_tools: function(){
            this.getPackages();
            console.debug("refresh" );
        }
    },
    mounted: function() {
        //start loading
        //look for new packages and tools every time Marketplace is loaded.
        this.getPackages();

    }
};

const TEST_RAC_ARCHIVES=[
    {
        archive_description: "This is a test archive",
        archive_id: "1",
        archive_name: "test1",
        created_on: "2020-01-27T21:03:13.358954+00:00",
        permissions: { data_type: "MAG", other: [] },
        created_by: "1000",
        display_name: "Test User 1"
    },
    {
        archive_description: "This is a test archive",
        archive_id: "112312",
        archive_name: "test2",
        created_on: "2020-01-27T21:03:13.358954+00:00",
        permissions: { data_type: "MAG", other: [] },
        created_by: "1000",
    },
    {
        archive_description: "This is a test archive",
        archive_id: "1122",
        archive_name: "test3",
        created_on: "2020-01-27T21:03:13.358954+00:00",
        permissions: { data_type: "MAG", other: [] },
        created_by: "1200",
    },
    {
        archive_description: "This is a test archive",
        archive_id: "11452",
        archive_name: "test4",
        created_on: "2020-01-27T21:03:13.358954+00:00",
        permissions: { data_type: "MAG", other: [] },
        created_by: "1200",
        display_name: "Test User 2"
    },
]
</script>

<style>
</style>
