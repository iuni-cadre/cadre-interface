<template>
    <section>
        <div class="container">
            <h2>Dashboard</h2>

            <hr />

            <h3>Quick Start</h3>
            <div class="py-3 row quick-start">
                <!-- <button @click="goToQueryInterface()" class="btn btn-primary">Query Interface</button>
            &nbsp;&nbsp;
                <button @click="goToNotebook()" class="btn btn-primary">Jupyter Notebook</button>-->
                <router-link
                    :to="{name: 'query-builder'}"
                    target
                    class="col d-flex"
                >
                    <div class="card flex-fill">
                        <h4 class="btn btn-primary btn-lg">Query Builder</h4>
                        <p>Pick a dataset and run a search query.</p>
                    </div>
                </router-link>
                <!-- <a target="_blank" :href="`${this.query_interface_url}?username=${this.username}&token=${this.token}`" class="btn btn-primary">Query Interface</a> -->

                <!-- <a :href="" class="btn btn-primary">Jupyter Notebook</a> -->
                <router-link
                    :to="{name: 'jupyter-hub'}"
                    target
                    class="col d-flex"
                >
                    <div class="card flex-fill">
                        <h4 class="btn btn-primary btn-lg">Jupyter Notebook</h4>
                        <p>Open a notebook environment to perform complex analytics on CADRE query results</p>
                    </div>
                </router-link>
            </div>
            <hr />
            <div class="d-flex justify-content-between align-items-baseline">
                <h3>Featured Packages</h3>&nbsp;&nbsp;
                <router-link
                    :to="{name: 'rac-marketplace'}"
                    target
                    class
                >Visit Marketplace</router-link>
            </div>
            <div class="">
                <div class="row col" v-if="!racpackages || racpackages.length == 0">
                    Could not find any featured packages.
                </div>
                <div v-else class="row flex-wrap d-flex mb-3">
                    <div
                        v-for="(racpackage, index) in racpackages"
                        :key="`racpackage_card_${index}`"
                        class="col-md-4 flex-fill d-flex"
                    >
                        <rac-package-card
                            @startLoading="startLoading"
                            @stopLoading="stopLoading"
                            :rac-package="racpackage"
                        ></rac-package-card>
                    </div>
                </div>
                
            </div>
            <!-- <span class="ml-3 d-inline-block">
                <span v-text="racpackages_total_count"></span> Total Packages
            </span> -->
            <!-- <div>
            {{jupyter_full_url}}
            </div>-->
            <hr />

            <your-packages
                @startLoading="startLoading"
                @stopLoading="stopLoading"
            ></your-packages>
            <hr />
            <your-tools
                @startLoading="startLoading"
                @stopLoading="stopLoading"
            ></your-tools>
            <hr />
            <your-archives
                @startLoading="startLoading"
                @stopLoading="stopLoading"
            ></your-archives>
            <!-- <modal
            @close="welcome_message = ''"
            v-if="welcome_message"
            modal-style="info"
            hide-footer=true
            >
            
            <div class="form-group">
                {{welcome_message}}
                <hr />
                <div class="form-group">
                <router-link
                :to="{name: 'your-profile'}"
                target
                class="col d-flex"
                >
                    <h3 class="btn btn-primary">Go to your User Profile</h3>
                
                
                </router-link>
                </div>
            </div>
            </modal> -->
        </div>
    </section>
</template>
<script>
import Modal from "@/components/Common/CommonModal";
import RacPackageCard from "@/components/Marketplace/MarketplaceRacPackageCard";
import YourTools from "@/components/Your/YourTools";
import YourArchives from "@/components/Your/YourArchives";
import YourPackages from "@/components/Your/YourPackages";

const RAC_PACKAGES_TO_SHOW = 3;

export default {
    data: function() {
        return {
            racpackages: []
        };
    },
    computed: {
        query_interface_url: function () {
            return this.$cadreConfig.query_interface_url;
        },
        jupyter_url: function () {
            return this.$cadreConfig.jupyter_url;
        },
        token: function () {
            return this.$store.getters["user/authToken"];
        },
        jupyter_token: function () {
            return this.$store.getters["user/jToken"];
        },
        username: function () {
            return this.$store.getters["user/username"];
        },

        // racpackages: function () {
        //     return this.$store.getters["racpackage/packages"].slice(
        //         0,
        //         RAC_PACKAGES_TO_SHOW
        //     );
        // },
        racpackages_total_count: function () {
            return this.$store.getters["racpackage/packages"].length;
        },
    },
    methods: {
        goToQueryInterface: function () {
            location.href = `${this.query_interface_url}?username=${this.username}&token=${this.token}`;
        },
        goToNotebook: function () {
            // location.href = this.jupyter_full_url;
            this.$router.push({ name: "jupyter-hub" });
        },

        startLoading({ key, message }) {
            this.$store.commit("loading/addKey", { key, message });
        },
        stopLoading({ key }) {
            this.$store.commit("loading/removeKey", { key });
        },
        async getFeaturedPackages(){
            this.startLoading({key: "featured"})
            try {
                let response = await this.$cadre.axios({
                    url: `${this.$cadreConfig.rac_api_prefix}/packages/featured`,
                    method: "GET",
                })
                // console.debug(response.data)
                this.racpackages = response.data;
            } catch (error) {
                // throw error;
                console.warn(error);
            }
            finally {
                this.stopLoading({key: "featured"});
            }
        }
        
    },
    components: {
        Modal,
        RacPackageCard,
        YourTools,
        YourArchives,
        YourPackages,
    },
    mounted: async function () {
        if (this.racpackages.length === 0) {
            this.startLoading({ key: "get_packages", message: "" });
            let get_packages_prom = this.$store.dispatch(
                "racpackage/getPackages"
            );
            this.getFeaturedPackages();
            let get_tools_prom = this.$store.dispatch("racpackage/getTools");
            Promise.all([get_packages_prom, get_tools_prom]).finally(() => {
                //stop loading
                this.stopLoading({ key: "get_packages" });
            });
        }
    }
};

const sample_user_profile = {
    user_id: 1000,
    display_name: "Test User",
    agreement_signed: true,
    date_agreement_signed: "2020-02-07T21:10:46.773823+00:00"
}
</script>
<style lang="scss" scoped>
.quick-start > a {
    text-decoration: none;
}
</style>

