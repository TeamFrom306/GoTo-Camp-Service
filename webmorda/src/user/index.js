import config from './../config';

var user = {
	get token() {
		return this.storage.get(config.tokenstring);
	},
	set token(value) {
		return this.storage.set(config.tokenstring, value);
	},
	get isLoggedIn() {
		return !!this.token;
	},
	storage: {
		get(key) {
			return localStorage.getItem(key);
		},

		set(key, value) {
			if (value) localStorage.setItem(key, value);
			return localStorage.getItem(key);
		},

		clear() { 
			localStorage.clear(); 
		},
	}
}

export default user;

export let token = user.token;
