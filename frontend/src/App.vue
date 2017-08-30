<template>
    <div id="app">
        <div class="ui fixed inverted menu">
            <div class="ui container">
                <a href="http://localhost:8080/" class="header item">
                    <img class="logo" src="./assets/logo.png">
                    Turbo songwriter!
                </a>
                <a href="http://localhost:8080/" class="item">Home</a>
            </div>
        </div>
        <div class="ui main text container">
            <song :item_id="current_song" v-show="is_song_shown" @convert_to_tex="convert_to_tex">
                <a @click.prevent="show_list">Retour à la liste</a>
            </song>
            <songslist @show_song="show_song" @edit_song="edit_song" v-if="is_list_shown"></songslist>
            <songform v-if="is_form_edition_shown" @song_saved="show_list()" titleform="Edit a song" :song="current_song">
                <a @click.prevent="show_list">Retour à la liste</a>
            </songform>
            <songtexform :song="current_song" v-if="is_tex_shown"></songtexform>
        </div>
    </div>
</template>

<script>
    import Songslist from './Songslist.vue'
    import Songform from './Songform.vue'
    import Songtexform from './Songtexform.vue'
    import Song from './Song.vue'

    export default {
        name: 'app',
        components: {
            Songslist,
            Songtexform,
            Songform,
            Song
        },
        data() {
            return {
                msg: 'Welcome to Your Vue.js App',
                current_song: 0,
                is_song_shown: false,
                is_list_shown: true,
                is_tex_shown: false,
                is_form_edition_shown: false
            }
        },
        methods: {
            show_song(song_id){
                this.$data.current_song = song_id
                this.$data.is_song_shown = true
                this.$data.is_list_shown = false
                this.$data.is_tex_shown = false
                this.$data.is_form_edition_shown = false
            },
            edit_song(song_id){
                this.$data.current_song = song_id
                this.$data.is_form_edition_shown = true
                this.$data.is_song_shown = false
                this.$data.is_list_shown = false
                this.$data.is_tex_shown = false
            },
            show_list(){
                this.$data.is_list_shown = true
                this.$data.is_tex_shown = false
                this.$data.is_song_shown = false
                this.$data.is_form_edition_shown = false
                this.$data.current_song = 0
            },
            convert_to_tex(song_id){
                this.$data.current_song = song_id
                this.$data.is_tex_shown = true
                this.$data.is_song_shown = false
                this.$data.is_list_shown = false
                this.$data.is_form_edition_shown = false
            }
        },
    }
</script>

<style>
    /*#app {*/
        /*font-family: 'Avenir', Helvetica, Arial, sans-serif;*/
        /*-webkit-font-smoothing: antialiased;*/
        /*-moz-osx-font-smoothing: grayscale;*/
        /*text-align: center;*/
        /*color: #2c3e50;*/
        /*margin-top: 60px;*/
    /*}*/

    /*h1, h2 {*/
        /*font-weight: normal;*/
    /*}*/

    /*ul {*/
        /*list-style-type: none;*/
        /*padding: 0;*/
    /*}*/

    /*li {*/
        /*margin: 0 10px;*/
    /*}*/

    /*a {*/
        /*color: #42b983;*/
    /*}*/
</style>
