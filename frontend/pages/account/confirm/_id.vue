<template>
  <div class="d-flex flex-column bg justify-content-between">
    <TopBar />
    <div class="mx-auto">
      <div
        class="font-theme border-theme mx-auto p-5 bg-color justify-content-center"
      >
        <div class="center text-white">
          <div class="d-flex align-items-center justify-content-center">
            <strong>{{ this.header }}</strong>
          </div>
          <b-button
            type="button"
            to="/login"
            class="btn-wider btn-purple mt-2 text-align btn-theme"
          >
            Continue to WeShare
          </b-button>
        </div>
      </div>
    </div>
    <div></div>
  </div>
</template>
<script>
import TopBar from "@/components/TopBar";

export default {
  name: "RegisterForm",
  components: { TopBar },
  middleware: ["auth-loggedIn"],
  head() {
    return {
      title: "Confirm account",
      meta: [
        {
          name: "viewport",
          content: "width=device-width, initial-scale=1, shrink-to-fit=no",
        },
      ],
    };
  },
  data() {
    return {
      id: this.$route.params.id,
      header: "Verifying your account ...",
    };
  },
  async mounted() {
    try {
      console.log(this.$route.params.id);
      var response = await this.$axios.post(
        `/account/${this.id}/confirm/`,
        this.id
      );
      console.log(response);
      this.header = "Welcome!";
    } catch (e) {
      this.header = "Cannot find id!";
    }
  },
};
</script>
