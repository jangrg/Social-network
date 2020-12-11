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
        <b-dropdown
          size="sm"
          variant="link"
          class="float-right"
          no-caret
          v-if="postedByUser && !editing"
        >
          <template #button-content>
            <span class="text-decoration-none">...</span>
          </template>
          <b-dropdown-item @click="editPost(true)">Edit</b-dropdown-item>
          <b-dropdown-item @click="deletePost">Delete</b-dropdown-item>
        </b-dropdown>
      </h5>

      <hr class="mt-2 post-separator-theme" />

      <p class="lead" v-if="!editing">
        {{ post.content }}
      </p>
      <div v-else>
        <b-form id="form">
          <div class="form-group">
            <label for=""></label>
            <textarea
              class="form-control"
              rows="4"
              v-model="newEditedPost.content"
              placeholder="Edit old post..."
            ></textarea>
          </div>
          <b-form-radio-group
            id="btn-radios-1"
            class="mr-auto mb-2"
            v-model="newEditedPost.visibility"
            :options="options"
            buttons
            plain
            name="radios-btn-default"
          ></b-form-radio-group>
          <b-form-group class="d-inline">
            <div class="image-upload">
              <label :for="`${post.image}`">
                <h5 class="font-theme lead">
                  <strong
                    v-if="post.image"
                    class="text-theme-secondary btn btn-purple"
                    >Change picture</strong
                  >
                  <strong v-else class="text-theme-secondary btn btn-purple"
                    >Upload picture</strong
                  > 
                </h5>
              </label>
              <input
                :id="`${post.image}`"
                name="image"
                type="file"
                accept="image/*"
                ref="file"
                v-on:change="changePictureUpload()"
              />
            </div>
            <!--
            <button
              class="btn-purple btn mt-4"
              v-if="newEditedPost.image"
              @click="discardImage"
            >
              Discard picture
            </button>
            -->
          </b-form-group>
        </b-form>
      </div>

      <div class="post-image">
        <img v-if="hasImage && !changedPicture" :src="post.image" />
        <img v-if="changedPicture" :src="imgEditedUrl" />
      </div>


      <div class="container-fluid float-right mb-2" v-if="editing">
        <button
          @click="saveEdited()"
          class="btn btn-purple mt-2 text-align btn-post"
        >
          Edit
        </button>
        <button
          @click="editPost(false)"
          class="btn btn-purple mt-2 text-align btn-post"
        >
          Discard
        </button>
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
      //liking and disliking
      liked: false,

      //Comment making
      comment: {
        comment_text: "",
        post: this.post.id,
      },

      //if post is getting edited
      newEditedPost: {
        content: this.post.content,
        id: this.post.id,
        image: this.post.image,
        type_attr: this.post.type_attr
      },
      editing: false,
      changedPicture: false,
      options: [
        { text: "Private", value: "private" },
        { text: "Public", value: "public" },
      ],
    };
  },
  methods: {
    changePictureUpload() {
      debugger;
      this.newEditedPost.image = this.$refs.file.files[0];
      this.changedPicture = true;
    },

    discardImage() {
      this.newEditedPost.image = null;
      this.changedPicture = false;
    },

    async likePost() {
      var classname = this.post.id;
      if (this.liked) {
        let res = await this.$axios.post(`post/${this.post.id}/unlike/`);
        if (res.status == 200) {
          this.liked = false;
          this.post.likes_num--;
          this.$toast.show("Post disliked!", { duration: 8000 });
          var post = document
            .getElementById(`${this.post.id}-${this.post.posted_by.username}`)
            .classList.toggle("like");
        } else {
          this.$toast.show("Post not successfully disliked...", {
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

    editPost(decision) {
      debugger;
      this.editing = decision;
      if (this.changedPicture) {
        this.changedPicture = decision;
      }
    },

    //saves edited post and emits it to the post feed for changing.
    async saveEdited() {
      try {
        let formData = new FormData();
        formData.append("content", this.newEditedPost.content);

        debugger;
        if (this.newEditedPost.image) {
          formData.append("image", this.newEditedPost.image);
          debugger;
        }
        debugger;
        let response = await this.$axios.patch(
          `post/${this.newEditedPost.id}/`,
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );
        debugger;
        if (response.status == 200) {
          this.$toast.show("Post succesfully edited!", { duration: 8000 });
          this.editing = false;
          this.$emit("edit", response.data);
        }
      } catch (e) {
        console.log(e);
      }
    },

    async deletePost() {
      if (confirm("Really want to delete this actualPost?")) {
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

    hasImage() {
      return this.post.image != null;
    },

    imgEditedUrl() {
      return URL.createObjectURL(this.newEditedPost.image);
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
    if (this.post.logged_user_liked) {
      document
        .getElementById(`${this.post.id}-${this.post.posted_by.username}`)
        .classList.toggle("like");
      this.liked = true;
    }
  },
};
</script>
