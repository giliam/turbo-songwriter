import Vue from 'vue'
import Vuex from 'vuex'

import axios from 'axios'

import {root_url} from '@/common/index.js'
import router from '@/router'

function parseJwt(token) {
    let base64Url = token.split('.')[1];
    let base64 = base64Url.replace('-', '+').replace('_', '/');
    return JSON.parse(window.atob(base64));
}

export default new Vuex.Store({
    state: {
      authorized: false
    },
    mutations: {
        set_authorized(state, value) {
            state.authorized = value
        }
    },
    getters: {
        has_jwt_token: state => {
            return state.authorized
        }
    },
    actions: {
        check_localstorage(context) {
            let data = {
                token: this._vm.$localstorage.get('token')
            }

            // gets token expiration date and current date
            let expiration_date = parseJwt(data.token).exp
            let current = Math.floor(Date.now() / 1000)

            // if token is expiring in less than 5 minutes, ask for a refresh 
            if( expiration_date > current && expiration_date - current < 300 ){
                console.log("ASKS for refresh")
                axios.post(root_url + "token-refresh/", data)
                    .then(response => {
                        context.commit("set_authorized", true);
                        axios.defaults.headers.common['Authorization'] = "JWT " + response.data.token;
                        this._vm.$localstorage.set('token', response.data.token)
                        
                        // redirects to main page
                        router.push({name:"root"})
                    },  (error) => {
                        // logs out
                        console.log(error)
                        context.dispatch('log_out')
                });
            // else checks validity
            }else{
                console.log("ASKS for verify")
                axios.post(root_url + "token-verify/", data)
                    .then(response => {
                        context.commit("set_authorized", true);
                        this._vm.$localstorage.set('token', response.data.token)
                        axios.defaults.headers.common['Authorization'] = "JWT " + this._vm.$localstorage.get('token');
                        
                        // redirects to main page
                        router.push({name:"root"})
                    },  (error) => {
                        // logs out
                        console.log(error)
                        context.dispatch('log_out')
                });
            }
        },
        
        async log_in(context, user) {
            let data = {
                username: user.username,
                password: user.password
            }
            await axios.post(root_url + "auth/login/", data)
                .then(response => {
                    // if connection succeeded, adds token
                    context.commit("set_authorized", true);
                    axios.defaults.headers.common['Authorization'] = "JWT " + response.data.token;
                    this._vm.$localstorage.set('token', response.data.token)
                    this._vm.$localstorage.set('username', data.username)
                },  (error) => {
                    console.log(error)
             });
            return context.getters.has_jwt_token
        },

        log_out(context) {
            context.commit("set_authorized", false);
            this._vm.$localstorage.remove('token')
            this._vm.$localstorage.remove('username')
            axios.defaults.headers.common['Authorization'] = "";
        }
    }
})