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
        startLoading({ key, message }) {
            this.$store.commit("loading/addKey", { key, message });
        },
        stopLoading({ key }) {
            this.$store.commit("loading/removeKey", { key });
        },
        loadPackage() {
            let url = `${this.$cadreConfig.rac_api_prefix}/packages/get-package/${this.package_id}`;
            // console.debug(url);
            let prom = this.axios({
                url: url,
                method: "GET",
                responseType: "json",
            });

            prom.then(
                (response) => {
                    this.racpackage = response.data;
                    console.debug(this.racpackage)
                },
                (error) => {
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
            );
            return prom;
        },
    },
    computed: {
        package_id() {
            return this.$route.params.package_id;
        },
    },
    mounted() {
        this.startLoading({ key: "loading-package" });
        this.loadPackage().finally(() => {
            this.stopLoading({ key: "loading-package" });
        });
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