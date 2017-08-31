<template>
    <form id="songform" class="ui form">
        <fieldset>
            <slot></slot>
            <legend class="ui dividing header">{{ titleform }}</legend>
            <p class="field">
                <label for="title">Title:</label>
                <input type="text" name="title" v-model="title">
            </p>
            <p class="field">
                <label for="author">Author:</label>
                <select name="author" v-model="author">
                    <option :value="sauthor.id" v-for="sauthor in authors" :selected="is_selected(author_selected.id, sauthor.id)">{{ sauthor.firstname }} {{ sauthor.lastname }}
                    </option>
                </select>
            </p>
            <p class="field">
                <label for="editor">Editor:</label>
                <select name="editor" v-model="editor">
                    <option :value="seditor.id" v-for="seditor in editors" :selected="is_selected(editor_selected.id, seditor.id)">
                        {{ seditor.name }}
                    </option>
                </select>
            </p>
            <p class="field">
                <label for="theme">Theme:</label>
                <select name="theme" v-model="theme" multiple="multiple">
                    <option :value="stheme.id" v-for="stheme in themes" :selected="is_selected_theme(stheme.id)">
                        {{ stheme.name }}
                    </option>
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

            <p class="field"><button @click.prevent="save()" class="ui button">Save</button><button @click.prevent="cancel()" class="ui button">Cancel</button></p>
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
                themes: Array(),
                theme_selected: Array(),
                author_selected: Object,
                editor_selected: Object
            }
        },
        props: {
            titleform: String,
            song: Number
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

            if( this.song != 0 ){
                axios.get("http://localhost:8000/songs/" + this.song + ".json")
                    .then(response => {
                        console.log("Received", response.data)
                        this.$data.title = response.data.title
                        this.$data.author_selected = response.data.author
                        this.$data.theme_selected = response.data.theme
                        this.$data.editor_selected = response.data.editor
                        this.$data.secli_number = response.data.secli_number
                        this.$data.comments = response.data.comments
                    })
            }
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
                if( this.song != 0 ) {
                    axios.put("http://localhost:8000/songs/" + this.song + "/", song)
                        .then(response => {
                            this.$emit("song_saved")
                        }, (error) => { console.log(error)});
                } else {
                    axios.post("http://localhost:8000/songs/list/", song)
                        .then(response => {
                            this.$emit("song_saved")
                        }, (error) => { console.log(error)});
                }
            },
            cancel() {
                this.$emit("song_saved")
            },
            is_selected(ref_id, current_id){
                return (ref_id == current_id ? "selected" : null)
            },
            is_selected_theme(current_id){
                for (var i = 0; i < this.$data.theme_selected.length; i++) {
                    if(current_id == this.$data.theme_selected[i])
                        return "selected"
                }
                return null
            }
        }
    }
</script>