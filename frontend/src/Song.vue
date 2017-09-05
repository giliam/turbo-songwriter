<template>
    <div id="song">
        <router-link :to="{name:'root'}">Retour à la liste</router-link>
        <form class="ui form">
            <div v-if="result.latex_code == null">
                <p><router-link tag="button" class="ui form button submit" :to="{name: 'song_force_conversion'}">Convert to LaTeX</router-link></p>
            </div>
            <div v-else>
                <p><router-link tag="button" class="ui form button submit" :to="{name: 'song_edit_latex'}">Edit LaTeX code</router-link></p>
                <p><router-link tag="button" class="ui form button submit" :to="{name: 'song_force_conversion'}">Force conversion to LaTeX</router-link></p>
            </div>
            <div>
                <p class="field">
                    <label for="enable_harmonization">Enable harmonization:</label>
                    <input type="checkbox" name="enable_harmonization" v-model="enable_harmonization">
                </p>
            </div>
        </form>
        <h2>{{ result.title }}</h2>
        <h4 v-if="result.author">{{ result.author.firstname }} {{ result.author.lastname}} - {{ result.editor.name }}</h4>
        <h4>Themes: <span v-for="(theme, id) in result.theme"><span v-if="id > 0">, </span>{{ theme.name }}</span></h4>
        <div v-if="!enable_harmonization">
            <div v-for="(paragraph, index) in result.paragraphs">
                <songparagraph :paragraph="paragraph">
                    <span @click="sendUp(paragraph, index)" v-if="paragraph.order>0">Up</span>
                    <span v-if="paragraph.order>0 && result.paragraphs.length-1>paragraph.order">-</span>
                    <span @click="sendDown(paragraph, index)" v-if="result.paragraphs.length-1>paragraph.order">Down</span>
                </songparagraph>
                <br>
            </div>
            <p><a @click.prevent="addParagraph()">Add a paragraph</a></p>
        </div>
        <div v-else>
            <songharmonization :song="result">
            </songharmonization>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'

    import Songparagraph from './Songparagraph.vue'
    import Songharmonization from './Songharmonization.vue'

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

                axios.get("http://localhost:8000/paragraphs/invert/" + id_top + "/and/" + id_bottom + "/")
                    .then(response => { console.log("Paragraph #", id_top, " and #", id_bottom, "inverted") },
                        (error) => { console.log("Error", error) });
            },
            addParagraph() {
                let nb_paragraphs = this.$data.result.paragraphs.length
                let paragraph = {
                    id: null,
                    order: nb_paragraphs,
                    song: this.$data.result.id,
                    verses: Array,
                    is_refrain: false
                }
                this.$data.result.paragraphs.push(paragraph)
            },
            launch_convert_to_tex(force_conversion){
                this.$emit("convert_to_tex", this.$route.params.item_id, force_conversion)
            },
            sendUp(paragraph, index){
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
                axios.get("http://localhost:8000/songs/" + this.$route.params.item_id + ".json")
                    .then(response => {
                        console.log("Received", response.data)
                        this.$data.result = response.data;
                    })
            }
        }
    }
</script>