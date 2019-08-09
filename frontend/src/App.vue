<template>
    <div id="app">
        <!-- <header class="container">
            <div v-if="!token">
                <a class="float-right"
                   :href="login_url">Login</a>
            </div>
            <router-link :to="{name: 'home'}">
                <h1>CADRE</h1>
            </router-link>
        </header> -->

        <header id="main-header">
            <nav class="container navbar navbar-expand-lg">
                <router-link class="navbar-brand"
                             :to="{name: 'home'}"><img src="@/assets/img/logo-and-type.svg"
                         alt="CADRE" /><span class="d-none">CADRE</span></router-link>
                <button class="navbar-toggler"
                        type="button"
                        data-toggle="collapse"
                        data-target="#navbarSupportedContent"
                        aria-controls="navbarSupportedContent"
                        aria-expanded="false"
                        aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>

                <div class="collapse navbar-collapse"
                     id="navbarSupportedContent">
                    <ul class="navbar-nav mr-auto">
                        <!-- {% for page in pages.children if page.header.main == true %} -->
                        <!-- <li class="nav-item">
                            <a href="{{url(page.url)}}">{{page.title}}</a>
                        </li> -->
                        <!-- {% endfor %} -->

                        <li class="nav-item">
                            <router-link :to="{name: 'query-builder'}"
                                         target="">Query Interface</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link :to="{name: 'jupyter-hub'}"
                                         target="">Jupyter Notebook</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link :to="{name: 'rac-marketplace'}"
                                         target="">RAC Marketplace</router-link>
                        </li>

                    </ul>

                    <div v-if="!token">
                        <a class="btn get-started-button"
                           :href="login_url">Login</a>
                    </div>
                    <div v-else>
                        Logged in as <span v-text="username"></span>
                    </div>

                </div>
            </nav>

        </header>

        <section v-if="is_under_construction"
                 class="d-flex justify-content-center construction">
            <img src="@/assets/under_construction.gif" />
        </section>

        <!-- <hr /> -->
        <!-- {{$store.getters["user/authToken"]}} -->
        <router-view v-if="token"
                     class=""
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
                    <fa icon="circle-notch"
                        spin />
                </div>
                <div v-for="(item, index) in loading_queue"
                     :key="`loading_${index}`"
                     v-text="item.message"></div>
            </div>
        </div>

        <footer id="main-footer">
            <div class="container">
                <div class="row">
                    <div class="col">
                        <a href="https://cadre.iu.edu"
                           class="cadre-logo"><img src="@/assets/img/logo-and-type.svg"
                                 alt="CADRE" /><span class="d-none">CADRE</span></a>
                        <!-- <div class="d-flex justify-content-between social-icons">
                            {# <a href=""><i class="fab fa-facebook-square"></i></a> #}
                            <a href=""><i class="fab fa-twitter"></i></a>
                            {# <a href=""><i class="fab fa-instagram"></i></a> #}
                        </div> -->
                    </div>
                    <div class="col">
                        &copy; <a href="https://iuni.iu.edu">Indiana University Network Science Institute</a>
                    </div>
                    <div class="col">
                        <a href="https://iuni.iu.edu"
                           class="cadre-logo"><img src="@/assets/img/iuni-logo.png"
                                 alt="CADRE" /><span class="d-none">IUNI</span></a>
                    </div>

                    <!-- {% for page in pages.children if page.header.main == true %}
            <div class="col">
                <a href="{{url(page.url)}}"><strong>{{page.title}}</strong></a>
                <ul class="list-unstyled">
                    {% for subpage in page.children %}
                    <li class="list-item">
                        <a href="{{url(subpage.url)}}">{{subpage.title}}</a>
                    </li>
                    {% endfor %}
                </ul>
            </div>
            {% endfor %}

            {# <div class="col">
                <strong>About CADRE</strong>
                {{site.title}}
                {% for mitem in site.menu %}
            <li>
                <a {% if mitem.class %}class="{{ mitem.class }}"{% endif %} href="{{ mitem.url }}">
                    {% if mitem.icon %}<i class="fa fa-{{ mitem.icon }}"></i>{% endif %}
                    {{ mitem.text }}
                </a>
            </li>
        {% endfor %} #} -->

                    <!-- {# </div>
            <div class="col">
                <strong>Documentation</strong>
            </div>
            <div class="col">
                <strong>Work With Us</strong>
            </div>
            <div class="col">
                <strong>Resources</strong>
            </div> #} -->
                </div>

            </div>
        </footer>
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
        ...mapGetters("user", ["authToken", "username"]),
        token: function() {
            return this.authToken;
        },
        login_url: function() {
            return this.$cadreConfig.login_url;
        },
        is_loading: function() {
            return Object.keys(this.loading_queue).length;
        },
        is_under_construction: function() {
            return this.$cadreConfig.under_construction;
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
        },
        validate: function() {
            // setTimeout(() => {
            //     this.removeFromLoadingQueue("initialize");
            // }, 2);

            this.$store.commit("user/initializeToken");
            let validate_prom = null;
            // console.debug(this.$route.query);
            // console.debug(this.$route);
            if (this.$route.query.cadre_token && this.$route.query.username) {
                let token = this.$route.query.cadre_token;
                let username = this.$route.query.username;
                let jupyter_token = this.$route.query.jupyter_token;
                this.$router.push({
                    path: this.$route.path,
                    query: {}
                });
                // console.debug(token, jupyter_token);
                validate_prom = this.$store.dispatch("user/validateToken", {
                    token: token,
                    username: username,
                    j_token: jupyter_token
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
    },
    mounted: function() {
        this.addToLoadingQueue("initialize");
        this.validate();
    },
    watch: {
        // "$route.query": function(){
        // }
    }
};
</script>

<style lang="scss">
@import "../node_modules/bootstrap/scss/bootstrap.scss";
@import "@/assets/cadre.scss";
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

#loading-screen {
    background: rgba(255, 255, 255, 0.6);
    // background: rgba(79, 61, 99, 0.99);
    z-index: 5000;
    position: fixed;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;

    .loading-content div.icon {
        font-size: 15rem;
    }
}

.construction img {
    max-width: 100%;
}
</style>
