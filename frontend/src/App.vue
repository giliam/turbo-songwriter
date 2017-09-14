<template>
    <div id="app">
        <div class="ui fixed inverted menu">
            <div class="ui container">
                <router-link :to="{name:'root'}" class="header item">
                    <img class="logo" src="./assets/logo.png">
                    Turbo songwriter!
                </router-link>
                <router-link :to="{name:'root'}" class="item">Songs</router-link>
                <router-link :to="{name:'authors_list'}" class="item">Authors</router-link>
                <router-link :to="{name:'editors_list'}" class="item">Editors</router-link>
                <router-link :to="{name:'themes_list'}" class="item">Themes</router-link>
                <router-link :to="{name:'chords_list'}" class="item">Chords</router-link>
                <a class="item" :href="print_root_url() + 'admin'">Admin</a>>
            </div>
        </div>
        <div class="ui main text container">
            <div id="song_container">
                <songform v-if="is_form_edition_shown" @song_saved="show_list()" titleform="Edit a song" :song="current_song">
                    <a @click.prevent="show_list">Retour à la liste</a>
                </songform>
                <songtexform :song="current_song" :force_conversion="force_latex_conversion" v-if="is_tex_shown" @song_saved="show_list()" ></songtexform>
            </div>
            <router-view></router-view>
        </div>
    </div>
</template>

<script>
    import Songslist from '@/components/Songslist.vue'
    import Songform from '@/components/Songform.vue'
    import Songtexform from '@/components/Songtexform.vue'
    import Song from '@/components/Song.vue'
    import Authorlist from '@/components/Authorlist.vue'
    import Editorlist from '@/components/Editorlist.vue'
    import Themelist from '@/components/Themelist.vue'
    import Chordlist from '@/components/Chordlist.vue'
    import {root_url} from '@/common/index.js'

    export default {
        name: 'app',
        components: {
            Songslist,
            Songtexform,
            Songform,
            Song,
            Editorlist,
            Authorlist,
            Chordlist,
            Themelist,
        },
        data() {
            return {
                msg: 'Welcome to Your Vue.js App',
                current_song: 0,
                force_latex_conversion: false,
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
            convert_to_tex(song_id, force_latex_conversion){
                this.$data.current_song = song_id
                this.$data.force_latex_conversion = force_latex_conversion
                this.$data.is_tex_shown = true
                this.$data.is_song_shown = false
                this.$data.is_list_shown = false
                this.$data.is_form_edition_shown = false
            },
            print_root_url(){
                return root_url
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
