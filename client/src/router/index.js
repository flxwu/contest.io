import Vue from 'vue';
import Router from 'vue-router';

const routerOptions = [
  { path: '/', component: 'Home' },
  { path: '/contest/:id', component: 'ContestDashboard' },
  { path: '/profile/:id', component: 'Profile' },
  { path: '/contestcreate', component: 'CreateContest' },
  { path: '/dashboard', component: 'Dashboard' },
  { path: '/contests', component: 'Contests' },
  { path: '*', component: '404Error' }
];

const routes = routerOptions.map(route => {
  return {
    ...route,
    component: () => import(`@/components/${route.component}.vue`)
  };
});

Vue.use(Router);

export default new Router({
  routes,
  mode: 'history'
});
