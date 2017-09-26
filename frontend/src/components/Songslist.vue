<template>
    <div>
        <div id="listsongs">
            <h2>{{ t('List of songs') }}</h2>
            <div class="ui list aligned large">
                <template v-for="item in results">
                    <songtitle :item="item"></songtitle>
                </template>
            </div>
        </div>
        <p style="margin-top:30px;"><router-link tag="a" class="ui button green" :to="{name: 'song_new'}">{{ t('Add a song') }}</router-link></p>
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