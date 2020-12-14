<template>
  <div class="d-flex flex-column font-theme">
    <TopBar />
    <div class="container-fluid row mx-auto">
      <div class="col-md-2"></div>
      <div class="col-md-8 no-border">
        <div v-for="result in searchResult" :key="result.id">
          <SearchResult :user="result" />
        </div>
        <div v-if="searchResult.length == 0" class="text-center mt-5">
          <h5><i>No results found...</i></h5>
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
  head: function() {
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

  data: function() {
    return {
      searchResult: []
    };
  },

  created: async function() {
      let result = await this.$axios.get(`/account/`, {params:  { query: this.$route.params.keyword}});
      this.searchResult = result.data;
  }
};
</script>

<style scoped></style>
