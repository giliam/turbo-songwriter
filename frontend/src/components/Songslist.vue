<template>
    <div>
        <div id="listsongs">
            <h2>{{ t('List of songs') }}</h2>
            <template v-if="get_number_pages() > 1">
                <paginate
                  :pageCount="get_number_pages()"
                  :page-range="2"
                  :clickHandler="changeSongsPage"
                  :prevText="'Prev'"
                  :nextText="'Next'"
                  :containerClass="'ui pagination menu'"
                  :page-class="'item'"
                  :next-class="'item'"
                  :prev-class="'item'"
                  >
                </paginate>
            </template>
            <div class="ui list aligned large">
                <template v-for="item in results">
                    <songtitle :item="item"></songtitle>
                </template>
            </div>
            <template v-if="get_number_pages() > 1">
                <paginate
                  :pageCount="get_number_pages()"
                  :page-range="2"
                  :clickHandler="changeSongsPage"
                  :prevText="'Prev'"
                  :nextText="'Next'"
                  :containerClass="'ui pagination menu'"
                  :page-class="'item'"
                  :next-class="'item'"
                  :prev-class="'item'"
                  >
                </paginate>
            </template>
        </div>
        <p style="margin-top:30px;"><router-link tag="a" class="ui button green" :to="{name: 'song_new'}">{{ t('Add a song') }}</router-link></p>
    </div>
</template>

<script>
    import axios from 'axios'
    import {root_url, songs_by_page} from '@/common/index.js'
    import Paginate from 'vuejs-paginate'
    
    import Songtitle from '@/components/Songtitle.vue'

    export default {
        name: "songslist",
        data() {
            return {
                results: Array,
                count: 0,
            }
        },
        components: {
            Songtitle,
            Paginate,
        },
        created() {
            axios.get(root_url + "songs/list/paginate/")
                .then(response => {
                    this.results = response.data["results"];
                    this.count = response.data["count"];
                }, 	(error) => { console.log(error) });
        },
        methods: {
            changeSongsPage(pageNum) {
                axios.get(root_url + "songs/list/paginate/?page=" + pageNum)
                .then(response => {
                    this.results = response.data["results"];
                    this.count = response.data["count"];
                },  (error) => { console.log(error) });
            },
            get_number_pages() {
                return Math.ceil(this.$data.count/songs_by_page)
            }
        }
    }
</script>

<style>
.ui.pagination.menu {
    padding-left: 0px;
}
</style>