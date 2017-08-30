<template>
    <div id="song">
        <slot></slot>
        <form class="ui form">
            <div v-if="result.latex_code == null">
                <p><button class="ui form button submit" @click.prevent="launch_convert_to_tex(true)">Convert to LaTeX</button></p>
            </div>
            <div v-else>
                <p><button class="ui form button submit" @click.prevent="launch_convert_to_tex(false)">Edit LaTeX code</button></p>
                <p><button class="ui form button submit" @click.prevent="launch_convert_to_tex(true)">Force conversion to LaTeX</button></p>
            </div>
        </form>
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
            },
            launch_convert_to_tex(force_conversion){
                this.$emit("convert_to_tex", this.item_id, force_conversion)
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