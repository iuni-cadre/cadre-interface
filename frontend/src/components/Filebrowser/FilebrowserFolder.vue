<template>
    <div>
        {{item.path}}
        <button @click="refreshFolder(item.path)">Refresh</button>
        <ul>
            <li v-for="subitem in item.children"
                :key="`li_${subitem.path}`">
                <component :is="subitem.type"
                           :item="subitem"
                           @refresh="(path) => {refreshFolder(path); }" />
            </li>
        </ul>
    </div>
</template>

<script>
import Folder from "./FilebrowserFolder";
import File from "./FilebrowserFile";

export default {
    name: "folder",
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
        }
    }
};
</script>

<style>
</style>
