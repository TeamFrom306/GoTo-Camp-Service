<template>
<div style="width: 100vw;height: 100vh;display: table;">
	<div style="display: table-cell;text-align: center;vertical-align: middle;">
		<div style="display: inline-block;text-align: left;">
			<ui-textbox
				style="margin:10px;display:inline-block"
				floating-label
				label="Password"
				v-model="password"
				@keydown.enter="login"
			></ui-textbox>
			<ui-button
				style="margin:10px;display:inline-block"
				@click="login"
			>Log in</ui-button>
		</div>
	</div>
</div>
</template>

<script>
	import {api} from '@/web';
	import hash from 'js-sha256';

	export default {
		data() {
			return {
				password: ''
			}
		},
		methods: {
			login() {
				console.log(this);
				if (this.password.length > 0)				
					api.login(require('js-sha256')(this.password), this.setToken);
				else
					this.error(406, "You must provide a password!");
			},
			setToken(token) {
				this.$root.$options.user.token = token;
			},
			error(code, error) {
				//TODO
				console.log("Error " + code + ": " + error);
			}
		}
	}
</script>
