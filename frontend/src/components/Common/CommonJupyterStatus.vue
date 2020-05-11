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
    props: {
        AutoStart: {
            type: Boolean,
            default: false
        },
        StatusInterval: {
            type: Number,
            default: 5000
        },
        StartDuration: {
            type: Number,
            default: 1000
        },
        AutoOpenOnConnect: {
            type: Boolean,
            default: false
        },
        HideButtons: {
            type: Boolean,
            default: false
        }
    },
    computed: {
        auto_start() {
            return this.AutoStart;
        },
        status_interval() {
            return this.StatusInterval;
        },
        start_duration() {
            return this.StartDuration;
        },
        hide_buttons() {
            return this.HideButtons;
        },
        jupyter_url: function() {
            return this.$cadreConfig.jupyter_url;
        },
        jupyter_full_url: function() {
            return `${this.jupyter_url}/user/${this.username}/lab/?token=${this.jupyter_token}`;
        },
        jupyter_api_new_url: function() {
            return "/new-notebook/" + this.username;
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
        getUserStatus: async function() {
            this.error_message = "";
            this.status = null;
            try {
                let response = await this.$cadre.racAxios({
                    url: this.jupyter_api_status_url
                });

                this.status = response.data;
                console.debug(this.status);
                if (this.status.servers[""] && this.status.servers[""].ready) {
                    //server is running
                    this.$emit("serverStarted");
                    this.server_running = true;
                    this.server_pending = false;
                } else if (
                    this.status.servers[""] &&
                    !this.status.servers[""].ready
                ) {
                    this.$emit("serverPending");
                    this.server_running = false;
                    this.server_pending = true;
                    setTimeout(this.getUserStatus, this.status_interval);
                } else {
                    //server is not running
                    this.server_running = false;
                    this.server_pending = false;
                    // this.tryToCreateJupyterHub();
                }
            } catch (error) {
                this.error_message = error.message;
            }

            return this.server_running;
        },
        tryToCreateJupyterHub: function() {
            let jupyter_prom = this.$cadre.racAxios({
                method: "POST",
                url: this.jupyter_api_new_url
            });
            jupyter_prom.then(
                response => {
                    // console.debug(response);
                    setTimeout(this.getUserStatus, this.start_duration);
                },
                error => {
                    setTimeout(this.getUserStatus, this.start_duration);
                    this.error_message = error.message;
                }
            );
        }
    },
    mounted: async function() {
        this.status = null;
        let running = await this.getUserStatus();
        if (!this.server_running && this.auto_start) {
            this.tryToCreateJupyterHub();
        }
    }
};
</script>
<template>
    <div>
        <div>
            Notebook status:
            <span v-if="!status && !error_message">Please Wait...</span>
            <b
                v-else
                v-text="server_running?'running':server_pending?'pending':'not running'"
            ></b>
        </div>

        <div
            class="alert alert-danger"
            v-if="error_message"
            v-text="error_message"
        ></div>

        <div class="d-flex justify-content-between" v-if="!hide_buttons">
            <button
                v-if="server_running"
                @click="goToNotebook()"
                class="btn btn-link"
            >Open Notebook</button>

            <button
                v-if="status && !server_running && !server_pending"
                @click="tryToCreateJupyterHub()"
                class="btn btn-link"
            >Start Notebook Server</button>
        </div>
        <div class="mt-3">
            <button
                @click="getUserStatus()"
                class="btn btn-link"
            >Update Status</button>
        </div>
    </div>
</template>