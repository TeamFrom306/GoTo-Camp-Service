//js
import Vue from 'vue';
import KeenUI from 'keen-ui';
import App from './App';
import router from './router';
import user from './user';

//css
import 'normalize.css';
import '../static/index.css';
import 'keen-ui/dist/keen-ui.min.css';

Vue.config.productionTip = false;

Vue.use(KeenUI);

router.beforeEach((to, from, next) => {
	if (to.meta.authorized && !user.isLoggedIn)
		router.replace("login");
	else if (to.meta.login && user.isLoggedIn)
		router.replace("/");
	else next();
});

new Vue({
	el: 'main',
	user,
	router,
	render: h => h(App),
});
