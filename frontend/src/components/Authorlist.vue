<template>
    <div>
        <div id="listauthors">
            <h2>List of authors</h2>
            <p @click="synchronize()">Update the list</p>
            <div v-if="!is_updating">
                <form v-if="is_editing" class="ui form">
                    <fieldset>
                        <legend>Edit an author</legend>
                        <p class="field">
                            <label for="firstname">Firstname: </label>
                            <input type="text" name="firstname" v-model="firstname">
                        </p>
                        <p class="field">
                            <label for="lastname">Lastname: </label>
                            <input type="text" name="lastname" v-model="lastname">
                        </p>
                        <p class="field">
                            <button class="ui button primary" @click.prevent="saveAuthor(true)">Save</button>
                            <button class="ui button" @click.prevent="hideAuthorForm()">Cancel</button>
                        </p>
                    </fieldset>
                </form>
                <ul v-if="!is_editing">
                    <li v-for="item in authors">
                        <p @click="editAuthor(item)">{{ item.firstname }} {{ item.lastname }}</p>
                    </li>
                </ul>
                <div>
                    <p><a @click.prevent="addAuthor()">Add an author</a></p>
                    <form v-if="is_adding" class="ui form">
                        <fieldset>
                            <legend>Add an author</legend>
                            <p class="field">
                                <label for="firstname">Firstname: </label>
                                <input type="text" name="firstname" v-model="firstname">
                            </p>
                            <p class="field">
                                <label for="lastname">Lastname: </label>
                                <input type="text" name="lastname" v-model="lastname">
                            </p>
                            <p class="field">
                                <button class="ui button primary" @click.prevent="saveAuthor(false)">Save</button>
                                <button class="ui button" @click.prevent="hideAuthorForm()">Cancel</button>
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
        name: "authorslist",
        data() {
            return {
                authors: Array,
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
            // TODO: Use VueX to prevent passing this signal all the way up
            launch_show_author(item_id) {
                this.$emit("show_author", item_id)
            },
            launch_edit_author(item_id) {
                this.$emit("edit_author", item_id)
            },
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
                this.$data.firstname = author.firstname
                this.$data.lastname = author.lastname
                this.$data.author_id = author.id
                this.$data.is_editing = true
            }
        }
    }
</script>