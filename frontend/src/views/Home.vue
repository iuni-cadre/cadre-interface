<template>
    <div>
        <h2>Dashboard</h2>

        <hr />

        <div>
            <button @click="goToQueryInterface()" class="btn btn-primary">Go To Query Interface</button>
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
        "token": function(){
            return this.$store.getters["user/authToken"];
        },
        "username": function(){
            return this.$store.getters["user/username"];
        }

    },
    methods: {
        goToQueryInterface: function(){
            location.href = `${this.query_interface_url}?username=${this.username}&token=${this.token}`;
        }
    },
    mounted: function() {
    }
};
</script>
<style lang="scss">
</style>

