<template>
    <div id="song">

        <div class="overlay">
          <div class="ui labeled icon vertical menu">
            <form class="ui form">
                <div v-if="result.latex_code == null">
                    <p><router-link tag="button" class="ui form button submit" :to="{name: 'song_force_conversion'}">{{ t('Convert to LaTeX') }}</router-link></p>
                </div>
                <div v-else>
                    <p><router-link tag="button" class="ui form button submit" :to="{name: 'song_edit_latex', params:{'item_id': result.id}}">{{ t('Edit LaTeX code') }}</router-link><router-link tag="button" class="ui form button submit" :to="{name: 'song_force_conversion', params:{'item_id': result.id}}">{{ t('Force conversion to LaTeX') }}</router-link></p>
                </div>
                <div>
                    <p class="field">
                        <label for="enable_harmonization">{{ t('Enable harmonization:') }}</label> <input type="checkbox" name="enable_harmonization" v-model="enable_harmonization">
                    </p>
                </div>
            </form>
            <router-link :to="{name: 'song_edit', params:{'item_id': result.id}}">{{ t('Edit song caracteristics') }}</router-link>        
          </div>
        </div>
        <router-link :to="{name:'root'}">{{ t('Back to the list') }}</router-link>
        <h1>{{ result.title }}</h1>
        <h3>{{ t('Old page number:') }} {{ result.old_page_number }} - {{ t('Page number:') }} {{ result.page_number }}</h3>
        <h4 v-if="result.author">{{ result.author.firstname }} {{ result.author.lastname}} - {{ result.editor.name }}</h4>
        <h4>{{ t('Themes:') }} <span v-for="(theme, id) in result.theme"><span v-if="id > 0">, </span>{{ theme.name }}</span></h4>
        <div v-if="!enable_harmonization">
            <div v-for="(paragraph, index) in result.paragraphs">
                <songparagraph :paragraph="paragraph">
                    <p><button class="ui red button" @click="deleteParagraph(paragraph, index)">{{ t('Delete the paragraph') }}</button></p>
                    <p v-if="paragraph.id">
                        <button class="ui button" @click="sendUp(paragraph, index)" v-if="paragraph.order>0">{{ t('Up') }}</button>
                        <button class="ui button" @click="sendDown(paragraph, index)" v-if="result.paragraphs.length-1>paragraph.order">{{ t('Down') }}</button>
                    </p>
                </songparagraph>
                <br>
            </div>
            <p><a @click.prevent="addParagraph()">{{ t('Add a paragraph') }}</a></p>
        </div>
        <div v-else>
            <songharmonization :song="result">
            </songharmonization>
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
                axios.get(root_url + "songs/" + this.$route.params.item_id + ".json")
                    .then(response => {
                        console.log("Received", response.data)
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
            }
        },
        mounted() {
            if( this.$route.params.item_id ){
                this.sync()
            }
        }
    }
</script>