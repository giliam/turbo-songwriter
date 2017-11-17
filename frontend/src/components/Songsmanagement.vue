<template>
    <div id="latex_homepage">
        <div class="ui grid">
            <div class="four wide column">
                <div class="ui vertical fluid tabular menu">
                    <div class="overlay" style="position: fixed; top: auto; left: auto; z-index: 10;">
                        <div class="ui labeled icon vertical menu">
                            <p>
                                <button @click.prevent="guessPages()" class="vertical_item ui button primary">{{ t('Guess the pages of those songs') }}</button>
                            </p>
                            <p>
                                <button @click.prevent="autofinder()" class="vertical_item ui button primary">{{ t('Autofind those songs codes') }}</button>
                            </p>
                            <p>
                                <button @click.prevent="editLatex()" class="vertical_item ui button primary">{{ t('Edit the latex of those songs') }}</button>
                            </p>
                            <p>
                                <button @click.prevent="cancel()" class="ui button">{{ t('Cancel') }}</button>
                            </p>
                            <p>
                                <router-link tag="button" class="vertical_item ui button purple" :to="{name:'additional_latexcode_list'}">{{ t('Edit additional latex code') }}</router-link>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="twelve wide stretched column">
                <template v-if="pagesGuessed === true || secliGuessedNumbers === true || latexCode === true">
                    Loading...
                </template>
                <template v-else-if="pagesGuessed">
                    <form id="songtexform" class="ui form">
                        <fieldset>
                            <legend>{{ t('Tex form for songs selected') }}</legend>
                            <template v-for="(item, n) in dataSongs">
                                <p class="field">
                                    <h3>{{item.title.toUpperCase()}}</h3>
                                    <template v-if="pagesGuessed[item.id]">
                                        <label :for="'content_'+n">{{ t('Guessed value: ') }}{{pagesGuessed[item.id][0]}} (<strong>{{ t('Title: ') }}{{pagesGuessed[item.id][1]}}</strong>)</label>
                                        <input type="text" :id="'content_'+n" v-model="pagesChosen[item.id]" />
                                    </template>
                                    <template v-else>
                                        <label :for="'content_'+n">{{ t('No guess: ') }}</label>
                                        <input type="text" :id="'content_'+n" v-model="pagesChosen[item.id]" />
                                    </template>
                                </p>
                            </template>
                            <p class="field"><button @click.prevent="savePages()" class="ui primary button">{{ t('Save') }}</button><button @click.prevent="cancel()" class="ui button">{{ t('Cancel') }}</button></p>
                        </fieldset>
                    </form>
                </template>
                <template v-else-if="latexCode">
                    <form id="songtexform" class="ui form">
                        <fieldset>
                            <legend>{{ t('Tex form for songs selected') }}</legend>
                            <p class="field">
                                <label for="content">Content:</label>
                                <textarea name="content" v-model="latexCode" v-focus></textarea>
                            </p>
                            <p class="field"><button @click.prevent="saveLatex()" class="ui primary button">{{ t('Save') }}</button><button @click.prevent="cancel()" class="ui button">{{ t('Cancel') }}</button></p>
                        </fieldset>
                    </form>
                </template>
                <template v-else-if="secliGuessedNumbers">
                    <form id="songtexform" class="ui form">
                        <fieldset>
                            <legend>{{ t('SECLI codes form for songs selected') }}</legend>
                            <template v-for="(item, n) in dataSongs">
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
                            <p class="field"><button @click.prevent="saveCodes()" class="ui primary button">{{ t('Save') }}</button><button @click.prevent="cancel()" class="ui button">{{ t('Cancel') }}</button></p>
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
                                <template v-for="(item, n) in dataSongs">
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
        name: "songs_management",
        data() {
            return {
                dataSongs: Array,
                secliGuessedNumbers: false,
                checkedNames: Array,
                pagesGuessed: false,
                latexCode: false,
                pagesChosen: false,
                allSelected: false,
                listIds: "",
            }
        },
        created() {
            axios.get(root_url + "songs/list.json")
                .then(response => {
                    // this.$data.dataSongs = response.data

                    this.$data.dataSongs = new Array()
                    for (var i = 0; i < response.data.length; i++) {
                        this.$data.dataSongs[i] = response.data[i];
                    }

                    this.$data.checkedNames = new Array(this.$data.dataSongs.length)

                },  (error) => { console.log(error) });
        },
        methods: {
            guessPages() {
                // prepares the URL
                let listIds = ""
                let numberSelectedSongs = 0;
                for (var i = 0; i < this.$data.checkedNames.length; i++) {
                    if( this.$data.checkedNames[i] ){
                        numberSelectedSongs++;
                        listIds += "" + this.$data.dataSongs[i].id + "/";
                    }
                }
                // if all songs have been selected, changes the url
                if( numberSelectedSongs == this.$data.checkedNames.length ){
                    listIds = "all/"
                }
                
                // if there is more then one 
                if( listIds.length > 0 )
                {
                    this.$data.pagesGuessed = true;
                    axios.get(root_url + "songs/guess/pages/" + listIds)
                    .then(response => {
                        // pagesGuessed = data from API or null for songs that didn't match any song in the external database
                        this.$data.pagesGuessed = new Array();
                        // pagesChosen = data to save (data in the forms)
                        this.$data.pagesChosen = new Array();
                        this.$data.listIds = listIds;

                        this.$data.pagesGuessed = response.data;

                        for (var i = 0; i < this.$data.dataSongs.length; i++) {
                            // if this title has been associated to a song in the external database
                            if( this.$data.pagesGuessed[this.$data.dataSongs[i].id] ){
                                this.$data.pagesChosen[this.$data.dataSongs[i].id] = response.data[this.$data.dataSongs[i].id][0];
                            } else {
                                this.$data.pagesChosen[this.$data.dataSongs[i].id] = "";
                            }
                        }
                    },  (error) => { console.log(error) });
                }
            },
            savePages() {
                // axios.post(root_url + "song/edit/multiple/tex/" + this.$data.listIds, data_code)
                //     .then(response => {
                //         console.log("Saved!")
                //     },  (error) => { console.log(error) })
                // this.$router.push({name:'latex_homepage'})
            },


            editLatex() {
                // prepares the URL
                let listIds = ""
                let numberSelectedSongs = 0;
                for (var i = 0; i < this.$data.checkedNames.length; i++) {
                    if( this.$data.checkedNames[i] ){
                        numberSelectedSongs++;
                        listIds += "" + this.$data.dataSongs[i].id + "/";
                    }
                }
                // if all songs have been selected, changes the url
                if( numberSelectedSongs == this.$data.checkedNames.length ){
                    listIds = "all/"
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
            saveLatex() {
                let data_code = {
                    code: this.$data.latexCode
                }
                axios.post(root_url + "song/edit/multiple/tex/" + this.$data.listIds, data_code)
                    .then(response => {
                        console.log("Saved!")
                    },  (error) => { console.log(error) })
                // this.$router.push({name:'latex_homepage'})
            },



            autofinder() {
                // prepares the URL
                let listIds = ""
                let numberSelectedSongs = 0;
                for (var i = 0; i < this.$data.checkedNames.length; i++) {
                    if( this.$data.checkedNames[i] ){
                        numberSelectedSongs++;
                        listIds += "" + this.$data.dataSongs[i].id + "/";
                    }
                }

                // if all songs have been selected, changes the url
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
                                // console.log(response.data[this.$data.dataSongs[i].id]);
                            }
                        }
                    },  (error) => { console.log(error) });
                }
            },
            saveCodes() {

            },


            cancel() {
                this.$data.pagesGuessed = false
                this.$data.secliGuessedNumbers = false
                this.$data.latexCode = false
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