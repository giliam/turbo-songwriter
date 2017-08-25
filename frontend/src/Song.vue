<template>
    <div id="song">
        <slot></slot>
        <h2>{{ result.title }}</h2>
        <h4 v-if="result.author">{{ result.author.firstname }} {{ result.author.lastname}} - {{ result.editor.name }}</h4>
        <h4>Themes: <span v-for="(theme, id) in result.theme"><span v-if="id > 0">, </span>{{ theme.name }}</span></h4>
        <div v-for="paragraph in result.paragraphs">
            <songparagraph :paragraph="paragraph"></songparagraph>
            <br>
        </div>
        <p><a @click.prevent="addParagraph()">Add a paragraph</a></p>
    </div>
</template>

<script>
    import axios from 'axios'

    import Songparagraph from './Songparagraph.vue'

    export default {
        components:{
            Songparagraph
        },
        props: {
            item_id: Number,
        },
        data() {
            return {
                result: Object
            }
        },
        methods:{
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
            }
        },
        watch : {
            item_id : function (value) {
                this.item_id = value
                if( this.item_id ){
                    axios.get("http://localhost:8000/songs/" + this.item_id + ".json")
                        .then(response => {
                            console.log("Received", response.data)
                            this.$data.result = response.data;
                        })
                }
            }
        }
    }
</script>