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
      <div class="image-upload">
        <label for="file">
          <h5 class="font-theme lead">
            <img class="image image-upload-picture" src="..\static\upload_picture_icon.png">
            <strong>Upload photo</strong>
          </h5>
        </label>
        <input id="file" class="image-upload" name="image" type="file" accept="image/*" ref="file" v-on:change="handleFileUpload()">
      </div>
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
        image: null,
      },
    };
  },
  methods: {
    handleFileUpload(){
      this.newPost.image = this.$refs.file.files[0];
    },

    async postForm() {
      // console.log(
      //   this.newPost.posted_by +
      //     " " +
      //     this.newPost.content +
      //     " " +
      //     this.newPost.likes_num
      // );
      try {
        let formData = new FormData();
        formData.append("content", this.newPost.content)
        if(this.newPost.image)
          formData.append("image", this.newPost.image)

        let response = await this.$axios.post(
          `post/`,
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data"
            }
          }
        );

        if (response.status == 201) {
          this.$toast.show("Post uspješno objavljen!", { duration: 8000 });
          let createdPost = response.data;
          document.getElementById("form").reset();
          this.$emit("post", createdPost);
        }
      } catch (e) {
        console.log(e)
        // this.$toast.error(`${e.response.status} ${e.response.statusText}`, {
        //   duration: 8000,
        // });
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