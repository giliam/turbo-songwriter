import Vue from 'vue'
import Router from 'vue-router'
import store from '@/store'

Vue.use(Router)

var router = new Router({
    mode:'history',
    routes: [{
        path: '/',
        component: require('@/components/Songslist.vue').default,
        name: 'root',
        auth: true
    },{
        path: '/song/display/:item_id(\\d+)',
        component: require('@/components/Song.vue').default,
        name: 'song_detail',
        auth: true
    },{
        path: '/song/compiled/pdf/:item_id(\\d+)',
        component: require('@/components/Songpdf.vue').default,
        name: 'song_pdf',
        auth: true
    },{
        path: '/song/add/',
        component: require('@/components/Songform.vue').default,
        name: 'song_new',
        auth: true
    },{
        path: '/song/add/with/verses/',
        component: require('@/components/Songaddform.vue').default,
        name: 'song_new_with_verses',
        auth: true
    },{
        path: '/groups/manage/',
        component: require('@/components/Groupsmanagement.vue').default,
        name: 'groups_management',
        auth: true
    },{
        path: '/song/other/lists/',
        component: require('@/components/Otherlists.vue').default,
        name: 'songs_other_lists',
        auth: true
    },{
        path: '/song/list/manage/',
        component: require('@/components/Songsmanagement.vue').default,
        name: 'songs_management',
        auth: true
    },{
        path: '/book/elements/order/',
        component: require('@/components/Orderbook.vue').default,
        name: 'book_order',
        auth: true
    },{
        path: '/song/edit/:item_id(\\d+)',
        component: require('@/components/Songeditform.vue').default,
        name: 'song_edit',
        auth: true
    },{
        path: '/song/force/latex/conversion/:item_id(\\d+)',
        component: require('@/components/Songtexform.vue').default,
        name: 'song_force_conversion',
        auth: true,
        props: { force_conversion: true }
    },{
        path: '/song/edit/latex/:item_id(\\d+)',
        component: require('@/components/Songtexform.vue').default,
        name: 'song_edit_latex',
        auth: true,
        props: { force_conversion: false },
    },{
        path: '/authors/',
        component: require('@/components/Authorlist.vue').default,
        name: 'authors_list',
        auth: true
    },{
        path: '/additional/latexcodes/',
        component: require('@/components/Additionallatexlist.vue').default,
        name: 'additional_latexcode_list',
        auth: true
    },{
        path: '/editors/',
        component: require('@/components/Editorlist.vue').default,
        name: 'editors_list',
        auth: true
    },{
        path: '/themes/',
        component: require('@/components/Themelist.vue').default,
        name: 'themes_list',
        auth: true
    },{
        path: '/chords/',
        component: require('@/components/Chordlist.vue').default,
        name: 'chords_list',
        auth: true
    },{
        path: '/logout/',
        component: require('@/components/Login.vue').default,
        name: 'logout',
        auth: true
    },{
        path: '/login/',
        component: require('@/components/Login.vue').default,
        name: 'login',
        auth: false
    }]
})


router.beforeEach(function (to, from, next) {
    window.scrollTo(0, 0)
    if (!store.getters.has_jwt_token && to.name != "login") {
        // if route requires auth and user isn't authenticated
        store.commit("set_original_target", to.name);
        next('/login')
    } else {
        next()
    }
})

export default router