<template>
    <section>
        <div class="container">
            <h2>Dashboard</h2>

            <hr />

            <h3>Quick Start</h3>
            <div class="py-3 row quick-start" style="margin-bottom: 200px">
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
            <!-- <span class="ml-3 d-inline-block">
                <span v-text="racpackages_total_count"></span> Total Packages
            </span> -->
            <!-- <div>
            {{jupyter_full_url}}
            </div>-->
            <hr />
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
import YourTools from "@/components/Your/YourTools";
import YourArchives from "@/components/Your/YourArchives";
import YourPackages from "@/components/Your/YourPackages";

const RAC_PACKAGES_TO_SHOW = 3;

export default {
    data: function() {
        return {
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

    },
    components: {
        Modal,
        YourTools,
        YourArchives,
        YourPackages,
    },
    mounted: async function () {
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

