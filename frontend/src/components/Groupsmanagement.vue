<template>
    <div>
        <p><button @click.prevent="sync(true)" class="ui button">{{ t('Back to the list') }}</button></p>
        <p><button class="ui button green" @click="sync(false)">{{ t('Refresh') }}</button></p>
        <template v-if="action == 'create'">
            <form class="ui form">
                <fieldset>
                    <legend class="ui dividing header">{{ t('Create a group') }}</legend>
                    <ul>
                        <template v-for="(item, n) in selectedSongs">
                            <template v-if="item">
                                <li>{{songsData[n].title}}</li>
                            </template>
                        </template>
                    </ul>
                    <p class="field">
                        <label for="name">{{ t('Name') }}:</label>
                        <input type="text" name="name" v-model="name">
                    </p>
                    <p class="field">
                        <button @click.prevent="create()" class="ui primary button">{{ t('Save') }}</button>
                        <slot><button @click.prevent="sync(true)" class="ui button">{{ t('Cancel') }}</button></slot>
                    </p>
                </fieldset>
            </form>
        </template>
        <template v-else-if="action == 'edit'">
            <form class="ui form">
                <fieldset>
                    <legend class="ui dividing header">{{ t('Edit a group') }}</legend>
                    <ul>
                        <template v-if="editedGroup.songs">
                            <template v-for="(item, n) in editedGroup.songs">
                                <li>{{item.title}} ({{item.get_printable_author}}) - <a @click.prevent="deleteFromGroup(item.id, editedGroup.id)">{{ t('Delete from group') }}</a></li>
                            </template>
                        </template>
                    </ul>
                    <p class="field">
                        <label for="name">{{ t('Name') }}:</label>
                        <input type="text" name="name" v-model="editedGroup.name">
                    </p>
                    <p class="field">
                        <button @click.prevent="saveEditedGroup()" class="ui primary button">{{ t('Save') }}</button>
                        <slot><button @click.prevent="sync(true)" class="ui button">{{ t('Cancel') }}</button></slot>
                    </p>
                </fieldset>
            </form>
            <ul>
                <template v-for="song in dataSongs">
                    <template v-if="!loadingSongs">
                        <li>{{song.title}} - <a @click.prevent="addToGroup(song.id, editedGroup.id)">{{ t('Add to group') }}</a></li>
                    </template>
                </template>
            </ul>
        </template>
        <template v-else>
            <table class="ui celled table">
                <thead>
                    <tr><th class="three wide">{{ t('Names') }}</th>
                    <th class="three wide">{{ t('Caracteristics') }}</th>
                    <th class="seven wide">{{ t('Songs') }}</th>
                    <th class="three wide">{{ t('Actions') }}</th>
                    </tr>
                </thead>
                <tbody>
                    <template v-for="(group, n) in dataGroups">
                        <tr>
                            <td><label :for="'selectionner_' + group.id">
                                <strong>{{group.name}}</strong>
                            </label></td>
                            <td>
                                <p class="item">
                                    <label :for="'select_' + group.id">
                                        <template v-if="group.selected">
                                            {{ t('Unselect') }}
                                        </template>
                                        <template v-else>
                                            {{ t('Select') }}
                                        </template>
                                    </label>
                                    <input type="checkbox" @click="selectGroup(group)" :id="'select_' + group.id" v-model="group.selected" />
                                </p>
                                <template v-if="group.selected">
                                    <p>{{ t('Selected for book') }}</p>
                                </template>
                            </td>
                            <td>
                                <label :for="'check_' + n">{{ t('Show/Hide') }}</label>
                                <input type="checkbox" :id="'check_' + n" v-model="dataShownGroups[n]">
                                <template v-if="isShownGroup(n)">
                                    <ul>
                                    <template v-for="song in group.songs">
                                        <li>{{song.title}}</li>
                                    </template>
                                    </ul>
                                </template>
                            </td>
                            <td>
                                <p><button @click="editGroup(n, group.id)" class="ui button primary">{{ t('Edit') }}</button></p>
                                <p><button @click="deleteGroup(group.id)" class="ui button red">{{ t('Delete') }}</button></p>
                            </td>
                        </tr>
                    </template>
                </tbody>
            </table>
        </template>
    </div>
</template>

