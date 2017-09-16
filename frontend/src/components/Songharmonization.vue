<template>
    <div>
        <div v-if="loaded" v-for="(paragraph, index) in song.paragraphs">
            <div v-for="(verse, vindex) in paragraph.verses">
                <p>
                    <form v-for="(l, i) in verse.content" v-if="isEnabled(paragraph.id, verse.id, i)">
                        <select v-model="harmonization">
                            <option v-for="chord in chords" :value="chord.id">{{ chord.note }}</option>
                        </select>
                        <button class="ui primary button" @click.prevent="save()">{{ t('Save') }}</button><button class="ui button" @click.prevent="cancel()">{{ t('Cancel') }}</button>
                    </form>
                </p>
                <p v-if="isHarmonized(verse.id)">
                    <p  v-html="printHarmonization(index, vindex, verse.id)"></p>
                </p>
                <p>
                    <span v-for="(l, i) in verse.content" @click.prevent="addHarmonization(paragraph.id, verse.id, i)"><b v-if="isEnabled(paragraph.id, verse.id, i) || isHarmonizedLetter(verse.id, i) !== false">{{ l }}</b><span v-else>{{ l }}</span></span>
                </p>
            </div>
            <p>~~~</p>
        </div>
        <div v-else>
            Loading...
        </div>
    </div>
</template>

<script>

    function getSelectedText() {
        var text = "";
        if (typeof window.getSelection != "undefined") {
            text = window.getSelection().toString();
        } else if (typeof document.selection != "undefined" && document.selection.type == "Text") {
            text = document.selection.createRange().text;
        }
        return text;
    }
    
    function doSomethingWithSelectedText() {
        var selectedText = getSelectedText();
        if (selectedText) {
            console.log("Selected", selectedText)
        }
    }
    
    document.onmouseup = doSomethingWithSelectedText;
    document.onkeyup = doSomethingWithSelectedText;


    import axios from 'axios'
    import {root_url} from '@/common/index.js'

    export default {
        props:{
            song: Object
        },
        data(){
            return {
                chords: Array,
                loaded: false,
                p_id_enabled: -1,
                v_id_enabled: -1,
                l_id_enabled: -1,
                harmonization: -1,
                harmonizations: Array
            }
        },
        created(){
            axios.get(root_url + "chords/list/")
                .then(response => {
                    console.log("Received chords", response.data)
                    this.$data.chords = response.data;
                })
            axios.get(root_url + "harmonization/list/song/" + this.song.id + "/")
                .then(response => {
                    console.log("Received harmonizations", response.data)
                    for (var i = 0; i < response.data.length; i++) {
                        if( this.$data.harmonizations[response.data[i].verse] )
                            this.$data.harmonizations[response.data[i].verse].push(response.data[i])
                        else
                            this.$data.harmonizations[response.data[i].verse] = [response.data[i]]
                    }
                    this.loaded = true
                })
        },
        methods:{
            isEnabled(p_id, v_id, l_id){
                return (this.$data.p_id_enabled == p_id 
                    && this.$data.v_id_enabled == v_id 
                    && this.$data.l_id_enabled == l_id)
            },

            isUnderlined(p_id, v_id, l_id){
                return this.isEnabled(p_id, v_id, l_id) ? "underlined" : ""
            },

            isHarmonized(v_id){
                if(this.$data.harmonizations[v_id]){
                    return true
                }
                else
                    return false
            },

            isHarmonizedLetter(v_id, i){
                if(this.$data.harmonizations[v_id]){
                    for (var j = 0; j < this.$data.harmonizations[v_id].length; j++) {
                        if( this.$data.harmonizations[v_id][j].spot_in_verse == i ){
                            return j
                        }
                    }
                    return false
                }
                else
                    return false
            },

            printHarmonization(p_index, v_index, v_id){
                if(this.isHarmonized(v_id)){
                    let output = ""
                    for (var i = 0; i < this.song.paragraphs[p_index].verses[v_index].content.length; i++) {
                        let v_id = this.song.paragraphs[p_index].verses[v_index].id
                        let found = false
                        for (var j = 0; j < this.$data.harmonizations[v_id].length; j++) {
                            if( this.$data.harmonizations[v_id][j].spot_in_verse == i ){
                                output += this.$data.harmonizations[v_id][j].chord.note
                                found = true
                                break
                            }
                        }
                        if(!found){
                            output += "<span style='color:white'>" + this.song.paragraphs[p_index].verses[v_index].content[i] + "</span>"
                        }
                    }
                    return output
                }
            },

            addHarmonization(p_id, v_id, l_id){
                this.$data.p_id_enabled = p_id
                this.$data.v_id_enabled = v_id
                this.$data.l_id_enabled = l_id
                this.$data.harmonization = -1
                let harmonized = this.isHarmonizedLetter(this.$data.v_id_enabled, this.$data.l_id_enabled)
                if( harmonized !== false ){
                    this.$data.harmonization = this.$data.harmonizations[v_id][harmonized].chord.id
                }
            },

            getCorrespondingChord(chord_id){
                for (var i = 0; i < this.$data.chords.length; i++) {
                    if( this.$data.chords[i].id == chord_id ){
                        return this.$data.chords[i]
                    }
                }
            },

            save(){
                let harmonized = this.isHarmonizedLetter(this.$data.v_id_enabled, this.$data.l_id_enabled)

                if( harmonized !== false ){
                    let harmonization = this.$data.harmonizations[this.$data.v_id_enabled][harmonized]
                    harmonization.chord = this.$data.harmonization
                    axios.put(root_url + "harmonization/" + harmonization.id + "/", harmonization)
                        .then(response => {
                            this.$data.harmonizations[this.$data.v_id_enabled][harmonized].chord = this.getCorrespondingChord(harmonization.chord) 
                            this.cancel()
                        }, error => {console.log(error)})
                }else{
                    let harmonization = {
                        verse: this.$data.v_id_enabled,
                        chord: this.$data.harmonization,
                        spot_in_verse: this.$data.l_id_enabled
                    }

                    axios.post(root_url + "harmonization/list/", harmonization)
                        .then(response => {
                            harmonization.chord = this.getCorrespondingChord(harmonization.chord)

                            if( this.$data.harmonizations[harmonization.verse] )
                                this.$data.harmonizations[harmonization.verse].push(harmonization)
                            else
                                this.$data.harmonizations[harmonization.verse] = [harmonization]
                            this.cancel()
                        })
                }
            },
            
            cancel(){
                this.$data.p_id_enabled = -1
                this.$data.v_id_enabled = -1
                this.$data.l_id_enabled = -1
                this.$data.harmonization = -1
            }
        }
    }
</script>

<style>
    .underlined {
        color:red;
    }
</style>