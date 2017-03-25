<template>
    <table class="table" style="width: 100%">
        <thead>
            <tr>
                <th>
                    <ui-textbox name floating-label label="Name" v-model="name"></ui-textbox>
                </th>
                <th>
                    <ui-textbox desc floating-label label="Description" v-model="description"></ui-textbox>
                </th>
                <th>
                    <ui-button add color="primary" @click="add">Add</ui-button>
                </th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="a in achievements">
                <td>{{ a.name }}</td>
                <td>{{ a.description }}</td>
                <td><ui-button color="red" @click="remove" :data-id="a.id">X</ui-button></td>
            </tr>
        </tbody>
    </table>
</template>

<script>
    import {api} from './../web';

    export default {
        data() {
            return {
                achievements: [],
                name: '',
                description: ''
            }
        },
        methods: {
            setAchievements(result) {
                this.achievements = result;
            },
            addHelper(result) {
                var id = result.id;
                var name = this.name;
                var description = this.description;
                this.achievements.push({id, name, description});
            },
            add() {
                var name = this.name;
                var description = this.description;
                api.achievements.add({name, description}, this.addHelper);
            },
            removeHelper(id) {
                // this.achievements.remove({id, name, description});
            },
            remove (e) {
                var id = e.dataset.id;
                api.achievements.remove(id, () => {this.removeHelper(id)});
            }
        },
        mounted() {
            api.achievements.get('', this.setAchievements);
        }
    }
</script>

<style scoped>
    [name],[desc],[add] {
        display: inline-block;
    }
</style>
