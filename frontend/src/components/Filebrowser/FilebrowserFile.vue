<template>
    <div class="file-name">
        <span class="filetype"><fa :icon="['far', 'file']" /></span> {{name}}
    </div>
</template>

<script>
export default {
    name: "file",
    computed: {
        name: function() {
            let tmp = this.item.path.split("/");
            let name = tmp.pop();
            return name || "/";
        }
    },
    props: {
        item: Object
    }
};
</script>

<style lang="scss" scoped>
.file-name {
    cursor: pointer;
    -ms-user-select: none;
    -webkit-user-select: none;
    user-select: none;

    button {
        display: none;
    }

    &:hover button{
        display: inline-block;
    }
}
</style>
