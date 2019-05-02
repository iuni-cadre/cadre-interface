<template>
    <div id="app">
        <div class="d-flex justify-content-center">
            <img src="@/assets/under_construction.gif" />
        </div>
        <header class="container">
            <a class="float-right"
               :href="login_url">Login</a>
            <h1>CADRE</h1>
        </header>
        <router-view v-if="token"
                     class="container"
                     @startLoading="startLoading"
                     @stopLoading="stopLoading"
                     :isLoading="is_loading" />
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

        <div v-if="is_loading"
             id="loading-screen"
             class="d-flex align-items-center justify-content-center">
            <div class="loading-content">
                <div class="icon">
                    <fa icon="compact-disc"
                        spin />
                </div>
                <div v-for="(item, index) in loading_queue"
                     :key="`loading_${index}`"
                     v-text="item.message"></div>
            </div>
        </div>
    </div>
</template>
<script>
import { mapGetters } from "vuex";
export default {
    data: function() {
        return {
            error_message: "",
            loading_queue: {},
            loading_timeout: 0,
            max_loading_time: 30000, //30 seconds
            min_loading_time: 500
        };
    },
    computed: {
        ...mapGetters("user", ["authToken"]),
        token: function() {
            return this.authToken;
        },
        login_url: function() {
            return this.$cadreConfig.login_url;
        },
        is_loading: function() {
            return Object.keys(this.loading_queue).length;
        }
    },
    methods: {
        startLoading: function({ key, message }) {
            this.addToLoadingQueue(key, message);
        },
        stopLoading: function({ key }) {
            this.removeFromLoadingQueue(key);
        },
        addToLoadingQueue: function(key, message) {
            if (!this.loading_queue[key]) {
                // this.loading_queue[key] = 0;
                this.$set(this.loading_queue, key, {
                    interval: 0,
                    timer: 0,
                    message: ""
                });
                this.loading_queue[key].interval = setInterval(() => {
                    this.loading_queue[key].timer += 100;
                }, 100);
            }
            this.loading_queue[key].message = message || "";
        },
        removeFromLoadingQueue: function(key) {
            if (this.loading_queue[key] !== undefined) {
                this.loading_queue[key].timer = setTimeout(() => {
                    if (this.loading_queue[key]) {
                        clearInterval(this.loading_queue[key].interval);
                        clearTimeout(this.loading_queue[key].timer);
                        this.$delete(this.loading_queue, key);
                    } else {
                        console.warn(
                            `Loading queue key "${key}" was not found.`
                        );
                    }
                }, this.min_loading_time - this.loading_queue[key].timer);
            }
        }
    },
    mounted: function() {
        this.addToLoadingQueue("initialize");
        // setTimeout(() => {
        //     this.removeFromLoadingQueue("initialize");
        // }, 2);

        this.$store.commit("user/initializeToken");
        let validate_prom = null;
        if (this.$route.query.token && this.$route.query.username) {
            let token = this.$route.query.token;
            let username = this.$route.query.username;
            this.$router.push({
                path: this.$route.path,
                query: {}
            });
            validate_prom = this.$store.dispatch("user/validateToken", {
                token: token,
                username: username
            });
        } else {
            validate_prom = this.$store.dispatch("user/validateToken");
        }

        validate_prom.then(
            result => {
                // console.info("Token valid.");
                // console.debug(this.token);
                this.removeFromLoadingQueue("initialize");
                this.$store.dispatch("user/beatHeart");
            },
            error => {
                this.removeFromLoadingQueue("initialize");
                this.error_message = "Unauthorized";
                console.error("Could not validate token.", error);
            }
        );
    }
};
</script>

<style lang="scss">
@import "../node_modules/bootstrap/scss/bootstrap.scss";

// #app {
//     font-family: "Avenir", Helvetica, Arial, sans-serif;
//     -webkit-font-smoothing: antialiased;
//     -moz-osx-font-smoothing: grayscale;
//     text-align: center;
//     color: #2c3e50;
// }
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

#loading-screen {
    background: rgba(255, 255, 255, 0.6);
    // background: rgba(79, 61, 99, 0.99);
    position: fixed;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;

    .loading-content div.icon {
        font-size: 15rem;
    }
}
</style>
