<template>
  <div class="container-fluid sticky-top font-theme-top-bar">
    <b-navbar class="top-bar top-bar-theme">
      <div class="row container-fluid">
        <b-navbar-brand class="lead-text col-3"
          ><strong>WeShare</strong></b-navbar-brand
        >
        <div class="col-7"></div>
        <div class="container-fluid col-2">
          <button
            v-if="this.$auth.user"
            class="btn btn-outline-dark btn-lg ml-auto"
            v-b-toggle.sidebar-right
          >
            <i class="fa fa-bars"></i>
          </button>
        </div>
      </div>
    </b-navbar>
    <SideBar @post="emitPost" v-if="this.$auth.user" />
  </div>
</template>

<script>

import SideBar from '@/components/SideBar';

export default {
  name: "TopBar",
  components: {SideBar},
  head: {
    link: [
      {
        rel: 'stylesheet',
        href: 'https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css'
      }
    ]
  },
  methods: {
    emitPost(parameters) {
      this.$emit('post', parameters);
    }
  }
};
</script>

<style></style>
