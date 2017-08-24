<template>
    <div id="app">
        <h1>Turbo songwriter !</h1>
        <song :item_id="current_song" v-show="!is_list_shown">
            <a @click.prevent="show_list">Retour à la liste</a>
        </song>
        <songslist @show_song="show_song" v-if="is_list_shown"></songslist>
    </div>
</template>

<script>
    import Songslist from './Songslist.vue'
    import Song from './Song.vue'

    export default {
        name: 'app',
        components: {
            Songslist,
            Song
        },
        data() {
            return {
                msg: 'Welcome to Your Vue.js App',
                current_song: 0,
                is_list_shown: true,
            }
        },
        methods: {
            show_song(param){
                this.$data.current_song = param
                console.log("Show main song", param)
                this.$data.is_list_shown = false
            },
            show_list(){
                this.$data.is_list_shown = true
                this.$data.current_song = 0
            }
        },
    }
</script>

<style>
    #app {
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
        margin-top: 60px;
    }

    h1, h2 {
        font-weight: normal;
    }

    ul {
        list-style-type: none;
        padding: 0;
    }

    li {
        display: inline-block;
        margin: 0 10px;
    }

    a {
        color: #42b983;
    }
</style>
