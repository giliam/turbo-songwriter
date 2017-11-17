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
                                <button @click.prevent="cancel()" class="ui button">{{ t('Cancel') }}</button>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="twelve wide stretched column">
                <template v-if="pagesGuessed === true">
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
        name: "latex_homepage",
        data() {
            return {
                dataSongs: Array,
                checkedNames: Array,
                pagesGuessed: false,
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
            save() {
                // axios.post(root_url + "song/edit/multiple/tex/" + this.$data.listIds, data_code)
                //     .then(response => {
                //         console.log("Saved!")
                //     },  (error) => { console.log(error) })
                // this.$router.push({name:'latex_homepage'})
            },
            cancel() {
                this.$data.pagesGuessed = false
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