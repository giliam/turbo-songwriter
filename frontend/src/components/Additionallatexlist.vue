<template>
    <div>
        <div id="listadditionallatexcode">
            <div v-if="!is_updating">
                <template v-if="is_editing">
                    <form class="ui form">
                        <fieldset>
                            <legend>{{ t('Edit an additional LaTeX code') }}</legend>
                            <p class="field">
                                <label for="name">{{ t('Name:') }} </label>
                                <input type="text" name="name" v-model="name">
                            </p>
                            <p class="field">
                                <label for="code">{{ t('Code:') }} </label>
                                <textarea name="code" v-model="code"></textarea>
                            </p>
                            <p class="field">
                                <button class="ui button primary" @click.prevent="saveAdditionalLaTeXCode(true)">{{ t('Save') }}</button>
                                <button class="ui button" @click.prevent="hideAdditionalCodeForm()">{{ t('Cancel') }}</button>
                            </p>
                        </fieldset>
                    </form>
                </template>
                <template v-else>
        		    <h2>{{ t('List of additional LaTeX codes') }}</h2>
        		    <p @click="synchronize()">{{ t('Update the list') }}</p>
    	            <ul>
            			<li v-for="item in additional_latexcodes">
                            <p @click="editAdditionalLaTeXCode(item)">{{ item.name }}</p>
                        </li>
                    </ul>
                </template>
                <div>
                    <p><a @click.prevent="addAdditionalCode()">{{ t('Add an additional LaTeX code') }}</a></p>
                    <form v-if="is_adding" class="ui form">
                        <fieldset>
                            <legend>{{ t('Add an additional LaTeX code') }}</legend>
                            <p class="field">
                                <label for="name">{{ t('Name:') }} </label>
                                <input type="text" name="name" v-model="name">
                            </p>
                            <p class="field">
                                <label for="code">{{ t('Code:') }} </label>
                                <textarea name="code" v-model="code"></textarea>
                            </p>
                            <p class="field">
                                <button class="ui button primary" @click.prevent="saveAdditionalLaTeXCode(false)">{{ t('Save') }}</button>
                                <button class="ui button" @click.prevent="hideAdditionalCodeForm()">{{ t('Cancel') }}</button>
                            </p>
                        </fieldset>
                    </form>
                </div>
            </div>
            <div v-else>
                {{ t('Updating...') }}
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'
    import {root_url} from '@/common/index.js'

    export default {
        data() {
            return {
                additional_latexcodes: Array,
                additional_code_id: -1,
                is_adding: false,
                is_updating: false,
                is_editing: false,
                name: "",
                code: "",
            }
        },
        components: {
        },
        created() {
            axios.get(root_url + "additional/latexcode/list/")
                .then(response => {
                    this.$data.additional_latexcodes = response.data;
                },  (error) => { console.log(error) });
        },
        methods:{
            addAdditionalCode() {
                this.$data.is_adding = !this.$data.is_adding
                this.$data.name = ""
                this.$data.code = ""
            },
            hideAdditionalCodeForm() {
                axios.get(root_url + "additional/latexcode/list/")
                    .then(response => {
                        this.$data.additional_latexcodes = response.data;
                    },  (error) => { console.log(error) });
                this.$data.is_adding = false
                this.$data.is_editing = false
            },
            synchronize(){
                this.$data.is_updating = true
                axios.get(root_url + "additional/latexcode/list/")
                    .then(response => {
                        this.$data.additional_latexcodes = response.data;
                        this.$data.is_updating = false
                    },  (error) => { console.log(error) });
            },
            saveAdditionalLaTeXCode(is_editing) {
                let additional_code = {
                    name: this.$data.name,
                    code: this.$data.code,
                };
                this.$data.is_updating = true
                if( is_editing ) {
                    axios.put(root_url + "additional/latexcode/" + this.$data.additional_code_id + "/", additional_code)
                        .then(response => {
                            axios.get(root_url + "additional/latexcode/list/")
                                .then(response => {
                                    this.$data.additional_latexcodes = response.data;
                                    this.$data.is_updating = false
                                },  (error) => { console.log(error) });
                        }, (error) => { console.log(error)});
                } else {
                    axios.post(root_url + "additional/latexcode/list/", additional_code)
                        .then(response => {
                            axios.get(root_url + "additional/latexcode/list/")
                                .then(response => {
                                    this.$data.additional_latexcodes = response.data;
                                    this.$data.is_updating = false
                                },  (error) => { console.log(error) });
                        }, (error) => { console.log(error)});
                }
                this.$data.is_adding = false
                this.$data.is_editing = false
                this.$data.additional_code_id = -1
            },

            editAdditionalLaTeXCode(additional_code){
                this.$data.name = additional_code.name
                this.$data.code = additional_code.code
                this.$data.additional_code_id = additional_code.id
                this.$data.is_editing = true
            }
        }
    }
</script>