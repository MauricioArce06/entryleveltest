import userList from "@/components/userList.vue";
import userDetail from "@/components/userDetail.vue";
import { createRouter, createWebHistory } from "vue-router";

const routes = [
  { path: "/", component: userList },
  { path: "/user/:id", name: "UserDetail", component: userDetail },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
