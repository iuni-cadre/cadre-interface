<template>
    <div class="container my-5">
        <!-- <new-archive-form @startLoading="(key)=>$emit('startLoading',key)" @stopLoading="(key)=>$emit('stopLoading',key)"/> -->
        {{user_id}}
        <test-component
            @startLoading="(key)=>$emit('startLoading',key)"
            @stopLoading="(key)=>$emit('stopLoading',key)"
        ></test-component>
    </div>
</template>

<script>
import TestComponent from "../../components/Filebrowser/FilebrowserMain";
// import TestComponent from "../../views/Jobs/JobsList";

const TOOLS = [
    {
        tool_description: "",
        tool_id: "aa8d1876-3007-439d-93bd-4619dc270857",
        tool_name: "test",
        created_on: "2020-01-27T21:03:13.358954+00:00",
        permissions: { data_type: "MAG", other: [] },
        created_by: "1000"
    }
];
const ARCHIVES = [
    {
        archive_description: "",
        archive_id: "1",
        archive_name: "test1",
        created_on: "2020-01-27T21:03:13.358954+00:00",
        permissions: { data_type: "MAG", other: [] },
        created_by: "1000"
    },
    {
        archive_description: "",
        archive_id: "2",
        archive_name: "test2",
        created_on: "2020-01-27T21:03:13.358954+00:00",
        permissions: { data_type: "MAG", other: [] },
        created_by: "1000"
    },
    {
        archive_description: "",
        archive_id: "3",
        archive_name: "test3",
        created_on: "2020-01-27T21:03:13.358954+00:00",
        permissions: { data_type: "MAG", other: [] },
        created_by: "1000"
    },
];
export default {
    components: {
        TestComponent
    },
    computed: {
        user_id: function() {
            return this.$store.state.user.user_id;
        },
        tools: function() {
            return TOOLS;
        },
        archives: function() {
            return ARCHIVES;
        }
    },
    methods: {
        updated: function() {
            // alert("UPDATED");
        }
    },
    mounted: function() {
        let sample_part1 = [
            {
                path: "/.packages",
                type: "folder"
            },
            {
                path: "/query-results",
                type: "folder"
            },
            {
                path: "/query-results/.JOBID1234.csv",
                type: "file",
                download_url: "https://xxxxxxxxxxx" //S3 bucket path or custom proxy url for downloading... however we decide to implement downloads
            },
            {
                path: "/query-results/.JOBID2345.csv",
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
            },
            {
                path: "/query-results/reqs.txt",
                type: "file"
            }
        ];

        this.$store.commit("filesystem/updateFileStructure", sample_part1);
        this.$store.commit("filesystem/updateFileStructure", sample_part2);
    }
};
</script>

<style>
</style>
