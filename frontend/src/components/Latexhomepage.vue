<template>
    <div id="latex_homepage">
        <div class="ui grid">
            <div class="four wide column">
                <div class="ui vertical fluid tabular menu">
                    <div class="overlay" style="position: fixed; top: auto; left: auto; z-index: 10;">
                        <div class="ui labeled icon vertical menu">
                            <p>
                                <button @click.prevent="edit()" class="vertical_item ui button primary">{{ t('Edit those songs') }}</button>
                            </p>
                            <p>
                                <button @click.prevent="cancel()" class="ui button">{{ t('Cancel') }}</button>
                            </p>
                            <router-link tag="button" class="vertical_item ui button purple" :to="{name:'additional_latexcode_list'}">{{ t('Edit additional latex code') }}</router-link>
                        </div>
                    </div>
                </div>
            </div>
            <div class="twelve wide stretched column">
                <h2>{{ t('List of songs') }}</h2>
                <div class="ui list aligned large">
                    <form id="latex_songs_selection" class="ui form">
                        <fieldset>
                            <legend>{{ t('Select the songs to edit') }}</legend>
                            <template v-for="item in results">
                                <p>
                                    <label :for="'selectionner_' + item.id">{{item.title}}:</label>
                                    <input type="checkbox" name="songs_selection" :id="'selectionner_' + item.id" />
                                </p>
                            </template>
                        </fieldset>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'
    import {root_url} from '@/common/index.js'

    export default {
        name: "latex_homepage",
        data() {
            return {
                results: Array,
            }
        },
        created() {
            axios.get(root_url + "songs/list.json")
                .then(response => {
                    this.results = response.data;
                },  (error) => { console.log(error) });
        },
        methods: {
            edit() {

            },
            cancel() {

            }
        }
    }
</script>