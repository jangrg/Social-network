<template>
  <b-form id="form" v-on:submit.prevent="postForm">
    <div class="form-group">
      <label for=""></label>
      <textarea
        class="form-control"
        rows="4"
        v-model="newPost.content"
        placeholder="Write a new post"
      ></textarea>
      <div v-if="!canUploadImage" class="image-upload">
        <label for="file">
          <h5 class="font-theme lead">
            <img
              class="image image-upload-picture"
              src="../static/upload_picture_icon.png"
            />
            <strong class="text-theme-secondary">Upload photo</strong>
          </h5>
        </label>
        <input
          id="file"
          name="image"
          type="file"
          accept="image/*"
          ref="file"
          v-on:change="handleFileUpload()"
        />
      </div>
    </div>

    <div v-if="canUploadImage" class="small-img-preview container-fluid">
      <img :src="imgUrl" />
      <button class="btn-purple btn" @click="discardImage">Discard</button>
    </div>

    <b-form-radio-group
      id="btn-radios-1"
      class="mr-auto"
      v-model="newPost.is_private"
      :options="options"
      buttons
      plain
      name="radios-btn-default"
    ></b-form-radio-group>

    <button
      @click.prevent="postForm"
      type="submit"
      class="btn btn-purple btn-fill mt-2 text-align btn-post"
      :disabled="!allowSubmit"
    >
      Post
    </button>
    <div v-if="openPreview">
      <ImagePreview :post="this.newPost" @post="setImage" />
    </div>
  </b-form>
</template>

<script>
import ImagePreview from "./ImagePreview.vue";

export default {
  components: { ImagePreview },
  name: "PostForm",
  data() {
    return {
      options: [
        { text: "Public", value: false },
        { text: "Private", value: true },
      ],

      openPreview: false,
      newPost: {
        content: "",
        is_private: false,
        is_store: false,
        image: null,
      },

      canUploadImage: false,
    };
  },
  methods: {
    handleFileUpload() {
      this.newPost.image = this.$refs.file.files[0];
      this.openPreview = true;
    },

    setImage(canUploadImage) {
      (this.openPreview = false), (this.canUploadImage = canUploadImage);
      if (!canUploadImage) this.newPost.image = null;
    },

    discardImage() {
      this.newPost.image = null;
      this.canUploadImage = false;
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
        formData.append("content", this.newPost.content);
        formData.append("is_private", this.newPost.is_private);
        formData.append("is_page", this.$nuxt.$route.name.includes("store"));
        if (this.newPost.image) formData.append("image", this.newPost.image);
        let response = await this.$axios.post(`post/`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
        if (response.status == 201) {
          this.$toast.show("Post succesfully posted!", { duration: 8000 });
          //Ovaj response ne vraca sliku prvi put!!
          let createdPost = response.data;
          this.newPost = {
            content: "",
            is_private: false,
            image: null,
          };
          this.canUploadImage = false;

          if (createdPost.is_private && this.$nuxt.$route.name == "explore") {
            this.$toast.show(
              "Private posts will not be visible on this feed.",
              { duration: 8000 }
            );
            this.$toast.show(
              "Please go to your profile page or home feed to see your private post!",
              { duration: 8000 }
            );
          } else this.$emit("post", createdPost);
        }
      } catch (e) {
        console.log(e);
      }
    },
  },
  computed: {
    allowSubmit() {
      return this.newPost.content != "";
    },

    imgUrl() {
      return URL.createObjectURL(this.newPost.image);
    },
  },
};
</script>

<style></style>
