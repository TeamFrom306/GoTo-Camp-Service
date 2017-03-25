import Main from '@/components/Main';
import Login from '@/components/Login';
import Router from 'vue-router';
import Vue from 'vue';

Vue.use(Router);

var router = new Router({
	mode: 'history',
	routes: [
		{
			path: '/',
			name: 'home',
			component: Main,
			children: [
				//TODO?
			],
			meta: {
				authorized: true
			}
		},
		{
			path: '/login',
			name: 'login',
			component: Login,
			meta: {
				login: true
			}
		},
		{
			path: '*',
			redirect: '/'
		}
	],
});

export default router;
