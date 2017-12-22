<template>
    <div>
        <div id="listsongs">
            <h2>{{ t(title) }}</h2>
            <p style="margin-top:30px;">
              <button class="ui button" @click.prevent="get_songs_without_author()">Without author</button>
              <button class="ui button" @click.prevent="get_songs_without_editor()">Without editor</button>
              <button class="ui button" @click.prevent="get_songs_with_latex_code()">With latex code</button>
              <button class="ui button" @click.prevent="get_songs_without_page_number()">Without page numbers</button>
            </p>
            <div class="ui list aligned large">
              <template v-if="isLoading">
                {{ t('Loading...') }}
              </template>
              <template v-else>
                <table class="ui celled table">
                  <thead>
                    <tr>
                      <th>{{ t('Title') }}</th>
                      <th>{{ t('Author') }}</th>
                      <th>{{ t('Editor') }}</th>
                      <th>{{ t('Page number') }}</th>
                      <th>{{ t('Latex code') }}</th>
                    </tr>
                  </thead>
                  <tbody>
                    <template v-for="item in results">
                      <songinfos :item="item"></songinfos>
                    </template>
                  </tbody>
                </table>
              </template>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'
    import {root_url} from '@/common/index.js'
    import Songinfos from '@/components/Songinfos.vue'

    export default {
        name: "otherlists",
        data() {
          return {
            results: Array,
            isLoading: false,
          }
        },
        components: {
          Songinfos,
        },
        created() {
        },
        methods: {
          get_songs_without_author() {
            this.$data.title = "Get songs without author"
            this.$data.isLoading = true
            axios.get(root_url + "songs/without/author/")
              .then(response => {
                this.results = response.data;
                this.$data.isLoading = false
              },  (error) => { console.log(error) });
          },
          get_songs_without_editor() {
            this.$data.title = "Get songs without editor"
            this.$data.isLoading = true
            axios.get(root_url + "songs/without/editor/")
              .then(response => {
                this.results = response.data;
                this.$data.isLoading = false
              },  (error) => { console.log(error) });
          },
          get_songs_with_latex_code() {
            this.$data.title = "Get songs with latex code"
            this.$data.isLoading = true
            axios.get(root_url + "songs/with/latex/code/")
              .then(response => {
                this.results = response.data;
                this.$data.isLoading = false
              },  (error) => { console.log(error) });
          },
          get_songs_without_page_number() {
            this.$data.title = "Get songs without page number"
            this.$data.isLoading = true
            axios.get(root_url + "songs/without/page/number/")
              .then(response => {
                this.results = response.data;
                this.$data.isLoading = false
              },  (error) => { console.log(error) });é
          },
      }
    }
</script>

<style>
.ui.pagination.menu {
    padding-left: 0px;
}
</style>