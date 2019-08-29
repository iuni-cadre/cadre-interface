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
                        @click="toggleMenu"
                        data-toggle="collapse"
                        data-target="#navbarSupportedContent"
                        aria-controls="navbarSupportedContent"
                        aria-expanded="false"
                        aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"><fa icon="bars" /></span>
                </button>

                <div class="collapse navbar-collapse"
                    :class="{'show': display_menu}"
                     id="navbarSupportedContent">
                    <ul class="navbar-nav mr-auto">
                        <!-- {% for page in pages.children if page.header.main == true %} -->
                        <!-- <li class="nav-item">
                            <a href="{{url(page.url)}}">{{page.title}}</a>
                        </li> -->
                        <!-- {% endfor %} -->

                        <li class="nav-item">
                            <router-link class="p-3 p-md-0 d-inline-block" :to="{name: 'query-builder-builder'}"
                                         target="">Query Interface</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link class="p-3 p-md-0 d-inline-block" :to="{name: 'jupyter-hub'}"
                                         target="">Jupyter Notebook</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link class="p-3 p-md-0 d-inline-block" :to="{name: 'rac-marketplace'}"
                                         target="">Marketplace</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link class="p-3 p-md-0 d-inline-block" :to="{name: 'jobs-list'}"
                                         target="">Job Status</router-link>
                        </li>

                    </ul>

                    <div v-if="!token">
                        <a class="btn get-started-button"
                           :href="login_url"><span class="p-3 p-md-0 d-inline-block">Login</span></a>
                    </div>
                    <div v-else>
                        Logged in as <span v-text="decodedUsername"></span>
                        &nbsp;
                        <a class="btn get-started-button"
                           @click="logout"><span class="p-3 p-md-0 d-inline-block">Logout</span></a>
                    </div>

                </div>
            </nav>

        </header>

        <section v-if="is_under_construction"
                 class="d-flex justify-content-center construction alert-warning">
            <!-- <img src="@/assets/under_construction.gif" /> -->

            <b>Work In Progress:&nbsp;</b> This application is currently under development. Design, features, and functionality will likely change prior to release.

        </section>

        <!-- <hr /> -->
        <!-- {{$store.getters["user/authToken"]}} -->
        <router-view v-if="token"
                     class=""
                     @startLoading="startLoading"
                     @stopLoading="stopLoading"
                     :isLoading="is_loading" />

        <template v-if="error_message">
            <div class="container pt-3">
                <div class="alert alert-danger">Error: <span v-text="error_message"></span></div>
            </div>
        </template>
        <template v-if="!token">
            <div class="container pt-3">
                <div class="alert alert-info">
                    You are not logged in.  You can log in <a class=""
                           :href="login_url"><span class="">here</span></a>.
                    </div>
                </div>
        </template>

        <div v-if="is_loading"
             id="loading-screen"
             class="d-flex align-items-center justify-content-center">
            <div class="loading-content">
                <div class="icon">
                    <!-- <fa icon="circle-notch"
                        spin /> -->
                    <spinner></spinner>
                </div>
                <div v-for="(item, index) in loading_queue"
                     :key="`loading_${index}`"
                     v-text="item.message"></div>
            </div>
        </div>

        <footer id="main-footer">
            <div class="container">
                <div class="logos d-flex flex-wrap flex-md-nowrap justify-content-between align-items-center">
                    <!-- <div class=""> -->
                        <a href="https://cadre.iu.edu"
                           class="cadre-logo"><img src="@/assets/img/cadre-logo.png"
                                 alt="CADRE" /><span class="d-none">CADRE</span></a>

                    <!-- </div> -->
                    <!-- <div class="">
                        &copy; <a href="https://iuni.iu.edu">Indiana University Network Science Institute</a>
                    </div> -->
                    <!-- <div class=""> -->
                        <a href="https://www.btaa.org/"
                           class="btaa-logo"><img src="@/assets/img/btaa-logo.png"
                                 alt="BTAA" /><span class="d-none">BTAA</span></a>
                    <!-- </div> -->
                    <!-- <div class=""> -->
                        <a href="https://libraries.indiana.edu/"
                           class="libraries-logo"><img src="@/assets/img/iu-libraries-logo.png"
                                 alt="IU Libraries" /><span class="d-none">IU Libraries</span></a>
                    <!-- </div> -->
                    <!-- <div class=""> -->
                        <a href="https://iuni.iu.edu"
                           class="iuni-logo"><img src="@/assets/img/iuni-logo.png"
                                 alt="IUNI" /><span class="d-none">IUNI</span></a>
                    <!-- </div> -->

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
import Spinner from "@/components/Common/CommonSpinner";

