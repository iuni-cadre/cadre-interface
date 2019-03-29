<template>
    <div>
        <h2>Dashboard</h2>

        <hr />

        <div>
            <button @click="goToQueryInterface()" class="btn btn-primary">Go To Query Interface</button>
            &nbsp;&nbsp;
            <button @click="goToNotebook()" class="btn btn-primary">Go To Jupyter Notebook</button>
        </div>
        <div>
            {{jupyter_full_url}}
        </div>
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
        "jupyter_full_url": function(){
            return `${this.jupyter_url}/user/${this.username}/tree/?token=${this.jupyter_token}`;
        }

    },
    methods: {
        goToQueryInterface: function(){
            location.href = `${this.query_interface_url}?username=${this.username}&token=${this.token}`;
        },
        goToNotebook: function(){
            location.href = this.jupyter_full_url;
        }
    },
    mounted: function() {
    }
};
</script>
<style lang="scss">
</style>

