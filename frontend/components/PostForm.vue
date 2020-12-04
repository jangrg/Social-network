<template>
  <b-form id="form">
    <div class="form-group ">
      <label for=""></label>
      <textarea
        class="form-control"
        rows="4"
        v-model="newPost.content"
        placeholder="Write a new post"
      ></textarea>
    </div>

    <button
      @click.prevent="postForm"
      type="submit"
      class="btn btn-purple btn-fill mt-2 text-align btn-post"
      :disabled="allowSubmit"
    >
      Post
    </button>
  </b-form>
</template>

<script>
export default {
  name: "PostForm",
  data() {
    return {
      newPost: {
        content: "",
        photo: null,
        type_attr: null,
        likes_num: 0,
        posted_by: this.$auth.user.id,
      },
    };
  },
  methods: {
    async postForm() {
      console.log(
        this.newPost.posted_by +
          " " +
          this.newPost.content +
          " " +
          this.newPost.likes_num
      );
      try {
        let res = await this.$axios.post(`post/`, this.newPost);

        console.log(res);
        if (res.status == 201) {
          this.$toast.show("Post uspješno objavljen!", { duration: 8000 });
          let createdPost = res.data;
          document.getElementById("form").reset();
          this.$emit("post", createdPost);
        }
      } catch (e) {
        this.$toast.error(`${e.response.status} ${e.response.statusText}`, {
          duration: 8000,
        });
      }
    },
    
  },
  computed: {
    allowSubmit() {
        return this.newPost.content == "";
    }
  }
};
</script>

<style>
</style>