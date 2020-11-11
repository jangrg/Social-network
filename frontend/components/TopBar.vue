<template>
  <div class="container-fluid sticky-top">
    <b-navbar variant="warning" class="top-bar">
      <div class="cont">
        <b-navbar-brand class="lead lead-text"
          ><strong>WeShare</strong></b-navbar-brand
        >
        <div class="container-fluid float-right">
          <button
            v-if="this.$auth.user"
            class="btn btn-dark btn-lg ml-auto"
            v-b-toggle.sidebar-right
          >
            Menu
          </button>
        </div>
      </div>
    </b-navbar>
  </div>
</template>

<script>
export default {
  name: "TopBar"
};
</script>

<style></style>
