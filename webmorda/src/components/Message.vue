<template>
    <div>
        <ui-textbox floating-label label="Message" v-model="message"></ui-textbox>
        <ui-select label="Groups" multiple :options="groups" v-model="selected" has-search></ui-select>
        <ui-button @click="send">Send</ui-button>
        <div class="pane">
            <ui-snackbar-container
                ref="snackbarContainer"
                position="right"
            ></ui-snackbar-container>
        </div>
    </div>
</template>

<script>
    import { UiSelect, UiButton, UiTextbox } from 'keen-ui';
    
    export default {
        components: {
            UiSelect, UiButton, UiTextbox
        },
        data() {
            return {
                message: '',
                groups: this.$root.children[0].groups,
                selected: []
            }
        },
        methods: {
            send() {
                require('./../web').api.message.send(this.message, this.selected);
            },
            success(result) {
                this.$refs.snackbarContainer.createSnackbar({
                    message: "'" + this.message + "' is sent!",
                });
            }
        }
    }
</script>
