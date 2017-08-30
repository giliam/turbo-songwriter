<template>
    <div>
        <div id="listsongs">
            <h2>List of songs</h2>
            <ul>
                <li v-for="item in results">
                    <songtitle :item="item" @show_song="launch_show_song" @edit_song="launch_edit_song"></songtitle>
                </li>
            </ul>
        </div>
        <div>
            <p><a @click.prevent="addSong()">Add a song</a></p>
            <songform v-if="is_adding" @song_saved="hideSongForm()" titleform="Add a song"></songform>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'

    import Songtitle from './Songtitle.vue'
    import Songform from './Songform.vue'

    export default {
        name: "songslist",
        data() {
            return {
                results: Array,
                is_adding: false,
            }
        },
        components: {
            Songtitle,
            Songform
        },
        created() {
            axios.get("http://localhost:8000/songs/list.json")
                .then(response => {
                    this.results = response.data;
                }, 	(error) => { console.log(error) });
        },
        methods:{
            // TODO: Use VueX to prevent passing this signal all the way up
            launch_show_song(item_id) {
                this.$emit("show_song", item_id)
            },
            launch_edit_song(item_id) {
                this.$emit("edit_song", item_id)
            },
            addSong() {
                this.$data.is_adding = !this.$data.is_adding
            },
            hideSongForm() {
                axios.get("http://localhost:8000/songs/list.json")
                    .then(response => {
                        this.results = response.data;
                    }, 	(error) => { console.log(error) });
                this.$data.is_adding = false
            }
        }
    }
</script>