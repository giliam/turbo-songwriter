import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
    mode:'history',
    routes: [{
        path: '/',
        component: require('@/components/Songslist.vue').default,
        name: 'root'
    },{
        path: '/song/display/:item_id(\\d+)',
        component: require('@/components/Song.vue').default,
        name: 'song_detail'
    },{
        path: '/song/add/',
        component: require('@/components/Songform.vue').default,
        name: 'song_new'
    },{
        path: '/song/edit/:item_id(\\d+)',
        component: require('@/components/Songeditform.vue').default,
        name: 'song_edit'
    },{
        path: '/song/force/latex/conversion/:item_id(\\d+)',
        component: require('@/components/Songtexform.vue').default,
        name: 'song_force_conversion',
        props: { force_conversion: true }
    },{
        path: '/song/edit/latex/:item_id(\\d+)',
        component: require('@/components/Songtexform.vue').default,
        name: 'song_edit_latex',
        props: { force_conversion: false }
    },{
        path: '/authors/',
        component: require('@/components/Authorlist.vue').default,
        name: 'authors_list'
    },{
        path: '/editors/',
        component: require('@/components/Editorlist.vue').default,
        name: 'editors_list'
    },{
        path: '/themes/',
        component: require('@/components/Themelist.vue').default,
        name: 'themes_list'
    },{
        path: '/chords/',
        component: require('@/components/Chordlist.vue').default,
        name: 'chords_list'
    },]
})
