import Hello from '@/components/Hello';
import Router from 'vue-router';
import Vue from 'vue';

Vue.use(Router);

export default new Router({
	mode: 'history',
	routes: [
		{
			path: '/hello',
			name: 'Hello',
			component: Hello,
		},
	],
});
