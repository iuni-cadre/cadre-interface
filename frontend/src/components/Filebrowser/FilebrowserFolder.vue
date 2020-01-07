<template>
    <div class="folder">
        <div
            @click="opened = !opened"
            class="folder-name"
        >
            <fa
                v-if="!opened"
                :icon="['fas', 'chevron-right']"
            />
            <fa
                v-if="opened"
                :icon="['fas', 'chevron-down']"
            />
            {{name}}
            <button
                class="btn btn-link"
                @click.stop.prevent="refreshFolder(item.path)"
            >
                <fa :icon="'sync-alt'" />
                <span>Refresh</span>
            </button>
        </div>
        <div v-if="!is_root">
            <input
                v-model="checked"
                type="checkbox"
            />
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
                    @refresh="(path) => {refreshFolder(path); }"
                    @checked="(path) => {selectPath(path)}"
                />
            </li>
            <li
                v-for="subitem in child_files"
                :key="`li_${subitem.path}`"
            >
                <file
                    :item="subitem"
                    @checked="(path) => {selectPath(path)}"
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
            checked: false
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
                return item.type === "file";
            });
        },
        child_folders: function() {
            return this.item.children.filter(item => {
                return item.type === "folder";
            });
        },
        is_root: function() {
            return this.name == "/";
        }
    },
    props: {
        item: Object
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
        }
    },
    watch: {
        checked: function() {
            this.selectPath(this.item.path);
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

    button {
        display: none;
        max-height: 1rem;
        vertical-align: top;
    }

    &:hover button {
        display: inline-block;
    }
}
</style>
