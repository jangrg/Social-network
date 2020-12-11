<template>
  <div class="d-flex flex-column font-theme">
    <TopBar />
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
    beforeDestroyed: function () {
      document
        .getElementById(`button-explore`)
        .classList.toggle("explore-clicked");
    },
  },
};
</script>

<style></style>
