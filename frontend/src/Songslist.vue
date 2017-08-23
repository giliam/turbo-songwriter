<template>
    <div id="listsongs">
        <h2>List of songs</h2>
        <ul>
            <li v-for="item in results"><songtitle @show_song="show_song" :item="item"></songtitle></li>
        </ul>
    </div>
</template>

<script>
    import axios from 'axios'

    import Songtitle from './Songtitle.vue'

    export default {
        name: "songslist",
        data() {
            return { results: Array }
        },
        components: {
            Songtitle
        },
        methods: {
            show_song(){
                console.log("Show song")
            }
        },
        created() {
            console.log("Launches request");
            axios.get("http://localhost:8000/songs/list.json")
                .then(response => {
                    console.log(response.data);
                    this.results = response.data;
                });
            console.log("done Request");
        }
    }
</script>