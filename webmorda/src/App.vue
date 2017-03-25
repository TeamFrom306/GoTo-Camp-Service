<template>
	<main>
		<router-view></router-view>
	</main>
</template>

<script>
	export default {
		name: 'main',
		data() {
			return {
				user: this.$root.$options.user
			}
		}
	};
</script>
