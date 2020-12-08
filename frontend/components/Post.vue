<template>
  <div class="media p-2 font-theme">
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
        <span class="three-dots"><strong>...</strong></span>
      </h5>

      <hr class="mt-0 post-separator-theme" />

      <p class="lead">
        {{ post.content }}
      </p>

      <div class="container-fluid">
        <span>Likes: {{ post.likes_num }}</span>
        <span> Comments: {{ 0 }} |</span>
        <span> Posted on: {{ date }} </span>
        <div class="d-inline float-right">
          <div :id="post.id" class="like-img" @click="likePost"></div>
          <!-- <button class="btn-sm btn-warning" @click="likePost"> -->
          <!-- <span v-if="!liked">Like this!</span>
          <span v-else>Dislike this!</span> -->
          <!-- </button> -->
          <!-- <button class="btn-sm btn-warning">Comment!</button> -->
        </div>
      </div>
      <hr class="post-separator-theme" />
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
    post: Object
  },
  data() {
    return {
      username: "",
      liked: false,
      comment: {
        comment_text: "",
        likes_num: 0,
        post: this.post.id
      }
    };
  },
  methods: {
    async likePost() {
      var classname = this.post.id;
      if (this.liked) {
        this.liked = false;
        this.post.likes_num--;
        this.$toast.show("Post unliked!", { duration: 8000 });
        var post = document
          .getElementById(`${this.post.id}`)
          .classList.toggle("like");
      } else {
        this.liked = true;
        let res = await this.$axios.post(`post/${this.post.id}/like/`);
        if (res.status == 200) {
          this.$toast.show("Post liked!", { duration: 8000 });
          this.post.likes_num++;
          document.getElementById(`${this.post.id}`).classList.toggle("like");
        } else {
          this.$toast.show("Post not successfully likes...", {
            duration: 8000
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
          duration: 8000
        });
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
    },
    noComment() {
      return this.comment.comment_text == "";
    },
    numberOfComments() {
      if (post.comments) {
        return post.comments > 5;
      }
    }
  },
  mounted() {
    var classname = this.post.id;
    //document.getElementById(this.post.id).classList.toggle(classname);
  }
};
</script>

<style></style>
