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
          <b-dropdown-item @click="editComment(true)">Edit</b-dropdown-item>
          <b-dropdown-item @click="deleteComment">Delete</b-dropdown-item>
        </b-dropdown>
      </h5>

      <hr class="mt-0 post-separator-theme" />

      <p class="lead" v-if="!editing">
        {{ comment.comment_text }}
      </p>
      <div class="d-block" v-else>
        <b-form class="container-fluid form-theme">
          <textarea
            type="text"
            class="form-control input-grey w-100"
            v-model="newComment.comment_text"
            placeholder="Comment"
          />
          <b-button
            variant="btn btn-purple mt-1"
            :disabled="noComment"
            type="submit"
            @click.prevent="saveEdited"
            ><span>Edit</span></b-button
          >
          <b-button
            variant="btn btn-purple mt-1"
            type="submit"
            @click.prevent="editComment(false)"
            ><span>Discard</span></b-button
          >
        </b-form>
      </div>

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
      editing: false,

      newComment: {
        id: this.comment.id,
        comment_text: this.comment.comment_text,
      },
    };
  },

  methods: {
    async likeComment() {
      if (this.liked) {
        let res = await this.$axios.post(
          `post/${this.comment.id}/unlike_comment/`
        );
        debugger;
        if (res.status == 200) {
          this.liked = false;
          this.comment.likes_num--;
          this.$toast.show("Comment disliked!", { duration: 8000 });
          var comment = document
            .getElementById(`${this.comment.id}-${this.comment.post}`)
            .classList.toggle("like");
        } else {
          this.$toast.show("Comment not succesfully disliked...", {
            duration: 8000,
          });
        }
      } else {
        debugger;
        let res = await this.$axios.post(
          `post/${this.comment.id}/like_comment/`
        );
        debugger;
        if (res.status == 200) {
          this.liked = true;
          this.comment.likes_num++;
          this.$toast.show("Comment liked!", { duration: 8000 });
          document
            .getElementById(`${this.comment.id}-${this.comment.post}`)
            .classList.toggle("like");
        } else {
          this.$toast.show("Comment not succesfully liked...", {
            duration: 8000,
          });
        }
      }
    },

    async deleteComment() {
      if (confirm("Really want to delete this comment?")) {
        let res = await this.$axios.delete(`comment/${this.comment.id}/`);
        debugger;
        if (res.status == 204) {
          this.$toast.show("Comment succesfully deleted.", {
            duration: 8000,
          });
          this.$emit("delete", this.comment.id);
        } else {
          this.$toast.show("Comment not successfully deleted...", {
            duration: 8000,
          });
        }
      }
    },

    editComment(decision) {
      this.editing = decision;
    },

    async saveEdited() {
      try {
        let formData = new FormData();
        formData.append("comment_text", this.newComment.comment_text);
        formData.append("id", this.newComment.id);

        debugger;
        let response = await this.$axios.patch(
          `comment/${this.newComment.id}/`,
          formData
        );
        debugger;
        if (response.status == 200) {
          this.$toast.show("Comment succesfully edited!", { duration: 8000 });
          this.editing = false;
          this.$emit("edit", response.data);
        }
      } catch (e) {
        console.log(e);
      }
    },
  },
  computed: {
    uniqueId() {
      return this.comment.id + "-" + this.comment.post;
    },
    postedByUser() {
      return this.$auth.user.id == this.comment.posted_by.id;
    },
    noComment() {
      return this.newComment.comment_text == "";
    },
  },
  mounted() {
    for (var i = 0; i < this.comment.liked_by.length; i++) {
      if (this.$auth.user.id == this.comment.liked_by[i].id) {
        document
          .getElementById(`${this.comment.id}-${this.comment.post}`)
          .classList.toggle("like");
        this.liked = true;
        break;
      }
    }
  },
};
</script>

<style>
</style>