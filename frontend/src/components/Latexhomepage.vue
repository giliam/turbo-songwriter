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
                <template v-if="latexCode === true">
                    Loading...
                </template>
                <template v-else-if="latexCode">
                    <form id="songtexform" class="ui form">
                        <fieldset>
                            <legend>{{ t('Tex form for songs selected') }}</legend>
                            <p class="field">
                                <label for="content">Content:</label>
                                <textarea name="content" v-model="latexCode" v-focus></textarea>
                            </p>
                            <p class="field"><button @click.prevent="save()" class="ui primary button">{{ t('Save') }}</button><button @click.prevent="cancel()" class="ui button">{{ t('Cancel') }}</button></p>
                        </fieldset>
                    </form>
                </template>
                <template v-else>
                    <h2>{{ t('List of songs') }}</h2>
                    <div class="ui list aligned large">
                        <form id="latex_songs_selection" class="ui form">
                            <fieldset>
                                <legend>{{ t('Select the songs to edit') }}</legend>
                                <template v-for="(item, n) in results">
                                    <p>
                                        <label :for="'selectionner_' + item.id">{{item.title}}:</label>
                                        <input type="checkbox" v-model="checkedNames[n]" :value="item.id" :id="'selectionner_' + item.id" />
                                    </p>
                                </template>
                            </fieldset>
                        </form>
                    </div>
                </template>
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
                checkedNames: Array,
                latexCode: false,
                listIds: "",
            }
        },
        created() {
            axios.get(root_url + "songs/list.json")
                .then(response => {
                    this.results = response.data;
                    this.checkedNames = new Array(this.results.length)
                },  (error) => { console.log(error) });
        },
        methods: {
            edit() {
                let listIds = ""
                for (var i = 0; i < this.$data.checkedNames.length; i++) {
                    if( this.$data.checkedNames[i] ){
                        listIds += "" + this.$data.results[i].id + "/";
                    }
                }
                if( listIds.length > 0 )
                {
                    this.$data.latexCode = true;
                    axios.get(root_url + "song/edit/multiple/tex/" + listIds)
                    .then(response => {
                        this.$data.listIds = listIds;
                        this.$data.latexCode = response.data.code;
                    },  (error) => { console.log(error) });
                }
            },
            save() {
                let data_code = {
                    code: this.$data.latexCode
                }
                axios.post(root_url + "song/edit/multiple/tex/" + this.$data.listIds, data_code)
                    .then(response => {
                        console.log("Saved!")
                    },  (error) => { console.log(error) })
                // this.$router.push({name:'latex_homepage'})
            },
            cancel() {
                this.$data.latexCode = false
                // this.$data.checkedNames = new Array()
            }
        }
    }
</script>