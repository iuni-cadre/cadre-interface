<template>
    <div class="file-name">
        <div class="checkbox-container"><input class="form-check-input" v-model="checked" type="checkbox" /></div>
        <div><span class="filetype"><fa :icon="['far', 'file']" /></span> {{name}}</div>
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

    div
    {
        display: inline-block;
    }

    .checkbox-container
    {
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
    .checkbox-container input
    {
        display: none;
    }
    &:hover .checkbox-container input, .checkbox-container input:checked
    {
        display: block;
    }
}
</style>
