<template>
    <div>
        <div id="listthemes">
            <div v-if="!is_updating">
                <template v-if="is_editing">
                    <form class="ui form">
                        <fieldset>
                            <legend>{{ t('Edit an theme') }}</legend>
                            <p class="field">
                                <label for="name">{{ t('Name:') }} </label>
                                <input type="text" name="name" v-model="name" v-focus>
                            </p>
                            <p class="field">
                                <button class="ui primary button" @click.prevent="saveTheme(true)">{{ t('Save') }}</button>
                                <button class="ui button" @click.prevent="hideThemeForm()">{{ t('Cancel') }}</button>
                            </p>
                        </fieldset>
                    </form>
                    <h3>{{ t('List of linked songs') }}</h3>
                    <ul>
                        <li v-for="item in songs">
                            <router-link :to="{name:'song_detail', params:{item_id:item.id}}">{{ item.title }}</router-link> - <router-link :to="{name:'song_edit', params:{item_id:item.id}}">{{ t('Edit') }}</router-link>
                        </li>
                    </ul>
                </template>
                <template v-else>
                    <h2>{{ t('List of themes') }}</h2>
                    <p><a class="ui button green" @click.prevent="addTheme()">{{ t('Add an theme') }}</a></p>
                    <button @click="synchronize()" class="ui button primary">{{ t('Update the list') }}</button>
                    <div class="ui list large">
                        <div v-for="item in themes" class="item" @click="editTheme(item)">
                            <i class="icon theme"></i>
                            {{ item.name }}
                        </div>
                    </div>
                </template>
                <div>
                    <p><a class="ui button green" @click.prevent="addTheme()">{{ t('Add an theme') }}</a></p>
                    <form v-if="is_adding" class="ui form">
                        <fieldset>
                            <legend>{{ t('Add an theme') }}</legend>
                            <p class="field">
                                <label for="name">{{ t('Name:') }} </label>
                                <input type="text" name="name" v-model="name" v-focus>
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
                songs: Array,
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
            addTheme() {
                this.$data.is_adding = !this.$data.is_adding
                this.$data.is_editing = false
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
                axios.get(root_url + "theme/list/songs/" + theme.id +"/")
                    .then(response => {
                        this.$data.songs = response.data;
                    },  (error) => { console.log(error) });
                this.$data.name = theme.name
                this.$data.theme_id = theme.id
                this.$data.is_editing = true
                this.$data.is_adding = false
            }
        }
    }
</script>