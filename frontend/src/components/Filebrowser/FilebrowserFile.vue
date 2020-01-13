<template>
    <div class="file-name">
        <div class="checkbox-container"><input :id="`checkbox ${item.path}`" class="form-check-input" v-model="checked" type="checkbox" /></div>
        <label :for="`checkbox ${item.path}`"><div><span class="filetype"><fa :icon="icon" /></span> {{name}}</div></label>
    </div>
</template>

<script>
export default {
    name: "file",
    data: function(){
        return {
            checked: this.selectedPaths.indexOf(this.item.path) >= 0
        }
    },
    computed: {
        name: function() {
            let tmp = this.item.path.split("/");
            let name = tmp.pop();
            return name || "/";
        },
        extension: function(){
            return this.item.path.split(".")[this.item.path.split(".").length - 1];
        },
        icon: function(){
            if(this.extension == "py")
            {
                return ['fab', 'python'];
            }
            else
            {
                return ['far', 'file'];
            }
        }
    },
    props: {
        item: Object,
        selectedPaths: Array
    },
    watch: {
        checked: function(){
            this.$emit("checked", this.item.path);
        }
    },
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
    label {
        cursor: pointer;
        margin: 0;
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
