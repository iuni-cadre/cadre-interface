<template>

    <div class="container my-5">
        <file-browser />
    </div>

</template>

<script>
import FileBrowser from "../../components/Filebrowser/FilebrowserMain";

export default {
    components: {
        FileBrowser
    },
    mounted: function() {

        let sample_part1 = [
            {
                path: "/packages",
                type: "folder"
            },
            {
                path: "/query-results",
                type: "folder"
            },
            {
                path: "/query-results/JOBID1234.csv",
                type: "file",
                download_url: "https://xxxxxxxxxxx" //S3 bucket path or custom proxy url for downloading... however we decide to implement downloads
            },
            {
                path: "/query-results/JOBID2345.csv",
                type: "file",
                download_url: "https://xxxxxxxxxxx" //S3 bucket path or custom proxy url for downloading... however we decide to implement downloads
            }
        ];

        let sample_part2 = [
            {
                path: "/query-results/JOBID123410.csv",
                type: "file",
                download_url: "https://xxxxxxxxxxx" //S3 bucket path or custom proxy url for downloading... however we decide to implement downloads
            },
            {
                path: "/query-results/JOBID234510.csv",
                type: "file",
                download_url: "https://xxxxxxxxxxx" //S3 bucket path or custom proxy url for downloading... however we decide to implement downloads
            },
            {
                path: "/query-results/packages",
                type: "folder"
            }
        ];

        this.$store.commit("filesystem/updateFileStructure", sample_part1);
        this.$store.commit("filesystem/updateFileStructure", sample_part2);

    }
};
</script>

<style>
</style>
