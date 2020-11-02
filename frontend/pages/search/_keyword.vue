<template>
  <div class="d-flex flex-column bg-pattern">
    <TopBar />
    <SideBar />

    <div class="container-fluid row  mx-auto">
      <div class="col-md-2"></div>
      <div class="col-md-8 white-container rounded">
        <h3>Search result({{searchResult.length}}):</h3>
        <!-- Samo za demonstraciju -->
        <SearchResult post="1"/>
        <SearchResult post="2"/>
        <SearchResult post="3"/>
      </div>
      
      <div class="col-md-2"></div>
    </div>
  </div>
</template>

<script>
import TopBar from "../../components/TopBar";

import SideBar from "../../components/SideBar";

import SearchResult from "../../components/SearchResult";

export default {
    name: "Home",
    components: { TopBar, SideBar, SearchResult },

    head() {
      return {
        title: "Login",
        meta: [
          {
            name: "viewport",
            content: "width=device-width, initial-scale=1, shrink-to-fit=no"
          }
        ]
      }
    },

    data() {
      return {
        keyword: this.$route.params.keyword,
        searchResult: ["", "", ""]
      }
    },

    /* search result fetching
    async mounted() {
    } */
}
</script>

<style scoped>

</style>