// import CryptoJS from "crypto-js";
import Base32 from "hi-base32";

import { mapGetters } from "vuex";
export default {
    data: function() {
        return {
            error_message: "",
            loading_queue: {},
            loading_timeout: 0,
            max_loading_time: 30000, //30 seconds
            min_loading_time: 500,
            display_menu: false
        };
    },
    computed: {
        ...mapGetters("user", ["authToken", "decodedUsername", "roles"]),
        token: function() {
            return this.authToken;
        },
        login_url: function() {
            return this.$cadreConfig.login_url;
        },
        logout_url: function() {
            return this.$cadreConfig.logout_url;
        },
        is_loading: function() {
            return Object.keys(this.loading_queue).length;
        },
        is_under_construction: function() {
            return this.$cadreConfig.under_construction;
        }
    },
    methods: {
        toggleMenu: function(){
            this.display_menu = !this.display_menu;
        },
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
        },

        logout: function() {
            this.startLoading("logout");

            let logout_prom = this.$store.dispatch("user/logout");

            logout_prom.then(
                response => {
                    window.location.href = this.$cadreConfig.logout_url;
                },
                error => {
                    this.error_message = "Could not log out.";
                }
            );

            logout_prom.finally(() => {
                this.stopLoading("logout");
            });
        }
    },
    mounted: function() {
        // this.addToLoadingQueue("test");
        this.addToLoadingQueue("initialize");
        this.validate();

        // let encoded = Base32.encode('this is a test');
        // console.debug(encoded);

        // console.debug(Base32.decode('MNYGK3DJNNQW4'));

        // var rawStr = "hello world!";
        // var wordArray = CryptoJS.enc.Utf8.parse(rawStr);
        // var base64 = CryptoJS.enc.Base64.stringify(wordArray);
        // console.log("encrypted:", base64);

        // //decrypt
        // // var parsedWordArray = CryptoJS.enc.Base64.parse(base64);
        // var parsedWordArray = CryptoJS.enc.Base64.parse("YW55IGNhcm5hbCBwbGVhcw==");
        // var parsedStr = parsedWordArray.toString(CryptoJS.enc.Utf8);
        // console.log("parsed:", parsedStr);
        // var parsedWordArray = CryptoJS.enc.Base64.parse("YW55IGNhcm5hbCBwbGVhcw=");
        // var parsedStr = parsedWordArray.toString(CryptoJS.enc.Utf8);
        // console.log("parsed:", parsedStr);
        // var parsedWordArray = CryptoJS.enc.Base64.parse("YW55IGNhcm5hbCBwbGVhcw");
        // var parsedStr = parsedWordArray.toString(CryptoJS.enc.Utf8);
        // console.log("parsed:", parsedStr);
        // var parsedWordArray = CryptoJS.enc.Base64.parse("YW55IGNhcm5hbCBwbGVhcw===");
        // var parsedStr = parsedWordArray.toString(CryptoJS.enc.Utf8);
        // console.log("parsed:", parsedStr);
    },
    components: {
        Spinner
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

#main-footer {
    .logos {
        position: relative;
        max-width: 100%;
        // border: solid blue 1px;
    }
    .logos a {
        // border: solid blue 1px;
        display: block;
        padding:  1rem;
    }
    .logos img
    {
        // border: solid blue 1px;
        max-width: 100%;
    }

}
</style>
