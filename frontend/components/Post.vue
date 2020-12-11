<template>
  <div class="media p-2 font-theme" :id="post.id">
    <div class="media-body post-theme p-5">
      <h5 class="lead">
        <b-avatar class="mb-2"></b-avatar>
        <strong
          ><nuxt-link
            class="text-theme"
            :to="{ name: 'users-id', params: { id: post.posted_by.id } }"
          >
            {{ post.posted_by.username }}
          </nuxt-link></strong
        >
        <b-dropdown size="sm" variant="link" class="float-right" no-caret v-if="postedByUser" >
          <template #button-content>
            <span class="text-decoration-none">...</span>
          </template>
          <b-dropdown-item @click="editPost">Edit</b-dropdown-item>
          <b-dropdown-item @click="deletePost">Delete</b-dropdown-item>
        </b-dropdown>
      </h5>

      <hr class="mt-2 post-separator-theme" />

      <p class="lead">
        {{ post.content }}
      </p>

      <div class="post-image">
        <img :src="post.image" />
      </div>

      <div class="container-fluid">
        <span>Likes: {{ post.likes_num }}</span>
        <span> Comments: {{ numberOfComments }} |</span>
        <span> Posted on: {{ date }} </span>
        <div class="d-inline float-right">
          <div
            :id="post.id + '-' + post.posted_by.username"
            class="like-img"
            @click="likePost"
          ></div>
          <!-- <button class="btn-sm btn-warning" @click="likePost">
            -->
          <!-- <span v-if="!liked">Like this!</span> -->
          <!-- <span v-else>Dislike this!</span> -->
          <!-- </button> -->
          <!-- <button class="btn-sm btn-warning">Comment!</button> -->
        </div>
      </div>
      <hr class="mt-4 post-separator-theme" />
      <b-form class="container-fluid form-theme">
        <textarea
          type="text"
          class="form-control input-grey w-100"
          v-model="comment.comment_text"
          placeholder="Comment"
        />
        <b-button
          variant="btn float-right btn-purple mt-1"
          :disabled="noComment"
          type="submit"
          @click.prevent="newComment"
          ><span>Comment</span></b-button
        >
      </b-form>
      <div
        class="ml-5 mt-4"
        v-for="comment in post.comments"
        :key="comment.posted_by.id"
      >
        <Comment :comment="comment" />
      </div>
    </div>
  </div>
</template>

<script>
import Comment from "@/components/Comment";

export default {
  name: "Post",
  components: { Comment },
  props: {
    post: Object,
  },
  data() {
    return {
      username: "",
      liked: false,
      comment: {
        comment_text: "",
        post: this.post.id,
      },
    };
  },
  methods: {
    async likePost() {
      var classname = this.post.id;
      if (this.liked) {
        let res = await this.$axios.post(`post/${this.post.id}/unlike/`);
        if (res.status == 200) {
          this.liked = false;
          this.post.likes_num--;
          this.$toast.show("Post unliked!", { duration: 8000 });
          var post = document
            .getElementById(`${this.post.id}-${this.post.posted_by.username}`)
            .classList.toggle("like");
        } else {
          this.$toast.show("Post not successfully unliked...", {
            duration: 8000,
          });
        }
      } else {
        let res = await this.$axios.post(`post/${this.post.id}/like/`);
        if (res.status == 200) {
          this.liked = true;
          this.post.likes_num++;
          this.$toast.show("Post liked!", { duration: 8000 });
          document
            .getElementById(`${this.post.id}-${this.post.posted_by.username}`)
            .classList.toggle("like");
        } else {
          this.$toast.show("Post not successfully liked...", {
            duration: 8000,
          });
        }
      }
    },
    editPost() {
      
    },
    async deletePost() {
      if (confirm("Really want to delete this post?")) {
        let res = await this.$axios.delete(`post/${this.post.id}/`);
        debugger;
        if (res.status == 204) {
          this.$toast.show("Post succesfully deleted.", {
            duration: 8000,
          });
          this.$emit("PostDelete", this.post.id);
        } else {
          this.$toast.show("Post not successfully deleted...", {
            duration: 8000,
          });
        }
      }
    },
    async newComment() {
      console.log(this.comment);
      try {
        let res = await this.$axios.post(`post/comment/`, this.comment);
        debugger;
        console.log(res);
        if (res.status == 201) {
          this.$toast.show("Comment successfully posted!", { duration: 8000 });
          let createdComment = res.data;
          debugger;
          this.comment.comment_text = "";
          this.post.comments.push(createdComment);
        }
      } catch (e) {
        this.$toast.error(`${e.response.status} ${e.response.statusText}`, {
          duration: 8000,
        });
      }
    },
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
    },
    noComment() {
      return this.comment.comment_text == "";
    },
    numberOfComments() {
      return this.post.comments.length;
    },
    postedByUser() {
      return this.$auth.user.id == this.post.posted_by.id;
    },
  },
  mounted() {
    for (var i = 0; i < this.post.liked_by.length; i++) {
      if (this.post.liked_by[i].id == this.$auth.user.id) {
        document
          .getElementById(`${this.post.id}-${this.post.posted_by.username}`)
          .classList.toggle("like");
        this.liked = true;
        break;
      }
    }
  },
};
</script>
