<template>
  <div class="container-fluid sticky-top">
    <b-navbar variant="warning">
      <b-navbar-brand class="lead"><strong>Welcome!</strong></b-navbar-brand>
      <div class="container-fluid float-right">
        <button
          v-if="this.$auth.user"
          class="btn btn-primary btn-lg ml-auto"
          v-b-toggle.sidebar-right
        >
          Menu
        </button>
      </div>
    </b-navbar>
  </div>
</template>

<script>
export default {
  name: "TopBar",
};
</script>

<style>
</style>