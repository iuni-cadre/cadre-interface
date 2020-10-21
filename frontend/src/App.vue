
<script>
import Spinner from "@/components/Common/CommonSpinner";
import Modal from "@/components/Common/CommonModal";

const TITLE = "CADRE Big Data Gateway";

// import CryptoJS from "crypto-js";
import Base32 from "hi-base32";

import { mapGetters } from "vuex";
export default {
    data() {
        return {
            error_message: "",
            // loading_queue: {},
            // loading_timeout: 0,
            // max_loading_time: 30000, //30 seconds
            // min_loading_time: 500,
            ready: false,
            display_menu: false,
            welcome_message: "",
            // display_name: "",
            agreement_signed: false,
            testing_page: false
        };
    },
    computed: {
        display_name(){
            return this.profile.display_name;
        },
        version() {
            return this.$version;
        },
        ...mapGetters("user", ["authToken", "decodedUsername", "roles", "profile"]),
        token() {
            return this.authToken;
        },
        login_url() {
            return this.$cadreConfig.login_url;
        },
        logout_url() {
            return this.$cadreConfig.logout_url;
        },
        is_loading() {
            return this.$store.getters["loading/is_loading"];
            // return Object.keys(this.loading_queue).length;
        },
        loading_queue() {
            return this.$store.getters["loading/loading_queue"];
        },
        is_under_construction() {
            return this.$cadreConfig.under_construction;
        },
    },
    methods: {
        toggleMenu() {
            this.display_menu = !this.display_menu;
        },
        startLoading({ key, message }) {
            this.addToLoadingQueue(key, message);
        },
        stopLoading({ key }) {
            this.removeFromLoadingQueue(key);
        },
        addToLoadingQueue(key, message) {
            this.$store.commit("loading/addKey", { key, message });
            // if (!this.loading_queue[key]) {
            //     // this.loading_queue[key] = 0;
            //     this.$set(this.loading_queue, key, {
            //         interval: 0,
            //         timer: 0,
            //         cooldown_timeout: 0,
            //         message: ""
            //     });
            //     this.loading_queue[key].interval = setInterval(() => {
            //         /*
            //             we need to keep track of how long this key has been
            //             loading so we can show the spinner for at least a minimum
            //             amount of time.
            //         */
            //         this.loading_queue[key].timer += 100;
            //     }, 100);
            // } else {
            //     /*
            //         Handles a race condition if we add the key again during the "cooldown" time,
            //         we need to cancel the old cooldown timer so that
            //         it doesn't cancel the NEW instance when it thinks it's
            //         canceling the old instance.  So just cancel the cooldown
            //         and keep going.
            //     */
            //     clearTimeout(this.loading_queue[key].cooldown_timeout);
            // }
            // this.loading_queue[key].message = message || "";
        },
        removeFromLoadingQueue(key) {
            this.$store.commit("loading/removeKey", { key });
            // if (this.loading_queue[key] !== undefined) {
            //     /*
            //         we want to make sure that the spinner is shown for at least half a second
            //         for UX purposes.  So it's not just a flash and people can't see it.
            //         If the given key has been loading for more than the minimum time, just go
            //         ahead and call the callback.  Otherwise, we need to keep spinning for the
            //         min load time minus the time it's already been spinning during the actual
            //         loading.
            //     */
            //     let cooldown_time = Math.max(
            //         this.min_loading_time - this.loading_queue[key].timer,
            //         1
            //     );
            //     /*
            //         After the given cooldown time cancel the time tracking interval,
            //         the cooldown timeout, and remove the key from the loading queue.
            //     */
            //     this.loading_queue[key].cooldown_timeout = setTimeout(() => {
            //         if (this.loading_queue[key]) {
            //             clearInterval(this.loading_queue[key].interval);
            //             clearTimeout(this.loading_queue[key].cooldown_timeout);
            //             this.$delete(this.loading_queue, key);
            //         } else {
            //             console.warn(
            //                 `Loading queue key "${key}" was not found.`
            //             );
            //         }
            //     }, cooldown_time);
            // }
        },
        validate() {
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
                    query: {},
                });
                // console.debug(token, jupyter_token);
                validate_prom = this.$store.dispatch("user/validateToken", {
                    token: token,
                    username: username,
                    j_token: jupyter_token,
                });
            } else {
                validate_prom = this.$store.dispatch("user/validateToken");
            }

            validate_prom.then(
                (result) => {
                    // console.info("Token valid.");
                    // console.debug(this.token);
                    // this.removeFromLoadingQueue("initialize");
                    this.$store.dispatch("user/beatHeart");
                },
                (error) => {
                    // this.removeFromLoadingQueue("initialize");
                    this.error_message = "Unauthorized";
                    console.warn("Could not validate token.", error);
                }
            );
            return validate_prom;
        },

        logout() {
            this.startLoading("logout");

            let logout_prom = this.$store.dispatch("user/logout");

            logout_prom.then(
                (response) => {
                    window.location.href = this.$cadreConfig.logout_url;
                },
                (error) => {
                    this.error_message = "Could not log out.";
                }
            );

            logout_prom.finally(() => {
                this.stopLoading("logout");
            });
        },

        async getProfile() {
            try {
                await this.$store.dispatch("user/getProfile");
            }
            catch(error) {
                console.warn(error);
            }
            let user_profile = this.$store.getters["user/profile"];
            // this.display_name = user_profile.display_name;
            this.agreement_signed = user_profile.agreement_signed;

        },
        firstLogin() {
            if(!this.ready) //wait until we've gotten the profile before we start checking for display name
            {
                return;
            }

            const welcome_message = "Welcome to CADRE! Before you begin, please update your Display Name."
            if (this.$store.getters["user/cognito_groups"].includes("wos_trial") && !this.agreement_signed){
                this.goToProfile()
                this.welcome_message = "Welcome to CADRE! Before you begin, please update your Display Name and sign the User Agreement."
            } else if (!this.display_name) {
                this.goToProfile()
                this.welcome_message = welcome_message;
            } else {
                this.welcome_message = "";
            }
        },
        goToProfile() {
            this.welcome_message = ""
            if(this.$route.name != "your-profile"){
                this.$router.push({ name: "your-profile" });
            }
        },
        updateTitle(name){
            // console.debug(name)
            if(!this.authToken)
            {
                document.title=`Log In - ${TITLE}`;
            }
            else
            {
                let title = this.$route.meta && this.$route.meta.title;
                document.title=`${name?name+ ' - ':''}${title?title+ ' - ':''}${TITLE}`;
            }
        }
    },
    async mounted() {
        this.addToLoadingQueue({key: "initializing"})
        try {
            await this.validate();
            await this.getProfile();
        } catch(e) {
            console.warn(e);
        }

        this.ready = true;
        this.$nextTick(()=>{
            this.firstLogin();
        });

        this.removeFromLoadingQueue({key: "initializing"})
        
        this.updateTitle();

    },
    components: {
        Spinner,
        Modal
    },
    watch: {
        "$route.name"(){
            this.firstLogin();
            this.updateTitle();
            
        },
        "authToken"(){
            this.updateTitle();
        }
    },
};

