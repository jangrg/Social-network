<template>
  <div class="d-flex flex-column font-theme">
    <TopBar />
    <div class="container-fluid row mx-auto">
      <div class="col-md-2"></div>
      <div class="col-md-8 no-border">
        <div v-for="result in searchResult" :key="result.id">
          <SearchResult :user="result" />
        </div>
        <div class="col-md-2"></div>
      </div>
    </div>
  </div>
</template>

<script>
import TopBar from "../../components/TopBar";

import SearchResult from "../../components/SearchResult";

export default {
  name: "Home",
  components: { TopBar, SearchResult },
  middleware: ["auth-notLoggedIn"],
  head() {
    return {
      title: "Login",
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
      // loaded: false,
      keyword: this.$route.params.keyword,
      searchResult: []
    };
  },

  async created() {
    try {
      let result = await this.$axios.get(`/account/`, {
        params: { search: this.keyword }
      });
      this.searchResult = result.data;
      // this.loaded = true;
    } catch (e) {
      // this.$toast.error(`${e.response.status} ${e.response.statusText}`, {
      //   duration: 8000,
      // });
      console.log(e);
    }
  }
};
</script>

<style scoped></style>
