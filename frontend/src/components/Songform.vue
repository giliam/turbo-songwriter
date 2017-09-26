<template>
    <form id="songform" class="ui form">
        <fieldset v-if="loaded">
            <legend class="ui dividing header">{{ printTitle() }}</legend>
            <p class="field">
                <label for="title">{{ t('Title') }}:</label>
                <input type="text" name="title" v-model="title" v-focus>
            </p>
            <p class="field">
                <label for="author">{{ t('Author') }}:</label>
                <select name="author" v-model="author">
                    <option :value="sauthor.id" v-for="sauthor in authors">{{ sauthor.firstname }} {{ sauthor.lastname }}
                    </option>
                </select>
            </p>
            <p class="field">
                <label for="editor">{{ t('Editor') }}:</label>
                <select name="editor" v-model="editor">
                    <option :value="seditor.id" v-for="seditor in editors">
                        {{ seditor.name }}
                    </option>
                </select>
            </p>
            <p class="field">
                <label for="theme">{{ t('Theme') }}:</label>
                <select name="theme" v-model="theme" multiple="multiple" @click="print()">
                    <option :value="stheme.id" v-for="stheme in themes">
                        {{ stheme.name }}
                    </option>
                </select>
            </p>
            <p class="field">
                <label for="secli_number">{{ t('SECLI Number ') }}:</label>
                <input type="text" name="secli_number" v-model="secli_number">
            </p>
            <p class="field">
                <label for="old_page_number">{{ t('V1 page number ') }}:</label>
                <input type="text" name="old_page_number" v-model="old_page_number">
            </p>
            <p class="field">
                <label for="page_number">{{ t('V2 page number ') }}:</label>
                <input type="text" name="page_number" v-model="page_number">
            </p>
            <p class="field">
                <label for="comments">{{ t('Comments') }}:</label>
                <textarea name="comments" v-model="comments"></textarea>
            </p>

            <p class="field"><button @click.prevent="save()" class="ui primary button">{{ t('Save') }}</button><button @click.prevent="cancel()" class="ui button">{{ t('Cancel') }}</button></p>
        </fieldset>
        <p v-else>
           {{ t('Loading...') }}  
        </p>
    </form>
</template>

<script>
    import axios from 'axios'
    import {root_url} from '@/common/index.js'

    export default {
        data() {
            return {
                loaded: false,
                title: "",
                author: 0,
                editor: 0,
                page_number: 0,
                old_page_number: 0,
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
        created() {
            axios.get(root_url + "authors/list/")
                .then(response => {
                    this.$data.authors = response.data;
                }, 	(error) => { console.log(error) });
            axios.get(root_url + "editors/list/")
                .then(response => {
                    this.$data.editors = response.data;
                }, 	(error) => { console.log(error) });
            axios.get(root_url + "themes/list/")
                .then(response => {
                    this.$data.themes = response.data;
                }, 	(error) => { console.log(error) });

            if( this.$route.params.item_id && this.$route.params.item_id != 0 ){
                axios.get(root_url + "songs/" + this.$route.params.item_id + ".json")
                    .then(response => {
                        console.log("Received", response.data)
                        this.$data.title = response.data.title
                        if( response.data.author )
                            this.$data.author = response.data.author.id
                        this.$data.theme = new Array()
                        for (var i = 0; i < response.data.theme.length; i++) {
                            this.$data.theme.push(response.data.theme[i].id)
                        }
                        if( response.data.editor )
                            this.$data.editor = response.data.editor.id
                        this.$data.secli_number = response.data.secli_number
                        this.$data.page_number = response.data.page_number
                        this.$data.old_page_number = response.data.old_page_number
                        this.$data.comments = response.data.comments
                        this.$data.loaded = true
                    })
            }
            else{
                this.$data.loaded = true
            }
        },
        methods: {
            printTitle(){
                if( !this.titleform ){
                    return this.t("Add a song")
                }
                return this.titleform
            },
            print(){
                console.log(this.$data.theme)
            },
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
                    page_number: this.$data.page_number,
                    old_page_number: this.$data.old_page_number,
                    comments: this.$data.comments,
                    theme: new_themes
                };

                let song_id = 0

                if( this.$route.params.item_id && this.$route.params.item_id != 0 ) {
                    axios.put(root_url + "songs/" + this.$route.params.item_id + "/", song)
                        .then(response => {
                            song_id = this.$route.params.item_id
                            console.log(song_id)
                            this.$router.push({name:'song_detail', params:{item_id:song_id}})
                        }, (error) => { console.log(error)});
                } else {
                    axios.post(root_url + "songs/list/", song)
                        .then(response => {
                            song_id = response.data.id
                            this.$router.push({name:'song_detail', params:{item_id:song_id}})
                        }, (error) => { console.log(error)});
                }

            },
            cancel() {
                this.$router.go(-1)
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