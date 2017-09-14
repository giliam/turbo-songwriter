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
        check_session(context, userdata) {
            let data = {
                username: userdata.username,
                token: userdata.token
            }
            // TODO: check token validity
            context.commit("set_jwt_token", userdata.token);
            context.commit("set_authorized", true);
            axios.defaults.headers.common['Authorization'] = "JWT " + userdata.token;
        },
        async log_in(context, user) {
            let data = {
                username: user.username,
                password: user.password
            }
            await axios.post(root_url + "auth/login/", data)
                .then(response => {
                    context.commit("set_jwt_token", response.data.token);
                    context.commit("set_authorized", true);
                    axios.defaults.headers.common['Authorization'] = "JWT " + response.data.token;
                    this._vm.$session.start()
                    this._vm.$session.set('token', response.data.token)
                    this._vm.$session.set('username', data.username)
                },  (error) => {
                    console.log(error)
             });
            return context.getters.has_jwt_token
        },
        log_out(context) {
            context.commit("set_jwt_token", null)
            context.commit("set_authorized", false);
            this._vm.$session.destroy()
            axios.defaults.headers.common['Authorization'] = "";
        }
    }
})