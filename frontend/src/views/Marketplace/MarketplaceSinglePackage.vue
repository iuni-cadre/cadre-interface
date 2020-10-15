<script>
import RacPackageCard from "@/components/Marketplace/MarketplaceRacPackageCard";
import Modal from "@/components/Common/CommonModal";
export default {
    name: "single-package",
    components: {
        RacPackageCard,
        Modal,
    },
    data() {
        return {
            racpackage: null,
            error_message: "",
        };
    },
    methods: {
        updatePageTitle(){
            let name = this.racpackage && this.racpackage.name
            console.debug(name);
            this.$emit("update-page-title", `${name}`)
        },
        startLoading({ key, message }) {
            this.$store.commit("loading/addKey", { key, message });
        },
        stopLoading({ key }) {
            this.$store.commit("loading/removeKey", { key });
        },
        async loadPackage() {
            let url = `${this.$cadreConfig.rac_api_prefix}/packages/get-package/${this.package_id}`;
            // console.debug(url);
            try {
                let response = await this.$cadre.axios({
                    url: url,
                    method: "GET",
                    responseType: "json",
                });

                this.racpackage = response.data;
                console.debug(this.racpackage)

            }catch(error) {
                if (error.response && error.response.status == 404) {
                    this.error_message =
                        "Requested package could not be found.";
                } else if (error.response && error.response.data && error.response.data.error){
                    this.error_message = error.response.data.error;
                }
                else {
                    this.error_message = "An unknown error occurred.";
                }
            }
        },
    },
    computed: {
        package_id() {
            return this.$route.params.package_id;
        },
    },
    async mounted() {
        this.startLoading({ key: "loading-package" });
        try {
            await this.loadPackage();
        }
        catch(error){

        }
        this.stopLoading({ key: "loading-package" });
        this.updatePageTitle();
    },
};
</script>

<template>
    <div class="container mt-3">
        <modal
            v-if="error_message"
            modal-type="error"
            modal-style="danger"
            @close="
                () => {
                    error_message = '';
                }
            "
        >
            <div v-text="error_message"></div>
        </modal>

        <rac-package-card
            v-if="racpackage"
            show-description="true"
            @startLoading="startLoading"
            @stopLoading="stopLoading"
            :rac-package="racpackage"
        ></rac-package-card>
    </div>
</template>

<style>
</style>