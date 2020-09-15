<template>
    <div>
        <query-builder-header />
        <section>
            <div class="container">
                <h3>Choose a Dataset</h3>
                <div class="card p-3">
                    <template v-for="(dataset, id) in datasets">
                        <div v-if="can_access_dataset(id)"
                             :key="`dataset_${id}`"
                             class="d-flex align-items-center">
                            <button class="btn m-3 p-3 d-flex align-items-center col-4 justify-content-between"
                                    :class="dataset_button_styles(id)"
                                    @click="selectDataset(id)">
                                <span v-text="dataset.name"></span>
                                <span class="checkbox">
                                    <fa :icon="['far', (id === selected_dataset?'dot-circle':'circle')]" />
                                </span>
                            </button>

                            <p class="m-3"
                               v-text="dataset.description || ''">
                            </p>
                        </div>

                        <div v-else
                             :key="`dataset_${id}`"
                             class="d-flex disabled dataset-disabled align-items-center">
                            <button disabled
                                    class="btn m-3 p-3 d-flex align-items-center col-4 justify-content-between disabled"
                                    :class="dataset_button_styles(id)">
                                <span v-text="dataset.name"></span>
                                <span class="checkbox">
                                    <fa :icon="['far', (id === selected_dataset?'dot-circle':'circle')]" />
                                </span>
                            </button>

                            <div class="p-3">
                                <p class="m-0 text-muted">
                                    Dataset is unavailable
                                </p>
                                <p class="m-0 text-muted"
                                   v-text="dataset.description || ''">
                                </p>
                            </div>
                        </div>
                    </template>
<hr />
                    <div class="">
                        <router-link :to="{name: 'query-builder-builder'}"
                                    class="btn btn-lg btn-primary m-3 ">Proceed to Query Builder</router-link>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>

<script>
import QueryBuilderHeader from "./QueryInterfaceHeader";

import Datasets from "../../datasets";
export default {
    computed: {
        datasets: function() {
            return Datasets;
        },
        selected_dataset: function() {
            return this.$store.getters["query/selectedDataset"];
        },
        dataset_button_styles: function() {
            let selected_styles = ["btn-primary"];
            let unselected_styles = ["btn-outline-primary"];
            let selected_dataset = this.selected_dataset;
            return function(dataset_id) {
                if (dataset_id == selected_dataset) {
                    return selected_styles;
                } else {
                    return unselected_styles;
                }
            };
        },
        can_access_dataset: function() {
            let user_roles = this.$store.getters["user/roles"];
            return function(dataset_id) {
                let allow = false;
                let dataset_roles = Datasets[dataset_id].allowed_roles;

                //short circuit... if dataset has no allowed roles, it's open for all
                if (dataset_roles.length == 0) {
                    return true;
                }
                //check all my roles.  If at least one of my roles is allowed for this data set, return true
                for (let role of user_roles) {
                    if (dataset_roles.indexOf(role) > -1) {
                        return true;
                    }
                }
            };
        }
    },
    methods: {
        selectDataset: function(dataset_id) {
            this.$store.commit("query/setSelectedDataset", dataset_id);
        }
    },
    components: {
        QueryBuilderHeader
    },
    mounted: function() {
        if (!this.selected_dataset) {
            this.selectDataset("mag");
        }
    }
};
</script>

<style scoped>
.dataset-disabled,
.dataset-disabled button {
    cursor: not-allowed;
}
.dataset-disabled
{
    opacity: .5;
}


button span
{
    font-size: 1.2rem;
}

a.btn
{
    text-decoration: none;
}
</style>
