let songtitle = {
  name: "songtitle",
  props:{
    item: Object
  },
  methods:{
    launch_show_song: function(item) {
      this.$emit("show_song", item.id)
    }
  },
  template: `<p>{{item.title}} - <a @click.prevent="launch_show_song(item)">Show</a></p>`,
}

let songslist = {
  name: "songslist",
  data() {
    return { results: Array }
  },
  components: {
    songtitle
  },
  template: `<div id="listsongs">
        <h2>List of songs</h2>
        <ul>
            <li v-for="item in results"><songtitle @show_song="show_song" :item="item"></songtitle></li>
        </ul>
    </div>`,
  methods: {
    show_song(){
      console.log("Show song")
    }
  },
  created() {
    axios.get(url_songs_list)
    .then(response => {
        this.results = response.data;
    })
  },
}

let song = {
  props: {
    item_id: Number
  },
  data() {
    return {
      result: Object
    }
  },
  template: `<div id="song">
    <h2>{{ result.title }}</h2>
  </div>`,
  created(){
    axios.get(url_song_detail.replace("/0/", "/" + this.$props.item_id + "/"))
    .then(response => {
        this.result = response.data;
    })
  }
}

let songparagraph = {
  props: {
    content: String,
    id: Number
  },
  methods: {
    edit () {
      console.log("Edit", this.$props.id)
    },
  },
  template: `<div>
    <p>{{ content }}</p>
    <button @click.prevent="edit">Edit</button>
  </div>`,
}

var vm = new Vue({
  el: '#app',
  data: {
    results: []
  },
  methods:{
    
  },
  components: { songparagraph, songtitle, songslist }
});