<template>
  <div class="media border p-1">
    <div class="media-body post-color p-1">
      <h5 class="lead mt-0">
        <strong
          ><nuxt-link :to="{name:'users-id', params: { id: post.posted_by }}">
             {{post.username}}
          </nuxt-link></strong
        >
      </h5>

      <p class="lead">
        {{ post.content }}
      </p>

      <div class="container-fluid">
        <span> Likes: {{ post.likes_num }}</span>
        <span> Comments: {{ 0 }} </span>
        <button class="btn-sm btn-secondary" @click="likePost">
          <span v-if="!liked">Like this!</span>
          <span v-else>Dislike this!</span>
        </button>
        <button class="btn-sm btn-secondary">Comment!</button>
      </div>
      <hr />

      <div class="ml-5" v-for="comment in comments" :key="comment.Id">
        <Post :post="comment"/>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Post",
  props: {
    post: Object,
    depth: Number,
    comments: Object,
  },
  data() {
    return {
      username: "",
      liked: false,
    };
  },
  methods: {
    likePost() {
      if (!this.liked) {
        this.liked = true;
      } else {
        this.liked = false;
      }
    },
  },
};
</script>

<style>
</style>