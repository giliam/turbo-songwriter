<template>
    <div>
        <div id="listsongs">
            <h2>{{ t('List of songs') }}</h2>
            <div v-for="item in results">
                <songtitle :item="item"></songtitle>
            </div>
        </div>
        <div>
            <p><router-link :to="{name: 'song_new'}">{{ t('Add a song') }}</router-link></p>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'
    import {root_url} from '@/common/index.js'

    import Songtitle from '@/components/Songtitle.vue'

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
            axios.get(root_url + "songs/list.json")
                .then(response => {
                    this.results = response.data;
                }, 	(error) => { console.log(error) });
        },
    }
</script>