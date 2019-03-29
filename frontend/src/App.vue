<template>
    <div id="app">
        <header class="container">
            <h1>CADRE</h1>
            <div v-if="!token">
                <a :href="login_url">Login</a>
            </div>
        </header>
        <!-- {{$store.getters["user/authToken"]}} -->
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
import { mapGetters } from 'vuex'
export default {
    data: function() {
        return {
            error_message: ""
        };
    },
    computed: {
        // token: function() {
        //     //if has token and token is valid
        //     // console.debug(this.$store.getters["user/authToken"])
        //     return (
        //         // this.$store.getters["user/authToken"] &&
        //         this.$store.getters["user/tokenIsValid"]
        //     );
        // },

        ...mapGetters("user", ['authToken']),
        token: function(){ return this.authToken; },
        login_url: function() {
            return this.$cadreConfig.login_url;
        }
    },
    mounted: function() {
        this.$store.commit("user/initializeToken");
        let validate_prom = null;
        if (this.$route.query.cadre_token && this.$route.query.username) {
            let token = this.$route.query.cadre_token;
            let username = this.$route.query.username;
            let jupyter_token = this.$route.query.jupyter_token;
            this.$router.push({
                path: this.$route.path,
                query: {}
            });
            // console.debug(token, jupyter_token);
            validate_prom = this.$store.dispatch("user/validateToken", {token:token, username:username, j_token:jupyter_token});
        } else {
            validate_prom = this.$store.dispatch("user/validateToken");
        }

        validate_prom.then(
            result => {
                // console.info("Token valid.");
                // console.debug(this.token);
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
