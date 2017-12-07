<template>
    <div id="song">
        <div class="ui grid">
            <div class="four wide column">
                <div class="ui vertical fluid tabular menu">
                    <div class="overlay" style="position: fixed; top: auto; left: auto; z-index: 10;">
                        <div class="ui labeled icon vertical menu">
                            <router-link tag="button" class="vertical_item ui button black" :to="{name:'root'}">{{ t('Back to the list') }}</router-link>
                            <h4>{{ t('Song') }}</h4>
                            <router-link tag="button" class="vertical_item ui form button primary" style="white-space: normal;" :to="{name: 'song_edit', params:{'item_id': result.id}}">{{ t('Edit song caracteristics') }}</router-link>        
                            <h4>{{ t('Harmonization') }}</h4>
                            <form class="ui form">
                                <div>
                                    <p class="field">
                                        <label for="enable_harmonization">{{ t('Enable harmonization:') }}</label> <input type="checkbox" name="enable_harmonization" v-model="enable_harmonization">
                                    </p>
                                </div>
                            </form>
                            <h4>{{ t('Latex') }}</h4>
                            <div v-if="result.latex_code == null">
                                <p><router-link tag="button" class="vertical_item ui form button purple" :to="{name: 'song_force_conversion'}">{{ t('Convert to LaTeX') }}</router-link></p>
                            </div>
                            <div v-else>
                                <p>
                                    <router-link tag="button" class="vertical_item ui form button primary" :to="{name: 'song_edit_latex', params:{'item_id': result.id}}">{{ t('Edit LaTeX code') }}</router-link><router-link tag="button" class="vertical_item ui form button purple" :to="{name: 'song_force_conversion', params:{'item_id': result.id}}">{{ t('Force conversion to LaTeX') }}</router-link><button class="vertical_item ui form button purple" @click.prevent="compileTex(result.id)">{{ t('Compile tex code') }}</button>
                                    <template v-if="result.latex_code.is_compiled">
                                        <router-link tag="button" class="vertical_item ui form button purple" :to="{name: 'song_pdf', params:{'item_id': result.id}}">{{ t('Display pdf') }}</router-link>
                                    </template>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>


            <div class="twelve wide stretched column">
                <h1>{{ result.title }}</h1>
                <h3>{{ t('Old page number:') }} {{ result.old_page_number }} - {{ t('Page number:') }} {{ result.page_number }}</h3>
                <h4 v-if="result.author">{{ result.author.firstname }} {{ result.author.lastname}} - <template v-if="result.editor">{{ result.editor.name }}</template></h4>
                <h4>{{ t('Themes:') }} <span v-for="(theme, id) in result.theme"><span v-if="id > 0">, </span>{{ theme.name }}</span></h4>
                <div v-if="!enable_harmonization">
                    <div v-for="(paragraph, index) in result.paragraphs">
                        <songparagraph :paragraph="paragraph">
                            <p><button class="ui red button" @click="deleteParagraph(paragraph, index)">{{ t('Delete the paragraph') }}</button></p>
                            <p v-if="paragraph.id">
                                <i class="arrow large up icon" @click="sendUp(paragraph, index)" v-if="paragraph.order>0"></i>
                                <i class="arrow large down icon" @click="sendDown(paragraph, index)" v-if="result.paragraphs.length-1>paragraph.order"></i>
                            </p>
                        </songparagraph>
                        <br>
                    </div>
                    <p><button class="ui button green" @click.prevent="addParagraph()">{{ t('Add a paragraph') }}</button></p>
                </div>
                <div v-else>
                    <songharmonization :song="result">
                    </songharmonization>
                </div>

            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'
    import {root_url} from '@/common/index.js'

    import Songparagraph from '@/components/Songparagraph.vue'
    import Songharmonization from '@/components/Songharmonization.vue'

    export default {
        components:{
            Songparagraph,
            Songharmonization
        },
        props: {
            item_id: Number,
        },
        data() {
            return {
                result: Object,
                enable_harmonization: false
            }
        },
        methods:{
            invertParagraph(id_top, id_bottom){
                id_top = this.$data.result.paragraphs[id_top].id
                id_bottom = this.$data.result.paragraphs[id_bottom].id

                axios.get(root_url + "paragraphs/invert/" + id_top + "/and/" + id_bottom + "/")
                    .then(response => { console.log("Paragraph #", id_top, " and #", id_bottom, "inverted") },
                        (error) => { console.log("Error", error) });
            },
            addParagraph() {
                let nb_paragraphs = this.$data.result.paragraphs.length
                console.log(nb_paragraphs)
                let paragraph = {
                    id: null,
                    order: nb_paragraphs,
                    song: this.$data.result.id,
                    verses: null,
                    is_refrain: false
                }
                this.$data.result.paragraphs.push(paragraph)
            },
            sync(){
                axios.get(root_url + "songs/" + this.$route.params.item_id + "/")
                    .then(response => {
                        this.$data.result = response.data;
                    })
            },
            deleteParagraph(paragraph, index){
                axios.delete(root_url + "paragraphs/" + paragraph.id + "/")
                    .then(response => { 
                        console.log("Deleted Paragraph #", paragraph.id)
                        this.sync()
                     },
                    (error) => { console.log("Error", error) });

            },
            sendUp(paragraph, index){
                if( !paragraph.id ){
                    return ""
                }
                let other_index = -1
                for (var i = 0; i < this.$data.result.paragraphs.length; i++) {
                    if( this.$data.result.paragraphs[i].order == paragraph.order-1 ){
                        other_index = i
                        this.$data.result.paragraphs[i].order = paragraph.order
                        paragraph.order--
                        break
                    }
                }
                if( other_index >= 0 ){
                    this.$data.result.paragraphs[index] = this.$data.result.paragraphs[other_index]
                    this.$data.result.paragraphs[other_index] = paragraph
                    this.invertParagraph(index, other_index)
                }
            },
            sendDown(paragraph, index){
                if( !paragraph.id ){
                    return ""
                }
                let other_index = -1
                for (var i = 0; i < this.$data.result.paragraphs.length; i++) {
                    if( this.$data.result.paragraphs[i].order == paragraph.order+1 ){
                        other_index = i
                        this.$data.result.paragraphs[i].order = paragraph.order
                        paragraph.order++
                        break
                    }
                }
                if( other_index >= 0 ){
                    this.$data.result.paragraphs[index] = this.$data.result.paragraphs[other_index]
                    this.$data.result.paragraphs[other_index] = paragraph
                    this.invertParagraph(index, other_index)
                }
            },
            compileTex(song_id) {
                axios.get(root_url + "song/compile/tex/" + this.$route.params.item_id + "/")
                    .then(response => {
                        this.$data.result.latex_code.is_compiled = true
                    })
            },
        },
        mounted() {
            if( this.$route.params.item_id ){
                this.sync()
            }
        }
    }
</script>