// ######## ######## ##     ## ########  ##          ###    ######## ########
//    ##    ##       ###   ### ##     ## ##         ## ##      ##    ##
//    ##    ##       #### #### ##     ## ##        ##   ##     ##    ##
//    ##    ######   ## ### ## ########  ##       ##     ##    ##    ######
//    ##    ##       ##     ## ##        ##       #########    ##    ##
//    ##    ##       ##     ## ##        ##       ##     ##    ##    ##
//    ##    ######## ##     ## ##        ######## ##     ##    ##    ########
</script>
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
        </header>-->

        <header id="main-header">
            <nav class="container navbar navbar-expand-lg">
                <router-link
                    class="navbar-brand"
                    :to="{name: 'home'}"
                >
                    <img
                        src="@/assets/img/logo-and-type.svg"
                        alt="CADRE"
                    />
                    <span class="d-none">CADRE</span>
                </router-link>
                <button
                    class="navbar-toggler"
                    type="button"
                    @click="toggleMenu"
                    data-toggle="collapse"
                    data-target="#navbarSupportedContent"
                    aria-controls="navbarSupportedContent"
                    aria-expanded="false"
                    aria-label="Toggle navigation"
                >
                    <span class="navbar-toggler-icon">
                        <fa icon="bars" />
                    </span>
                </button>

                <div
                    v-if="token"
                    class="collapse navbar-collapse"
                    :class="{'show': display_menu}"
                    id="navbarSupportedContent"
                >
                    <ul class="navbar-nav mr-auto">
                        <!-- {% for page in pages.children if page.header.main == true %} -->
                        <!-- <li class="nav-item">
                            <a href="{{url(page.url)}}">{{page.title}}</a>
                        </li>-->
                        <!-- {% endfor %} -->

                        <li class="nav-item">
                            <router-link
                                class="p-3 p-md-0 d-inline-block"
                                :to="{name: 'home'}"
                                target
                            >Dashboard</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link
                                class="p-3 p-md-0 d-inline-block"
                                :to="{name: 'query-builder-builder'}"
                                target
                            >Query Builder</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link
                                class="p-3 p-md-0 d-inline-block"
                                :to="{name: 'jobs-list'}"
                                target
                            >Job Status</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link
                                class="p-3 p-md-0 d-inline-block"
                                :to="{name: 'jupyter-hub'}"
                                target
                            >Notebook</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link
                                class="p-3 p-md-0 d-inline-block"
                                :to="{name: 'rac-marketplace'}"
                                target
                            >Marketplace</router-link>
                        </li>
                        <!-- <li class="nav-item">
                            <router-link class="p-3 p-md-0 d-inline-block"
                                         :to="{name: 'your-home'}"
                                         target="">Your CADRE</router-link>
                        </li>-->
                    </ul>

                    <div v-if="!token">
                        <!-- <a
                            class="btn get-started-button"
                            :href="login_url"
                        >
                            <span class="p-3 p-md-0 d-inline-block">Login</span>
                        </a>-->
                    </div>
                    <div v-else>
                        Logged in as
                        <router-link
                            class="p-3 p-md-0 d-inline-block"
                            :to="{name: 'your-profile'}"
                            target
                        >
                            <span v-text="display_name || decodedUsername" :title="decodedUsername"></span>
                        </router-link>&nbsp;
                        <button
                            class="btn get-started-button"
                            @click="logout"
                        >
                            <span class="p-3 p-md-0 d-inline-block">Log Out</span>
                        </button>
                    </div>
                </div>
            </nav>
        </header>

        <section
            v-if="version.warning"
            class="d-flex justify-content-center construction alert-warning small p-1"
        >
            <div>
                <div
                    class="text-center"
                    v-if="is_under_construction"
                >
                    <img src="@/assets/under_construction.gif" />
                </div>
                <span v-text="version.warning"></span>
            </div>
        </section>

        <template v-if="error_message && token">
            <div class="container pt-3">
                <div class="alert alert-danger">
                    Error:
                    <span v-text="error_message"></span>
                </div>
            </div>
        </template>

        <router-view
            v-if="token"
            class
            @startLoading="startLoading"
            @stopLoading="stopLoading"
            @update-page-title="updateTitle"
            @update-profile="getProfile"
            :isLoading="is_loading"
        />

        <modal
            @close="goToProfile()"
            v-if="token && welcome_message"
            modal-style="info"
            close-button-label="Go to your User Profile"
            >
                <h5>{{welcome_message}}</h5>
            </modal>


        <template v-if="!token">
            <div class="container">
                <div class="not-logged-in-alert alert alert-warning">
                    Login Status:
                    <strong>Not logged in</strong>
                </div>

                <div class="not-logged-in-alert alert alert-info d-flex">
                    <div></div>
                    <div>
                        <p>
                            To access/query all versions of Web of Science
                            (WoS) databases, institutional/organizational
                            login is required. To do so, click “Log in to CADRE”
                            below, then select CILogon on the next page.
                        </p>
                        <p>
                            Please note that even if your institutional/organizational
                            account is also a Google/G Suite/Gmail account,
                            you still need to log in through CILogon to access WoS.
                        </p>

                        <a
                            class="btn btn-primary btn-lg px-5"
                            :href="login_url"
                        >Log In to CADRE</a>
                    </div>
                </div>
            </div>

            <!-- <div class="container pt-3">
                <div class="alert alert-info">
                    You are not logged in. You can log in
                    <a
                        class
                        :href="login_url"
                    >
                        <span class>here</span>
                    </a>.
                </div>
            </div>
            <div class="container">
                <p>
                    The Collaborative Archive &amp; Data Research
                    Environment is a science gateway to standardized text-
                    and data-mining services for large datasets—with reproducbility
                    and collaboration in mind. All in a cloud-based platform.
                </p>
                <p>
                    For more information about CADRE, visit
                    <a
                        href="https://cadre.iu.edu/"
                        target="_blank"
                    >the CADRE home page</a>.
                </p>
            </div>-->
        </template>
        <!-- 
 ######  ########  #### ##    ## ##    ## ######## ########  
