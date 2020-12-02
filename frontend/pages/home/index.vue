<template>
  <div class="d-flex flex-column font-theme">
    <TopBar @post="setPost" />
    <div class="container-fluid row mx-auto">
      <div class="col-md-2"></div>
      <div class="col-md-8 no-border">
        <div class="text-center">
          <!-- <h3>📣</h3> -->
          <div class="container-fluid new-post">
            <b-form id="form">
              <div class="form-group">
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
              >
                Post
              </button>
            </b-form>
          </div>
        </div>
        <div v-for="post in posts" :key="post.id">
          <Post :post="post" />
        </div>

        <div class="col-md-2"></div>
      </div>
    </div>
  </div>
</template>

<script>
import { ButtonPlugin } from "bootstrap-vue";

import TopBar from "@/components/TopBar";

import SideBar from "@/components/SideBar";

import Post from "@/components/Post";

import Footer from "@/components/Footer";

export default {
  name: "Home",
  components: { TopBar, SideBar, Post, Footer },
  middleware: ["auth-notLoggedIn"],
  head() {
    return {
      title: "Home",
      meta: [
        {
          name: "viewport",
          content: "width=device-width, initial-scale=1, shrink-to-fit=no"
        }
      ],
      bodyAttrs: {
        class: "body-theme"
      }
    };
  },
  data() {
    return {
      posts: [],
      newPost: {
        content: "",
        photo: null,
        type_attr: null,
        likes_num: 0,
        posted_by: this.$auth.user.id
      }
    };
  },
  methods: {
    setPost(parameters) {
      this.posts.unshift(parameters);
    },
    allowSubmit() {},
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
          // this.$emit("post", createdPost);
          this.posts.unshift(createdPost);
        }
      } catch (e) {
        this.$toast.error(`${e.response.status} ${e.response.statusText}`, {
          duration: 8000
        });
      }
    }
  },
  created: async function() {
    let response = await this.$axios.get(`post/`);

    this.posts = response.data;
  }
};
</script>

<style></style>
