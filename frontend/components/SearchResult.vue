<template>
  <div class="media border p-1">
    <div class="media-body post-color p-1">
      <h5 class="lead mt-0">
        <strong><nuxt-link :to="{name:'users-id', params: {id: this.user.id}}">{{user.username}}</nuxt-link></strong>
      </h5>
    </div>
  </div>
</template>

<script>
export default {
  name: "SearchResult",
  props: {
    user: Object
  }
};
</script>

<style>
</style>