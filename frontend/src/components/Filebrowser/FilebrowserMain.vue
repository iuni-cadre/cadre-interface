<template>
    <div>
        <!-- This is a file browser -->
        <!-- {{selected_paths}} -->

        <div
            v-for="item in file_structure"
            :key="`file_browser_${item.path}`"
        >
            <component
                :is="item.type"
                :item="item"
                :selectedPaths="selected_paths"
                :select-one="selectOne"
                :files-only="filesOnly"
                @error="handleError"
                @refresh="(path)=>{ refreshFolder(path) }"
                @checked="(path)=>{ selectPath(path) }"
                @unchecked="(path)=>{ deselectPath(path) }"
            />
        </div>
        <div v-if="file_structure.length == 0">
            Could not fetch file listing
        </div>
        <modal
            v-if="error_message"
            @close="error_message=''"
            modalStyle="danger"
        >
            <div v-text="error_message"></div>
        </modal>
        <!-- <pre>{{
            selected_paths
        }}</pre>-->
        <!-- <template v-if="error_message">
            <div class="modal show"
                 style="display: block;"
                 tabindex="-1"
                 role="dialog">
                <div class="modal-dialog "
                     role="document">
                    <div class="modal-content">
                        <div class="alert alert-danger mb-0">
                            <div class="modal-header">
                                <h5 class="modal-title">There was a problem with your query</h5>
                                <button type="button"
                                        class="close"
                                        @click="error_message = ''"
                                        aria-label="Close">
                                    <span aria-hidden="true">&times;</span>
                                </button>
                            </div>
                            <div class="modal-body">
                                <p v-text="error_message"></p>
                            </div>
                            <div class="modal-footer">
                                <button type="button"
                                        class="btn btn-secondary"
                                        @click="error_message = ''">OK</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="modal-backdrop fade show"
                 @click="error_message = ''"></div>
        </template>-->
    </div>
</template>

<script>
import Folder from "./FilebrowserFolder";
import File from "./FilebrowserFile";
import Modal from "../Common/CommonModal";
export default {
    data: function() {
        return {
            opened_paths: [],
            error_message: "",
            selected_paths: []
        };
    },
    computed: {
        file_structure: function() {
            return this.$store.state.filesystem.file_structure;
        }
    },
    props: {
        value: Array,
        selectOne: {
            type: Boolean,
            default: false
        },
        filesOnly: {
            type: Boolean,
            default: false
        }
    },
    methods: {
        handleError: function(error_message) {
            this.error_message = error_message;
        },
        refreshFolder: function(path) {
            console.debug(path);
            this.getFiles(path);
        },
        getFiles: function(path) {
            console.debug(path);
        },
        selectPath: function(path) {
            if(!this.selectOne)
            {
                let path_index = this.selected_paths.indexOf(path);
                if (path_index < 0) {
                    this.selected_paths.push(path);
                } else {
                    // this.selected_paths.splice(path_index, 1);
                }
            }
            else
            {
                this.$set(this, "selected_paths", [path]);
            }
            return this.selected_paths;
        },
        deselectPath: function(path) {
            // if(!this.selectOne)
            // {
                let path_index = this.selected_paths.indexOf(path);
                if (path_index < 0) {
                    // this.selected_paths.push(path);
                } else {
                    this.selected_paths.splice(path_index, 1);
                }
            // }
            // else
            // {
            //     // this.$set(this, "selected_paths", [path]);
            // }
            return this.selected_paths;
        }
    },
    components: {
        Folder,
        File,
        Modal
    },
    watch: {
        selected_paths: function() {
            this.$emit("input", this.selected_paths);
        },
        value: function() {
            if (this.value != this.selected_paths) {
                this.$set(this, "selected_paths", this.value);
            }
        }
    },
    mounted: function() {
        let filesystem_prom = this.$store.dispatch("filesystem/getFiles", {path: "/"});
        filesystem_prom.then(
            resp => {},
            err => {
                console.error(err);
                this.handleError("Could not fetch user file listing.");
            }
        );
    }
};
</script>
<style lang="scss" scoped>
</style>
