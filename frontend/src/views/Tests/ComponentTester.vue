<template>
    <div class="container my-5">
        <!-- <new-archive-form @startLoading="(key)=>$emit('startLoading',key)" @stopLoading="(key)=>$emit('stopLoading',key)"/> -->
        {{user_id}}
        <test-component :rac-tool="tools[0]" @startLoading="(key)=>$emit('startLoading',key)" @stopLoading="(key)=>$emit('stopLoading',key)" ></test-component>
    </div>
</template>

<script>
// import FileBrowser from "../../components/Filebrowser/FilebrowserMain";
// import NewToolForm from "../../components/Marketplace/MarketplaceNewToolForm";
// import NewArchiveForm from "../../components/Marketplace/MarketplaceNewArchiveForm";
import TestComponent from "../../components/Marketplace/MarketplaceRacToolCard";

const TOOLS = [
    {
        created_on: "2020-01-17T16:55:08.192095+00:00",
        tool_description: "asdf",
        tool_id: "2bdaf7fa-1859-4a45-826b-1a998f0e67cc",
        tool_name: "asdf",
        tool_script_name: "/ISSI-tutorial/plotgraph.py",
        created_by: "1000"
    }
];

export default {
    components: {
        // NewArchiveForm
        TestComponent
    },
    computed: {
        user_id: function() {
            return this.$store.state.user.user_id;
        },
        tools: function(){return TOOLS}
    },
    methods: {
        updated: function() {
            // alert("UPDATED");
        }
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
            },
            {
                path: "/query-results/script.py",
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
