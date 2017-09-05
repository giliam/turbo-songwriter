<template>
    <div>
        <div id="listsongs">
            <h2>List of songs</h2>
            <ul>
                <li v-for="item in results">
                    <songtitle :item="item"></songtitle>
                </li>
            </ul>
        </div>
        <div>
            <p><router-link :to="{name: 'song_new'}">Add a song</router-link></p>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'

    import Songtitle from './Songtitle.vue'

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
    }
</script>