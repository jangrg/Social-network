<template>
  <div class="media border p-1">
    <div class="media-body post-color p-1">
      <h5 class="lead mt-0">
        <strong> Username link number {{post}}</strong>
      </h5>
    </div>
  </div>
</template>

<script>
export default {
  name: "Search",
  props: {
    post: String,
  },
};
</script>

<style>
</style>