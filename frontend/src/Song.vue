<template>
    <div id="song">
        <slot></slot>
        <h2>{{ result.title }}</h2>
        <div id="paragraphs" v-for="paragraph in result.paragraphs">
            <songparagraph :paragraph="paragraph"></songparagraph>
        </div>
        <p><a @click.prevent="addParagraph()">Add a paragraph</a></p>
        <button @click.prevent="save()">Save</button>
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
                console.log("Adds paragraph", this.$data.result.paragraphs.length)
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
            save() {
                console.log("Save")
            }
        },
        watch : {
            item_id : function (value) {
                console.log("Receives", value)
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