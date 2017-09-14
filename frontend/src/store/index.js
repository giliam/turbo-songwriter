import Vue from 'vue'
import Vuex from 'vuex'

import axios from 'axios'
import {root_url} from '@/common/index.js'


export default new Vuex.Store({
    state: {
      jwt_token: null,
      authorized: false
    },
    mutations: {
        set_jwt_token(state, value) {
            state.jwt_token = value
        },
        set_authorized(state, value) {
            state.authorized = value
        }
    },
    getters: {
        has_jwt_token: state => {
            return !!state.jwt_token
        }
    },
    actions: {
        log_in(context, user) {
            let data = {
                username: user.username,
                password: user.password
            }
            axios.post(root_url + "auth/login/", data)
                .then(response => {
                    context.commit("set_jwt_token", response.data.token);
                    context.commit("set_authorized", true);
                    return true
                },  (error) => { console.log(error) });
            return false
        },
        log_out(context, username, password) {
            context.commit("set_jwt_token", null)
            context.commit("set_authorized", false);
        }
    }
})