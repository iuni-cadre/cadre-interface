<template>
    <div>
        <!-- This is a file browser -->
        <div v-for="item in file_structure"
             :key="`file_browser_${item.path}`">
            <component :is="item.type"
                       :item="item"
                       :selectedPaths="selected_paths"
                       @error="handleError"
                       @refresh="(path)=>{ refreshFolder(path) }" 
                       @checked="(path)=>{ selectPath(path) }"/>
        </div>

        <!-- <pre>{{
            selected_paths
        }}</pre> -->
        <template v-if="error_message">
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
        </template>
    </div>
</template>

<script>
import Folder from "./FilebrowserFolder";
import File from "./FilebrowserFile";
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
        value: Array
    },
    methods: {
        handleError: function(error_message) {
            this.error_message = error_message;
        },
        refreshFolder: function(path) {
            console.debug(path);
            this.getFiles(path);
        },
        getFiles: function(path)
        {
            console.debug(path);
        },
        selectPath: function(path){
            let path_index = this.selected_paths.indexOf(path);
            if(path_index < 0)
            {
                this.selected_paths.push(path);
            }
            else
            {
                this.selected_paths.splice(path_index, 1);
            }
            return this.selected_paths;
        }
    },
    components: {
        Folder,
        File
    },
    watch: {
        selected_paths: function(){
            this.$emit("input", this.selected_paths);
        },
        value: function(){
            if(this.value != this.selected_paths)
            {
                this.$set(this, "selected_paths", this.value);
            }
        }
    },
    mounted: function() {
        let filesystem_prom = this.$store.dispatch("filesystem/getFiles");
        filesystem_prom.then(
            resp => {},
            err => {
                console.error(err);
                this.handleError("Could not reach server.");
            }
        );
    }
};
</script>
<style lang="scss" scoped>
</style>
