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
                        <h4 class="btn btn-primary btn-lg">Query Interface</h4>
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
            <h3>Top Packages</h3>&nbsp;&nbsp;
            <div class="row flex-wrap d-flex mb-3">
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
            <router-link
                :to="{name: 'rac-marketplace'}"
                target
                class="btn btn-primary"
            >Visit Full RAC Marketplace</router-link>
            <span class="ml-3 d-inline-block">
                <span v-text="racpackages_total_count"></span> Total Packages
            </span>
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
            <modal
            @close="goToProfile()"
            v-if="welcome_message"
            modal-style="info"
            close-button-label="Go to your User Profile"
            >
                <h5>{{welcome_message}}</h5>
            </modal>
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
            welcome_message: "",
            display_name: "",
            agreement_signed: false,
            testing_page: true
        };
    },
    computed: {
        query_interface_url: function() {
            return this.$cadreConfig.query_interface_url;
        },
        jupyter_url: function() {
            return this.$cadreConfig.jupyter_url;
        },
        token: function() {
            return this.$store.getters["user/authToken"];
        },
        jupyter_token: function() {
            return this.$store.getters["user/jToken"];
        },
        username: function() {
            return this.$store.getters["user/username"];
        },

        racpackages: function() {
            return this.$store.getters["racpackage/packages"].slice(
                0,
                RAC_PACKAGES_TO_SHOW
            );
        },
        racpackages_total_count: function() {
            return this.$store.getters["racpackage/packages"].length;
        }
    },
    methods: {
        goToQueryInterface: function() {
            location.href = `${this.query_interface_url}?username=${this.username}&token=${this.token}`;
        },
        goToNotebook: function() {
            // location.href = this.jupyter_full_url;
            this.$router.push({ name: "jupyter-hub" });
        },
        
        startLoading({key, message}){
            this.$store.commit("loading/addKey", {key, message});
        },
        stopLoading({key}){
            this.$store.commit("loading/removeKey", {key});
        },
        getProfile: function() {
            let prom = new Promise((resolve, reject) => {
                if (this.testing_page === true){
                    let user_profile = sample_user_profile;
                    this.$set(this, "display_name", user_profile.display_name);
                    this.$set(this, "agreement_signed", user_profile.agreement_signed);
                    resolve();
                } 
                else {
                    let axios_prom = this.$cadre.axios({
                        url: this.get_user_profile_endpoint,
                        method: "GET",
                        data:{
                            user_id: this.user_id

                        }
                    });
                    axios_prom.then(
                        response => {
                            let user_profile = response.data;
                            this.$set(this, "display_name", user_profile.display_name);
                            this.$set(this, "agreement_signed", user_profile.display_name);
                            resolve(response);
                        },
                        error => {
                            console.error(error);
                            reject(error);
                        }
                    );
                }
            });
            return prom;
        },
        firstLogin: function() {
            if (this.$store.state.user.cognito_groups != null) {
                if (this.$store.getters["user/cognito_groups"].includes("wos_trial") & !this.agreement_signed){
                    this.welcome_message = "Welcome to CADRE! Before you begin, please update your Display Name and sign the User Agreement."
                } else if (!this.display_name) {
                this.welcome_message = "Welcome to CADRE! Before you begin, please update your Display Name."
            }
            } else if (!this.display_name) {
                this.welcome_message = "Welcome to CADRE! Before you begin, please update your Display Name."
            }
        },
        goToProfile: function() {
            this.$router.push({ name: "your-profile" });
        }
    },
    components: {
        Modal,
        RacPackageCard,
        YourTools,
        YourArchives,
        YourPackages
    },
    mounted: function() {
        if (this.racpackages.length === 0) {
            this.startLoading({ key: "get_packages", message: "" });
            let get_packages_prom = this.$store.dispatch(
                "racpackage/getPackages"
            );
            let get_tools_prom = this.$store.dispatch("racpackage/getTools");
            Promise.all([get_packages_prom, get_tools_prom]).finally(() => {
                //stop loading
                this.stopLoading({ key: "get_packages" });
            });
        }
        this.getProfile();
        this.firstLogin();
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

