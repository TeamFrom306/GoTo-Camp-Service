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
				user: this.$root.$options.user,
				groups: [],
				users: [],
				teams: []
			}
		},
		methods: {
			setGroups(response) {
				this.groups = response;
			},
			setUsers(response) {
				this.users = response;
			},
			setTeams(response) {
				this.teams = response;
			}
		},
		mounted() {
			require('./web').api.groups.get('', this.setSchedule, console.log);
			require('./web').api.users.get('', this.setUsers, console.log);
			require('./web').api.teams.get('', this.setTeams, console.log);
		}
	};
</script>
