<template>
  <div class="d-flex flex-column font-theme">
    <TopBar @post="setPost" />
    <div class="container-fluid row mx-auto">
      <div class="col-md-2"></div>
      <PostFeed :filter="''" />

      <div class="col-md-2"></div>
    </div>
  </div>
</template>

<script>
import { ButtonPlugin } from "bootstrap-vue";

import TopBar from "@/components/TopBar";

import Footer from "@/components/Footer";

import PostFeed from "@/components/PostFeed"

export default {
  name: "Home",
  components: { TopBar, Footer, PostFeed },
  middleware: ["auth-notLoggedIn"],
  head() {
    return {
      title: "Home",
      meta: [
        {
          name: "viewport",
          content: "width=device-width, initial-scale=1, shrink-to-fit=no",
        },
      ],
      bodyAttrs: {
        class: "body-theme",
      },
    };
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
  },
  created: async function () {
    let response = await this.$axios.get(`post/followed_posts/`);
    // followed_posts/
    this.posts = response.data;
    console.log(this.posts);
    document.getElementById(`button-home`).classList.toggle("home-clicked");
  },
  beforeDestroyed: function () {
    document.getElementById(`button-home`).classList.toggle("home-clicked");
  },
};
</script>

<style></style>
