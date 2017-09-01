<template>
    <div>
        <div v-for="(verse,index) in paragraph.verses">
            <songverse :verse="verse" :is_refrain="paragraph.is_refrain">
                <span v-if="verse.order>0 || paragraph.verses.length-1>verse.order"> - </span>
                <span @click="sendUp(verse, index)" v-if="verse.order>0">Up</span>
                <span v-if="verse.order>0 && paragraph.verses.length-1>verse.order"> - </span>
                <span @click="sendDown(verse, index)" v-if="paragraph.verses.length-1>verse.order">Down</span>
            </songverse>
        </div>
        <fieldset>
            <p>
                <form class="ui form">
                    <p class="field">
                        <label for="content">Is refrain?</label>
                        <input type="checkbox" v-model="paragraph.is_refrain" @click.prevent="sendIsRefrain()">
                    </p>
                </form>
                <button class="ui button" @click.prevent="addVerse">Add a verse</button>
                <slot></slot>
            </p>
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
        </fieldset>
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
            invertVerse(id_top, id_bottom){
                id_top = this.paragraph.verses[id_top].id
                id_bottom = this.paragraph.verses[id_bottom].id

                axios.get("http://localhost:8000/verses/invert/" + id_top + "/and/" + id_bottom + "/")
                    .then(response => { console.log("Verse #", id_top, " and #", id_bottom, "inverted") },
                        (error) => { console.log("Error", error) });
            },
            addVerse(){
                this.$data.display_form_add = true
            },
            cancelNewVerse() {
                this.$data.display_form_add = false
            },
            sendIsRefrain() {
                // TODO: check why checkbox is not checked at the beginning and checked after. 
                // FIX: sth like click.after ?
                this.paragraph.is_refrain = !this.paragraph.is_refrain
                if( this.paragraph.id === null ){
                    let new_paragraph = {
                        order: this.paragraph.order,
                        song: this.paragraph.song,
                        is_refrain: this.paragraph.is_refrain,
                        verses: null
                    };
                    axios.post("http://localhost:8000/paragraphs/list/", new_paragraph)
                        .then(response => {
                            this.paragraph.id = response.data.id;
                            console.log("Is refrain (", this.paragraph.is_refrain, ") saved")
                        },  (error) => { console.log("Error", error) });
                }else{
                    let update_paragraph = {
                        id: this.paragraph.id,
                        song: this.paragraph.song,
                        order: this.paragraph.order,
                        is_refrain: this.paragraph.is_refrain
                    };
                    axios.put("http://localhost:8000/paragraphs/" + this.paragraph.id + "/", update_paragraph)
                        .then(response => { console.log("Is refrain (", this.paragraph.is_refrain, ") saved") },
                            (error) => { console.log("Error", error) });
                }
            },
            sendNewVerse(){
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
            },
            sendUp(verse, index){
                let other_index = -1
                for (var i = 0; i < this.paragraph.verses.length; i++) {
                    if( this.paragraph.verses[i].order == verse.order-1 ){
                        other_index = i
                        this.paragraph.verses[i].order = verse.order
                        verse.order--
                        break
                    }
                }
                if( other_index >= 0 ){
                    this.paragraph.verses[index] = this.paragraph.verses[other_index]
                    this.paragraph.verses[other_index] = verse
                    this.invertVerse(index, other_index)
                }
            },
            sendDown(verse, index){
                let other_index = -1
                for (var i = 0; i < this.paragraph.verses.length; i++) {
                    if( this.paragraph.verses[i].order == verse.order+1 ){
                        other_index = i
                        this.paragraph.verses[i].order = verse.order
                        verse.order++
                        break
                    }
                }
                if( other_index >= 0 ){
                    this.paragraph.verses[index] = this.paragraph.verses[other_index]
                    this.paragraph.verses[other_index] = verse
                    this.invertVerse(index, other_index)
                }
            }
        }
    }
</script>