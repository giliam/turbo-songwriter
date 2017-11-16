<template>
    <div id="app">
        <div class="ui fixed inverted menu">
            <div class="ui container">
                <router-link :to="{name:'root'}" class="header item">
                    <img class="logo" src="./assets/logo.png">
                    Turbo songwriter!
                </router-link>
                <template v-if="has_jwt_token()">
                    <router-link :to="{name:'root'}" class="item">{{ t('Songs') }}</router-link>
                    <router-link :to="{name:'authors_list'}" class="item">{{ t('Authors') }}</router-link>
                    <router-link :to="{name:'editors_list'}" class="item">{{ t('Editors') }}</router-link>
                    <router-link :to="{name:'themes_list'}" class="item">{{ t('Themes') }}</router-link>
                    <router-link :to="{name:'chords_list'}" class="item">{{ t('Chords') }}</router-link>
                    <router-link :to="{name:'latex_homepage'}" class="item">{{ t('LaTeX') }}</router-link>
                    <router-link :to="{name:'secli_homepage'}" class="item">{{ t('SECLI') }}</router-link>
                    <router-link :to="{name:'logout'}" class="item">{{ t('Logout') }}</router-link>
                </template>
                <template v-else>
                    <router-link :to="{name:'login'}" class="item">{{ t('Login') }}</router-link>
                </template>
                <a class="item" :href="print_root_url() + 'admin'">{{ t('Admin') }}</a>>
            </div>
        </div>
        <div class="ui main text container" style="margin-left:auto; margin-right:auto;">
            <router-view></router-view>
        </div>
    </div>
</template>

<script>
    import { mapGetters, mapActions } from 'vuex'
    import {root_url} from '@/common/index.js'

    export default {
        name: 'app',
        mounted(){
            this.$translate.setLang('fr_FR');
        },
        created(){
            if( this.$localstorage.get('token') && this.$localstorage.get('username') ){
                this.check_localstorage()
            }else{
            }
        },
        methods: {
            ...mapGetters([
                'has_jwt_token'
            ]),
            ...mapActions([
                'check_localstorage'
            ]),
            print_root_url(){
                return root_url
            }
        },
    }
</script>

<style>
    /*#app {*/
        /*font-family: 'Avenir', Helvetica, Arial, sans-serif;*/
        /*-webkit-font-smoothing: antialiased;*/
        /*-moz-osx-font-smoothing: grayscale;*/
        /*text-align: center;*/
        /*color: #2c3e50;*/
        /*margin-top: 60px;*/
    /*}*/

    /*h1, h2 {*/
        /*font-weight: normal;*/
    /*}*/

    /*ul {*/
        /*list-style-type: none;*/
        /*padding: 0;*/
    /*}*/

    /*li {*/
        /*margin: 0 10px;*/
    /*}*/

    /*a {*/
        /*color: #42b983;*/
    /*}*/

    fieldset{
        margin-top:1em;
        margin-bottom:1em;
    }
</style>
