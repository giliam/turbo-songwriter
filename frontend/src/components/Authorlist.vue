<template>
    <div>
        <div id="listauthors">
            <div v-if="!is_updating">
                <template v-if="is_editing">
                    <form class="ui form">
                        <fieldset>
                            <legend>{{ t('Edit an author') }}</legend>
                            <p class="field">
                                <label for="firstname">{{ t('Firstname:') }}</label>
                                <input type="text" name="firstname" v-model="firstname">
                            </p>
                            <p class="field">
                                <label for="lastname">{{ t('Lastname:') }}</label>
                                <input type="text" name="lastname" v-model="lastname">
                            </p>
                            <p class="field">
                                <button class="ui button primary" @click.prevent="saveAuthor(true)">{{ t('Save') }}</button>
                                <button class="ui button" @click.prevent="hideAuthorForm()">{{ t('Cancel') }}</button>
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
                    <h2>{{ t('List of authors') }}</h2>
                    <p @click="synchronize()">{{ t('Update the list') }}</p>
                    <ul>
                        <li v-for="item in authors">
                            <p @click="editAuthor(item)">{{ item.firstname }} {{ item.lastname }}</p>
                        </li>
                    </ul>
                </template>
                <div>
                    <p><a @click.prevent="addAuthor()">{{ t('Add an author') }}</a></p>
                    <form v-if="is_adding" class="ui form">
                        <fieldset>
                            <legend>{{ t('Add an author') }}</legend>
                            <p class="field">
                                <label for="firstname">{{ t('Firstname:') }}</label>
                                <input type="text" name="firstname" v-model="firstname">
                            </p>
                            <p class="field">
                                <label for="lastname">{{ t('Lastname:') }}</label>
                                <input type="text" name="lastname" v-model="lastname">
                            </p>
                            <p class="field">
                                <button class="ui button primary" @click.prevent="saveAuthor(false)">{{ t('Save') }}</button>
                                <button class="ui button" @click.prevent="hideAuthorForm()">{{ t('Cancel') }}</button>
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
        name: "authorslist",
        data() {
            return {
                authors: Array,
                songs: Array,
                author_id: -1,
                is_adding: false,
                is_updating: false,
                is_editing: false,
                firstname: "",
                lastname: ""
            }
        },
        components: {
        },
        created() {
            axios.get(root_url + "authors/list/")
                .then(response => {
                    this.$data.authors = response.data;
                },  (error) => { console.log(error) });
        },
        methods:{
            addAuthor() {
                this.$data.is_adding = !this.$data.is_adding
                this.$data.firstname = ""
                this.$data.lastname = ""
            },
            hideAuthorForm() {
                axios.get(root_url + "authors/list/")
                    .then(response => {
                        this.$data.authors = response.data;
                    },  (error) => { console.log(error) });
                this.$data.is_adding = false
                this.$data.is_editing = false
            },
            synchronize(){
                this.$data.is_updating = true
                axios.get(root_url + "authors/list/")
                    .then(response => {
                        this.$data.authors = response.data;
                        this.$data.is_updating = false
                    },  (error) => { console.log(error) });
            },
            saveAuthor(is_editing) {
                let author = {
                    firstname: this.$data.firstname,
                    lastname: this.$data.lastname
                };
                this.$data.is_updating = true
                if( is_editing ) {
                    axios.put(root_url + "authors/" + this.$data.author_id + "/", author)
                        .then(response => {
                            axios.get(root_url + "authors/list/")
                                .then(response => {
                                    this.$data.authors = response.data;
                                    this.$data.is_updating = false
                                },  (error) => { console.log(error) });
                        }, (error) => { console.log(error)});
                } else {
                    axios.post(root_url + "authors/list/", author)
                        .then(response => {
                            axios.get(root_url + "authors/list/")
                                .then(response => {
                                    this.$data.authors = response.data;
                                    this.$data.is_updating = false
                                },  (error) => { console.log(error) });
                        }, (error) => { console.log(error)});
                }
                this.$data.is_adding = false
                this.$data.is_editing = false
                this.$data.author_id = -1
            },
            editAuthor(author){
                axios.get(root_url + "author/list/songs/" + author.id +"/")
                    .then(response => {
                        this.$data.songs = response.data;
                    },  (error) => { console.log(error) });
                this.$data.firstname = author.firstname
                this.$data.lastname = author.lastname
                this.$data.author_id = author.id
                this.$data.is_editing = true
            }
        }
    }
</script>