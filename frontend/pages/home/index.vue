<template>
  <div class="d-flex flex-column bg-pattern">
    <TopBar />
    <SideBar @posts = "setPosts"/>

    <div class="container-fluid row mx-auto">
      <div class="col-md-2"></div>
      <div class="col-md-8 white-container rounded">
        <h3>Recent posts:</h3>

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
  middleware: ['auth-notLoggedIn'],
  head() {
    return {
      title: "Home",
      meta: [
        {
          name: "viewport",
          content: "width=device-width, initial-scale=1, shrink-to-fit=no",
        },
      ],
    };
  },
  data() {
    return {
      posts: [],
    };
  },
  methods: {
    setPosts(parameters) {
      this.posts = parameters;
    }
  },
  computed: {
    user() {
      return this.$auth.user;
    },
  },
};
</script>

<style>
</style>
