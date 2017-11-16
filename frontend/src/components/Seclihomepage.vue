<template>
    <div id="secli_homepage">
        <div class="ui grid">
            <div class="four wide column">
                <div class="ui vertical fluid tabular menu">
                    <div class="overlay" style="position: fixed; top: auto; left: auto; z-index: 10;">
                        <div class="ui labeled icon vertical menu">
                            <p>
                                <button @click.prevent="autofinder()" class="vertical_item ui button primary">{{ t('Autofind those songs codes') }}</button>
                            </p>
                            <p>
                                <button @click.prevent="cancel()" class="ui button">{{ t('Cancel') }}</button>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="twelve wide stretched column">
                <template v-if="secliGuessedNumbers === true">
                    {{ t('Loading...') }}
                </template>
                <template v-else-if="secliGuessedNumbers">
                    <form id="songtexform" class="ui form">
                        <fieldset>
                            <legend>{{ t('SECLI codes form for songs selected') }}</legend>
                            <template v-for="(item, n) in results">
                                <div class="ui grid sixteen columns">
                                    <div class="four wide column center">
                                        <h3>{{ t('Song:') }} {{item.title}}</h3>
                                        <h4>{{ t('Written by:') }} {{item.get_printable_author}}</h4>
                                    </div>
                                    <div class="twelve wide column">
                                        <template v-if="secliGuessedNumbers[item.id].code">
                                            <p>
                                            <strong>{{ secliGuessedNumbers[item.id].title }}</strong>
                                            </p>
                                            <p>
                                            <em>{{ t('Author: ') }} {{ secliGuessedNumbers[item.id].author[0] }} - {{ t('Composer: ') }} {{ secliGuessedNumbers[item.id].author[1] }}</em>
                                            </p>
                                            <p>
                                            <input type="text" :name="'content_' + item.id" size="width:150px" v-model="secliGuessedNumbers[item.id].code" />
                                            </p>
                                        </template>
                                        <template v-else>
                                            <div class="ui grid sixteen columns">
                                                <template v-for="(song_proposal, l) in secliGuessedNumbers[item.id]">
                                                    <div class="six wide column">
                                                        <p class="field">
                                                            <label :for="'selection_propositions_' + item.id + '_' + l">{{ t('Select this code: ') }}</label>
                                                            <input type="radio" :id="'selection_propositions_' + item.id + '_' + l" :name="'selection_propositions_' + item.id" v-model="song_proposal.selected" />
                                                        </p>
                                                    </div>
                                                    <div class="ten wide column">
                                                        <p>
                                                        <strong>{{ song_proposal.title }}</strong>
                                                        </p>
                                                        <p>
                                                        <em>{{ t('Author: ') }} {{ song_proposal.author[0] }} - {{ t('Composer: ') }} {{ song_proposal.author[1] }}</em>
                                                        </p>
                                                        <p class="field">
                                                            <input type="text" :name="'content_' + item.id" v-model="song_proposal.code" style="width:150px" />
                                                        </p>
                                                    </div>
                                                </template>
                                            </div>
                                        </template>
                                    </div>
                                </div>
                                <div class="ui section divider"></div>
                            </template>
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
                                <p>
                                    <label for="select_all"><strong>{{ t('Select all:') }}</strong></label>
                                    <input type="checkbox" id="select_all" v-model="allSelected" @change="select_all()"/>
                                </p>
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
        name: "secli_homepage",
        data() {
            return {
                results: Array,
                checkedNames: Array,
                secliGuessedNumbers: false,
                allSelected: false,
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
            autofinder() {
                let listIds = ""
                let numberSelectedSongs = 0;
                for (var i = 0; i < this.$data.checkedNames.length; i++) {
                    if( this.$data.checkedNames[i] ){
                        numberSelectedSongs++;
                        listIds += "" + this.$data.results[i].id + "/";
                    }
                }
                if( numberSelectedSongs == this.$data.checkedNames.length ){
                    listIds = "all/"
                }
                if( listIds.length > 0 )
                {
                    this.$data.secliGuessedNumbers = true;
                    axios.get(root_url + "copyrights/extract/" + listIds)
                    .then(response => {
                        this.$data.listIds = listIds;
                        this.$data.secliGuessedNumbers = response.data;
                        for (var i = 0; i < this.$data.checkedNames.length; i++) {
                            if( this.$data.checkedNames[i] ){
                                // console.log(response.data[this.$data.results[i].id]);
                            }
                        }
                    },  (error) => { console.log(error) });
                }
            },
            save() {

            },
            cancel() {
                this.$data.secliGuessedNumbers = false
                // this.$data.checkedNames = new Array()
            },
            select_all() {
                for (var i = 0; i < this.$data.checkedNames.length; i++) {
                    this.$data.checkedNames[i] = this.$data.allSelected;
                }
            }
        }
    }
</script>