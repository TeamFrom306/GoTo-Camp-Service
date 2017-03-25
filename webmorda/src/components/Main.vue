<template>
	<div class="page__demo-group page__demo-group--has-tabs">
			<ui-toolbar
				brand="Admin page"
				remove-brand-divider
				text-color="white"
				type="colored"
				:removeNavIcon="true"
				:raised="false"
			></ui-toolbar>

			<ui-tabs
				background-color="primary"
				fullwidth
				indicator-color="white"
				text-color-active="white"
				text-color="white"
				type="text"
			>
				<ui-tab title="Events" icon="book">
					<events></events>
				</ui-tab>

				<ui-tab title="Achievements" icon="people">
					<achievements></achievements>
				</ui-tab>

				<ui-tab title="Users" icon="collections_bookmark">
					<users></users>
				</ui-tab>

				<ui-tab title="Teams" icon="collections_bookmark">
					<teams></teams>
				</ui-tab>

				<ui-tab title="Message" icon="favorite">
					<message></message>
				</ui-tab>

				<ui-tab title="Help & info settings" icon="favorite">
					<help></help>
				</ui-tab>
			</ui-tabs>
		</div>
</template>

<script>
	module.exports = {
		components: {
			events: require('./Events'),
			help: require('./Help'),
			message: require('./Message'),
			achievements: require('./Achievements'),
			teams: require('./Teams'),
			users: require('./Users')
		},
		data() {
			return {
				
			}
		},
	}
</script>
