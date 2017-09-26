<template>
    <div>
        <div id="listadditionallatexcode">
            <div v-if="!is_updating">
                <template v-if="is_editing">
                    <form class="ui form">
                        <fieldset>
                            <legend>{{ t('Edit an additional LaTeX code') }}</legend>
                            <p class="field">
                                <label for="name">{{ t('Identifier:') }} </label>
                                <input type="text" name="name" v-model="name" v-focus>
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
        		    <button @click="synchronize()" class="ui button primary">{{ t('Update the list') }}</button>
    	            <div class="ui list large">
                        <div v-for="item in additional_latexcodes" class="item" @click="editAdditionalLaTeXCode(item)">
                            <i class="icon code"></i>
                            {{ item.name }}
                        </div>
                    </div>
                    <div>
                        <p><button class="ui button green" @click.prevent="addAdditionalCode()">{{ t('Add an additional LaTeX code') }}</button></p>
                        <form v-if="is_adding" class="ui form">
                            <fieldset>
                                <legend>{{ t('Add an additional LaTeX code') }}</legend>
                                <p class="field">
                                    <label for="name">{{ t('Identifier:') }} </label>
                                    <input type="text" name="name" v-model="name" v-focus>
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
                    <p>
                        <div class="ui vertical buttons" v-if="!is_adding">
                            <button class="ui button purple" @click.prevent="getWholeTexCode()">{{ t('Get whole LaTeX code') }}</button>
                            <template v-if="url_whole_code">
                                <a class="ui button black" :href="url_whole_code" target="_blank">{{ t('Link to pdf') }}</a>
                            </template>
                        </div>
                    </p>
                </template>
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
                url_whole_code: null,
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
                this.$data.is_editing = false
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
                this.$data.is_adding = false
            },

            getWholeTexCode(){
                axios.get(root_url + "get/whole/tex/")
                    .then(response => {
                        this.$data.url_whole_code = root_url + response.data.url
                    },  (error) => { console.log(error) });
            }
        }
    }
</script>