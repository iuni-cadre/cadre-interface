<template>
    <div>
        <query-builder-header />
        <h2>Choose a Dataset</h2>
        <div class="card p-3">
            <template v-for="(dataset, id) in datasets">
                <div :key="`dataset_${id}`"
                     class="d-flex">
                    <button class="btn m-3 p-3 d-flex align-items-center col-4 justify-content-between"
                            :class="dataset_button_styles(id)"
                            @click="selectDataset(id)">
                        <span v-text="dataset.name"></span>
                        <span class="checkbox">
                            <fa :icon="['far', (id === selected_dataset?'check-square':'square')]" />
                        </span>
                    </button>

                    <p class="m-3"
                       v-text="dataset.description || ''">
                    </p>
                </div>
            </template>

        </div>
            <div class="mt-3">
                <router-link :to="{name: 'query-builder-builder'}"
                             class="btn btn-lg btn-primary">Proceed to Query Builder</router-link>
            </div>
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
        }
    },
    methods: {
        selectDataset: function(dataset_id) {
            this.$store.commit("query/setSelectedDataset", dataset_id);
        }
    },
    components: {
        QueryBuilderHeader
    }
};
</script>

<style>
</style>
