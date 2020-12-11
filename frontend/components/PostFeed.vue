<template>
  <div class="col-md-8 no-border my-3">
    <div class="text-center">
      <div v-if="anotherUser" class="container-fluid new-post">
        <PostForm @post="setPost" />
      </div>
    </div>
    <div v-for="post in posts" :key="post.id">
      <Post :post="post" @PostDelete="deletePost" />
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
    filter: String,
  },
  data() {
    return {
      posts: [],
    };
  },
  methods: {
    setPost(parameters) {
      this.posts.unshift(parameters);
    },
    deletePost(parameters) {
      debugger;
      for (var i = 0; i < this.posts.length; i++) {
        if (this.posts[i].id == parameters) {
          this.posts.splice(i, 1);
          break;
        }
      }
    },
  },
  computed: {
    anotherUser() {
      debugger;
      if (this.$nuxt.$route.name == "users-id") {
        return this.$nuxt.$route.params.id === this.$auth.user.id;
      }
      return true;
    },
  },
  created: async function () {
    let response = await this.$axios.get(`post/${this.filter}`);
    this.posts = response.data;
    console.log(this.posts);
    document
      .getElementById(`button-explore`)
      .classList.toggle("explore-clicked");
  },
};
</script>

<style>
</style>