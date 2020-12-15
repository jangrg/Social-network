<template>
  <div class="col-md-8 no-border my-3">
    <div class="text-center">
      <div v-if="anotherUser" class="container-fluid new-post">
        <PostForm @post="setPost" />
      </div>
    </div>
    <div v-for="post in posts" :key="post.id">
      <Post :post="post" @PostDelete="deletePost" @edit="replacePost" />
    </div>
  </div>
</template>

<script>
import PostForm from "@/components/PostForm";
import Post from "@/components/Post";

export default {
  name: "PostFeed",
  components: { Post, PostForm },
  props: {
    filter: String
  },
  data() {
    return {
      posts: [],
      otherStore: true
    };
  },
  async beforeCreate() {
    try {
      let token = this.$auth.getToken("local");
      let response = await this.$axios.get("page/my_page/", {
        headers: { Authorization: `${token}` }
      });
      this.otherStore = this.$nuxt.$route.params.id != response.data.id;
    } catch (e) {}
  },
  methods: {
    setPost(parameters) {
      this.posts.unshift(parameters);
    },
    //very costly, but im bad at programming therefore i dont know of any other way that doesnt mess with props.
    replacePost(editedPost) {
      debugger;
      for (var i = 0; i < this.posts.length; i++) {
        if (editedPost.id == this.posts[i].id) {
          this.posts.splice(i, 1, editedPost);
          break;
        }
      }
    },
    //also very costly, but again bad at programming therefore i dont know of any other way that doesnt mess with props.
    deletePost(parameters) {
      debugger;
      for (var i = 0; i < this.posts.length; i++) {
        if (this.posts[i].id == parameters) {
          this.posts.splice(i, 1);
          break;
        }
      }
    }
  },
  computed: {
    anotherUser() {
      debugger;
      if (this.$nuxt.$route.name == "users-id") {
        return this.$nuxt.$route.params.id === this.$auth.user.id;
      } else if (this.$nuxt.$route.name == "store-id") {
        return !this.otherStore;
      }
      return true;
    }
  },
  created: async function() {
    let response;
    if (this.filter.includes("page")) {
      console.log("tu");
      response = await this.$axios.get(`page/${this.filter}`);
    } else response = await this.$axios.get(`post/${this.filter}`);
    this.posts = response.data;
    console.log(this.posts);
  }
};
</script>

<style></style>
