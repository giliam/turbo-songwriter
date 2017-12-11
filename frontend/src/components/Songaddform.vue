<template>
    <form id="songform" class="ui form">
        <fieldset v-if="loaded">
            <legend class="ui dividing header">{{ t('Add a song with the lyrics') }}</legend>
            {{ t('To add a song with the lyrics, just put all the verses, one per line, in the text box below. Please separate each paragraph with an empty line. If one (or more) paragraph is a refrain, put two underscores (__) in front of each verse of the paragraph.') }}
            <p class="field">
                <label for="title">{{ t('Title') }}:</label>
                <input type="text" name="title" v-model="title" v-focus>
            </p>
            <p class="field">
                <label for="author">{{ t('Author') }}:</label>
                <select name="author" v-model="author">
                    <option :value="null">
                    </option>
                    <option :value="sauthor.id" v-for="sauthor in authors">{{ sauthor.lastname }} {{ sauthor.firstname }}
                    </option>
                </select>
            </p>
            <p class="field">
                <label for="editor">{{ t('Editor') }}:</label>
                <select name="editor" v-model="editor">
                    <option :value="null">
                    </option>
                    <option :value="seditor.id" v-for="seditor in editors">
                        {{ seditor.name }}
                    </option>
                </select>
            </p>
            <p class="field">
                <label for="theme">{{ t('Theme') }}:</label>
                <select name="theme" v-model="theme" multiple="multiple">
                    <option :value="stheme.id" v-for="stheme in themes">
                        {{ stheme.name }}
                    </option>
                </select>
            </p>
            <p class="field">
                <label for="verses">{{ t('Verses') }}:</label>
                <textarea name="verses" style="height:500px;" v-model="verses"></textarea>
            </p>
            <p class="field">
                <label for="is_refrain">{{ t('Is a refrain?') }}</label>
                <input type="checkbox" id="is_refrain" name="is_refrain" v-model="is_refrain" />
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
                author: null,
                editor: null,
                is_refrain: false,
                page_number: 0,
                old_page_number: 0,
                secli_number: "",
                comments: "",
                verses: "",
                theme: Array(),
                authors: Array(),
                editors: Array(),
                themes: Array(),
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

            this.$data.loaded = true
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
                    is_refrain: this.$data.is_refrain,
                    secli_number: this.$data.secli_number,
                    page_number: this.$data.page_number,
                    old_page_number: this.$data.old_page_number,
                    comments: this.$data.comments,
                    verses: this.$data.verses,
                    theme: new_themes
                };

                let song_id = 0

                axios.post(root_url + "song/new/with/verses/", song)
                    .then(response => {
                        song_id = response.data.id
                        this.$router.push({name:'song_detail', params:{item_id:song_id}})
                    }, (error) => { console.log(error)});
            },
            cancel() {
                this.$router.go(-1)
            }
        }
    }
</script>