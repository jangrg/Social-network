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
        <b-dropdown
          size="sm"
          variant="link"
          class="float-right"
          no-caret
          v-if="postedByUser"
        >
          <template #button-content>
            <span class="text-decoration-none">...</span>
          </template>
          <b-dropdown-item @click="editComment">Edit</b-dropdown-item>
          <b-dropdown-item @click="deleteComment">Delete</b-dropdown-item>
        </b-dropdown>
      </h5>

      <hr class="mt-0 post-separator-theme" />

      <p class="lead">
        {{ comment.comment_text }}
      </p>

      <div class="container-fluid">
        <span>Likes: {{ comment.likes_num }}</span>
        <div class="d-inline float-right">
          <div :id="uniqueId" class="like-img" @click="likeComment"></div>
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

  methods: {
    async likeComment() {
      if (this.liked) {
        let res = await this.$axios.post(
          `post/unlike_comment/?id=${this.comment.id}`
        );
        if (res.status == 200) {
          this.liked = false;
          this.comment.likes_num--;
          this.$toast.show("Comment unliked!", { duration: 8000 });
          var comment = document
            .getElementById(`${this.comment.id}-${this.comment.post}`)
            .classList.toggle("like");
        } else {
          this.$toast.show("Comment not successfully unliked...", {
            duration: 8000,
          });
        }
      } else {
        let res = await this.$axios.post(
          `post/like_comment/?id=${this.comment.id}`
        );
        if (res.status == 200) {
          this.liked = true;
          this.comment.likes_num++;
          this.$toast.show("Comment liked!", { duration: 8000 });
          document
            .getElementById(`${this.comment.id}-${this.comment.post}`)
            .classList.toggle("like");
        } else {
          this.$toast.show("Comment not successfully liked...", {
            duration: 8000,
          });
        }
      }
    },
    deleteComment(){},
    editComment(){},
  },
  computed: {
    uniqueId() {
      return this.comment.id + "-" + this.comment.post;
    },
    postedByUser() {
      return this.$auth.user.id == this.comment.posted_by.id;
    },
  },
};
</script>

<style>
</style>