<template>
    <form id="songform" class="ui form">
        <fieldset>
            <legend class="ui dividing header">Add a song</legend>
            <p class="field">
                <label for="title">Title:</label>
                <input type="text" name="title" v-model="title">
            </p>
            <p class="field">
                <label for="author">Author:</label>
                <select name="author" v-model="author">
                    <option :value="sauthor.id" v-for="sauthor in authors">{{ sauthor.firstname }} {{ sauthor.lastname }}</option>
                </select>
            </p>
            <p class="field">
                <label for="editor">Editor:</label>
                <select name="editor" v-model="editor">
                    <option :value="seditor.id" v-for="seditor in editors">{{ seditor.name }}</option>
                </select>
            </p>
            <p class="field">
                <label for="theme">Theme:</label>
                <select name="theme" v-model="theme" multiple="multiple">
                    <option :value="stheme.id" v-for="stheme in themes">{{ stheme.name }}</option>
                </select>
            </p>
            <p class="field">
                <label for="secli_number">SECLI Number :</label>
                <input type="text" name="secli_number" v-model="secli_number">
            </p>
            <p class="field">
            <label for="comments">Comments:</label>
            <textarea name="comments" v-model="comments"></textarea>
            </p>

            <p class="field"><button @click.prevent="save()" class="ui button">Save</button></p>
        </fieldset>
    </form>
</template>

<script>
    import axios from 'axios'

    export default {
        data() {
            return {
                title: "",
                author: 0,
                editor: 0,
                secli_number: "",
                comments: "",
                theme: Array(),
                authors: Array(),
                editors: Array(),
                themes: Array()
            }
        },
        mounted() {
            axios.get("http://localhost:8000/authors/list/")
                .then(response => {
                    this.$data.authors = response.data;
                }, 	(error) => { console.log(error) });
            axios.get("http://localhost:8000/editors/list/")
                .then(response => {
                    this.$data.editors = response.data;
                }, 	(error) => { console.log(error) });
            axios.get("http://localhost:8000/themes/list/")
                .then(response => {
                    this.$data.themes = response.data;
                }, 	(error) => { console.log(error) });
        },
        methods: {
            save(){
                let new_themes = [];
                for(let theme in this.$data.theme){
                    new_themes.push(this.$data.theme[theme])
                }
                let song = {
                    title: this.$data.title,
                    author: this.$data.author,
                    editor: this.$data.editor,
                    secli_number: this.$data.secli_number,
                    comments: this.$data.comments,
                    theme: new_themes
                };
                axios.post("http://localhost:8000/songs/list/", song)
                    .then(response => {
                        this.$emit("song_saved")
                    }, (error) => { console.log(error)});
            }
        }
    }
</script>