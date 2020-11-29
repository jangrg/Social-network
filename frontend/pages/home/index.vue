<template>
  <div class="d-flex flex-column font-theme">
    <TopBar @post="setPost" />
    <div class="container-fluid row mx-auto">
      <div class="col-md-2"></div>
      <div class="col-md-8 no-border">
        <div class="text-center">
          <h3>📣</h3>
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

import SideBar from "@/components/SideBar";

import Post from "@/components/Post";

import Footer from "@/components/Footer";

export default {
  name: "Home",
  components: { TopBar, SideBar, Post, Footer },
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
    let response = await this.$axios.get(`post/`);

    this.posts = response.data.reverse();
  },
  computed: {
    user() {
      return this.$auth.user;
    },
    fullPage() {
      return document.height() <= window.height();
    },
  },
};
</script>

<style></style>
