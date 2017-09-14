import Vue from 'vue'
import Vuex from 'vuex'

import axios from 'axios'
import {root_url} from '@/common/index.js'


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
            // TODO: check token validity
            context.commit("set_authorized", true);
            axios.defaults.headers.common['Authorization'] = "JWT " + this._vm.$localstorage.get('token');
        },
        async log_in(context, user) {
            let data = {
                username: user.username,
                password: user.password
            }
            await axios.post(root_url + "auth/login/", data)
                .then(response => {
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