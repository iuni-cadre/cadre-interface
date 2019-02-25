<template>
    <div id="app">
        {{token}}
        <header class="container">
            <h1>CADRE</h1>
        </header>
        <router-view v-if="token"
                     class="container" />
        <template v-else-if="error_message">
            <div class="container">
                <div class="alert alert-danger">Error: <span v-text="error_message"></span></div>
            </div>
        </template>
        <template v-else>
            <div class="container">
                Loading...
            </div>
        </template>
    </div>
</template>
<script>
export default {
    data: function() {
        return {
            error_message: ""
        };
    },
    computed: {
        token: function() {
            //if has token and token is valid
            return this.$store.getters["user/authToken"] && this.$store.getters["user/tokenIsValid"];
        }
    },
    mounted: function() {
        let validate_prom = null;
        if (this.$route.query.token) {
            let token = this.$route.query.token;
            this.$router.push({
                path: this.$route.path,
                query: {}
            });
            validate_prom = this.$store.dispatch("user/validateToken", token);
        } else {
            validate_prom = this.$store.dispatch("user/validateToken");
        }

        validate_prom.then(
            result => {
                // console.info("Token valid.");
            },
            error => {
                this.error_message = "Unauthorized";
                console.error("Could not validate token.", error);
            }
        );
    }
};
</script>

<style lang="scss">
@import "../node_modules/bootstrap/scss/bootstrap.scss";

#app {
    //   font-family: 'Avenir', Helvetica, Arial, sans-serif;
    //   -webkit-font-smoothing: antialiased;
    //   -moz-osx-font-smoothing: grayscale;
    //   text-align: center;
    //   color: #2c3e50;
}
#nav {
    padding: 30px;
    a {
        font-weight: bold;
        color: #2c3e50;
        &.router-link-exact-active {
            color: #42b983;
        }
    }
}
</style>
