<template>
    <div>
        <div id="listeditors">
            <div v-if="!is_updating">
                <template v-if="is_editing">
                    <form class="ui form">
                        <fieldset>
                            <legend>{{ t('Edit an editor') }}</legend>
                            <p class="field">
                                <label for="name">{{ t('Name:') }} </label>
                                <input type="text" name="name" v-model="name" v-focus>
                            </p>
                            <p class="field">
                                <button class="ui button primary" @click.prevent="saveEditor(true)">{{ t('Save') }}</button>
                                <button class="ui button" @click.prevent="hideEditorForm()">{{ t('Cancel') }}</button>
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
        		    <h2>{{ t('List of editors') }}</h2>
        		    <button @click="synchronize()" class="ui button primary">{{ t('Update the list') }}</button>
                    <div class="ui list large">
                        <div v-for="item in editors" class="item" @click="editEditor(item)">
                            <i class="icon book"></i>
                            {{ item.name }}
                        </div>
                    </div>
                </template>
                <div>
                    <p><a class="ui button green" @click.prevent="addEditor()">{{ t('Add an editor') }}</a></p>
                    <form v-if="is_adding" class="ui form">
                        <fieldset>
                            <legend>{{ t('Add an editor') }}</legend>
                            <p class="field">
                                <label for="name">{{ t('Name:') }} </label>
                                <input type="text" name="name" v-model="name" v-focus>
                            </p>
                            <p class="field">
                                <button class="ui button primary" @click.prevent="saveEditor(false)">{{ t('Save') }}</button>
                                <button class="ui button" @click.prevent="hideEditorForm()">{{ t('Cancel') }}</button>
                            </p>
                        </fieldset>
                    </form>
                </div>
            </div>
            <div v-else>
                {{ t('Updating...') }}
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'
    import {root_url} from '@/common/index.js'

    export default {
        name: "editorslist",
        data() {
            return {
                editors: Array,
                songs: Array,
                editor_id: -1,
                is_adding: false,
                is_updating: false,
                is_editing: false,
                name: "",
            }
        },
        components: {
        },
        created() {
            axios.get(root_url + "editors/list/")
                .then(response => {
                    this.$data.editors = response.data;
                },  (error) => { console.log(error) });
        },
        methods:{
            addEditor() {
                this.$data.is_adding = !this.$data.is_adding
                this.$data.is_editing = false
                this.$data.name = ""
            },
            hideEditorForm() {
                axios.get(root_url + "editors/list/")
                    .then(response => {
                        this.$data.editors = response.data;
                    },  (error) => { console.log(error) });
                this.$data.is_adding = false
                this.$data.is_editing = false
            },
            synchronize(){
                this.$data.is_updating = true
                axios.get(root_url + "editors/list/")
                    .then(response => {
                        this.$data.editors = response.data;
                        this.$data.is_updating = false
                    },  (error) => { console.log(error) });
            },
            saveEditor(is_editing) {
                let editor = {
                    name: this.$data.name,
                };
                this.$data.is_updating = true
                if( is_editing ) {
                    axios.put(root_url + "editors/" + this.$data.editor_id + "/", editor)
                        .then(response => {
                            axios.get(root_url + "editors/list/")
                                .then(response => {
                                    this.$data.editors = response.data;
                                    this.$data.is_updating = false
                                },  (error) => { console.log(error) });
                        }, (error) => { console.log(error)});
                } else {
                    axios.post(root_url + "editors/list/", editor)
                        .then(response => {
                            axios.get(root_url + "editors/list/")
                                .then(response => {
                                    this.$data.editors = response.data;
                                    this.$data.is_updating = false
                                },  (error) => { console.log(error) });
                        }, (error) => { console.log(error)});
                }
                this.$data.is_adding = false
                this.$data.is_editing = false
                this.$data.editor_id = -1
            },
            editEditor(editor){
                axios.get(root_url + "editor/list/songs/" + editor.id +"/")
                    .then(response => {
                        this.$data.songs = response.data;
                    },  (error) => { console.log(error) });
                this.$data.name = editor.name
                this.$data.editor_id = editor.id
                this.$data.is_editing = true
                this.$data.is_adding = false
            }
        }
    }
</script>