<template>
    <div>
        <button class="green ui button" @click="synchronize()">{{ t('Update the page') }}</button>
        
        <div v-if="loaded" v-for="(paragraph, index) in song.paragraphs">
            <div v-for="(verse, vindex) in paragraph.verses">
                <p>
                    <form v-if="isEnabledVerse(paragraph.id, verse.id)">
                        <select v-model="harmonization" v-focus>
                            <option v-for="chord in chords" :value="chord.id">{{ chord.note }}</option>
                        </select>
                        <button class="ui primary button" @click.prevent="save()">{{ t('Save') }}</button><button class="ui button" @click.prevent="cancel()">{{ t('Cancel') }}</button><button class="ui button red" @click.prevent="deleteHarmonization()">{{ t('Delete') }}</button>
                    </form>
                </p>
                <template v-if="isHarmonized(verse.id)">
                    <p class="harmonization" v-html="printHarmonization(index, vindex, verse.id)"></p>
                </template>
                <p :id="'verse_' + verse.id" @mouseup="selectText(paragraph.id, verse.id, 'verse_' + verse.id)" @keyup="selectText(paragraph.id, verse.id, 'verse_' + verse.id)">
                    <span v-for="(l, i) in verse.content" @click.prevent="addHarmonization(paragraph.id, verse.id, i, i)" :class="isEnabled(paragraph.id, verse.id, i) || isHarmonizedLetter(verse.id, i) !== false ? 'underlined' : ''">{{ l }}</span>
                </p>
            </div>
            <p>~~~</p>
        </div>

        <div v-if="!loaded">
            <p style="margin:25px"><i class="spinner loading icon"></i></p>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'
    import {root_url} from '@/common/index.js'

    export default {
        props:{
            song: Object
        },
        data(){
            return {
                chords: [],
                loaded: false,
                p_id_enabled: -1,
                v_id_enabled: -1,
                l_start_id_enabled: -1,
                l_end_id_enabled: -1,
                harmonization: -1,
                harmonizations: [],
                already_printed: [],
            }
        },
        created(){
            this.synchronize()
        },
        methods:{
            synchronize(){
                this.$data.harmonizations = []
                this.loaded = false
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
            getSelectedText() {
                let text = "";
                if (typeof window.getSelection != "undefined") {
                    text = window.getSelection().toString();
                } else if (typeof document.selection != "undefined" && document.selection.type == "Text") {
                    text = document.selection.createRange().text;
                }
                return text;
            },
            selectText(p_id, v_id, verse_id) {
                let text = "";
                if (typeof window.getSelection != "undefined") {
                    // thanks to https://stackoverflow.com/a/11559168
                    var sel = window.getSelection();
                    var div = document.getElementById(verse_id);

                    if (sel.rangeCount) {
                        // Get the selected range
                        var range = sel.getRangeAt(0);

                        // Check that the selection is wholly contained within the div text
                        if (range.commonAncestorContainer == div) {
                            // Create a range that spans the content from the start of the div
                            // to the start of the selection
                            var precedingRange = document.createRange();
                            precedingRange.setStartBefore(div.firstChild);
                            precedingRange.setEnd(range.startContainer, range.startOffset);

                            // Get the text preceding the selection and do a crude estimate
                            // of the number of words by splitting on white space
                            var textPrecedingSelection = precedingRange.toString();
                            let cut_text = div.textContent.substring(textPrecedingSelection.length)
                            let selection = sel.toString()
                            
                            let starting_point = textPrecedingSelection.length
                            for (var i = 0; i < cut_text.length; i++) {
                                if( cut_text[i] == selection[0] ) {
                                    cut_text = cut_text.substring(i, i+selection.length)
                                    starting_point += i
                                    break
                                }
                            }

                            this.addHarmonization(p_id, v_id, starting_point, starting_point+selection.length-1)
                        }
                    }
                } else if (typeof document.selection != "undefined" && document.selection.type == "Text") {
                    text = document.selection.createRange().text;
                }
            },
            isEnabledVerse(p_id, v_id){
                return (this.$data.p_id_enabled == p_id 
                    && this.$data.v_id_enabled == v_id)
            },
            isEnabled(p_id, v_id, l_id){
                return (this.$data.p_id_enabled == p_id 
                    && this.$data.v_id_enabled == v_id 
                    && this.$data.l_start_id_enabled <= l_id
                    && this.$data.l_end_id_enabled >= l_id )
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

            isHarmonizedLetter(v_id, i, j){
                if(this.$data.harmonizations[v_id]){
                    for (var j = 0; j < this.$data.harmonizations[v_id].length; j++) {
                        if( this.$data.harmonizations[v_id][j].start_spot_in_verse <= i 
                            && this.$data.harmonizations[v_id][j].end_spot_in_verse >= i ){
                            return j
                        }
                    }
                    return false
                }
                else
                    return false
            },

            printHarmonization(p_index, v_index, v_id){
                let output = ""
                if(this.isHarmonized(v_id)){
                    
                    this.$data.already_printed[v_id] = []

                    for (var i = 0; i < this.song.paragraphs[p_index].verses[v_index].content.length; i++) {
                        let v_id = this.song.paragraphs[p_index].verses[v_index].id

                        let found = false
                        for (var j = 0; j < this.$data.harmonizations[v_id].length; j++) {
                            if( this.$data.harmonizations[v_id][j].start_spot_in_verse <= i 
                                && this.$data.harmonizations[v_id][j].end_spot_in_verse >= i
                                && this.$data.already_printed[v_id].indexOf(j) == -1 ){
                                output += this.$data.harmonizations[v_id][j].chord.note
                                this.$data.already_printed[v_id].push(j)
                                found = true
                                break
                            }
                        }
                        if(!found){
                            output += "<span style='color:white'>" + this.song.paragraphs[p_index].verses[v_index].content[i] + "</span>"
                        }
                    }
                }
                return output
            },

            addHarmonization(p_id, v_id, l_start_id, l_end_id){
                this.$data.p_id_enabled = p_id
                this.$data.v_id_enabled = v_id
                this.$data.l_start_id_enabled = l_start_id
                this.$data.l_end_id_enabled = l_end_id
                this.$data.harmonization = -1
                let harmonized = this.isHarmonizedLetter(this.$data.v_id_enabled, this.$data.l_start_id_enabled, this.$data.l_end_id_enabled)
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
                let harmonized = this.isHarmonizedLetter(this.$data.v_id_enabled, this.$data.l_start_id_enabled, this.$data.l_end_id_enabled)

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
                        start_spot_in_verse: this.$data.l_start_id_enabled,
                        end_spot_in_verse: this.$data.l_end_id_enabled
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
                this.$data.l_start_id_enabled = -1
                this.$data.l_end_id_enabled = -1
                this.$data.harmonization = -1
            },
            
            deleteHarmonization(){
                let harmonized = this.isHarmonizedLetter(this.$data.v_id_enabled, this.$data.l_start_id_enabled, this.$data.l_end_id_enabled)

                if( harmonized !== false ){
                    let harmonization = this.$data.harmonizations[this.$data.v_id_enabled][harmonized]
                    axios.delete(root_url + "harmonization/" + harmonization.id + "/")
                        .then(response => {
                            this.$data.harmonizations[this.$data.v_id_enabled].splice(harmonized, 1)
                            this.cancel()
                            this.synchronize()
                        }, error => {console.log(error)})
                }
            },
        }
    }
</script>

<style>
    .underlined{
        text-decoration: underline;
    }
    .harmonization {
        font-size: 0.95em;
    }
</style>