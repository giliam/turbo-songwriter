<template>
    <div>
        <div id="listsongs">
            <h2>List of songs</h2>
            <ul>
                <li v-for="item in results"><songtitle :item="item" @show_song="launch_show_song"></songtitle></li>
            </ul>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'

    import Songtitle from './Songtitle.vue'
    import Song from './Song.vue'

    export default {
        name: "songslist",
        data() {
            return {
                results: Array,
            }
        },
        components: {
            Songtitle,
        },
        created() {
            axios.get("http://localhost:8000/songs/list.json")
                .then(response => {
                    this.results = response.data;
                }, 	(error) => { console.log(error) });
        },
        methods:{
            launch_show_song: function(item_id) {
                this.$emit("show_song", item_id)
            }
        }
    }
</script>