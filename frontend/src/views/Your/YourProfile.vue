<template>
    <div>
        <section>
            <div class="container">
                <h2>Your CADRE Profile</h2>
                <hr />
                <div class="card">
                    <h3>About You</h3>
                        <hr />
                        <div class="row">
                            <div class="form-group col">
                                <h5>Display Name</h5>
                                <input
                                    class="form-control"
                                    type="text"
                                    :placeholder="[[ current_user_profile.display_name ]]"
                                    v-model="new_display_name"
                                />
                            </div>
                            <div class="fill-height flex-fill align-center col-5 alert">
                                <p>
                                    Your Display Name will be shown when you publish a Package or Tool to the Marketplace.
                                </p>
                            </div>
                        </div>
                        <div class="form-group text-left">
                            <h5>Terms of Service Agreement</h5>
                            <div>
                            <input type="checkbox"
                            id="tos_confirm" 
                            name="tos_confirm"
                            v-model="new_tos_confirm"
                            :disabled="current_user_profile.tos_signed"
                            class="mr-2">
                            <label>
                            By checking this box, I confirm I've read, understand and agree to the </label>
                            <button
                                class="btn btn-link"
                                @click="terms_of_service_open = true;"
                            >Terms of Service.</button>

                            <modal
                                v-if="terms_of_service_open"
                                @close="terms_of_service_open = false"     
                                modal-style="success"
                                modal-title="Terms of Service"
                                close-button-label="Close"
                                >
                                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer lacinia mauris sit amet ligula ultrices, nec scelerisque metus molestie. Praesent a vehicula odio. Pellentesque dapibus enim non metus varius vestibulum. Vestibulum elementum dolor ut tincidunt ultrices. Phasellus fringilla nulla vitae consectetur varius. Donec egestas pellentesque iaculis. Phasellus dignissim, est vitae elementum aliquet, diam felis euismod risus, eget ornare felis neque sit amet tellus. Morbi nunc odio, maximus congue eleifend in, consectetur in urna. Donec dictum ipsum est, in consectetur enim pellentesque dignissim. Nam gravida, purus interdum convallis condimentum, augue mi vehicula nibh, nec hendrerit sem enim at quam. Duis porta, orci vitae blandit convallis, ex orci euismod erat, quis aliquam lectus dui sit amet orci. Pellentesque lorem odio, suscipit eget commodo in, luctus eget erat. Etiam molestie facilisis est, vitae luctus elit lobortis sit amet. Sed nibh libero, suscipit et rutrum sit amet, ultrices sed velit.
                                </p>
                            </modal>
                            </div>

                            <div class="col3"
                            v-text="`Agreement signed on ${new Date(current_user_profile.date_tos_signed).toUTCString()}`"
                            v-if="current_user_profile.date_tos_signed">
                            </div>
                            <hr />
                            <div class="mt-3">
                                <button
                                    class="float-left btn btn-primary" 
                                    :disabled="!new_display_name && new_tos_confirm === current_user_profile.tos_signed"
                                    @click=updateProfile()
                                >Update Profile</button> 
                            </div>
                            <!-- <div v-text="`test the displayname value: ${new_display_name}`">
                            </div>
                            <div
                                v-text="`test the checkbox value: ${new_tos_confirm}`">
                            </div> -->
                        </div>
                </div>
            </div>
        </section>
    </div>
</template>

<script>
import Modal from "@/components/Common/CommonModal";


export default {
    data: function() {
        return {
            terms_of_service_open:false,
            get_user_profile_endpoint: this.$cadreConfig.rac_api_prefix + "/profile/get-user-profile",
            update_user_profile_endpoint: this.$cadreConfig.rac_api_prefix + "/profile/update-user-profile",
            current_user_profile: [],
            new_display_name: "",
            new_tos_confirm: false,
            update_successful:false,

            //set testing_page to true to use sample user profile
            testing_page: false
        };
    },
    computed: {
        user_id: function() {
            return this.$store.state.user.user_id;
        }
    },
    components: {
        Modal
    },
    methods: {
        getProfile: function() {
            let prom = new Promise((resolve, reject) => {
                if (this.testing_page === true){
                    let user_profile = sample_user_profile;
                    this.$set(this, "current_user_profile", user_profile);
                    this.$set(this, "new_tos_confirm", user_profile.tos_signed)
                } 
                else {
                    let axios_prom = this.$cadre.axios({
                        url: this.get_user_profile_endpoint,
                        method: "GET",
                        data:{
                            user_id: this.user_id

                        }
                    });
                    axios_prom.then(
                        response => {
                            let user_profile = response.data;
                            this.$set(this, "current_user_profile", user_profile);
                            this.$set(this, "new_tos_confirm", user_profile.tos_signed)
                            resolve(response);
                        },
                        error => {
                            console.error(error);
                            reject(error);
                        }
                    );
                }
            });
            return prom;
        },
        //subject to change as middleware is built, accomodate if user doesn't update all fields.
        updateProfile: function() {
            let prom = new Promise((resolve, reject) => {
                let axios_prom = this.$cadre.axios({
                    url: this.$cadreConfig.rac_api_prefix + "/profile/update-user-profile",
                    method:"POST",
                    data: {
                        user_id: this.user_id,
                        new_display_name: this.new_display_name,
                        new_tos_confirm: this.new_tos_confirm
                    }
                });
                axios_prom.then(
                    response => {
                        this.update_successful = true
                        resolve(response)
                    },
                    error => {
                        console.error(error);
                        reject(error)
                    }
                );
            });
            return prom;
        }
    },
    watch: {
        refresh_profile: function(){
            this.getProfile();
            console.debug("refresh");
        }
    },
    mounted: function() {
        this.getProfile();

    }
};



const sample_user_profile = {
    user_id: 1000,
    display_name: "Test User",
    tos_signed: true,
    date_tos_signed: "2020-02-07T21:10:46.773823+00:00"
}
</script>

<style lang="scss">
$border: solid gray 1px;

</style>
