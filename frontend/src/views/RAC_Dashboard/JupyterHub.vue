<template>
    <div>
        <!-- Notebook URL: {{jupyter_full_url}} -->
        <section>
            <div class="container">
                <h2>Jupyter Notebook</h2>

                <div class="alert"
                     :class="{
                 'alert-success':server_running,
                 'alert-info':server_pending || !status,
                 'alert-warning': status && !server_running && !server_pending
                 }">
                    Notebook status: <span v-if="!status && !error_message">Please Wait...</span><b v-else
                       v-text='server_running?"running":server_pending?"pending":"not running"'></b>
                </div>

                <div class="alert alert-danger"
                     v-if="error_message"
                     v-text="error_message"></div>
                <div class="d-flex justify-content-between">
                    <button v-if="server_running"
                            @click="goToNotebook()"
                            class="btn btn-primary btn-lg">Go To Notebook</button>
                    <button v-if="server_running"
                            @click="stopServer()"
                            class="btn btn-danger btn-lg">Stop Notebook Server</button>

                    <button v-if="status && !server_running && !server_pending"
                            @click="tryToCreateJupyterHub()"
                            class="btn btn-primary btn-lg">Start Notebook Server</button>

                </div>
                <div class="mt-3">
                    <button @click="getUserStatus()"
                            class="btn btn-primary btn-lg">Update Status</button>

                </div>
                <!-- <pre v-text="status"></pre> -->
            </div>
        </section>
    </div>
</template>

<script>
export default {
    data: function() {
        return {
            error_message: "",
            status: null,
            server_running: false,
            server_pending: false
        };
    },
    computed: {
        jupyter_url: function() {
            return this.$cadreConfig.jupyter_url;
        },
        jupyter_full_url: function() {
            return `${this.jupyter_url}/user/${this.username}/lab/?token=${this.jupyter_token}`;
        },
        jupyter_api_new_url: function() {
            return "/new-notebook/" + this.username;
        },
        jupyter_api_stop_url: function() {
            return "/stop-notebook/" + this.username;
        },
        jupyter_api_status_url: function() {
            return "/notebook-status/" + this.username;
        },
        jupyter_api_token_url: function() {
            return "/get-new-notebook-token/" + this.username;
        },
        token: function() {
            return this.$store.getters["user/authToken"];
        },
        jupyter_token: function() {
            return this.$store.getters["user/jToken"];
        },
        username: function() {
            return this.$store.getters["user/username"];
        }
    },
    methods: {
        getNewToken: function() {
            let prom = this.$cadre.racAxios({
                url: this.jupyter_api_token_url
            });
            prom.then(
                response => {
                    console.debug(response.data);
                    this.$store.commit("user/setJToken", response.data);
                },
                error => {
                    console.warn(error);
                    this.error_message = "Could not refresh Jupyter Token";
                }
            );
            return prom;
        },
        goToNotebook: function() {
            let prom = this.getNewToken();
            prom.then(
                response => {
                    // location.href = this.jupyter_full_url;
                    window.open(this.jupyter_full_url, "_blank");
                },
                error => {
                    console.warn(error);
                }
            );
            console.debug(this.jupyter_full_url);
        },
        getUserStatus: function() {
            this.error_message = "";
            this.status = null;
            let prom = this.$cadre.racAxios({
                url: this.jupyter_api_status_url
            });
            prom.then(
                response => {
                    this.status = response.data;
                    console.debug(this.status);
                    if (
                        this.status.servers[""] &&
                        this.status.servers[""].ready
                    ) {
                        //server is running
                        this.server_running = true;
                        this.server_pending = false;
                    } else if (
                        this.status.servers[""] &&
                        !this.status.servers[""].ready
                    ) {
                        this.server_running = false;
                        this.server_pending = true;

                        setTimeout(this.getUserStatus, 5000);
                    } else {
                        //server is not running
                        this.server_running = false;
                        this.server_pending = false;
                        // this.tryToCreateJupyterHub();
                    }
                },
                error => {
                    this.error_message = error.message;
                }
            );
        },
        tryToCreateJupyterHub: function() {
            let jupyter_prom = this.$cadre.racAxios({
                method: "POST",
                url: this.jupyter_api_new_url
            });
            jupyter_prom.then(
                response => {
                    console.debug(response);
                    setTimeout(this.getUserStatus, 1000);
                },
                error => {
                    setTimeout(this.getUserStatus, 1000);
                    this.error_message = error.message;
                }
            );
        },
        stopServer: function() {
            this.error_message = "";
            this.status = null;
            let jupyter_prom = this.$cadre.racAxios({
                method: "POST",
                url: this.jupyter_api_stop_url
            });
            jupyter_prom.then(
                response => {
                    console.debug(response);
                    setTimeout(this.getUserStatus, 1000);
                },
                error => {
                    setTimeout(this.getUserStatus, 1000);
                    // this.error_message = error.message;
                }
            );
        }
    },
    mounted: function() {
        this.getUserStatus();
    }
};
</script>

<style>
</style>
