import Vue from 'vue';
import Router from 'vue-router';
import Fetch from '../components/Fetch.vue'; 
import Todo from '../components/Todo.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/fetch',
      name: 'fetch',
      component: Fetch,
    },
    {
      path: '/todo',
      name: 'todo',
      component: Todo,
    },
  ],
});
