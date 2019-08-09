<template>
    <div>
        <section class="blue">
            <div class="container">
                <h2>Query Builder</h2>
                <nav class="text-center">
                    <ul class="list-unstyled d-flex justify-content-center">
                        <li class="list-item">
                            <router-link :to="{name: 'query-builder'}">Choose Dataset</router-link>
                        </li>

                        <li class="list-item">
                            <router-link :to="{name: 'query-builder-builder'}">Query Builder</router-link>
                        </li>

                        <li class="list-item">
                            <router-link :to="{name: 'query-builder-jobs'}">Jobs Status</router-link>
                        </li>
                    </ul>
                </nav>
            </div>
        </section>
    </div>
</template>

<script>
export default {};
</script>

<style lang="scss" scoped>
nav li {
    padding: 0 2rem;
}
nav li:first-child {
    padding-left: 0;
}
</style>

