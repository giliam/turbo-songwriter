<template>
    <div>
        <div v-for="(paragraph, index) in song.paragraphs">
            <div v-for="(verse, vindex) in paragraph.verses">
                <p>
                    <form v-for="(l, i) in verse.content" v-if="isEnabled(paragraph.id, verse.id, i)">
                        <select v-model="harmonization">
                            <option v-for="chord in chords" :value="chord.id">{{ chord.note }}</option>
                        </select>
                        <button @click.prevent="save()">Save</button><button @click.prevent="cancel()">Cancel</button>
                    </form>
                </p>
                <p>
                    <span v-for="(l, i) in verse.content" @click.prevent="addHarmonization(paragraph.id, verse.id, i)"><b v-if="isEnabled(paragraph.id, verse.id, i)">{{ l }}</b><span v-else>{{ l }}</span></span>
                </p>
            </div>
            <p>~~~</p>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'

    export default {
        props:{
            song: Object
        },
        data(){
            return {
                chords: Array,
                p_id_enabled: -1,
                v_id_enabled: -1,
                l_id_enabled: -1,
                harmonization: -1
            }
        },
        mounted(){
            axios.get("http://localhost:8000/chords/list/")
                .then(response => {
                    console.log("Received", response.data)
                    this.$data.chords = response.data;
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
            addHarmonization(p_id, v_id, l_id){
                this.$data.p_id_enabled = p_id
                this.$data.v_id_enabled = v_id
                this.$data.l_id_enabled = l_id
                this.$data.harmonization = -1
            },
            save(){
                // If harmonization exists TODO
                if( false ){

                }else{
                    let harmonization = {
                        verse: this.$data.v_id_enabled,
                        chord: this.$data.harmonization,
                        spot_in_verse: this.$data.l_id_enabled
                    }

                    // axios.post("http://localhost:8000/harmonization/list/", harmonization)
                    //     .then(response => {
                    //         console.log("Saved!", response.data)
                    //     })
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