<template>
    <div>
        <h2>Dashboard</h2>

        <hr />

        <div>
            <!-- <button @click="goToQueryInterface()" class="btn btn-primary">Query Interface</button>
            &nbsp;&nbsp;
            <button @click="goToNotebook()" class="btn btn-primary">Jupyter Notebook</button> -->
            <router-link :to="{name: 'query-builder'}" target="_blank" class="btn btn-primary">Query Interface</router-link>
            <!-- <a target="_blank" :href="`${this.query_interface_url}?username=${this.username}&token=${this.token}`" class="btn btn-primary">Query Interface</a> -->
            &nbsp;&nbsp;
            <!-- <a :href="" class="btn btn-primary">Jupyter Notebook</a> -->
            <router-link :to="{name: 'jupyter-hub'}" target="_blank" class="btn btn-primary">Jupyter Notebook</router-link>
        </div>
        <!-- <div>
            {{jupyter_full_url}}
        </div> -->
    </div>
</template>
<script>
export default {
    data: function() {
        return {

        };
    },
    computed: {
        "query_interface_url": function(){
            return this.$cadreConfig.query_interface_url;
        },
        "jupyter_url": function(){
            return this.$cadreConfig.jupyter_url;
        },
        "token": function(){
            return this.$store.getters["user/authToken"];
        },
        "jupyter_token": function(){
            return this.$store.getters["user/jToken"];
        },
        "username": function(){
            return this.$store.getters["user/username"];
        },

    },
    methods: {
        goToQueryInterface: function(){
            location.href = `${this.query_interface_url}?username=${this.username}&token=${this.token}`;
        },
        goToNotebook: function(){
            // location.href = this.jupyter_full_url;
            this.$router.push({name: "jupyter-hub"});
        }
    },
    mounted: function() {
    }
};
</script>
<style lang="scss">
</style>