<script>
    import axios from 'axios'
    import {root_url} from '@/common/index.js'

    export default {
        name: "groupsmanagement",
        props:{
            selectedSongs: Array,
            songsData: Array,
            actionSent: String,
        },
        data(){
            return {
                action: "list",
                name: "",
                dataGroups: Array,
                dataShownGroups: Array,
                dataSongs: Array,
                editedGroup: null,
                editedGroupId: null,
                loadingSongs: false,
            }
        },
        created() {
            this.$data.action = this.actionSent
            axios.get(root_url + "groups/list/")
                .then(response => {
                    this.$data.dataGroups = response.data
                    this.$data.dataShownGroups = Array()
                    for (var i = 0; i < response.data.length; i++) {
                        this.$data.dataShownGroups[i] = false
                    }
                },  (error) => { console.log(error) });

            axios.get(root_url + "songs/list/")
                .then(response => {
                    this.$data.dataSongs = response.data
                },  (error) => { console.log(error) });
        },
        methods: {
            create(){
                let songsIds = new Array()
                for (var i = 0; i < this.selectedSongs.length; i++) {
                    if( this.selectedSongs[i] ){
                        songsIds.push(this.songsData[i].id)
                    }
                }
                let group = {
                    name: this.$data.name,
                    songs: songsIds,
                }

                axios.post(root_url + "groups/list/", group)
                    .then(response => {
                    },  (error) => { console.log(error) });
            },
            deleteGroup(groupId){
                axios.delete(root_url + "groups/" + groupId + "/")
                    .then(response => { 
                        this.sync(true)
                     },
                    (error) => { console.log("Error", error) });
            },
            editGroup(n, groupId){
                this.$data.editedGroup = this.$data.dataGroups[n]
                this.$data.editedGroupId = n
                this.action = "edit"
            },
            saveEditedGroup(){
                let group = {
                    name: this.$data.editedGroup.name,
                    songs: new Array(),
                }
                for (var i = 0; i < this.$data.editedGroup.songs.length; i++) {
                    group.songs.push(this.$data.editedGroup.songs[i].id)
                }
                axios.put(root_url + "groups/" + this.$data.editedGroup.id + "/", group)
                    .then(response => { 
                        this.sync(true)
                     },
                    (error) => { console.log("Error", error) });
            },
            deleteFromGroup(songId, groupId){
                let group = {
                    name: this.$data.editedGroup.name,
                    songs: new Array(),
                }
                for (var i = 0; i < this.$data.editedGroup.songs.length; i++) {
                    if( this.$data.editedGroup.songs[i].id != songId )
                        group.songs.push(this.$data.editedGroup.songs[i].id)
                }
                axios.put(root_url + "groups/" + this.$data.editedGroup.id + "/", group)
                    .then(response => { 
                        this.sync(true)
                     },
                    (error) => { console.log("Error", error) });
            },
            addToGroup(songId, groupId){
                let group = {
                    name: this.$data.editedGroup.name,
                    songs: new Array(),
                }
                for (var i = 0; i < this.$data.editedGroup.songs.length; i++) {
                    group.songs.push(this.$data.editedGroup.songs[i].id)
                }

                let posHor = window.scrollX
                let posVer = window.scrollY

                this.$data.loadingSongs = true

                group.songs.push(songId)

                axios.put(root_url + "groups/" + this.$data.editedGroup.id + "/", group)
                    .then(response => { 
                        this.$data.dataGroups.songs = response.data.songs
                        this.$data.loadingSongs = false
                        this.sync(false)
                        setTimeout(function(){ window.scrollTo(posHor, posVer) }, 500);
                    },
                    (error) => { console.log("Error", error) });
            },
            sync(cancel){
                axios.get(root_url + "groups/list/")
                    .then(response => {
                        this.$data.dataGroups = response.data
                        if(cancel)
                            this.cancelGroupManagement()
                        if(this.action == "edit"){
                            this.$data.editedGroup = this.$data.dataGroups[this.$data.editedGroupId]
                        }
                    },  (error) => { console.log(error) });
            },
            cancelGroupManagement() {
                this.$data.action = "list"
                this.$data.editedGroupId = null
            },
            selectGroup(group){
                let new_group = {
                    name: group.name,
                    selected: !group.selected,
                    order_value: group.order_value
                }

                new_group.songs = new Array()
                for (var i = 0; i < group.songs.length; i++) {
                    new_group.songs.push(group.songs[i].id)
                }

                axios.put(root_url + "groups/" + group.id + "/", new_group)
                    .then(response => { 
                        this.sync(true)
                     },
                    (error) => { console.log("Error", error) });
            },
            isShownGroup(group){
                return this.$data.dataShownGroups[group]
            }
        }
    }
</script>