<template>
    <div>
        <div id="listeditors">
            <h2>{{ t('List of editors') }}</h2>
            <p @click="synchronize()">{{ t('Update the list') }}</p>
            <div v-if="!is_updating">
                <form v-if="is_editing" class="ui form">
                    <fieldset>
                        <legend>{{ t('Edit an editor') }}</legend>
                        <p class="field">
                            <label for="name">{{ t('Name:') }} </label>
                            <input type="text" name="name" v-model="name">
                        </p>
                        <p class="field">
                            <button class="ui button primary" @click.prevent="saveEditor(true)">{{ t('Save') }}</button>
                            <button class="ui button" @click.prevent="hideEditorForm()">{{ t('Cancel') }}</button>
                        </p>
                    </fieldset>
                </form>
                <ul v-if="!is_editing">
                    <li v-for="item in editors">
                        <p @click="editEditor(item)">{{ item.name }}</p>
                    </li>
                </ul>
                <div>
                    <p><a @click.prevent="addEditor()">{{ t('Add an editor') }}</a></p>
                    <form v-if="is_adding" class="ui form">
                        <fieldset>
                            <legend>{{ t('Add an editor') }}</legend>
                            <p class="field">
                                <label for="name">{{ t('Name:') }} </label>
                                <input type="text" name="name" v-model="name">
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
                Updating...
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
            // TODO: Use VueX to prevent passing this signal all the way up
            launch_show_editor(item_id) {
                this.$emit("show_editor", item_id)
            },
            launch_edit_editor(item_id) {
                this.$emit("edit_editor", item_id)
            },
            addEditor() {
                this.$data.is_adding = !this.$data.is_adding
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
                this.$data.name = editor.name
                this.$data.editor_id = editor.id
                this.$data.is_editing = true
            }
        }
    }
</script>