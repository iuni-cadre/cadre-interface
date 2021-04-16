<script>
import Datasets from "../../datasets";
export default {
    data() {
        return {
            field_value: "",
            filter_type: null,
            filter_value: null,
            operator: null,
            range: {
                begin: null,
                end: null,
            },
            debounce_timer: 0,
        };
    },
    props: {
        index: Number,
        query_errors: Object,
        queries: Array,
        operator_types: Array,
        value: Object,
    },
    computed: {
        current_field() {
            return this.fields[this.field_value];
        },
        fields() {
            return this.$store.getters["query/inputFields"];
        },
        field_options() {
            // return field_options;
            let field_array = [];
            let fields = this.fields;
            for (let field in fields) {
                field_array.push({ value: field, label: fields[field] });
            }

            const exclusive_fields =
                (Datasets[this.$store.getters["query/selectedDataset"]] &&
                    Datasets[this.$store.getters["query/selectedDataset"]]
                        .fields.exclusive_input_fields) ||
                [];

            let exclusive_selected = this.queries
                .filter((item) => exclusive_fields.includes(item.field))
                .map((item) => item.field);

            return function (current_value) {
                // console.debug(exclusive_selected, current_value)
                if (exclusive_selected.length > 0) {
                    let filtered = field_array.filter(
                        (item) =>
                            item.value == current_value ||
                            !exclusive_selected.includes(item.value)
                    );
                    return filtered;
                }

                return field_array;
            };
        },
    },
    watch: {
        field_value() {
            // queries[index].field
            this.filter_type = this.current_field.type || "text";
            this.$emit("fieldChanged", {
                index: this.index,
                field: this.field_value,
            });
        },
        // filter_type() {
        //     console.debug("change range");

        // },
        filter_value() {
            this.$emit("valueChanged", {
                index: this.index,
                value: this.filter_value,
            });

            if (this.filter_type == "range") {
                try {
                    const [b, e] = this.filter_value.split("/");
                    this.range.begin = b.split("T")[0];
                    this.range.end = e.split("T")[0];
                } catch (e) {
                    console.debug("Ignore this", e);
                }
            }
        },
        value(o, n) {
            this.field_value = this.value.field;
            this.filter_value = this.value.value;
            this.operator = this.value.operator;
        },
        range: {
            deep: true,
            handler() {
                const b = new Date(this.range.begin + "T00:00:00");
                const e = new Date(this.range.end + "T00:00:00");
                // console.debug(b, e)
                if (
                    isNaN(b.getTime()) ||
                    isNaN(e.getTime()) ||
                    b.getTime() >= e.getTime()
                ) {
                    console.debug("Invalid Date Range");
                    // this.filter_value = null;  //Using this will cause the whole filter to blank out if one field is invalid
                    return;
                }

                const value =
                    b.toISOString().split(".")[0] +
                    "/" +
                    e.toISOString().split(".")[0];

                this.filter_value = value;
            },
        },
    },
    methods: {
        removeFilter() {
            this.$emit("removeFilter", { index: this.index });
        },
        debounceRange(callback) {
            clearTimeout(this.debounce_timer);
            this.debounce_timer = 0;
            this.debounce_timer = setTimeout(() => {
                callback();
            }, 1000);
        },
    },
    mounted() {
        this.field_value = this.value.field;
        this.filter_value = this.value.value;
        this.operator = this.value.operator;
    },
};
</script>

<template>
    <div>
        <div
            class="alert d-flex justify-content-between align-items-end"
            :class="{ 'alert-danger': query_errors[index] }"
        >
            <div class="form-group">
                <label :for="`field_${index}`">Field</label>
                <select
                    :id="`field_${index}`"
                    class="form-control"
                    v-model="field_value"
                >
                    <option disabled selected :value="''">
                        Choose a search field
                    </option>
                    <option
                        v-for="field in field_options(queries[index].field)"
                        :key="`${field.value}_${index}`"
                        :value="field.value"
                        v-text="field.label.label || field.label"
                    ></option>
                </select>
            </div>
            <div class="form-group col">
                <label :for="`value_${index}`">Value</label>
                <input
                    v-if="filter_type == 'text'"
                    :id="`value_${index}`"
                    class="form-control"
                    type="text"
                    v-model="filter_value"
                />
                <div
                    class="d-flex align-items-center"
                    v-else-if="filter_type == 'range'"
                >
                    <label :for="`value_${index}_b`" class="mx-3 my-0">
                        From:
                    </label>
                    <input
                        :id="`value_${index}_b`"
                        class="form-control"
                        type="date"
                        :value="range.begin"
                        @blur="
                            (e) => {
                                range.begin = e.target.value;
                            }
                        "
                        @input="
                            (e) => {
                                debounceRange(() => {
                                    range.begin = e.target.value;
                                });
                            }
                        "
                        placeholder="YYYY-MM-DD"
                    />
                    <label :for="`value_${index}_e`" class="mx-3 my-0">
                        To:
                    </label>
                    <input
                        :id="`value_${index}_e`"
                        class="form-control"
                        type="date"
                        :value="range.end"
                        @blur="
                            (e) => {
                                range.end = e.target.value;
                            }
                        "
                        @input="
                            (e) => {
                                debounceRange(() => {
                                    range.end = e.target.value;
                                });
                            }
                        "
                        placeholder="YYYY-MM-DD"
                    />

                </div>
                <input
                    v-else
                    class="form-control disabled"
                    disabled
                    placeholder="Choose a field"
                />
            </div>

            <div class="form-group">
                <button
                    class="btn btn-outline-danger"
                    type="button"
                    @click.stop.prevent="removeFilter"
                >
                    <fa icon="trash-alt" class="mr-1" /> Remove Filter
                </button>
            </div>
            
        </div>
            <!-- {{filter_value}} -->

        <div v-if="index != queries.length - 1">
            <!-- <div v-if="operator_types.length > 1" class="form-group">
                <label>Operator</label>
                <select
                    class="form-control"
                    style="width: auto"
                    v-model="queries[index].operator"
                >
                    <option disabled selected :value="''">
                        Choose an operand
                    </option>
                    <option
                        v-for="operator in operator_types"
                        :key="`${operator}_${index}`"
                        :value="operator"
                        v-text="operator"
                    ></option>
                </select>
            </div> -->
            <div>
                <!-- <input type="hidden" 
                                        :value="operator_types[0]" 
                                        v-model="queries[index].operator" /> -->
                {{ operator_types[0] }}
            </div>
        </div>
    </div>
</template>

<style>
</style>