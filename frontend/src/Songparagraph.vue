<template>
    <div>
        <div v-for="verse in paragraph.verses">
            <songverse :verse="verse"></songverse>
        </div>
        <p><button class="ui button" @click.prevent="addVerse">Add a verse</button></p>
        <form v-if="display_form_add" class="ui form">
            <fieldset>
                <p class="field">
                    <label for="content">Content:</label>
                    <input type="text" v-model="new_verse_content" @keyup.enter="sendNewVerse()">
                </p>

                <button class="ui button" type="submit" @click.prevent="sendNewVerse()">Send</button>
                <button class="ui button" @click.prevent="cancelNewVerse()">Cancel</button>
            </fieldset>
        </form>
    </div>
</template>

<script>
    import axios from 'axios'

    import Songverse from './Songverse.vue'

    export default {
        components: {
            Songverse
        },
        data(){
            return {
                display_form_add: false,
                new_verse_content: ""
            }
        },
        props: {
            paragraph: Object
        },
        methods: {
            addVerse(){
                this.$data.display_form_add = true
            },
            cancelNewVerse() {
                this.$data.display_form_add = false
            },
            sendNewVerse(){
                console.log("Send new verse");
                let verse = {
                    id: null,
                    paragraph: this.paragraph.id,
                    order: this.paragraph.verses.length,
                    content: this.$data.new_verse_content
                };

                if( this.paragraph.id === null ){
                    let new_paragraph = {
                        order: this.paragraph.order,
                        song: this.paragraph.song,
                        is_refrain: this.paragraph.is_refrain,
                        verses: null
                    };
                    console.log("Saves paragraph first", new_paragraph);
                    axios.post("http://localhost:8000/paragraphs/list/", new_paragraph)
                        .then(response => {
                            verse.paragraph = response.data.id;
                            axios.post("http://localhost:8000/verses/list/", verse)
                                .then(response2 => { console.log(response2.data)
                                }, 	(error2) => { console.log(error2) });
                            this.$data.display_form_add = false
                        }, 	(error) => { console.log("Error", error) });
                    this.paragraph.verses = [verse];
                    this.new_verse_content = ""
                }else{
                    axios.post("http://localhost:8000/verses/list/", verse)
                        .then(response => { console.log(response.data)
                        }, 	(error) => { console.log(error) });
                    this.paragraph.verses.push(verse)
                    this.$data.display_form_add = false
                    this.new_verse_content = ""
                }
            }
        }
    }
</script>