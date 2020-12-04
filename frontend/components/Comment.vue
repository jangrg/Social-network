<template>
   <div class="p-1 font-theme">
    <hr class="post-separator-theme" />
    <div class="p-1">
      <h5 class="lead">
        <b-avatar class="mb-2"></b-avatar>
        <strong
          ><nuxt-link
            class="text-theme"
            :to="{ name: 'users-id', params: { id: comment.posted_by.id } }"
          >
            {{ comment.posted_by.username }}
          </nuxt-link></strong
        >
        <span class="three-dots"><strong>...</strong></span>
      </h5>

      <hr class="mt-0 post-separator-theme" />

      <p class="lead">
        {{ comment.comment_text }}
      </p>

      <div class="container-fluid">
        <span>Likes: {{ comment.likes_num }}</span>
        <div class="d-inline float-right">
          <div :id="23" class="like-img" @click="likeComment"></div>
          <!-- <button class="btn-sm btn-warning" @click="likePost"> -->
          <!-- <span v-if="!liked">Like this!</span>
          <span v-else>Dislike this!</span> -->
          <!-- </button> -->
          <!-- <button class="btn-sm btn-warning">Comment!</button> -->
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
    name: "Comment",
    props: {
        comment: Object,
    },
    data() {
    return {
      liked: false,
    };
  },
}
</script>

<style>

</style>