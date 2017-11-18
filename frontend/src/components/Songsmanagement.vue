<template>
    <div id="latex_homepage">
        <div class="ui grid">
            <div class="four wide column">
                <div class="ui vertical fluid tabular menu">
                    <div class="overlay" style="position: fixed; top: auto; left: auto; z-index: 10;">
                        <div class="ui labeled icon vertical menu">
                            <p>
                                <button @click.prevent="guessPages()" class="vertical_item ui button orange">{{ t('Guess the pages of those songs') }}</button>
                            </p>
                            <p>
                                <button @click.prevent="autofinder()" class="vertical_item ui button yellow">{{ t('Autofind those songs codes') }}</button>
                            </p>
                            <p>
                                <button @click.prevent="editLatex()" class="vertical_item ui button purple">{{ t('Edit the latex of those songs') }}</button>
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
                <div class="ui negative message" v-if="errorMessage">
                    <i class="close icon" @click="errorMessage = false"></i>
                    <div class="header">
                        {{ t('Error') }}
                    </div>
                    <p>
                        {{errorMessage}}
                    </p>
                </div>
                <template v-if="pagesGuessed === true || secliGuessedNumbers === true || latexCode === true">
                    Loading...
                </template>
                <template v-else-if="pagesGuessed">
                    <form id="songtexform" class="ui form">
                        <fieldset>
                            <legend>{{ t('Pages choices for selected songs') }}</legend>
                            <template v-for="(item, n) in checkedNames">
                                <template v-if="item">
                                    <p class="field">
                                        <h3>{{dataSongs[n].title.toUpperCase()}}</h3>
                                        <template v-if="pagesGuessed[dataSongs[n].id]">
                                            <label :for="'content_'+n">{{ t('Guessed value: ') }}{{pagesGuessed[dataSongs[n].id][0]}} (<strong>{{ t('Title: ') }}{{pagesGuessed[dataSongs[n].id][1]}}</strong>)</label>
                                            <input type="text" :id="'content_'+n" v-model="pagesChosen[dataSongs[n].id]" />
                                        </template>
                                        <template v-else>
                                            <label :for="'content_'+n">{{ t('No guess: ') }}</label>
                                            <input type="text" :id="'content_'+n" v-model="pagesChosen[dataSongs[n].id]" />
                                        </template>
                                    </p>
                                </template>
                            </template>
                            <p class="field"><button @click.prevent="savePages()" class="ui primary button">{{ t('Save') }}</button><button @click.prevent="cancel()" class="ui button">{{ t('Cancel') }}</button></p>
                        </fieldset>
                    </form>
                </template>
                <template v-else-if="latexCode">
                    <form id="songtexform" class="ui form">
                        <fieldset>
                            <legend>{{ t('Tex form for selected songs') }}</legend>
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
                            <template v-for="(item, n) in checkedNames">
                                <template v-if="item">
                                    <div class="ui grid sixteen columns">
                                        <div class="four wide column center">
                                            <h3>{{ t('Song:') }} {{dataSongs[n].title}}</h3>
                                            <h4>{{ t('Written by:') }} {{dataSongs[n].get_printable_author}}</h4>
                                        </div>
                                        <div class="twelve wide column">
                                            <template v-if="secliGuessedNumbers[dataSongs[n].id].code">
                                                <p>
                                                <strong>{{ secliGuessedNumbers[dataSongs[n].id].title }}</strong>
                                                </p>
                                                <p>
                                                <em>{{ t('Author: ') }} {{ secliGuessedNumbers[dataSongs[n].id].author[0] }} - {{ t('Composer: ') }} {{ secliGuessedNumbers[dataSongs[n].id].author[1] }}</em>
                                                </p>
                                                <p>
                                                <input type="text" :name="'content_' + dataSongs[n].id" size="width:150px" v-model="secliGuessedNumbers[dataSongs[n].id].code" />
                                                </p>
                                            </template>
                                            <template v-else>
                                                <div class="ui grid sixteen columns">
                                                    <template v-for="(song_proposal, l) in secliGuessedNumbers[dataSongs[n].id]">
                                                        <div class="six wide column">
                                                            <p class="field">
                                                                <label :for="'selection_propositions_' + dataSongs[n].id + '_' + l">{{ t('Select this code: ') }}</label>
                                                                <input type="radio" :value="l" :id="'selection_propositions_' + dataSongs[n].id + '_' + l" :name="'selection_propositions_' + dataSongs[n].id" v-model="secliSelectedChoices[n]" />
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
                                                                <input type="text" :name="'content_' + dataSongs[n].id" v-model="secliGuessedNumbers[dataSongs[n].id][l].code" style="width:150px" />
                                                            </p>
                                                        </div>
                                                    </template>
                                                </div>
                                            </template>
                                        </div>
                                    </div>
                                    <div class="ui section divider"></div>
                                </template>
                            </template>
                            <p class="field"><button @click.prevent="saveCodes()" class="ui primary button">{{ t('Save') }}</button><button @click.prevent="cancel()" class="ui button">{{ t('Cancel') }}</button></p>
                        </fieldset>
                    </form>
                </template>
                <template v-else>
                    <h2>{{ t('List of songs') }}</h2>
                    <div class="ui list aligned large">
                        <form id="latex_songs_selection" class="ui form">
                            <p>
                                <label for="select_all"><strong>{{ t('Select all:') }}</strong></label>
                                <input type="checkbox" id="select_all" v-model="allSelected" @change="select_all()"/>
                            </p>
                            <table class="ui celled table">
                              <thead>
                                <tr><th>{{ t('Title') }}</th>
                                <th>{{ t('Author') }}</th>
                                <th>{{ t('Code') }}</th>
                                <th>{{ t('Page') }}</th>
                                <th>{{ t('Select') }}</th>
                              </tr></thead>
                              <tbody>
                                <template v-for="(item, n) in dataSongs">
                                    <tr>
                                        <td><label :for="'selectionner_' + item.id">
                                            <strong>{{item.title}}</strong>
                                        </label></td>
                                        <td><label :for="'selectionner_' + item.id">{{item.get_printable_author}}</label></td>
                                        <td><label :for="'selectionner_' + item.id">{{item.secli_number}}</label></td>
                                        <td><label :for="'selectionner_' + item.id">{{item.page_number}}</label></td>
                                        <td><input type="checkbox" v-model="checkedNames[n]" :value="item.id" :id="'selectionner_' + item.id" /></td>
                                    </tr>
                                </template>
                                </tbody>
                            </table>
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
                checkedNames: Array,
                allSelected: false,
                listIds: "",
                
                secliGuessedNumbers: false,
                secliSelectedChoices: Array,

                pagesGuessed: false,
                pagesChosen: false,
                
                latexCode: false,
                
                errorMessage: false,
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
            computeListIds() {
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
                    this.$data.listIds = listIds;
                }
            },

            guessPages() {
                this.computeListIds()
                
                // if there is more then one 
                if( this.$data.listIds.length > 0 )
                {
                    this.$data.pagesGuessed = true;
                    axios.get(root_url + "songs/guess/pages/" + this.$data.listIds)
                    .then(response => {
                        // pagesGuessed = data from API or null for songs that didn't match any song in the external database
                        this.$data.pagesGuessed = new Array();
                        // pagesChosen = data to save (data in the forms)
                        this.$data.pagesChosen = new Array();

                        this.$data.pagesGuessed = response.data;

                        for (var i = 0; i < this.$data.checkedNames.length; i++) {
                            if( this.$data.checkedNames[i] ){
                                // if this title has been associated to a song in the external database
                                if( this.$data.pagesGuessed[this.$data.dataSongs[i].id] ){
                                    this.$data.pagesChosen[this.$data.dataSongs[i].id] = response.data[this.$data.dataSongs[i].id][0];
                                } else {
                                    this.$data.pagesChosen[this.$data.dataSongs[i].id] = "";
                                }
                            }
                        }
                    },  (error) => { console.log(error) });
                }
            },
            savePages() {
                let dataToSend = new Array()

                for (var i = 0; i < this.$data.checkedNames.length; i++) {
                    if( this.$data.checkedNames[i] ){
                        let songId = this.$data.dataSongs[i].id;
                        if( this.$data.pagesChosen[songId] != "" ) {
                            dataToSend.push({
                                id: songId,
                                page: this.$data.pagesChosen[songId]
                            })
                        }
                    }
                }

                axios.post(root_url + "songs/guess/pages/" + this.$data.listIds, dataToSend)
                    .then(response => {
                        this.cancel()
                        this.update()
                    },  (error) => { console.log(error) });
            },


            editLatex() {
                this.computeListIds()

                if( this.$data.listIds.length > 0 )
                {
                    this.$data.latexCode = true;
                    axios.get(root_url + "song/edit/multiple/tex/" + this.$data.listIds)
                    .then(response => {
                        this.$data.latexCode = response.data.code;
                    },  (error) => { console.log(error) });
                }
            },
            saveLatex() {
                let dataToSend = {
                    code: this.$data.latexCode
                }
                axios.post(root_url + "song/edit/multiple/tex/" + this.$data.listIds, dataToSend)
                    .then(response => {
                        this.cancel()
                        this.update()
                    },  (error) => { console.log(error) })
                // this.$router.push({name:'latex_homepage'})
            },



            autofinder() {
                this.computeListIds()
                
                if( this.$data.listIds.length > 0 )
                {
                    this.$data.secliGuessedNumbers = true;
                    axios.get(root_url + "copyrights/extract/" + this.$data.listIds)
                    .then(response => {
                        this.$data.secliGuessedNumbers = response.data;
                        this.$data.secliSelectedChoices = new Array();
                        for (var i = 0; i < this.$data.checkedNames.length; i++) {
                            if( this.$data.checkedNames[i] ){
                                if( this.$data.secliGuessedNumbers[this.$data.dataSongs[i].id].length ){
                                    this.$data.secliSelectedChoices[i] = undefined;
                                }
                            }
                        }

                    },  (error) => { console.log(error) });
                }
            },
            saveCodes() {
                let dataToSend = new Array()

                for (var i = 0; i < this.$data.checkedNames.length; i++) {
                    if( this.$data.checkedNames[i] ){
                        let songId = this.$data.dataSongs[i].id;
                        let currentSongSecli = this.$data.secliGuessedNumbers[songId];

                        if( currentSongSecli.length && this.$data.secliSelectedChoices[i] === undefined ) {
                            this.$data.errorMessage = this.$translate.text("You forgot to select the best matching element for at least one song. Don't forget you still can edit the code in the input in the right column.");
                            return "";
                        }else{
                            // When there are many choices possible (no obvious matching song)
                            if( currentSongSecli.length ) {
                                dataToSend.push({
                                    id: songId,
                                    chosenNumber: currentSongSecli[this.$data.secliSelectedChoices[i]].code
                                })
                            }
                            // When a matching song was found.
                            else {
                                dataToSend.push({
                                    id: songId,
                                    chosenNumber: currentSongSecli.code
                                })
                            }
                        }
                    }
                }

                axios.post(root_url + "copyrights/extract/" + this.$data.listIds, dataToSend)
                    .then(response => {
                        this.cancel()
                        this.update()
                    },  (error) => { console.log(error) })

            },

            update() {
                axios.get(root_url + "songs/list.json")
                .then(response => {
                    // this.$data.dataSongs = response.data

                    this.$data.dataSongs = new Array()
                    for (var i = 0; i < response.data.length; i++) {
                        this.$data.dataSongs[i] = response.data[i];
                    }
                },  (error) => { console.log(error) });
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