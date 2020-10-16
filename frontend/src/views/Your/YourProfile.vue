

<script>
import Modal from "@/components/Common/CommonModal";

export default {
    data: function () {
        return {
            current_user_profile: [],
            new_display_name: "",
            update_successful: false,
            first_name: "",
            middle_initial: "",
            last_name: "",
            university: "",
            department: "",
            research_area: "",
            university_email_address: "",
            // research_period: "",
            // start_date: "",
            // end_date: "",
            // subscribe_newsletter: false,
            // research_projects: "",
            // cadre_interest: "",
            agree_access_policy: false,
            agree_not_share_data: false,
            agree_not_share_username: false,
            agree_safeguard_username: false,
            agree_unauthorized_responsibility: false,
            agree_loss_control: false,
            agree_publications_acknowledge: false,
            agree_receive_emails: false,
            agree_works_submitted: false,
            agree_comply: false,
            agreement_signed: false,
            completed_access_form: [],

            success_message: "",
            error_message: "",

            //access_agreement_confirm: false,
            //set testing_page to true to use sample user profile
            testing_page: false,
        };
    },
    computed: {
        user_id: function () {
            return this.$store.state.user.user_id;
        },
        trial_user: function () {
            if (this.$store.state.user.cognito_groups != null) {
                if (
                    this.$store.state.user.cognito_groups.includes("wos_trial")
                ) {
                    return true;
                } else {
                    return false;
                }
            } else {
                return false;
            }
        },
    },
    components: {
        Modal,
    },
    methods: {
        async getProfile() {
            this.$store.commit("loading/addKey", {
                key: "getProfile",
                message: "",
            });
            try {
                let response = await this.$store.dispatch("user/getProfile");
                let user_profile = response.data;
                this.$set(this, "current_user_profile", user_profile);
                this.$set(
                    this,
                    "agreement_signed",
                    user_profile.agreement_signed
                );
                this.$set(
                    this,
                    "completed_access_form",
                    user_profile.access_form_fields
                );
                this.new_display_name = user_profile.display_name;
            } catch (error) {
                throw error;
            } finally {
                this.$store.commit("loading/removeKey", { key: "getProfile" });
            }
        },
        async createProfile() {
            let response = undefined;
            try {
                response = await this.$cadre.axios({
                    url:
                        this.$cadreConfig.rac_api_prefix +
                        "/profile/create-user-profile",
                    method: "POST",
                    data: {
                        user_id: this.user_id,
                    },
                });
            } catch (error) {
                throw error;
            }
            return response;
        },
        //Element(s) in user profile section updated
        async updateProfile() {
            this.$store.commit("loading/addKey", {
                key: "profileUpdate",
                message: "Updating Profile",
            });
            let prom = new Promise(async (resolve, reject) => {
                let axios_prom = this.$cadre.axios({
                    url:
                        this.$cadreConfig.rac_api_prefix +
                        "/profile/update-user-profile",
                    method: "POST",
                    data: {
                        user_id: this.user_id,
                        new_display_name: this.new_display_name,
                    },
                });
                axios_prom.then(
                    async (response) => {
                        this.update_successful = true;
                        this.success_message =
                            "Profile was updated successfully.";
                        await this.getProfile(); //this.$store.dispatch("user/getProfile");
                        // let user_profile = this.$store.getters["user/profile"];

                        resolve(response);
                    },
                    (error) => {
                        console.error(error);
                        this.error_message = "Profile could not be updated.";
                        reject(error);
                    }
                );
                axios_prom.finally(() => {
                    this.$store.commit("loading/removeKey", {
                        key: "profileUpdate",
                    });
                });
            });
            return prom;
        },
        //Access form fields submitted
        submitUserAgreement: function () {
            this.$store.commit("loading/addKey", {
                key: "agreementUpdate",
                message: "Updating Agreement",
            });
            let prom = new Promise((resolve, reject) => {
                let access_form_fields = [
                    {
                        first_name: this.first_name,
                        middle_initial: this.middle_initial,
                        last_name: this.last_name,
                        university: this.university,
                        department: this.department,
                        research_area: this.research_area,
                        university_email_address: this.university_email_address,
                        agree_access_policy: this.agree_access_policy,
                        agree_not_share_data: this.agree_not_share_data,
                        agree_not_share_username: this.agree_not_share_username,
                        agree_safeguard_username: this.agree_safeguard_username,
                        agree_unauthorized_responsibility: this
                            .agree_unauthorized_responsibility,
                        agree_loss_control: this.agree_loss_control,
                        agree_publications_acknowledge: this
                            .agree_publications_acknowledge,
                        agree_receive_emails: this.agree_receive_emails,
                        agree_works_submitted: this.agree_works_submitted,
                        agree_comply: this.agree_comply,
                    },
                ];
                let axios_prom = this.$cadre.axios({
                    url:
                        this.$cadreConfig.rac_api_prefix +
                        "/profile/update-user-agreement",
                    method: "POST",
                    data: {
                        user_id: this.user_id,
                        access_form_fields: access_form_fields,
                    },
                });
                axios_prom.then(
                    (response) => {
                        this.agreement_signed = true;
                        this.success_message = "Agreement signed.";
                        resolve(response);
                    },
                    (error) => {
                        console.error(error);
                        this.error_message = "Agreement could not be updated.";
                        reject(error);
                    }
                );
                axios_prom.finally(() => {
                    this.$store.commit("loading/removeKey", {
                        key: "agreementUpdate",
                    });
                });
            });
            return prom;
        },
    },
    watch: {
        update_successful: function (after, before) {
            this.getProfile();
            console.debug("refresh");
        },
        agreement_signed: function (after, before) {
            this.getProfile();
            console.debug("refresh");
        },
    },
    async mounted() {
        try {
            await this.getProfile();
            console.debug(this.current_user_profile);
            if (
                !this.new_display_name ||
                this.trial_user & !this.current_user_profile.agreement_signed
            ) {
                try {
                    await this.createProfile();
                } catch (error) {
                    console.warn(error);
                }
            }
        } catch (error) {
            console.warn(error);
        }
    },
};
const sample_user_profile = {
    user_id: 1000,
    display_name: "Test User",
    agreement_signed: true,
    date_agreement_signed: "2020-02-07T21:10:46.773823+00:00",
};
</script>


