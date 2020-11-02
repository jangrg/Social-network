<template>
  <div class="d-flex flex-column bg-pattern">
    <TopBar />
    <SideBar />

    <div class="container-fluid row  mx-auto">
      <div class="col-md-2"></div>
      <div class="col-md-8 white-container rounded">
        <h3>New posts today:</h3>

      <!-- <div v-for="post in posts" :key="post.id"> -->
        <Post />
      <!-- </div> -->
      </div>
      
      <div class="col-md-2"></div>
    </div>
  </div>
</template>

<script>
import { ButtonPlugin } from "bootstrap-vue";

import TopBar from "../../components/TopBar";

import SideBar from "../../components/SideBar";

import Post from "../../components/Post";

export default {
  name: "Home",
  components: { TopBar, SideBar, Post },
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
      postList: "" //Will require to give posts here. Probably a JSON list, needs to be fetched from server in mounted function
    }
  },
  mounted: function() {
      // postList = await this.$axios.post(`account/posts/`);
  },
  computed: {
    user() {
      return this.$store.state.User.user;
    }
  },
};
</script>

<style>
</style>
