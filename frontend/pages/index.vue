<template>
  <div class="bg d-flex flex-column justify-content-between">
    <TopBar />
    <div class="mx-auto" v-if="!user">
      <div
        class="border-theme font-theme rounded mx-auto p-4 bg-color justify-content-center"
      >
        <div class="d-flex flex-column container-fluid">
          <h1 class="title text-theme">
            Welcome
          </h1>
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
          content: "width=device-width, initial-scale=1, shrink-to-fit=no"
        }
      ]
    };
  },
  computed: {
    user() {
      return this.$auth.user;
    }
  }
};
</script>

<style scoped></style>
