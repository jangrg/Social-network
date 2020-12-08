<template>
  <div class="d-flex flex-column font-theme">
    <TopBar />
    <div class="container-fluid row mx-auto">
      <div class="col-md-2"></div>
      <div class="col-md-8 no-border">
        <div class="text-center">
          <div class="container-fluid new-post">
            <PostForm @post="setPost" />
          </div>
        </div>
        <div v-for="post in posts" :key="post.id">
          <Post :post="post" />
        </div>

        <div class="col-md-2"></div>
      </div>
    </div>
  </div>
</template>

<script>
import { ButtonPlugin } from "bootstrap-vue";

import TopBar from "@/components/TopBar";

import Post from "@/components/Post";

import Footer from "@/components/Footer";

import PostForm from "@/components/PostForm";

export default {
  name: "Home",
  components: { TopBar, Post, Footer, PostForm },
  middleware: ["auth-notLoggedIn"],
  head() {
    return {
      title: "Home",
      meta: [
        {
          name: "viewport",
          content: "width=device-width, initial-scale=1, shrink-to-fit=no"
        }
      ],
      bodyAttrs: {
        class: "body-theme"
      }
    };
  },
  data() {
    return {
      posts: []
    };
  },
  methods: {
    setPost(parameters) {
      this.posts.unshift(parameters);
    }
  },
  created: async function() {
    let response = await this.$axios.get(`post/`);
    this.posts = response.data;
    console.log(this.posts);
    document
      .getElementById(`button-explore`)
      .classList.toggle("explore-clicked");
  },
  beforeDestroyed: function() {
    document
      .getElementById(`button-explore`)
      .classList.toggle("explore-clicked");
  }
};
</script>

<style></style>