<template>
    <!-- 
######## ######## ##     ## ########  ##          ###    ######## ######## 
   ##    ##       ###   ### ##     ## ##         ## ##      ##    ##       
   ##    ##       #### #### ##     ## ##        ##   ##     ##    ##       
   ##    ######   ## ### ## ########  ##       ##     ##    ##    ######   
   ##    ##       ##     ## ##        ##       #########    ##    ##       
   ##    ##       ##     ## ##        ##       ##     ##    ##    ##       
   ##    ######## ##     ## ##        ######## ##     ##    ##    ########  -->
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
                            <h5>
                                <label for="display_name">Display Name</label>
                            </h5>
                            <input
                                class="form-control"
                                type="text"
                                placeholder="Display Name"
                                v-model="new_display_name"
                                id="display_name"
                            />
                        </div>
                        <div
                            class="fill-height flex-fill align-center col-5 alert"
                        >
                            <p>
                                Your Display Name will be shown when you publish
                                a Package or Tool to the Marketplace.
                            </p>
                        </div>
                    </div>
                    <div class="form-group text-left">
                        <div class="mt-3">
                            <button
                                class="float-left btn btn-primary"
                                :disabled="!new_display_name"
                                @click="updateProfile()"
                            >
                                Update Profile
                            </button>
                        </div>
                    </div>
                </div>

                <div
                    class="card mb-3"
                    v-if="trial_user && !current_user_profile.agreement_signed"
                >
                    <div class="alert alert-info">
                        <p>Hey there,</p>
                        <p>
                            You may have already filled out this form or worked
                            on the platform, but
                            <a
                                href="/news-and-events/news/cadre-executes-beta-launch-invites-institutions-to-trial-platform"
                                target="_blank"
                                >our Beta Launch</a
                            >
                            has changed things up, and we are asking trial users
                            to resubmit their forms through our new system.
                            Thank you in advance for your understanding!
                        </p>
                        <p>
                            If you want to stay in the loop on updates like
                            this,
                            <a href="/news-and-events" target="_blank"
                                >subscribe to our newsletter</a
                            >.
                        </p>
                    </div>

                    <h3>CADRE Trial User Form</h3>
                    <hr />

                    <div class="row mb-5">
                        <div
                            class="form-group col mb-5"
                            v-text="
                                `Agreement signed on ${new Date(
                                    current_user_profile.date_agreement_signed
                                ).toUTCString()}`
                            "
                            v-if="current_user_profile.date_agreement_signed"
                        ></div>
                        <form @submit.stop.prevent="submitUserAgreement()">
                            <div class="form-group col mb-5">
                                <p>
                                    The following form must be completed by
                                    anyone using
                                    <a
                                        href="https://cadre.iu.edu/"
                                        target="_blank"
                                        >Collaborative Archive &amp; Data
                                        Research Environment</a
                                    >
                                    (CADRE) as part of their affiliated
                                    institution's trial period with CADRE.
                                </p>
                                <h4 class="mb-3">Personal Information</h4>
                                <div
                                    class="form-row mb-3 d-flex flex-fill align-center"
                                >
                                    <div class="col">
                                        <label for="trial_form_first_name"
                                            >First Name</label
                                        >
                                        <input
                                            id="trial_form_first_name"
                                            required
                                            class="form-control"
                                            type="text"
                                            v-model="first_name"
                                            :placeholder="first_name"
                                        />
                                    </div>
                                    <div class="col-sm-2">
                                        <label for="trial_form_middle_initial"
                                            >Middle Initial</label
                                        >
                                        <input
                                            id="trial_form_middle_initial"
                                            class="form-control"
                                            type="text"
                                            v-model="middle_initial"
                                            :placeholder="middle_initial"
                                        />
                                    </div>
                                    <div class="col">
                                        <label for="trial_form_last_name"
                                            >Last Name</label
                                        >
                                        <input
                                            id="trial_form_last_name"
                                            required
                                            class="form-control"
                                            type="text"
                                            v-model="last_name"
                                            :placeholder="last_name"
                                        />
                                    </div>
                                </div>
                                <div class="form-row mb-3">
                                    <div class="col">
                                        <label for="trial_form_university"
                                            >University</label
                                        >
                                        <select
                                            id="trial_form_university"
                                            required
                                            class="form-control"
                                            type="text"
                                            v-model="university"
                                        >
                                            <option disabled selected>
                                                Select One
                                            </option>
                                            <option>
                                                University of Toronto
                                            </option>
                                        </select>
                                    </div>
                                    <div class="col">
                                        <label for="trial_form_department"
                                            >Department/School</label
                                        >
                                        <input
                                            id="trial_form_department"
                                            required
                                            class="form-control"
                                            type="text"
                                            v-model="department"
                                            :placeholder="department"
                                        />
                                    </div>
                                </div>
                                <div class="form-row mb-3">
                                    <div class="col">
                                        <label for="trial_form_research_area"
                                            >Research Area</label
                                        >
                                        <input
                                            id="trial_form_research_area"
                                            required
                                            class="form-control"
                                            type="text"
                                            v-model="research_area"
                                            :placeholder="research_area"
                                        />
                                    </div>
                                    <div class="col">
                                        <label for="trial_form_university_email"
                                            >University Affiliated Email
                                            Address</label
                                        >
                                        <input
                                            id="trial_form_university_email"
                                            required
                                            class="form-control"
                                            type="text"
                                            v-model="university_email_address"
                                            :placeholder="
                                                university_email_address
                                            "
                                        />
                                    </div>
                                </div>
                                <!-- <label for="trial_form">Expected Research Period</label>
                                <input
                                    id="trial_form"
                                    class="form-control mb-3"
                                    type="text"
                                    v-model=" research_period"
                                    :placeholder=" research_period"
                                />
                                <div class="form-row mb-3">
                                    <div class="col">
                                        <label for="trial_form">Start Date</label>
                                        <input
                                            id="trial_form"
                                            class="form-control"
                                            type="text"
                                            v-model=" start_date"
                                            placeholder="mm/dd/yyyy"
                                        />
                                    </div>
                                    <div class="col">
                                        <label for="trial_form">End Date</label>
                                        <input
                                            id="trial_form"
                                            class="form-control"
                                            type="text"
                                            v-model=" end_date"
                                            placeholder="mm/dd/yyyy"
                                        />
                                    </div>
                                </div>
                                <label> for="trial_form" Would you like to be subscribed to CADRE's newsletter?</label>
                                <div class="form-group 
                                    id="trial_form"col-5">
                                <input
                                    class="mr-2 "
                                    type="radio"
                                    name="yes_subscribe"
                                    value=true
                                    v-model=" subscribe_newsletter"
                                />Yes
                                <input
                                    class="mr-2 ml-3"
                                    type="radio"
                                    name="no_subscribe"
                                    value=false
                                    v-model=" subscribe_newsletter"
                                />No
                                </div> -->
                            </div>
                            <!-- <div class="form-group col mb-5">
                                <h4 class="mb-3">Project Information</h4>
                                <div class="form-group col">
                                    <p>
                                        In order to better understand the needs of our users and make sure the necessary services and tools are available, please share what kind of research projects you are interested in pursuing.
                                    </p>
                                    <textarea 
                                        type="text"
                                        class="form-control mb-3"
                                        :placeholder=" research_projects"
                                        v-model=" research_projects">
                                    </textarea>
                                    <p>
                                        Why are you interested in using CADRE for your project?
                                    </p>
                                    <textarea 
                                        type="text"
                                        class="form-control"
                                        :placeholder=" cadre_interest"
                                        v-model=" cadre_interest">
                                    </textarea>
                                </div>
                            </div> -->
                            <div class="form-group col mb-5">
                                <h4 class="mb-3">
                                    Trial Period and Data Retention
                                </h4>
                                <div class="form-group col">
                                    <p>
                                        Your university’s trial period lasts
                                        three months from the date the initial
                                        trial and licensing agreement is signed.
                                        Please reach out to CADRE or your
                                        university’s CADRE representative to
                                        confirm the exact date the institution’s
                                        trial began. You will be sent an email
                                        reminder two weeks before the end of
                                        your trial period to ensure you have
                                        enough time to remove your data and
                                        code, if necessary.
                                    </p>
                                </div>
                            </div>
                            <div class="form-group col mb-5">
                                <h4 class="mb-3">
                                    Expectations for Trial and Technical Support
                                </h4>
                                <div class="form-group col">
                                    <p>
                                        As part of our trial, you will receive
                                        access to all of the available CADRE
                                        features and datasets that our paying
                                        members receive access to, including Web
                                        of Science data through your
                                        institution’s license. Open access
                                        dataset Microsoft Academic Graph is also
                                        included in CADRE.
                                    </p>
                                    <p>
                                        Any questions you have about the
                                        platform should be asked in the
                                        #cadre-users Slack channel. Email
                                        <a href="mailto:smcgavin@iu.edu">Stephanie Hernandez McGavin</a> with a
                                        request to join CADRE’s Slack workspace.
                                        To report bugs about the platform, fill
                                        out CADRE’s <a href="/contact-us">contact form</a> with your
                                        message.
                                    </p>
                                </div>
                            </div>
                            <div class="form-group col mb-5">
                                <h4 class="mb-3">
                                    Data Access Use and Conditions
                                </h4>
                                <div class="form-group col">
                                    <p>
                                        Finally, please confirm that you agree
                                        to the following:
                                    </p>
                                    <div class="form-group">
                                        <div class="form-group">
                                            <label
                                                for="agree_access_policy"
                                                class="align-left"
                                            >
                                                <input
                                                    required
                                                    type="checkbox"
                                                    id="agree_access_policy"
                                                    name="agree_confirm"
                                                    v-model="
                                                        agree_access_policy
                                                    "
                                                    class=""
                                                />
                                                You have read and agreed to the
                                                terms of the
                                                <a
                                                    href="https://iuni.iu.edu/resources/datasets/cadre/access-policy"
                                                    target="_blank"
                                                    >CADRE Access Policy</a
                                                >
                                            </label>
                                        </div>
                                        <div class="form-group">
                                            <label
                                                for="agree_not_share_data"
                                                class="align-left"
                                            >
                                                <input
                                                    required
                                                    type="checkbox"
                                                    id="agree_not_share_data"
                                                    name="agree_not_share_data"
                                                    v-model="
                                                        agree_not_share_data
                                                    "
                                                    class=""
                                                />
                                                Any data extracted from the
                                                enclave at your request should
                                                not be shared with anyone.
                                            </label>
                                        </div>
                                        <div class="form-group">
                                            <label
                                                for="agree_not_share_username"
                                                class="align-left"
                                            >
                                                <input
                                                    required
                                                    type="checkbox"
                                                    id="agree_not_share_username"
                                                    name="agree_not_share_username"
                                                    v-model="
                                                        agree_not_share_username
                                                    "
                                                    class=""
                                                />
                                                Usernames and passwords should
                                                not be shared with anyone.
                                            </label>
                                        </div>
                                        <div class="form-group">
                                            <label
                                                for="agree_safeguard_username"
                                                class="align-left"
                                            >
                                                <input
                                                    required
                                                    type="checkbox"
                                                    id="agree_safeguard_username"
                                                    name="agree_safeguard_username"
                                                    v-model="
                                                        agree_safeguard_username
                                                    "
                                                    class=""
                                                />
                                                You agree to safeguard your
                                                username and password.
                                            </label>
                                        </div>
                                        <div class="form-group">
                                            <label
                                                for="agree_unauthorized_responsibility"
                                                class="align-left"
                                            >
                                                <input
                                                    required
                                                    type="checkbox"
                                                    id="agree_unauthorized_responsibility"
                                                    name="agree_unauthorized_responsibility"
                                                    v-model="
                                                        agree_unauthorized_responsibility
                                                    "
                                                    class=""
                                                />
                                                Any unauthorized use of that
                                                account will be your individual
                                                responsibility.
                                            </label>
                                        </div>
                                        <div class="form-group">
                                            <label
                                                for="agree_loss_control"
                                                class="align-left"
                                            >
                                                <input
                                                    required
                                                    type="checkbox"
                                                    id="agree_loss_control"
                                                    name="agree_loss_control"
                                                    v-model="agree_loss_control"
                                                    class=""
                                                />
                                                Any loss of your personal
                                                control over the username or
                                                password has to be reported to
                                                the CADRE Data Manager.
                                            </label>
                                        </div>
                                        <div class="form-group">
                                            <label
                                                for="agree_publications_acknowledge"
                                                class="align-left"
                                            >
                                                <input
                                                    required
                                                    type="checkbox"
                                                    id="agree_publications_acknowledge"
                                                    name="agree_publications_acknowledge"
                                                    v-model="
                                                        agree_publications_acknowledge
                                                    "
                                                    class=""
                                                />
                                                All publications that result
                                                from using the data need to have
                                                the acknowledgement text
                                                described in sections 2.2 - 2.5
                                                of the CADRE Access Policy.
                                            </label>
                                        </div>
                                        <div class="form-group">
                                            <label
                                                for="agree_receive_emails"
                                                class="align-left"
                                            >
                                                <input
                                                    required
                                                    type="checkbox"
                                                    id="agree_receive_emails"
                                                    name="agree_receive_emails"
                                                    v-model="
                                                        agree_receive_emails
                                                    "
                                                    class=""
                                                />
                                                You are willing to receive
                                                emails from the IUNI Data
                                                Manager containing news
                                                regarding the enclave and CADRE
                                                data.
                                            </label>
                                        </div>
                                        <div class="form-group">
                                            <label
                                                for="agree_works_submitted"
                                                class="align-left"
                                            >
                                                <input
                                                    required
                                                    type="checkbox"
                                                    id="agree_works_submitted"
                                                    name="agree_works_submitted"
                                                    v-model="
                                                        agree_works_submitted
                                                    "
                                                    class=""
                                                />
                                                Scholarly works that result from
                                                using the data will be submitted
                                                to the IUNI Data Manager as soon
                                                as they are published.
                                            </label>
                                        </div>
                                        <div class="form-group">
                                            <label
                                                for="agree_comply"
                                                class="align-left"
                                            >
                                                <input
                                                    required
                                                    type="checkbox"
                                                    id="agree_comply"
                                                    name="agree_comply"
                                                    v-model="agree_comply"
                                                    class=""
                                                />
                                                I affirm that to the best of my
                                                knowledge all information
                                                provided above is complete and
                                                true and that I will comply with
                                                all Indiana University policies
                                                with regards to the use of
                                                restricted data.
                                            </label>
                                        </div>
                                    </div>
                                    <div class="mt-3">
                                        <button
                                            class="float-left btn btn-primary"
                                            type="submit"
                                        >
                                            Confirm Agreement
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </section>
        <modal
            @close="success_message = ''"
            v-if="success_message"
            modal-style="success"
            close-button-label="OK"
        >
            <h5>{{ success_message }}</h5>
        </modal>
        <modal
            @close="error_message = ''"
            v-if="error_message"
            modal-style="danger"
            close-button-label="Close"
        >
            <h5>{{ error_message }}</h5>
        </modal>
    </div>
</template>
<style lang="scss">
$border: solid gray 1px;
</style>
