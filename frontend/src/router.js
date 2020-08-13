import Vue from "vue";
import Router from "vue-router";


import HomeDashboard from "./views/RAC_Dashboard/Home.vue";

// import JupyterHub from  "./views/RAC_Dashboard/JupyterHub.vue";
// import QI_Home from  "./views/QueryInterface/Home.vue";
// import QI_Jobs from  "./views/QueryInterface/Jobs.vue";
let JupyterHub = () => import( /* webpackChunkName: "rac" */ "./views/RAC_Dashboard/JupyterHub.vue");
let QI_Home = () => import( /* webpackChunkName: "query_builder" */ "./views/QueryInterface/QueryInterfaceDataSets.vue");
let QI_Builder = () => import( /* webpackChunkName: "query_builder" */ "./views/QueryInterface/QueryInterfaceBuilder.vue");
let JobsList = () => import( /* webpackChunkName: "rac" */ "./views/Jobs/JobsList.vue");
let RAC_Marketplace = () => import( /* webpackChunkName: "rac" */ "./views/Marketplace/MarketplaceHome.vue");
let YourHome = () => import( /* webpackChunkName: "your" */ "./views/Your/YourHome.vue");
let YourProfile = () => import( /* webpackChunkName: "your_profile" */ "./views/Your/YourProfile.vue");

Vue.use(Router);

export default new Router({
    mode: "history",
    base: process.env.BASE_URL,
    routes: [
        {
            path: "/",
            name: "home",
            component: HomeDashboard
        },
        {
            path: "/dashboard",
            name: "dashboard",
            component: HomeDashboard
        },
        {
            path: "/jupyter",
            name: "jupyter-hub",
            component: JupyterHub
        },
        {
            path: "/query-builder/choose-data-set",
            name: "query-builder",
            component: QI_Home
        },
        {
            path: "/query-builder/build-query",
            name: "query-builder-builder",
            component: QI_Builder
        },
        {
            path: "/jobs",
            name: "jobs-list",
            component: JobsList
        },
        {
            path: "/jobs/:job_id",
            name: "jobs-list-id",
            component: JobsList
        },
        {
            path: "/rac",
            name: "rac-marketplace",
            component: RAC_Marketplace
        },
        {
            path: "/your",
            name: "your-home",
            component: YourHome
        },
        {
            path: "/profile",
            name: "your-profile",
            component: YourProfile
        },
        {
            path: "/component_test",
            name: "component_test",
            component: () => import(/* webpackChunkName: "Test" */ './views/Tests/ComponentTester.vue')
        }
        // {
        //   path: '/about',
        //   name: 'about',
        //   // route level code-splitting
        //   // this generates a separate chunk (about.[hash].js) for this route
        //   // which is lazy-loaded when the route is visited.
        //   component: () => import(/* webpackChunkName: "about" */ './views/About.vue')
        // }
    ],
    scrollBehavior() {
        document.getElementById('app').scrollIntoView()
    }
});
