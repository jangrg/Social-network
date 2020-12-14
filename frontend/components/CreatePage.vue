<template>
  <transition name="preview">
    <div class="overlay">
      <div class="media font-theme text-left">
        <div class="media-body post-theme p-5">
          <div class="center">
            <div class="text-center">
              <strong class="text-theme text-title">WeShare</strong>
            </div>
            <b-form class="mx-auto mt-2 text-center">
              <b-form-input
                required
                class="input-style"
                v-model="form.name"
                type="text"
                placeholder="Enter the name of your store"
              >
              </b-form-input>

              <b-form-input
                required
                class="input-style"
                v-model="form.location"
                type="text"
                placeholder="Enter the location of your store"
              >
              </b-form-input>

              <b-form-timepicker
                class="input-add-space"
                v-model="startTime"
                locale="de"
                placeholder="Enter when the store opens"
              ></b-form-timepicker>

              <b-form-timepicker
                class="input-add-space"
                v-model="endTime"
                locale="de"
                placeholder="Enter when the store closes"
              ></b-form-timepicker>

              <span class="input-add-space"
                >Select a few categories in which your store belongs to:</span
              >
              <div>
                <button
                  id="accessories"
                  class="btn btn-purple mt-2 text-align accessories"
                  @click="selectAccessories"
                >
                  Accessories
                </button>
                <button
                  id="clothing"
                  class="btn btn-purple mt-2 text-align clothing"
                  @click="selectClothing"
                >
                  Clothing
                </button>
                <button
                  id="home"
                  class="btn btn-purple mt-2 text-align home"
                  @click="selectHome"
                >
                  Home
                </button>
                <button
                  id="entertainment"
                  class="btn btn-purple mt-2 text-align entertainment"
                  @click="selectEntertainment"
                >
                  Entertain.
                </button>
                <button
                  id="art"
                  class="btn btn-purple mt-2 text-align art"
                  @click="selectArt"
                >
                  Art
                </button>
                <button
                  id="tools"
                  class="btn btn-purple mt-2 text-align tools"
                  @click="selectTools"
                >
                  Tools
                </button>
              </div>

              <button
                @click.prevent="create"
                :disabled="!allowSubmit"
                class="btn btn-purple mt-2 text-align"
              >
                Submit
              </button>
            </b-form>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: "CreatePage",
  props: {
    post: Object
  },
  data() {
    return {
      form: {
        name: "",
        date_created: "",
        location: "",
        work_time: "",
        categories: []
      },
      startTime: "",
      endTime: ""
    };
  },
  methods: {
    async create() {
      try {
        // this.form.work_time = this.startTime + "-" + this.endTime;
        // var today = new Date();
        // var dd = String(today.getDate()).padStart(2, "0");
        // var mm = String(today.getMonth() + 1).padStart(2, "0"); //January is 0!
        // var yyyy = today.getFullYear();
        // today = mm + "/" + dd + "/" + yyyy;
        // this.form.date_created = today;
        let formData = new FormData();
        formData.append("name", this.form.name);
        formData.append("location", this.form.location);
        // formData.append("work_time", this.startTime + "-" + this.endTime);
        // formData.append("categories", this.form.categories);
        let response = await this.$axios.post(`page/`, formData);
        this.$toast.show(response.data.message, { duration: 8000 });
        console.log(response.data);
        this.$router.push("/");
      } catch (e) {
        this.$toast.error(e, { duration: 8000 });
        console.log(e.data);
      }
    },
    selectAccessories() {
      if (this.form.categories.indexOf("accessories") > -1)
        this.removeA(this.form.categories, "accessories");
      else this.form.categories.push("accessories");
      document.getElementById(`accessories`).classList.toggle("btn-selected");
    },
    selectClothing() {
      if (this.form.categories.indexOf("clothing") > -1)
        this.removeA(this.form.categories, "clothing");
      else this.form.categories.push("clothing");
      document.getElementById(`clothing`).classList.toggle("btn-selected");
    },
    selectHome() {
      if (this.form.categories.indexOf("home") > -1)
        this.removeA(this.form.categories, "home");
      else this.form.categories.push("home");
      document.getElementById(`home`).classList.toggle("btn-selected");
    },
    selectEntertainment() {
      if (this.form.categories.indexOf("entertainment") > -1)
        this.removeA(this.form.categories, "entertainment");
      else this.form.categories.push("entertainment");
      document.getElementById(`entertainment`).classList.toggle("btn-selected");
    },
    selectArt() {
      if (this.form.categories.indexOf("art") > -1)
        this.removeA(this.form.categories, "art");
      else this.form.categories.push("art");
      document.getElementById(`art`).classList.toggle("btn-selected");
    },
    selectTools() {
      if (this.form.categories.indexOf("tools") > -1)
        this.removeA(this.form.categories, "tools");
      else this.form.categories.push("tools");
      document.getElementById(`tools`).classList.toggle("btn-selected");
    },
    removeA(arr) {
      var what,
        a = arguments,
        L = a.length,
        ax;
      while (L > 1 && arr.length) {
        what = a[--L];
        while ((ax = arr.indexOf(what)) !== -1) {
          arr.splice(ax, 1);
        }
      }
      return arr;
    }
  },
  computed: {
    allowSubmit() {
      return true;
      //   if (this.form.categories.length !== 0) return true;
      //   return false;
    }
  }
};
</script>
