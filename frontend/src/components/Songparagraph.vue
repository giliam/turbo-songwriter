<template>
    <div class="ui grid sixteen columns">
        <div class="four wide column center">
            <p>
                <form class="ui form">
                    <span class="field">
                        <label for="content">{{ t('Is refrain?') }}</label>
                        <input type="checkbox" v-model="paragraph.is_refrain" @click.prevent="sendIsRefrain()">
                    </span>
                </form>
            </p>
            <p>
                <button class="ui button green" @click.prevent="addVerse">{{ t('Add a verse') }}</button>
            </p>
            <slot></slot>
        </div>
        <div class="twelve wide column">
            <div v-for="(verse,index) in paragraph.verses">
                <songverse :verse="verse" :is_refrain="paragraph.is_refrain">
                    <span v-if="verse.order>0 || paragraph.verses.length-1>verse.order"> - </span>
                    <i class="arrow up icon" @click.prevent="sendUp(verse, index)" v-if="verse.order>0"></i>
                    <span v-if="verse.order>0 && paragraph.verses.length-1>verse.order"> - </span>
                    <i class="arrow down icon" @click.prevent="sendDown(verse, index)" v-if="paragraph.verses.length-1>verse.order"></i>
                </songverse>
            </div>
            <form v-if="display_form_add" class="ui form">
                <p class="field">
                    <label for="content">Content:</label>
                    <input type="text" v-model="new_verse_content" v-focus>
                </p>

                <button class="ui button" type="submit" @click.prevent="sendNewVerse()">{{ t('Send') }}</button>
                <button class="ui button" @click.prevent="cancelNewVerse()">{{ t('Cancel') }}</button>
            </form>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'
    import {root_url} from '@/common/index.js'

    import Songverse from '@/components/Songverse.vue'

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

                axios.get(root_url + "verses/invert/" + id_top + "/and/" + id_bottom + "/")
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
                    axios.post(root_url + "paragraphs/list/", new_paragraph)
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
                    axios.put(root_url + "paragraphs/" + this.paragraph.id + "/", update_paragraph)
                        .then(response => { console.log("Is refrain (", this.paragraph.is_refrain, ") saved") },
                            (error) => { console.log("Error", error) });
                }
            },
            sendNewVerse(){
                let verse = {
                    id: null,
                    paragraph: this.paragraph.id,
                    order: this.paragraph.verses ? this.paragraph.verses.length : 0,
                    content: this.$data.new_verse_content
                };

                if( this.paragraph.id === null ){
                    let new_paragraph = {
                        order: this.paragraph.order,
                        song: this.paragraph.song,
                        is_refrain: this.paragraph.is_refrain,
                        verses: null
                    };
                    
                    axios.post(root_url + "paragraphs/list/", new_paragraph)
                        .then(response => {
                            verse.paragraph = response.data.id;
                            this.paragraph.id = response.data.id;
                            axios.post(root_url + "verses/list/", verse)
                                .then(response2 => { 
                                    verse = response2.data
                                    this.paragraph.verses = [verse];
                                }, 	(error2) => { console.log(error2) });
                        },  (error) => { console.log("Error", error) });

                    this.$data.display_form_add = false
                    this.new_verse_content = ""
                }else{
                    axios.post(root_url + "verses/list/", verse)
                        .then(response => { 
                            verse = response.data
                            this.paragraph.verses.push(verse)
                        },  (error) => { console.log(error) });

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