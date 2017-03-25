<template>
<div class="parent">
	<div class="centered">
		<div class="l-form">
			<ui-textbox
				style="margin:10px;display:block;width:100%;margin-bottom:30px"
				floating-label
				label="Password"
				v-model="password"
				:error="error"
				:invalid="inputInvalid"
				:autofocus="true"
				@input="refresh"
				@keydown.enter="login"
			></ui-textbox>
			<ui-button
				style="margin:10px;display:block;width:100%"
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
				password: '',
				error: '',
				inputInvalid: false
			}
		},
		methods: {
			login() {
				console.log(this.$root);
				
				if (this.password.length > 0)				
					api.login(require('js-sha256')(this.password), this.setToken, this.errorCallback);
				else
					this.errorCallback(406, "You must provide a password!");
			},
			setToken(response) {
				this.$root.$options.user.token = response.token;
				this.$router.push("/");
			},
			errorCallback(code, error) {
				this.inputInvalid = true;
				this.error = "Error " + code + ": " + error;
				console.log("Error " + code + ": " + error);
			},
			refresh() {
				this.inputInvalid = false;
			}
		}
	}
</script>

<style>
	.parent {
		width: 100vw;
		height: 100vh;
		display: table;
	}
	.centered {
		display: table-cell;
		text-align: center;
		vertical-align: middle;
	}
	.l-form {
		display: inline-block;
		text-align: left;
		width: 300px;
	}
	.ui-textbox__feedback {
		position: absolute !important;
	}
</style>
