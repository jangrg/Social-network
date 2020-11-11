<template>
  <div class="media p-1">
    <div class="media-body post-color p-5">
      <h5 class="lead mt-1">
        <strong
          ><nuxt-link
            class="text-dark"
            :to="{ name: 'users-id', params: { id: post.posted_by.id } }"
          >
            {{ post.posted_by.username }}
          </nuxt-link></strong
        >
        <span class="three-dots"><strong>...</strong></span>
      </h5>

      <hr class="mt-0" />

      <p class="lead">
        {{ post.content }}
      </p>

      <div class="container-fluid">
        <span v-if="!liked">Likes: {{ post.likes_num }}</span>
        <span v-else>Likes: {{ post.likes_num + 1 }}</span>
        <span> Comments: {{ 0 }} |</span>
        <span> Posted on: {{ date }} </span>
        <div class="d-inline float-right">
          <div id="like-img" class="like-img" @click="likePost"></div>
          <!-- <button class="btn-sm btn-warning" @click="likePost"> -->
          <!-- <span v-if="!liked">Like this!</span>
          <span v-else>Dislike this!</span> -->
          <!-- </button> -->
          <!-- <button class="btn-sm btn-warning">Comment!</button> -->
        </div>
      </div>
      <hr />
      <div class="ml-5 comment">Add a comment ...</div>
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
    depth: Number
  },
  data() {
    return {
      username: "",
      liked: false
    };
  },
  methods: {
    likePost() {
      var classname = this.post.id;
      if (!this.liked) {
        this.liked = true;
        document.getElementsByClassName(classname)[0].classList.toggle("like");
      } else {
        this.liked = false;
        document.getElementsByClassName(classname)[0].classList.toggle("like");
      }
    }
  },
  computed: {
    date() {
      let date = new Date(this.post.time);
      let string =
        (date.getDate() < 10 ? "0" + date.getDate() : date.getDate()) +
        "/" +
        (date.getMonth() < 10 ? "0" + date.getMonth() : date.getMonth()) +
        "/" +
        date.getFullYear() +
        " at " +
        (date.getHours() < 10 ? "0" + date.getHours() : date.getHours()) +
        ":" +
        (date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes());
      // debugger;
      return string;
    }
  },
  mounted() {
    var classname = this.post.id;
    document.getElementById("like-img").classList.toggle(classname);
  }
};
</script>

<style></style>
