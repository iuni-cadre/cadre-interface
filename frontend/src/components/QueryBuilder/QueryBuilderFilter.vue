<script>
import Datasets from "../../datasets";
export default {
    data() {
        return {
            field_value: "",
            filter_values: [
                {
                    value: "",
                    operator: null,
                },
            ],
            filter_type: null,
            // filter_value: null,
            operator: null,
            range: [
                {
                    begin: null,
                    end: null,
                },
            ],
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
        // filter_value() {
        //     this.$emit("valueChanged", {
        //         index: this.index,
        //         value: this.filter_value,
        //     });

        //     if (this.filter_type == "range") {
        //         try {
        //             const [b, e] = this.filter_value.split("/");
        //             this.range.begin = b.split("T")[0];
        //             this.range.end = e.split("T")[0];
        //         } catch (e) {
        //             console.debug("Ignore this", e);
        //         }
        //     }
        // },
        filter_values: {
            deep: true,
            handler() {
                this.$emit("valueChanged", {
                    index: this.index,
                    value: this.filter_values,
                });

                if (this.filter_type == "range") {
                    for (let i in this.filter_values)
                        try {
                            const [b, e] = this.filter_value[i].split("/");
                            this.range[i].begin = b.split("T")[0];
                            this.range[i].end = e.split("T")[0];
                        } catch (e) {
                            console.debug("Ignore this", e);
                        }
                }
            },
        },
        value: {
            deep: true,
            handler(o, n) {
                this.field_value = this.value.field;
                this.$set(this, "filter_values", this.value.value);
            },
        },
        range: {
            deep: true,
            handler(o, n) {
                let index = this.findChangedIndex(o, n);
                if (index < 0) {
                    return;
                }

                const b = new Date(this.range[index].begin + "T00:00:00");
                const e = new Date(this.range[index].end + "T00:00:00");
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

                this.filter_values[index] = value;
            },
        },
    },
    methods: {
        removeFilter() {
            this.$emit("removeFilter", { index: this.index });
        },
        removeFilterValue(index) {
            this.filter_values.splice(index, 1);
            this.range.splice(index, 1);
            this.filter_values[0].operator = "";
        },
        debounceRange(callback) {
            clearTimeout(this.debounce_timer);
            this.debounce_timer = 0;
            this.debounce_timer = setTimeout(() => {
                callback();
            }, 1000);
        },
        addAnotherFilterValue() {
            this.filter_values.push({
                operator: "AND",
                value: "",
            });
            this.filter_values[0].operator = "";
            this.range.push({
                begin: null,
                end: null,
            });
        },
        findChangedIndex(o, n) {
            for (let i = 0; i < o.length; i++) {
                if (o[i].begin != n[i].begin || o[i].end != n[i].end) {
                    return i;
                }
            }
            return -1;
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
    <div class="filter_box mb-3">
        <div
            class="alert d-flex justify-content-between align-items-start"
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
                <label :for="`value_${index}`">Values</label>
                <div
                    class=""
                    v-for="(value, value_index) in filter_values"
                    :key="`value_field_${index}_${value_index}`"
                >
                    <span class="">
                        <select
                            v-if="value_index > 0"
                            v-model="filter_values[value_index].operator"
                            class="form-control w-auto"
                        >
                            <option>AND</option>
                            <option>OR</option>
                        </select>
                        <input
                            type="hidden"
                            value=""
                            v-else
                            v-model="filter_values[value_index].operator"
                        />
                    </span>
                    <div class="d-flex">
                        <input
                            v-if="filter_type == 'text'"
                            :id="`value_${index}_${value_index}`"
                            class="form-control"
                            type="text"
                            v-model="filter_values[value_index].value"
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
                        <button
                            v-if="filter_values.length > 1"
                            style="white-space: nowrap"
                            class="btn btn-outline-danger"
                            type="button"
                            @click.stop.prevent="removeFilterValue(value_index)"
                        >
                            <fa icon="trash-alt" class="mr-1" /> Remove Value
                        </button>
                    </div>
                </div>

                <div class="mt-3">
                    <button
                        @click.stop.prevent="addAnotherFilterValue"
                        class="btn btn-outline-primary"
                    >
                        Add Another Filter Value
                    </button>
                </div>
            </div>
        </div>
        <!-- {{filter_value}} -->

        <div class="d-flex justify-content-end p-3">
            <button
                class="btn btn-outline-danger"
                type="button"
                @click.stop.prevent="removeFilter"
            >
                <fa icon="trash-alt" class="mr-1" /> Remove Filter
            </button>
        </div>

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
.filter_box {
    border: solid black 1px;
    border-radius: 1rem;
}
</style>