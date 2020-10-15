<template>
    <div>
        <div class="row">
            <div class="col-12 col-md-6 d-flex align-items-between justify-content-center justify-content-md-start">
                <label class="btn btn-sm mr-3 mb-0  d-flex align-items-center"
                    :class="{
                                'btn-outline-primary': fields_view != 'selected',
                                'btn-primary': fields_view == 'selected'
                            }"
                        for="show_selected_only"><input type="radio"
                        v-model="fields_view"
                        value="selected" class="mr-1" id="show_selected_only"/> Show Selected Only</label>
                <label class="btn btn-sm  mb-0 d-flex align-items-center"
                    for="all_available_fields"
                    :class="{
                                'btn-outline-primary': fields_view != 'all',
                                'btn-primary': fields_view == 'all'
                            }"><input type="radio"
                        id="all_available_fields"
                        v-model="fields_view"
                        value="all" class="mr-1" /> Show All Available Fields</label>
            </div>  
            <div class="col-12 col-md-6 d-flex p-3 p-md-0  align-items-between justify-content-center justify-content-md-end">
                <button @click.stop.prevent="deselectAll"
                    class="btn btn-outline-primary btn-sm d-flex align-items-center">Deselect All</button>
                <button @click.stop.prevent="selectAll"
                    class="btn btn-outline-primary btn-sm d-flex align-items-center ml-3">Select All</button>
            </div>  
        </div>
        <hr />
        <div class="container">
            <div class="row ">
                <template v-for="field in fields">
                    <div class="col-sm-6 col-lg-4 d-flex align-items-center"
                         :key="`${field.field}_field`"
                         v-if="fields_view=='all' || selected_fields.indexOf(field.field) >= 0">
                        <label class="btn d-flex align-items-center"
                            :class="{
                                    'btn-outline-primary': selected_fields.indexOf(field.field) == -1,
                                    'btn-primary': selected_fields.indexOf(field.field) >= 0,
                            }"
                            :for="`${field.field}_field`"
                        >
                            <input type="checkbox"
                                   class="mr-2"
                                   :id="`${field.field}_field`"
                                   v-model="selected_fields"
                                   :value="field.field" />

                            <span :for="`${field.field}_field`"
                                  v-text="field.label"></span>
                        </label>
                    </div>
                </template>
                <template v-if="selected_fields.length == 0">
                    <div class="m-3">No output fields are selected.</div>
                </template>
            </div>
        </div>

    </div>
</template>

<script>
export default {
    data: function() {
        return {
            selected_fields: [],
            fields_view: "selected",
        };
    },
    props: {
        Value: Array,
    },
    computed: {
        fields: function() {
            // return this.$store.getters["query/validFields"];
            let selectable_fields = this.$store.getters["query/outputFields"]
                                    .filter(field=>field.type == "single");
            selectable_fields = selectable_fields.sort((a,b)=>a.label == b.label?0:a.label > b.label?1:-1);
            return selectable_fields
        },
    },
    methods: {

        deselectAll: function() {
            this.selected_fields.splice(0, this.selected_fields.length);
        },
        selectAll: function() {
            this.$set(this, "selected_fields", this.fields.map(item=>item.field));
        },
    },
    watch: {
        Value: function(o, n){
            if(o != n)
            {
                this.$set(this, "selected_fields", this.Value);
            }
        },
        selected_fields: function(o, n){
            if(o != n)
            {
                this.$emit("input", this.selected_fields);
            }
            if(this.selected_fields == 0)
            {
                this.fields_view = 'all';
            }
        }
    }
};
</script>

<style>
</style>
