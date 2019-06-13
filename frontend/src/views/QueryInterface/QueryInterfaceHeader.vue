<template>
    <div>
        <h1>Query Builder</h1>
        <nav>
            <ul class="list-unstyled d-flex">
                <li>
                    <router-link :to="{name: 'query-builder'}">Choose Dataset</router-link>
                </li>

                <li>
                    <router-link :to="{name: 'query-builder-builder'}">Query Builder</router-link>
                </li>

                <li>
                    <router-link :to="{name: 'query-builder-jobs'}">Jobs Status</router-link>
                </li>
            </ul>
        </nav>
        <hr />
    </div>
</template>

<script>
export default {};
</script>

<style lang="scss" scoped>
    nav li
    {
        padding: 0 2rem;
    }
    nav li:first-child
    {
        padding-left: 0;
    }
</style>