##    ## ##     ##  ##  ###   ## ###   ## ##       ##     ## 
##       ##     ##  ##  ####  ## ####  ## ##       ##     ## 
 ######  ########   ##  ## ## ## ## ## ## ######   ########  
      ## ##         ##  ##  #### ##  #### ##       ##   ##   
##    ## ##         ##  ##   ### ##   ### ##       ##    ##  
 ######  ##        #### ##    ## ##    ## ######## ##     ##
        -->

        <div
            v-if="is_loading"
            id="loading-screen"
            class="d-flex align-items-center justify-content-center"
        >
            <div class="loading-content">
                <div class="icon">
                    <!-- <fa icon="circle-notch"
                    spin />-->
                    <spinner></spinner>
                </div>
                <div
                    v-for="(item, index) in loading_queue"
                    :key="`loading_${index}`"
                    v-text="item.message"
                ></div>
            </div>
        </div>

        <!-- 
########  #######   #######  ######## ######## ########  
##       ##     ## ##     ##    ##    ##       ##     ## 
##       ##     ## ##     ##    ##    ##       ##     ## 
######   ##     ## ##     ##    ##    ######   ########  
##       ##     ## ##     ##    ##    ##       ##   ##   
##       ##     ## ##     ##    ##    ##       ##    ##  
##        #######   #######     ##    ######## ##     ##
        -->

        <footer id="main-footer">
            <div class="container">
                <div
                    class="logos d-flex flex-wrap flex-md-nowrap justify-content-between align-items-center"
                >
                    <!-- <div class=""> -->
                    <a
                        href="https://cadre.iu.edu"
                        class="cadre-logo"
                    >
                        <img
                            src="@/assets/img/cadre-logo.png"
                            alt="CADRE"
                        />
                        <span class="d-none">CADRE</span>
                    </a>

                    <a
                        href="https://www.btaa.org/"
                        class="btaa-logo"
                    >
                        <img
                            src="@/assets/img/btaa-logo.png"
                            alt="BTAA"
                        />
                        <span class="d-none">BTAA</span>
                    </a>
                    <a
                        href="https://libraries.indiana.edu/"
                        class="libraries-logo"
                    >
                        <img
                            src="@/assets/img/iu-libraries-logo.png"
                            alt="IU Libraries"
                        />
                        <span class="d-none">IU Libraries</span>
                    </a>
                    <a
                        href="https://iuni.iu.edu"
                        class="iuni-logo"
                    >
                        <img
                            src="@/assets/img/iuni-logo.png"
                            alt="IUNI"
                        />
                        <span class="d-none">IUNI</span>
                    </a>
                </div>
                <div
                    class="mt-5 text-center "
                ><a href="/gateway-privacy" target="_blank">Privacy Policy</a></div>
                <div
                    class="mt-5 text-center small text-muted"
                >CADRE Big Data Gateway Version {{version.number}}</div>
            </div>
        </footer>
        <div class="feedback-link">
            <a
                href="/contact-us/feedback"
                target="_blank"
                class="btn btn-primary"
            >Send Feedback</a>
        </div>
    </div>
</template>

<style lang="scss">
@import "@/assets/bootstrap_variables.scss";
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

.not-logged-in-alert.alert-warning {
    margin-top: 4rem;
}
.not-logged-in-alert.alert-info {
    margin-bottom: 10rem;
}

header#main-header .nav-item {
    // font-size: .875rem;
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
        padding: 1rem;
    }
    .logos img {
        // border: solid blue 1px;
        max-width: 100%;
    }
}

.feedback-link {
    position: fixed;
    right: 1rem;
    bottom: 1rem;
    // opacity: 0.5;

    // &:hover {
    //     opacity: 1;
    // }

    a {
        text-decoration: none;
    }
}
</style>
