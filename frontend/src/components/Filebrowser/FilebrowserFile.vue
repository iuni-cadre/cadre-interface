<template>
    <div class="file-name">
        <div><span class="filetype"><fa :icon="['far', 'file']" /></span> {{name}}</div>
        <div><input v-model="checked" type="checkbox" /></div>
    </div>
</template>

<script>
export default {
    name: "file",
    data: function(){
        return {
            checked: false
        }
    },
    computed: {
        name: function() {
            let tmp = this.item.path.split("/");
            let name = tmp.pop();
            return name || "/";
        }
    },
    props: {
        item: Object
    },
    watch: {
        checked: function(){
            this.$emit("checked", this.item.path);
        }
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
