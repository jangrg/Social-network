<template>
  <div
    class="bg"
    :class="{
      'd-flex': !user,
      'flex-column': !user,
      'justify-content-between': !user,
    }"
  >
    <TopBar />
    <div class="mx-auto" v-if="!user">
      <div
        class="lead border rounded mx-auto p-4 white-container justify-content-center"
      >
        <div class="d-flex flex-column container">
          <h1 class="title">Welcome to our Social Network</h1>
          <h2 class="subtitle">Feel free to register now!</h2>
          <div class="links">
            <b-button class="btn btn-primary btn-lg text-align" to="/register"
              >Register</b-button
            >
            <b-button
              variant="btn btn-outline-primary btn-lg text-align"
              to="/login"
              >Login</b-button
            >
          </div>
        </div>
      </div>
    </div>
    <div></div>
  </div>
</template>

<script>
import { ButtonPlugin } from "bootstrap-vue";

import TopBar from "../components/TopBar";

export default {
  name: "Homepage",
  components: {TopBar},
  head() {
    return {
      title: "Homepage",
      meta: [
        {
          name: "viewport",
          content: "width=device-width, initial-scale=1, shrink-to-fit=no",
        },
      ],
    };
  },
  //TODO - store resets at /, need to find a better solution, myb nuxt auth.
  //created: function() {
  //  {
  //    console.log("Here in created!");
  //    if(this.$store.state.User.user)
  //      this.$router.push('/home')
  //  }
  //},
  computed: {
    user() {
      return this.$auth.user;
    }
  }
};
</script>

<style scoped>
</style>
