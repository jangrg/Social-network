<template>
  <div class="d-flex flex-column bg justify-content-between">
    <BrandName form="Verify your email" />
    <div class="mx-auto">
      <div
        class="lead border rounded mx-auto p-5 white-container justify-content-center"
      >
        <div class="center">
          <div class="d-flex align-items-center justify-content-center">
            <strong>{{ this.header }}</strong>
          </div>
          <b-button
            type="button"
            to="/login"
            class="btn-wider btn btn-primary mt-2 text-align"
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
import BrandName from "../../../components/BrandName";

export default {
  name: "RegisterForm",
  components: { BrandName },

  head() {
    return {
      title: "Register",
      meta: [
        {
          name: "viewport",
          content: "width=device-width, initial-scale=1, shrink-to-fit=no"
        }
      ]
    };
  },
  data() {
    return {
      id: this.$route.params.id,
      header: "Verifying your account ..."
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
  }
};
</script>
