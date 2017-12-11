<template>
    <div>
        <template v-if="isHarmonized()">
            <p class="harmonization" v-html="printHarmonization()"></p>
        </template>
        <p :id="'verse_' + verse.id" @mouseup="selectText()" @keyup="selectText()">
            <span v-for="(l, i) in verse.content" @click.prevent="addHarmonization(i, i)" :class="isEnabled(i) || isHarmonizedLetter(i) !== false ? 'underlined' : ''">{{ l }}</span>
        </p>
        <p>
            <form v-if="isEnabledVerse()">
                <select v-model="harmonization" v-focus @keyup.enter.prevent="saveVerseHarmonization()">
                    <option v-for="chord in chords" :value="chord.id">{{ chord.note }}</option>
                </select>
                <button class="ui primary button" @click.prevent="saveVerseHarmonization()">{{ t('Save') }}</button><button class="ui button" @click.prevent="cancelVerseHarmonization()">{{ t('Cancel') }}</button><button class="ui button red" @click.prevent="deleteHarmonization()">{{ t('Delete') }}</button>
            </form>
        </p>
    </div>
</template>

<script>
    import axios from 'axios'
    import {root_url} from '@/common/index.js'    

    export default {
        props:[
            'verse',
            'chords',
            'p_id_enabled',
            'v_id_enabled',
            'harmonizations_given',
        ],
        data() {
            return {
                l_start_id_enabled: -1,
                l_end_id_enabled: -1,
                harmonizations: [],
                harmonization: -1,
                isHarmonizationEnabled: false,
                already_printed: "",
            }
        },
        created(){
            if(this.harmonizations_given){
                for (var i = 0; i < this.harmonizations_given.length; i++) {
                    this.$data.harmonizations[i] = {
                        start_spot_in_verse:  this.harmonizations_given[i].start_spot_in_verse,
                        end_spot_in_verse: this.harmonizations_given[i].end_spot_in_verse,
                        id: this.harmonizations_given[i].id,
                        verse: this.harmonizations_given[i].verse,
                        chord: {
                            id: this.harmonizations_given[i].chord.id,
                            note: this.harmonizations_given[i].chord.note,
                        }
                    }
                }
            }else{
                this.$data.harmonizations = false
            }
        },
        methods: {
            addHarmonization(l_start_id, l_end_id){
                this.$data.l_start_id_enabled = l_start_id
                this.$data.l_end_id_enabled = l_end_id
                this.$data.harmonization = -1
                this.$data.isHarmonizationEnabled = true
                let harmonized = this.isHarmonizedLetter(this.$data.l_start_id_enabled, this.$data.l_end_id_enabled)
                if( harmonized !== false ){
                    this.$data.harmonization = this.$data.harmonizations[harmonized].chord.id
                }
            },
            printHarmonization(){
                console.log("Prints harmonization", this.verse.id)
                let output = ""
                if(this.isHarmonized()){
                    
                    this.$data.already_printed = []

                    for (var i = 0; i < this.verse.content.length; i++) {
                        let v_id = this.verse.id

                        let found = false
                        for (var j = 0; j < this.$data.harmonizations.length; j++) {
                            if( this.$data.harmonizations[j].start_spot_in_verse <= i 
                                && this.$data.harmonizations[j].end_spot_in_verse >= i
                                && this.$data.already_printed.indexOf(j) == -1 ){
                                output += this.$data.harmonizations[j].chord.note
                                this.$data.already_printed.push(j)
                                found = true
                                break
                            }
                        }
                        if(!found){
                            output += "<span style='color:white'>" + this.verse.content[i] + "</span>"
                        }
                    }
                }
                return output
            },
            selectText() {
                let text = "";
                if (typeof window.getSelection != "undefined") {
                    // thanks to https://stackoverflow.com/a/11559168
                    var sel = window.getSelection();
                    var div = document.getElementById("verse_" + this.verse.id);

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

                            this.addHarmonization(starting_point, starting_point+selection.length-1)
                        }
                    }
                } else if (typeof document.selection != "undefined" && document.selection.type == "Text") {
                    text = document.selection.createRange().text;
                }
            },
            isEnabledVerse(){
                return this.$data.isHarmonizationEnabled
            },
            isEnabled(l_id){
                return (this.$data.isHarmonizationEnabled
                    && this.$data.l_start_id_enabled <= l_id
                    && this.$data.l_end_id_enabled >= l_id )
            },

            isUnderlined(l_id){
                return this.isEnabled(l_id) ? "underlined" : ""
            },

            isHarmonized(){
                if(this.$data.harmonizations){
                    return true
                }
                else{
                    console.log("Not harmonized")
                    return false
                }
            },

            isHarmonizedLetter(i, j){
                if(this.$data.harmonizations){
                    for (var j = 0; j < this.$data.harmonizations.length; j++) {
                        if( this.$data.harmonizations[j].start_spot_in_verse <= i 
                            && this.$data.harmonizations[j].end_spot_in_verse >= i ){
                            return j
                        }
                    }
                    return false
                }
                else
                    return false
            },
            getCorrespondingChord(chord_id){
                for (var i = 0; i < this.chords.length; i++) {
                    if( this.chords[i].id == chord_id ){
                        return this.chords[i]
                    }
                }
            },
            saveVerseHarmonization(){
                let harmonized = this.isHarmonizedLetter(this.$data.l_start_id_enabled, this.$data.l_end_id_enabled)

                if( harmonized !== false ){
                    let harmonization = this.$data.harmonizations[harmonized]
                    harmonization.chord = this.$data.harmonization
                    axios.put(root_url + "harmonization/" + harmonization.id + "/", harmonization)
                        .then(response => {
                            this.$data.harmonizations[harmonized].chord = this.getCorrespondingChord(harmonization.chord) 
                            this.cancelVerseHarmonization()
                        }, error => {console.log(error)})
                }else{
                    let harmonization = {
                        verse: this.verse.id,
                        chord: this.$data.harmonization,
                        start_spot_in_verse: this.$data.l_start_id_enabled,
                        end_spot_in_verse: this.$data.l_end_id_enabled
                    }

                    axios.post(root_url + "harmonization/list/", harmonization)
                        .then(response => {
                            harmonization.chord = this.getCorrespondingChord(harmonization.chord)

                            if( this.$data.harmonizations )
                                this.$data.harmonizations.push(harmonization)
                            else
                                this.$data.harmonizations = [harmonization]
                            this.cancelVerseHarmonization()
                        })
                }
            },
            cancelVerseHarmonization(){
                this.$data.l_start_id_enabled = -1
                this.$data.l_end_id_enabled = -1
                this.$data.harmonization = -1
                this.$data.isHarmonizationEnabled = false
            },

            deleteHarmonization(){
                let harmonized = this.isHarmonizedLetter(this.$data.l_start_id_enabled, this.$data.l_end_id_enabled)

                if( harmonized !== false ){
                    let harmonization = this.$data.harmonizations[harmonized]
                    axios.delete(root_url + "harmonization/" + harmonization.id + "/")
                        .then(response => {
                            this.$data.harmonizations.splice(harmonized, 1)
                            this.cancelVerseHarmonization()
                        }, error => {console.log(error)})
                }
            },
        }
    }
</script>