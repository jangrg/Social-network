<template>
  <div class="bg d-flex flex-column justify-content-between">
    <TopBar />
    <div class="mx-auto" v-if="!user">
      <div
        class="lead border rounded mx-auto p-4 white-container justify-content-center"
      >
        <div class="d-flex flex-column container-fluid">
          <h1 class="title">Welcome to <strong>WeShare</strong></h1>
          <h2 class="subtitle">Feel free to register now!</h2>
          <div class="links mx-auto">
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
    <Footer />
  </div>
</template>

<script>
import { ButtonPlugin } from "bootstrap-vue";

import TopBar from "@/components/TopBar";

import Footer from "@/components/Footer";

export default {
  name: "Homepage",
  components: { TopBar, Footer },
  middleware: ["auth-loggedIn"],
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
  computed: {
    user() {
      return this.$auth.user;
    },
  },
};
</script>

<style scoped>
</style>
