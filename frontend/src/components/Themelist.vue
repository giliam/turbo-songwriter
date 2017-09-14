<template>
    <div>
        <div id="listthemes">
            <h2>{{ t('List of themes') }}</h2>
            <p @click="synchronize()">{{ t('Update the list') }}</p>
            <div v-if="!is_updating">
                <form v-if="is_editing" class="ui form">
                    <fieldset>
                        <legend>{{ t('Edit an theme') }}</legend>
                        <p class="field">
                            <label for="name">{{ t('Name:') }} </label>
                            <input type="text" name="name" v-model="name">
                        </p>
                        <p class="field">
                            <button class="ui primary button" @click.prevent="saveTheme(true)">{{ t('Save') }}</button>
                            <button class="ui button" @click.prevent="hideThemeForm()">{{ t('Cancel') }}</button>
                        </p>
                    </fieldset>
                </form>
                <ul v-if="!is_editing">
                    <li v-for="item in themes">
                        <p @click="editTheme(item)">{{ item.name }}</p>
                    </li>
                </ul>
                <div>
                    <p><a @click.prevent="addTheme()">{{ t('Add an theme') }}</a></p>
                    <form v-if="is_adding" class="ui form">
                        <fieldset>
                            <legend>{{ t('Add an theme') }}</legend>
                            <p class="field">
                                <label for="name">{{ t('Name:') }} </label>
                                <input type="text" name="name" v-model="name">
                            </p>
                            <p class="field">
                                <button class="ui primary button" @click.prevent="saveTheme(false)">{{ t('Save') }}</button>
                                <button class="ui button" @click.prevent="hideThemeForm()">{{ t('Cancel') }}</button>
                            </p>
                        </fieldset>
                    </form>
                </div>
            </div>
            <div v-else>
                Updating...
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'
    import {root_url} from '@/common/index.js'

    export default {
        name: "themeslist",
        data() {
            return {
                themes: Array,
                theme_id: -1,
                is_adding: false,
                is_updating: false,
                is_editing: false,
                name: "",
            }
        },
        components: {
        },
        created() {
            axios.get(root_url + "themes/list/")
                .then(response => {
                    this.$data.themes = response.data;
                },  (error) => { console.log(error) });
        },
        methods:{
            // TODO: Use VueX to prevent passing this signal all the way up
            launch_show_theme(item_id) {
                this.$emit("show_theme", item_id)
            },
            launch_edit_theme(item_id) {
                this.$emit("edit_theme", item_id)
            },
            addTheme() {
                this.$data.is_adding = !this.$data.is_adding
                this.$data.name = ""
            },
            hideThemeForm() {
                axios.get(root_url + "themes/list/")
                    .then(response => {
                        this.$data.themes = response.data;
                    },  (error) => { console.log(error) });
                this.$data.is_adding = false
                this.$data.is_editing = false
            },
            synchronize(){
                this.$data.is_updating = true
                axios.get(root_url + "themes/list/")
                    .then(response => {
                        this.$data.themes = response.data;
                        this.$data.is_updating = false
                    },  (error) => { console.log(error) });
            },
            saveTheme(is_editing) {
                let theme = {
                    name: this.$data.name,
                };
                this.$data.is_updating = true
                if( is_editing ) {
                    axios.put(root_url + "themes/" + this.$data.theme_id + "/", theme)
                        .then(response => {
                            axios.get(root_url + "themes/list/")
                                .then(response => {
                                    this.$data.themes = response.data;
                                    this.$data.is_updating = false
                                },  (error) => { console.log(error) });
                        }, (error) => { console.log(error)});
                } else {
                    axios.post(root_url + "themes/list/", theme)
                        .then(response => {
                            axios.get(root_url + "themes/list/")
                                .then(response => {
                                    this.$data.themes = response.data;
                                    this.$data.is_updating = false
                                },  (error) => { console.log(error) });
                        }, (error) => { console.log(error)});
                }
                this.$data.is_adding = false
                this.$data.is_editing = false
                this.$data.theme_id = -1
            },
            editTheme(theme){
                this.$data.name = theme.name
                this.$data.theme_id = theme.id
                this.$data.is_editing = true
            }
        }
    }
</script>