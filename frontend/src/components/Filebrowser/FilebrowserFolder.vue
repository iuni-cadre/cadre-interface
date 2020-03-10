<template>
    <div class="folder">
        <div class="folder-name-container">
            <div
                v-if="!is_root"
                class="checkbox-container form-check"
            >
                <input
                    v-if="!filesOnly"
                    class="form-check-input"
                    v-model="checked"
                    type="checkbox"
                />
            </div>
            <div
                @click="opened = !opened"
                class="folder-name"
            >
                <span class="chevron">
                    <fa
                        v-if="!opened"
                        :icon="['fas', 'chevron-right']"
                    />
                    <fa
                        v-if="opened"
                        :icon="['fas', 'chevron-down']"
                    />
                </span>
                <span :class="{'checked':checked}">{{name}}</span>
                <!-- <button
                    class="btn btn-link"
                    @click.stop.prevent="refreshFolder(item.path)"
                >
                    <fa :icon="'sync-alt'" />
                    <span>Refresh</span>
                </button> -->
            </div>
        </div>

        <ul
            v-if="opened"
            class="list-unstyled"
        >
            <li
                v-for="subitem in child_folders"
                :key="`li_${subitem.path}`"
            >
                <folder
                    :item="subitem"
                    :selectedPaths="selectedPaths"
                    :select-one="selectOne"
                    :files-only="filesOnly"
                    @refresh="(path) => {refreshFolder(path); }"
                    @checked="(path) => {selectPath(path)}"
                    @unchecked="(path) => {deselectPath(path)}"
                />
            </li>
            <li
                v-for="subitem in child_files"
                :key="`li_${subitem.path}`"
            >
                <file
                    :item="subitem"
                    :selectedPaths="selectedPaths"
                    :select-one="selectOne"
                    :files-only="filesOnly"
                    @checked="(path) => {selectPath(path)}"
                    @unchecked="(path) => {deselectPath(path)}"
                />
            </li>
        </ul>
    </div>
</template>

<script>
import Folder from "./FilebrowserFolder";
import File from "./FilebrowserFile";

export default {
    name: "folder",
    data: function() {
        return {
            opened: false,
            checked: this.selectedPaths.indexOf(this.item.path) >= 0,
            show_hidden: false
        };
    },
    computed: {
        name: function() {
            let tmp = this.item.path.split("/");
            let name = tmp.pop();
            return name || "/";
        },
        child_files: function() {
            return this.item.children.filter(item => {
                return item.type === "file" && (this.show_hidden || item.path.split("/").pop()[0] != ".");
            });
        },
        child_folders: function() {
            return this.item.children.filter(item => {
                return item.type === "folder" && (this.show_hidden || item.path.split("/").pop()[0] != ".");
            });
        },
        is_root: function() {
            return this.name == "/";
        }
    },
    props: {
        item: Object,
        selectedPaths: Array,
        selectOne: {
            type: Boolean,
            default: false
        },
        filesOnly: {
            type: Boolean,
            default: false
        }
    },
    components: {
        File,
        Folder
    },
    methods: {
        refreshFolder: function(path) {
            this.$emit("refresh", path);
        },
        selectPath: function(path) {
            this.$emit("checked", path);
        },
        deselectPath: function(path) {
            this.$emit("unchecked", path);
        }
    },
    watch: {
        checked: function() {
            if (this.checked == true) {
                this.selectPath(this.item.path);
            } else {
                this.deselectPath(this.item.path);
            }
        },
        selectedPaths: function() {
            if (this.selectedPaths.indexOf(this.item.path) < 0) {
                this.checked = false;
            } else {
                this.checked = true;
            }
        },
        opened: function(){
            if(this.opened)
            {
                let filesystem_prom = this.$store.dispatch("filesystem/getFiles", {path: this.item.path});
                filesystem_prom.then(
                    resp => {},
                    err => {
                        console.error(err);
                        this.handleError("Could not fetch user file listing.");
                    }
                );
            }
        }
    },
    mounted: function() {
        if (this.is_root) {
            this.opened = true;
        }
    }
};
</script>

<style lang="scss" scoped>
button.btn {
    padding: 0;
    margin: 0;
    span {
        display: none;
    }
}
ul {
    margin-left: 1rem;
}
.folder-name {
    cursor: pointer;
    -ms-user-select: none;
    -webkit-user-select: none;
    user-select: none;
}

.chevron {
    padding-right: 0.5rem;
}
.folder-name-container {
    & > div {
        display: inline-block;
    }
    .checked {
        font-weight: bold;
    }

    button {
        display: none;
        max-height: 1rem;
        vertical-align: top;
    }

    &:hover button {
        display: inline-block;
    }

    .checkbox-container {
        // display: block;
        // background-color: blue;
        // position: absolute;
        margin-left: -2rem;
        padding-left: 2rem;
        width: 2rem;
        position: relative;
        height: 1.5rem;
        vertical-align: middle;
    }
    .checkbox-container input {
        display: none;
    }
    &:hover .checkbox-container input,
    .checkbox-container input:checked {
        display: block;
    }
}
</style>
