<template>
    <div>
        <section>
            <div class="container">
                <h2>Your CADRE Profile</h2>
                <hr />
                <div class="card container mb-3">
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
                        <!-- <h5>Terms of Service Agreement</h5>
                        <div>
                            <input type="checkbox"
                            id="tos_confirm" 
                            name="tos_confirm"
                            v-model="new_tos_confirm"
                            :disabled="current_user_profile.agreement_signed"
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
                        v-text="`Agreement signed on ${new Date(current_user_profile.date_agreement_signed).toUTCString()}`"
                        v-if="current_user_profile.date_agreement_signed">
                        </div> 
                        <hr />-->
                        <div class="mt-3">
                            <button
                                class="float-left btn btn-primary" 
                                :disabled="!new_display_name"
                                @click=updateProfile()
                            >Update Profile</button> 
                        </div>
                        <div v-text="`test the displayname value: ${new_display_name}`">
                        </div>
                        <div v-text="`test the checkbox value: ${new_tos_confirm}`">
                        </div>
                        <div v-text="`test the checkbox value: ${access_form_fields.first_name}`">
                        </div> 
                        <div v-text="`test the checkbox value: ${access_form_fields.last_name}`">
                        </div> 
                        <div v-text="`test the checkbox value: ${access_form_fields.first_name}`">
                        </div> 
                        <div v-text="`test the checkbox value: ${access_form_fields.start_date}`">
                        </div> 
                    </div>
            </div>
            <div class="card mb-3">
                <h3>CADRE User Agreement</h3>
                    <hr />
                    <div class="row mb-5">
                        <form @submit.stop.prevent="submitAgreement()">
                            <div class="form-group col mb-5">
                                <h4 class="mb-3">Personal Information</h4>
                                <div class="form-row mb-3 d-flex flex-fill align-center">
                                    <div class="col">
                                        <label>First Name</label>
                                        <input
                                            class="form-control"
                                            type="text"
                                            v-model="access_form_fields.first_name"
                                            :placeholder="access_form_fields.first_name"
                                        />
                                    </div>
                                    <div class="col-sm-2">
                                        <label>Middle Initial</label>
                                        <input
                                            class="form-control"
                                            type="text"
                                            v-model="access_form_fields.middle_initial"
                                            :placeholder="access_form_fields.middle_initial"
                                        />
                                    </div>
                                    <div class="col">
                                        <label>Last Name</label>
                                        <input
                                            class="form-control"
                                            type="text"
                                            v-model="access_form_fields.last_name"
                                            :placeholder="access_form_fields.last_name"
                                        />
                                    </div>
                                </div>
                                <div class="form-row mb-3">
                                    <div class="col">
                                    <label>University</label>
                                    <input
                                        class="form-control"
                                        type="text"
                                        v-model="access_form_fields.university"
                                        :placeholder="access_form_fields.university"
                                    />
                                    </div>
                                    <div class="col">
                                        <label>Department/School</label>
                                        <input
                                            class="form-control"
                                            type="text"
                                            v-model="access_form_fields.department"
                                            :placeholder="access_form_fields.department"
                                        />
                                    </div>
                                </div>
                                <div class="form-row mb-3">
                                    <div class="col">
                                        <label>Research Area</label>
                                        <input
                                            class="form-control"
                                            type="text"
                                            v-model="access_form_fields.research_area"
                                            :placeholder="access_form_fields.research_area"
                                        />
                                    </div>
                                    <div class="col">
                                        <label>University Affiliated Email Address</label>
                                        <input
                                            class="form-control"
                                            type="text"
                                            v-model="access_form_fields.university_email_address"
                                            :placeholder="access_form_fields.university_email_address"
                                        />
                                    </div>
                                </div>
                                <label>Expected Research Period</label>
                                <input
                                    class="form-control mb-3"
                                    type="text"
                                    v-model="access_form_fields.research_period"
                                    :placeholder="access_form_fields.research_period"
                                />
                                <div class="form-row mb-3">
                                    <div class="col">
                                        <label>Start Date</label>
                                        <input
                                            class="form-control"
                                            type="text"
                                            v-model="access_form_fields.start_date"
                                            placeholder="mm/dd/yyyy"
                                        />
                                    </div>
                                    <div class="col">
                                        <label>End Date</label>
                                        <input
                                            class="form-control"
                                            type="text"
                                            v-model="access_form_fields.end_date"
                                            placeholder="mm/dd/yyyy"
                                        />
                                    </div>
                                </div>
                                <label> Would you like to be subscribed to CADRE's newsletter?</label>
                                <div class="form-group col-5">
                                <input
                                    class="mr-2 "
                                    type="radio"
                                    name="yes_subscribe"
                                    value=true
                                    v-model="access_form_fields.subscribe_newsletter"
                                />Yes
                                <input
                                    class="mr-2 ml-3"
                                    type="radio"
                                    name="no_subscribe"
                                    value=false
                                    v-model="access_form_fields.subscribe_newsletter"
                                />No
                                </div>
                                <!-- <div v-text="`test the subscribe value: ${access_form_fields.subscribe_newsletter}`">
                                </div> -->
                            </div>
                            <div class="form-group col mb-5">
                                <h4 class="mb-3">Project Information</h4>
                                <div class="form-group col">
                                    <p>
                                        In order to better understand the needs of our users and make sure the necessary services and tools are available, please share what kind of research projects you are interested in pursuing.
                                    </p>
                                    <textarea 
                                        type="text"
                                        class="form-control mb-3"
                                        :placeholder="access_form_fields.research_projects"
                                        v-model="access_form_fields.research_projects">
                                    </textarea>
                                    <p>
                                        Why are you interested in using CADRE for your project?
                                    </p>
                                    <textarea 
                                        type="text"
                                        class="form-control"
                                        :placeholder="access_form_fields.cadre_interest"
                                        v-model="access_form_fields.cadre_interest">
                                    </textarea>
                                </div>
                            </div>
                            <div class="form-group col mb-5">
                                <h4 class="mb-3">Trial Period and Data Retention</h4>
                                <div class="form-group col">
                                    <p>
                                        Your university’s trial period lasts <b>three months</b> from the date the initial trial and licensing agreement is signed. Please reach out to CADRE or your university’s CADRE representative to confirm the exact date the institution’s trial began. 
                                    </p>
                                    <p>
                                        We cannot guarantee that your data or code will be retained on the platform after your trial period ends. However, you will be sent an email reminder <b>two weeks</b> before the end of your trial period to ensure you have enough time to remove your data and code, if necessary.
                                    </p>
                                </div>
                            </div>
                            <div class="form-group col mb-5">
                                <h4 class="mb-3">Expectations for Trial and Technical Support</h4>
                                <div class="form-group col">
                                    <p>
                                        As part of our trial, you will receive access to all of the available CADRE features and datasets that our paying members receive access to, including Microsoft Academic Graph and the Web of Science.  
                                    </p>
                                    <p>
                                        Any questions you have about the platform should be asked in the #cadre-users Slack channel. Email <a href="mailto:smcgavin@iu.edu">Stephanie Hernandez McGavin</a> with a request to join CADRE’s Slack workspace. To report bugs about the platform, fill out CADRE’s <a href="https://cadre.iu.edu/contact-us">contact form</a> with your message.
                                    </p>
                                </div>
                            </div>
                            <div class="form-group col mb-5">
                                <h4 class="mb-3">Expectations for Trial and Technical Support</h4>
                                <div class="form-group col">
                                    <p>
                                        Finally, please confirm that you agree to the following: 
                                    </p>
                                    <ul>
                                        <li> You have read and agreed to the terms of the
                                        <button
                                            class="btn btn-link"
                                            @click="access_policy_open = true;"
                                        >CADRE Access Policy.</button>

                                        <modal
                                            v-if="access_policy_open"
                                            @close="access_policy_open = false"     
                                            modal-style="success"
                                            modal-title="CADRE Access Policy"
                                            close-button-label="Close"
                                            >
                                            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer lacinia mauris sit amet ligula ultrices, nec scelerisque metus molestie. Praesent a vehicula odio. Pellentesque dapibus enim non metus varius vestibulum. Vestibulum elementum dolor ut tincidunt ultrices. Phasellus fringilla nulla vitae consectetur varius. Donec egestas pellentesque iaculis. Phasellus dignissim, est vitae elementum aliquet, diam felis euismod risus, eget ornare felis neque sit amet tellus. Morbi nunc odio, maximus congue eleifend in, consectetur in urna. Donec dictum ipsum est, in consectetur enim pellentesque dignissim. Nam gravida, purus interdum convallis condimentum, augue mi vehicula nibh, nec hendrerit sem enim at quam. Duis porta, orci vitae blandit convallis, ex orci euismod erat, quis aliquam lectus dui sit amet orci. Pellentesque lorem odio, suscipit eget commodo in, luctus eget erat. Etiam molestie facilisis est, vitae luctus elit lobortis sit amet. Sed nibh libero, suscipit et rutrum sit amet, ultrices sed velit.
                                            </p>
                                        </modal>
                                        </li>
                                        <li> Any data extracted from the enclave at your request should not be shared with anyone.</li>
                                        <li> Usernames and passwords should not be shared with anyone.</li> 
                                        <li> You agree to safeguard your username and password.</li> 
                                        <li> Any unauthorized use of that account will be your individual responsibility.</li> 
                                        <li> Any loss of your personal control over the username or password has to be reported to the CADRE Data Manager.</li>
                                        <li> All publications that result from using the data need to have the acknowledgement text described in sections 2.2 - 2.5 of the CADRE Access Policy.</li>
                                        <li> You are willing to receive emails from the IUNI Data Manager containing news regarding the enclave and CADRE data.</li>
                                        <li> Scholarly works that result from using the data will be submitted to the IUNI Data Manager as soon as they are published.</li>
                                    </ul>
                                    <div class="check">
                                        <label for="agree_confirm" class="text-center align-middle">
                                            <input 
                                                type="checkbox"
                                                id="agree_confirm" 
                                                name="agree_confirm"
                                                v-model="access_form_fields.agreements_confirmed"
                                                class=""
                                                :disabled="access_form_fields.agreements_confirmed"/>
                                            I affirm that to the best of my knowledge all information provided above is complete and true and that I will comply with all Indiana University policies with regards to the use of restricted data. </label>
                                    </div>
                                    <div class="mt-3">
                                        <button
                                            class="float-left btn btn-primary" 
                                            :disabled="!access_form_fields.agreements_confirmed"
                                            @click=updateUserAgreement()
                                            type="submit"
                                        >Confirm Agreement</button> 
                                    </div>
                                </div>
                            </div>
                        </form>
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
            terms_of_service_open: false,
            access_policy_open: false,
            get_user_profile_endpoint: this.$cadreConfig.rac_api_prefix + "/profile/get-user-profile",
            update_user_profile_endpoint: this.$cadreConfig.rac_api_prefix + "/profile/update-user-profile",
            current_user_profile: [],
            new_display_name: "",
            new_tos_confirm: false,
            update_successful:false,
            access_form_fields:[
                {
                    first_name: "",
                    middle_initial: "",
                    last_name: "",
                    university: "",
                    department:"",
                    research_area: "",
                    university_email_address: "",
                    research_period: "",
                    start_date: "",
                    end_date: "",
                    subscribe_newsletter: false,
                    research_projects: "",
                    cadre_interest: "",
                    agreements_confirmed: false
                }],
            access_agreement_confirm: false,

            //set testing_page to true to use sample user profile
            testing_page: true
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
                    this.$set(this, "new_tos_confirm", user_profile.agreement_signed)
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
                            this.$set(this, "new_tos_confirm", user_profile.agreement_signed);
                            this.$set(this, "access_form_fields", user_profile.access_form_fields);
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
        },
        updateUserAgreement: function() {
            let prom = new Promise((resolve, reject) => {
                let axios_prom = this.$cadre.axios({
                    url: this.$cadreConfig.rac_api_prefix + "/profile/update-user-agreement",
                    method:"POST",
                    data: {
                        user_id: this.user_id,
                        access_form_fields: this.access_form_fields
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
    agreement_signed: true,
    date_agreement_signed: "2020-02-07T21:10:46.773823+00:00"
}
</script>

<style lang="scss">
$border: solid gray 1px;

</style>
