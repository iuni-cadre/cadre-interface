import Vue from "vue";
import Router from "vue-router";
import HomeDashboard from "./views/RAC_Dashboard/Home.vue";
import JupyterHub from "./views/RAC_Dashboard/JupyterHub.vue";
import QI_Home from "./views/QueryInterface/Home.vue";
import QI_Jobs from "./views/QueryInterface/Jobs.vue";

Vue.use(Router);

export default new Router({
    mode: "history",
    base: process.env.BASE_URL,
    routes: [
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
            path: "/query-builder",
            name: "query-builder",
            component: QI_Home
        },
        {
            path: "/query-builder/jobs",
            name: "query-builder-jobs",
            component: QI_Jobs
        }
        // {
        //   path: '/about',
        //   name: 'about',
        //   // route level code-splitting
        //   // this generates a separate chunk (about.[hash].js) for this route
        //   // which is lazy-loaded when the route is visited.
        //   component: () => import(/* webpackChunkName: "about" */ './views/About.vue')
        // }
    ]
});
