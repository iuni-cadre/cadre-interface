<template>
    <div>
        <form @submit.stop.prevent>
            <div class="form-group">
                <label>Environment</label>
                <div class="form-control">Python</div>
            </div>
            <div class="form-group">
                <label>Name</label>
                <input
                    v-model="data_to_send.name"
                    placeholder="e.g. My Tool"
                    type="text"
                    class="form-control"
                />
            </div>
            <div class="form-group">
                <label>Description</label>
                <textarea
                    v-model="data_to_send.description"
                    placeholder="e.g. My Tool transforms the given data and returns 2 files."
                    class="form-control"
                ></textarea>
            </div>
            <div class="form-group">
                <label>Script Files</label>
                <div class="form-control file-browser-control">
                    <file-browser v-model="data_to_send.file_paths"></file-browser>
                </div>
            </div>
            <div class="form-group">
                <label>Entrypoint File</label>
                <!-- <input
                    v-model="data_to_send.entrypoint"
                    type="text"
                    class="form-control"
                    placeholder="e.g. /directory/start.py"
                />-->
                <select
                    class="form-control"
                    v-model="data_to_send.entrypoint"
                >
                    <option
                        value
                        disabled
                    >Choose an entrypoint file</option>
                    <option
                        v-for="path in entrypoint_options"
                        :key="path"
                        v-text="path"
                        :value="path"
                    ></option>
                </select>
            </div>
            <div class="form-group">
                <label>Installation Commands</label>
                <small class="ml-1 text-muted">(optional)</small>
                <textarea
                    v-model="data_to_send.install_commands"
                    class="form-control"
                    placeholder="e.g. pip install -r tool_dir/requirements.txt"
                ></textarea>
            </div>
            <div class="form-group">
                <button class="btn btn-primary">Create New Tool</button>
            </div>
            {{data_to_send}}
        </form>
    </div>
</template>

<script>
import FileBrowser from "../../components/Filebrowser/FilebrowserMain";

export default {
    data: function() {
        return {
            data_to_send: {
                name: "",
                install_commands: "",
                description: "",
                file_paths: [],
                entrypoint: "",
                environment: ""
            }
        };
    },
    computed: {
        entrypoint_options: function() {
            return this.data_to_send.file_paths.filter(path => {
                if (path.slice(-3) == ".py") {
                    return true;
                } else {
                    return false;
                }
            });
        }
    },
    components: {
        FileBrowser
    },
    mounted: function() {
        this.data_to_send.environment = "python";
    }
};
</script>

<style>
.form-control.file-browser-control {
    height: 10rem;
    overflow: auto;
}
</style>