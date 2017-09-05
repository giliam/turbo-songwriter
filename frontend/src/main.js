import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const router = new VueRouter({
    mode:'history',
    routes: [{
        path: '/',
        component: require('./Songslist.vue'),
        name: 'root'
    },{
        path: '/song/display/:item_id(\\d+)',
        component: require('./Song.vue'),
        name: 'song_detail'
    },{
        path: '/song/add/',
        component: require('./Songform.vue'),
        name: 'song_new'
    },{
        path: '/song/edit/:item_id(\\d+)',
        component: require('./Songeditform.vue'),
        name: 'song_edit'
    },{
        path: '/authors/',
        component: require('./Authorlist.vue'),
        name: 'authors_list'
    },{
        path: '/editors/',
        component: require('./Editorlist.vue'),
        name: 'editors_list'
    },{
        path: '/themes/',
        component: require('./Themelist.vue'),
        name: 'themes_list'
    },{
        path: '/chords/',
        component: require('./Chordlist.vue'),
        name: 'chords_list'
    },]
})

new Vue({
  el: '#app',
  router: router,
  render: h => h(require('./App.vue'))
})
