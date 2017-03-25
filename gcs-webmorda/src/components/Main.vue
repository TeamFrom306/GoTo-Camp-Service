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
				<ui-tab title="Schedule" icon="book">
					Schedule
				</ui-tab>

				<ui-tab title="Achievements" icon="people">
					Achievements
				</ui-tab>

				<ui-tab title="Users" icon="collections_bookmark">
					Users
				</ui-tab>

				<ui-tab title="Favourites" icon="favorite">
					Urgent
				</ui-tab>
			</ui-tabs>
		</div>
</template>
