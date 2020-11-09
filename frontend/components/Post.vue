<template>
  <div class="media border p-1">
    <div class="media-body post-color p-1">
        <h5 class="lead mt-0">
          <strong
            ><nuxt-link
              class="text-warning"
              :to="{ name: 'users-id', params: { id: post.posted_by.id } }"
            >
              {{ post.posted_by.username }}
            </nuxt-link></strong
          >
        </h5>

      <hr class="mt-0">

      <p class="lead">
        {{ post.content }}
      </p>

      <div class="container-fluid">
        <span> Likes: {{ post.likes_num }} |</span>
        <span> Comments: {{ 0 }} |</span>
        <span> Posted on: {{date}} </span>
        <div class="d-inline float-right">
          <button class="btn-sm btn-warning" @click="likePost">
            <span v-if="!liked">Like this!</span>
            <span v-else>Dislike this!</span>
          </button>
          <button class="btn-sm btn-warning">Comment!</button>
        </div>
      </div>
      <hr />

      <div class="ml-5" v-for="comment in post.comments" :key="comment.Id">
        <Post :post="null" />
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
  computed : {
    date() {
      let date = new Date(this.post.time);
      let string = date.getDate() + "/" + date.getMonth() + "/" + date.getFullYear() + " at " + date.getHours() + ":" + date.getMinutes();
      debugger
      return string;
    }
  }
};
</script>

<style>
</style>